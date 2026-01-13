"""
Unified normalizer for biomedical concept normalization.

Works with DuckDB databases built by build_umls_duckdb, build_ontology_duckdb,
or build_merged_duckdb. All use a standardized schema.
"""

from __future__ import annotations

import contextlib
from collections.abc import Mapping, Sequence
from textwrap import dedent

import duckdb
import polars as pl

from norm_toolkit.constants import (
    ATOMS_TABLE,
    DEFAULT_PREFER_TTYS,
    DEFS_TABLE,
    EDGES_TABLE,
    HIT_STRUCT_TYPE,
    NS_TABLE,
    NW_TABLE,
    TYPES_TABLE,
)
from norm_toolkit.models import ConceptInfo
from norm_toolkit.normalizer_utils import (
    apply_concept_name_rows,
    apply_definition_rows,
    apply_semantic_type_rows,
    build_concept_names_sql,
    build_definitions_sql,
    build_hits_agg_expr,
    build_lookup_sql,
    build_normalized_query_map,
    build_ontology_filter_clauses,
    build_pref_join,
    build_query_rows,
    build_semantic_types_sql,
    init_concept_info_map,
)


class DuckDBNormalizer:
    """
    High-throughput normalizer using DuckDB.

    Works with databases built by any of the build functions. Uses exact match
    via normalized string index and optional partial match via word-level index.
    """

    def __init__(
        self,
        db_path: str,
        threads: int = 8,
    ) -> None:
        """
        Initialize the normalizer.

        Args:
            db_path: Path to DuckDB database file
            threads: Number of DuckDB threads to use
        """
        self.db_path = db_path
        self.con = duckdb.connect(db_path, read_only=True)
        self.con.execute(f"PRAGMA threads={threads}")

        # Detect database capabilities
        self._has_types = self._table_has_rows(TYPES_TABLE)
        self._has_defs = self._table_has_rows(DEFS_TABLE)
        self._has_edges = self._table_has_rows(EDGES_TABLE)
        self._has_stt = self._column_has_values(ATOMS_TABLE, "stt")

    def _table_has_rows(self, table: str) -> bool:
        """Check if a table exists and has rows."""
        try:
            result = self.con.execute(f"SELECT 1 FROM {table} LIMIT 1").fetchone()
            return result is not None
        except Exception:
            return False

    def _column_has_values(self, table: str, column: str) -> bool:
        """Check if a column has any non-null values."""
        try:
            result = self.con.execute(f"SELECT 1 FROM {table} WHERE {column} IS NOT NULL LIMIT 1").fetchone()
            return result is not None
        except Exception:
            return False

    @staticmethod
    def _sql_literal(value: str) -> str:
        return "'" + value.replace("'", "''") + "'"

    @classmethod
    def _values_as_rows(cls, values: Sequence[str]) -> str:
        return ", ".join(f"({cls._sql_literal(value)})" for value in values)

    @classmethod
    def _values_as_in_list(cls, values: Sequence[str]) -> str:
        return ", ".join(cls._sql_literal(value) for value in values)

    def _lookup(
        self,
        q_to_nstrs: Mapping[str, Sequence[str]],
        all_queries: Sequence[str],
        prefer_ttys: list[str] | None,
        filter_ontologies: list[str] | None,
        exclude_ontologies: list[str] | None,
        *,
        top_k: int | None = 25,
        ont_top_k: int | None = None,
        allow_partial: bool = True,
        min_coverage: float = 0.6,
        min_word_hits: int | None = None,
        coverage_weight: int = 25,
    ) -> pl.DataFrame:
        """
        Core lookup via exact + partial match paths.

        Returns DataFrame with columns: input_string, hits (list of structs)
        """
        if (top_k is None) == (ont_top_k is None):
            raise ValueError("Exactly one of top_k or ont_top_k must be set.")
        if top_k is not None:
            top_k = max(1, int(top_k))
        if ont_top_k is not None:
            ont_top_k = max(1, int(ont_top_k))

        qmap_rows, qword_rows = build_query_rows(q_to_nstrs, allow_partial=allow_partial)

        if not qmap_rows:
            return pl.DataFrame({"input_string": all_queries, "hits": [[] for _ in all_queries]}).cast(
                {"hits": pl.List(HIT_STRUCT_TYPE)}
            )

        qmap_df = pl.DataFrame(qmap_rows, schema=["Q", "NSTR"], orient="row")
        self.con.register("qmap", qmap_df.to_arrow())

        # Word-level table for partial path
        partial_enabled = allow_partial and bool(qword_rows)
        if partial_enabled:
            qwords_df = pl.DataFrame(qword_rows, schema=["Q", "NSTR", "NWD"], orient="row")
            self.con.register("qwords", qwords_df.to_arrow())

        # Build preference clauses
        tty_join, tty_bump_expr = build_pref_join(
            prefer_ttys,
            column_expr="a.name_type",
            alias="pt",
            value_col="tty",
            values_sql_builder=self._values_as_rows,
        )

        # Ontology filtering (include and exclude)
        combined_where, nw_filter_clause = build_ontology_filter_clauses(
            filter_ontologies,
            exclude_ontologies,
            values_sql_builder=self._values_as_in_list,
        )

        # STT bump
        stt_bump_expr = "CASE WHEN a.stt='PF' THEN 1 ELSE 0 END" if self._has_stt else "0"

        hits_agg_expr = build_hits_agg_expr(
            kind="duckdb",
            score_expr="rank::BIGINT",
            total_score_expr="total_score::BIGINT",
        )

        sql = build_lookup_sql(
            with_ctes=[],
            ns_table=NS_TABLE,
            nw_table=NW_TABLE,
            atoms_table=ATOMS_TABLE,
            tty_join=tty_join,
            combined_where=combined_where,
            nw_filter_clause=nw_filter_clause,
            stt_bump_expr=stt_bump_expr,
            tty_bump_expr=tty_bump_expr,
            min_word_hits=min_word_hits,
            min_coverage=min_coverage,
            coverage_weight=coverage_weight,
            top_k=top_k,
            ont_top_k=ont_top_k,
            partial_enabled=partial_enabled,
            coverage_cast="DOUBLE",
            hits_agg_expr=hits_agg_expr,
        )

        # Register all queries for preserving order
        allq_df = pl.DataFrame({"Q": all_queries, "idx": list(range(len(all_queries)))})
        self.con.register("allq", allq_df.to_arrow())

        out = self.con.execute(sql).pl()
        out = out.with_columns(pl.col("hits").fill_null([]).cast(pl.List(HIT_STRUCT_TYPE)))

        with contextlib.suppress(Exception):
            self.con.unregister("qmap")
            self.con.unregister("allq")
            if partial_enabled:
                self.con.unregister("qwords")

        return out

    def normalize(
        self,
        strings: Sequence[str],
        synonyms: Sequence[Sequence[str] | None] | None = None,
        top_k: int | None = 25,
        ont_top_k: int | None = None,
        prefer_ttys: list[str] | None = None,
        filter_ontologies: list[str] | None = None,
        exclude_ontologies: list[str] | None = None,
        allow_partial: bool = True,
        min_coverage: float = 0.6,
        min_word_hits: int | None = None,
        coverage_weight: int = 25,
    ) -> pl.DataFrame:
        """
        Normalize input strings to ranked concepts.

        Args:
            strings: Input strings to normalize
            synonyms: Optional list of synonym lists aligned with `strings`
                (same length required). Synonyms are normalized and used
                alongside the main string to improve matching. Results are
                still keyed by the original input string.
            top_k: Maximum number of results per query (mutually exclusive with ont_top_k)
            ont_top_k: Maximum number of results per ontology (mutually exclusive with top_k)
            prefer_ttys: Term types to prefer (e.g., ["PT", "MH"])
            filter_ontologies: Restrict to these ontologies (include only)
            exclude_ontologies: Exclude these ontologies
            allow_partial: Enable word-overlap partial matching
            min_coverage: Minimum fraction of query words that must match
            min_word_hits: Minimum absolute word hits required
            coverage_weight: Weight for coverage in scoring

        Returns:
            DataFrame with columns: input_string, hits (list of match structs),
            and synonyms (list of strings) if synonyms were provided.
        """
        # Apply defaults
        if prefer_ttys is None:
            prefer_ttys = DEFAULT_PREFER_TTYS

        strings_list = list(strings)
        query_keys = [f"q{i}" for i in range(len(strings_list))] if synonyms is not None else strings_list

        # Build normalized string map with per-entry keys
        q_to_nstrs, syn_list = build_normalized_query_map(strings_list, synonyms, query_keys=query_keys)

        result = self._lookup(
            q_to_nstrs=q_to_nstrs,
            all_queries=query_keys,
            prefer_ttys=prefer_ttys,
            filter_ontologies=filter_ontologies,
            exclude_ontologies=exclude_ontologies,
            top_k=top_k,
            ont_top_k=ont_top_k,
            allow_partial=allow_partial,
            min_coverage=min_coverage,
            min_word_hits=min_word_hits,
            coverage_weight=coverage_weight,
        )

        result = result.with_columns(pl.Series("input_string", strings_list))

        # Add synonyms column if synonyms were provided
        if synonyms is not None:
            syn_list = syn_list if syn_list is not None else [[] for _ in strings_list]
            result = result.with_columns(pl.Series("synonyms", syn_list))

        return result

    def concept_info(
        self,
        concept_ids: Sequence[str],
        prefer_ttys: list[str] | None = None,
        prefer_def_sources: list[str] | None = None,
    ) -> dict[str, ConceptInfo]:
        """
        Get detailed information for concepts.

        Args:
            concept_ids: List of concept IDs
            prefer_ttys: Preferred term types
            prefer_def_sources: Preferred sources for definitions

        Returns:
            Dict mapping concept_id to ConceptInfo
        """
        if not concept_ids:
            return {}
        id_list, res = init_concept_info_map(concept_ids)
        id_df = pl.DataFrame({"concept_id": id_list})
        self.con.register("idmap", id_df.to_arrow())

        self._populate_concept_info(res, prefer_ttys, prefer_def_sources)

        with contextlib.suppress(Exception):
            self.con.unregister("idmap")

        return res

    def _populate_concept_info(
        self,
        res: dict[str, ConceptInfo],
        prefer_ttys: list[str] | None,
        prefer_def_sources: list[str] | None,
    ) -> None:
        """Populate ConceptInfo for all concepts."""
        if prefer_ttys is None:
            prefer_ttys = DEFAULT_PREFER_TTYS

        # Build preference clauses
        tty_join, tty_bump = build_pref_join(
            prefer_ttys,
            column_expr="a.name_type",
            alias="pt",
            value_col="tty",
            values_sql_builder=self._values_as_rows,
        )
        def_pref_join, def_pref_bump = build_pref_join(
            prefer_def_sources,
            column_expr="d.source",
            alias="pds",
            value_col="sab",
            values_sql_builder=self._values_as_rows,
        )

        stt_bump = "CASE WHEN a.stt='PF' THEN 1 ELSE 0 END" if self._has_stt else "0"

        # Main query for names
        sql = build_concept_names_sql(
            idmap_cte=None,
            atoms_table=ATOMS_TABLE,
            tty_join=tty_join,
            tty_bump=tty_bump,
            stt_bump=stt_bump,
        )

        out = self.con.execute(sql).pl()
        apply_concept_name_rows(res, out.iter_rows(named=True))

        # Definitions (if available)
        if self._has_defs:
            self._populate_definitions(res, def_pref_join, def_pref_bump)

        # Semantic types (if available)
        if self._has_types:
            self._populate_semantic_types(res)

    def _populate_definitions(
        self,
        res: dict[str, ConceptInfo],
        def_pref_join: str,
        def_pref_bump: str,
    ) -> None:
        """Populate definitions for concepts."""
        sql = build_definitions_sql(
            idmap_cte=None,
            defs_table=DEFS_TABLE,
            def_pref_join=def_pref_join,
            def_pref_bump=def_pref_bump,
        )

        out = self.con.execute(sql).pl()
        apply_definition_rows(res, out.iter_rows(named=True))

    def _semantic_type_query(self) -> str:
        return build_semantic_types_sql(idmap_cte=None, types_table=TYPES_TABLE)

    def _populate_semantic_types(self, res: dict[str, ConceptInfo]) -> None:
        """Populate semantic types for concepts."""
        out = self.con.execute(self._semantic_type_query()).pl()
        apply_semantic_type_rows(res, out.iter_rows(named=True))

    def concept_semantic_types(self, concept_ids: Sequence[str]) -> dict[str, list[dict[str, str]]]:
        """
        Get semantic types for concepts.

        Returns dict mapping concept_id to list of {"tui": ..., "sty": ...}
        """
        if not self._has_types or not concept_ids:
            return {cid: [] for cid in concept_ids}

        id_list = list(dict.fromkeys(concept_ids))
        id_df = pl.DataFrame({"concept_id": id_list})
        self.con.register("idmap", id_df.to_arrow())

        out = self.con.execute(self._semantic_type_query()).pl()

        with contextlib.suppress(Exception):
            self.con.unregister("idmap")

        res: dict[str, list[dict[str, str]]] = {cid: [] for cid in id_list}
        for row in out.iter_rows(named=True):
            res[row["concept_id"]].append({"tui": row["type_id"], "sty": row["type_name"]})

        return res

    def get_narrower_concepts(
        self,
        concept_id: str,
        max_depth: int | None = 10,
        filter_ontologies: list[str] | None = None,
    ) -> list[str]:
        """
        Get all narrower (descendant) concept IDs using recursive traversal.

        Uses the hierarchy edges to walk down the tree/DAG from the given concept.

        Args:
            concept_id: Starting concept ID (broader term)
            max_depth: Maximum depth to traverse (1 = direct children only, None = all descendants)
            filter_ontologies: Only follow edges from these ontologies (e.g., ["UMLS", "CHEBI"])

        Returns:
            List of descendant concept IDs (excludes the starting concept)
        """
        if not self._has_edges:
            return []

        # Build ontology filter clause
        ontology_filter = ""
        if filter_ontologies:
            ontologies_sql = self._values_as_in_list(filter_ontologies)
            ontology_filter = f" AND e.ontology IN ({ontologies_sql})"

        # DuckDB recursive CTE
        query = dedent(
            f"""
            WITH RECURSIVE walk(concept_id, depth) AS (
                SELECT $1::VARCHAR, 0

                UNION ALL

                SELECT e.child_id, w.depth + 1
                FROM walk w
                JOIN {EDGES_TABLE} e ON e.parent_id = w.concept_id
                WHERE ($2 IS NULL OR w.depth < $2){ontology_filter}
            )
            SELECT DISTINCT concept_id
            FROM walk
            WHERE concept_id != $1
            """
        )

        result = self.con.execute(query, [concept_id, max_depth]).fetchall()
        return [r[0] for r in result]

    def close(self) -> None:
        """Close the database connection."""
        self.con.close()

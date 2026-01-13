"""
Async PostgreSQL normalizer for biomedical concept normalization.

Works with PostgreSQL databases using the same schema as DuckDB databases
built by build_umls_duckdb, build_ontology_duckdb, or build_merged_duckdb.
"""

import json
from collections.abc import Mapping, Sequence
from textwrap import dedent
from typing import Any

import polars as pl
from sqlalchemy import RowMapping, text
from sqlalchemy.ext.asyncio import AsyncEngine

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
from norm_toolkit.normalizer_cache import ExpansionCache, NormalizerCache
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


class _SqlParams:
    def __init__(self) -> None:
        self.params: dict[str, Any] = {}
        self._idx = 0

    def add(self, value: Any) -> str:
        key = f"p{self._idx}"
        self.params[key] = value
        self._idx += 1
        return f":{key}"

    def add_row(self, values: Sequence[Any]) -> str:
        return f"({', '.join(self.add(value) for value in values)})"

    def add_rows(self, rows: Sequence[Sequence[Any]]) -> str:
        return ", ".join(self.add_row(row) for row in rows)

    def add_values(self, values: Sequence[Any]) -> str:
        return ", ".join(self.add(value) for value in values)

    def add_single_column_values(self, values: Sequence[Any]) -> str:
        return self.add_rows([[value] for value in values])

    def add_cast(self, value: Any, sql_type: str) -> str:
        return f"CAST({self.add(value)} AS {sql_type})"


class PostgresNormalizer:
    """
    Async normalizer using PostgreSQL via SQLAlchemy.

    Optimized for small batch processing (1-5 strings at a time).
    Uses VALUES clauses instead of temp tables for efficiency with small batches.
    """

    def __init__(
        self,
        engine: AsyncEngine,
        schema: str = "public",
        owned_resource: Any | None = None,
        cache_maxsize: int = 10000,
        enable_cache: bool = True,
    ) -> None:
        """
        Initialize the normalizer with an SQLAlchemy AsyncEngine.

        Args:
            engine: SQLAlchemy AsyncEngine (caller manages lifecycle)
            schema: PostgreSQL schema where tables are located (default: "public")
            owned_resource: Optional resource with async close() method to clean up
                when this normalizer is closed (e.g., AlloyDB AsyncConnector)
            cache_maxsize: Maximum number of entries in each cache
            enable_cache: Whether to enable caching for normalization and expansion

        Note:
            After creating the normalizer, call `await normalizer.initialize()`
            to detect database capabilities before using other methods.
        """
        self._engine = engine
        self._schema = schema
        self._owned_resource = owned_resource
        self._has_types = False
        self._has_defs = False
        self._has_edges = False
        self._has_stt = False
        self._initialized = False

        # Initialize caches
        self._cache: NormalizerCache | None = NormalizerCache(maxsize=cache_maxsize) if enable_cache else None
        self._expansion_cache: ExpansionCache | None = ExpansionCache(maxsize=cache_maxsize) if enable_cache else None

        # Build qualified table names
        prefix = f"{schema}." if schema else ""
        self._ns_table = f"{prefix}{NS_TABLE}"
        self._nw_table = f"{prefix}{NW_TABLE}"
        self._atoms_table = f"{prefix}{ATOMS_TABLE}"
        self._types_table = f"{prefix}{TYPES_TABLE}"
        self._defs_table = f"{prefix}{DEFS_TABLE}"
        self._edges_table = f"{prefix}{EDGES_TABLE}"

    async def _ensure_initialized(self) -> None:
        """Lazily initialize on first use."""
        if self._initialized:
            return
        self._has_types = await self._table_has_rows(self._types_table)
        self._has_defs = await self._table_has_rows(self._defs_table)
        self._has_edges = await self._table_has_rows(self._edges_table)
        self._has_stt = await self._column_has_values(self._atoms_table, "stt")
        self._initialized = True

    async def _table_has_rows(self, table: str) -> bool:
        """Check if a table exists and has rows."""
        try:
            async with self._engine.connect() as conn:
                result = await conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
                return result.scalar() is not None
        except Exception:
            return False

    async def _column_has_values(self, table: str, column: str) -> bool:
        """Check if a column has any non-null values."""
        try:
            async with self._engine.connect() as conn:
                result = await conn.execute(text(f"SELECT 1 FROM {table} WHERE {column} IS NOT NULL LIMIT 1"))
                return result.scalar() is not None
        except Exception:
            return False

    async def _fetch_rows(self, sql: str, params: Mapping[str, Any] | None = None) -> Sequence[RowMapping]:
        async with self._engine.connect() as conn:
            result = await conn.execute(text(sql), params or {})
            return result.mappings().all()

    async def normalize(
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
        await self._ensure_initialized()

        if prefer_ttys is None:
            prefer_ttys = DEFAULT_PREFER_TTYS

        if (top_k is None) == (ont_top_k is None):
            raise ValueError("Exactly one of top_k or ont_top_k must be set.")
        if top_k is not None:
            top_k = max(1, int(top_k))
        if ont_top_k is not None:
            ont_top_k = max(1, int(ont_top_k))

        strings_list = list(strings)
        query_keys = [f"q{i}" for i in range(len(strings_list))] if synonyms is not None else strings_list

        def make_cache_key(nstrs: tuple[str, ...]) -> Any:
            return NormalizerCache.make_key(
                nstrs,
                top_k=top_k,
                ont_top_k=ont_top_k,
                prefer_ttys=prefer_ttys,
                filter_ontologies=filter_ontologies,
                exclude_ontologies=exclude_ontologies,
                allow_partial=allow_partial,
                min_coverage=min_coverage,
                min_word_hits=min_word_hits,
                coverage_weight=coverage_weight,
            )

        # Build normalized string map with per-entry keys (tuples for cache keys)
        q_to_nstrs, syn_list = build_normalized_query_map(strings_list, synonyms, query_keys=query_keys)

        # Check cache for each input
        cached_hits: dict[str, list[dict[str, Any]]] = {}
        uncached_q_to_nstrs: dict[str, tuple[str, ...]] = {}

        for q, nstrs in q_to_nstrs.items():
            if not nstrs:
                # No normalized strings, empty result
                cached_hits[q] = []
                continue

            if self._cache is not None:
                cache_key = make_cache_key(nstrs)
                cached = self._cache.get(cache_key)
                if cached is not None:
                    cached_hits[q] = cached
                    continue

            uncached_q_to_nstrs[q] = nstrs

        # Query DB for uncached entries
        if uncached_q_to_nstrs:
            fresh_result = await self._lookup(
                q_to_nstrs=uncached_q_to_nstrs,
                all_queries=list(uncached_q_to_nstrs),
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

            # Enrich fresh results
            fresh_result = await self._enrich_hits_with_concept_info(fresh_result, prefer_ttys)

            # Cache fresh results and add to cached_hits
            for row in fresh_result.iter_rows(named=True):
                q = row["input_string"]
                hits = row["hits"] or []
                cached_hits[q] = hits

                if self._cache is not None:
                    nstrs = uncached_q_to_nstrs[q]
                    cache_key = make_cache_key(nstrs)
                    self._cache.set(cache_key, hits)

        # Build final result in original order
        result_data = [
            {"input_string": strings_list[i], "hits": cached_hits.get(query_keys[i], [])}
            for i in range(len(strings_list))
        ]
        result = pl.DataFrame(result_data).cast({"hits": pl.List(HIT_STRUCT_TYPE)})

        # Add synonyms column if synonyms were provided
        if synonyms is not None:
            syn_list = syn_list if syn_list is not None else [[] for _ in strings_list]
            result = result.with_columns(pl.Series("synonyms", syn_list))

        return result

    async def _lookup(
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
        """Core lookup via exact + partial match paths."""
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

        # Build parameters and VALUES clauses using named parameters
        sql_params = _SqlParams()

        qmap_values = sql_params.add_rows(qmap_rows)

        qwords_values = sql_params.add_rows(qword_rows) if qword_rows else ""

        allq_values = ", ".join(
            f"({sql_params.add(q)}, {sql_params.add_cast(i, 'INTEGER')})" for i, q in enumerate(all_queries)
        )

        # Build preference clauses (parameterized to prevent SQL injection)
        tty_join, tty_bump_expr = build_pref_join(
            prefer_ttys,
            column_expr="a.name_type",
            alias="pt",
            value_col="tty",
            values_sql_builder=sql_params.add_single_column_values,
        )

        # Ontology filtering (parameterized to prevent SQL injection)
        combined_where, nw_filter_clause = build_ontology_filter_clauses(
            filter_ontologies,
            exclude_ontologies,
            values_sql_builder=sql_params.add_values,
        )

        # STT bump
        stt_bump_expr = "CASE WHEN a.stt='PF' THEN 1 ELSE 0 END" if self._has_stt else "0"

        partial_enabled = allow_partial and bool(qwords_values)

        qmap_cte = f"qmap(Q, NSTR) AS (VALUES {qmap_values})"
        allq_cte = f"allq(Q, idx) AS (VALUES {allq_values})"
        with_ctes = [qmap_cte]
        if partial_enabled:
            with_ctes.append(f"qwords(Q, NSTR, NWD) AS (VALUES {qwords_values})")
        with_ctes.append(allq_cte)

        hits_agg_expr = build_hits_agg_expr(
            kind="postgres",
            score_expr="rank",
            total_score_expr="total_score",
        )

        sql = build_lookup_sql(
            with_ctes=with_ctes,
            ns_table=self._ns_table,
            nw_table=self._nw_table,
            atoms_table=self._atoms_table,
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
            coverage_cast="DOUBLE PRECISION",
            hits_agg_expr=hits_agg_expr,
        )

        rows = await self._fetch_rows(sql, sql_params.params)

        # Parse results into Polars DataFrame
        # Note: asyncpg auto-deserializes JSON, so hits may already be a list
        data = []
        for row in rows:
            input_string = row["input_string"]
            hits_raw = row["hits"]
            if hits_raw is None:
                hits = []
            elif isinstance(hits_raw, list):
                hits = hits_raw  # Already deserialized by asyncpg
            else:
                hits = json.loads(hits_raw)  # String, needs parsing
            data.append({"input_string": input_string, "hits": hits})

        return pl.DataFrame(data).cast({"hits": pl.List(HIT_STRUCT_TYPE)})

    async def _enrich_hits_with_concept_info(
        self,
        result: pl.DataFrame,
        prefer_ttys: list[str] | None,
    ) -> pl.DataFrame:
        """Enrich hits with pref_name, description, and synonyms from concept_info."""
        # Collect all unique concept_ids from hits
        all_concept_ids: set[str] = set()
        for hits in result["hits"].to_list():
            if hits:
                for hit in hits:
                    if hit and "global_identifier" in hit:
                        all_concept_ids.add(hit["global_identifier"])

        concept_infos = await self.concept_info(list(all_concept_ids), prefer_ttys=prefer_ttys)

        # Enrich each hit
        enriched_data = []
        for row in result.iter_rows(named=True):
            enriched_hits = []
            for hit in row["hits"] or []:
                enriched_hit = dict(hit)
                cid = hit.get("global_identifier")
                info = concept_infos.get(cid) if cid else None
                if info:
                    enriched_hit["pref_name"] = info.preferred_name
                    enriched_hit["description"] = info.description
                    enriched_hit["synonyms"] = info.synonyms or []
                else:
                    enriched_hit["pref_name"] = None
                    enriched_hit["description"] = None
                    enriched_hit["synonyms"] = []
                enriched_hits.append(enriched_hit)
            enriched_data.append({"input_string": row["input_string"], "hits": enriched_hits})

        return pl.DataFrame(enriched_data).cast({"hits": pl.List(HIT_STRUCT_TYPE)})

    async def concept_info(
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
        await self._ensure_initialized()

        if not concept_ids:
            return {}

        if prefer_ttys is None:
            prefer_ttys = DEFAULT_PREFER_TTYS

        id_list, res = init_concept_info_map(concept_ids)

        # Build idmap VALUES clause using named parameters
        sql_params = _SqlParams()
        idmap_values = sql_params.add_single_column_values(id_list)

        # Build preference clauses
        tty_join, tty_bump = build_pref_join(
            prefer_ttys,
            column_expr="a.name_type",
            alias="pt",
            value_col="tty",
            values_sql_builder=sql_params.add_single_column_values,
        )

        stt_bump = "CASE WHEN a.stt='PF' THEN 1 ELSE 0 END" if self._has_stt else "0"

        # Main query for names
        sql = build_concept_names_sql(
            idmap_cte=f"idmap(concept_id) AS (VALUES {idmap_values})",
            atoms_table=self._atoms_table,
            tty_join=tty_join,
            tty_bump=tty_bump,
            stt_bump=stt_bump,
        )

        rows = await self._fetch_rows(sql, sql_params.params)
        apply_concept_name_rows(res, rows)

        # Definitions (if available)
        if self._has_defs:
            await self._populate_definitions(res, id_list, prefer_def_sources)

        # Semantic types (if available)
        if self._has_types:
            await self._populate_semantic_types(res, id_list)

        return res

    async def _populate_definitions(
        self,
        res: dict[str, ConceptInfo],
        id_list: list[str],
        prefer_def_sources: list[str] | None,
    ) -> None:
        """Populate definitions for concepts."""
        sql_params = _SqlParams()
        idmap_values = sql_params.add_single_column_values(id_list)

        def_pref_join, def_pref_bump = build_pref_join(
            prefer_def_sources,
            column_expr="d.source",
            alias="pds",
            value_col="sab",
            values_sql_builder=sql_params.add_single_column_values,
        )

        sql = build_definitions_sql(
            idmap_cte=f"idmap(concept_id) AS (VALUES {idmap_values})",
            defs_table=self._defs_table,
            def_pref_join=def_pref_join,
            def_pref_bump=def_pref_bump,
        )

        rows = await self._fetch_rows(sql, sql_params.params)
        apply_definition_rows(res, rows)

    async def _fetch_semantic_type_rows(
        self,
        id_list: Sequence[str],
    ) -> Sequence[RowMapping]:
        if not id_list:
            return []

        sql_params = _SqlParams()
        idmap_values = sql_params.add_single_column_values(id_list)

        sql = build_semantic_types_sql(
            idmap_cte=f"idmap(concept_id) AS (VALUES {idmap_values})",
            types_table=self._types_table,
        )

        return await self._fetch_rows(sql, sql_params.params)

    async def _populate_semantic_types(
        self,
        res: dict[str, ConceptInfo],
        id_list: list[str],
    ) -> None:
        """Populate semantic types for concepts."""
        rows = await self._fetch_semantic_type_rows(id_list)
        apply_semantic_type_rows(res, rows)

    async def concept_semantic_types(
        self,
        concept_ids: Sequence[str],
    ) -> dict[str, list[dict[str, str]]]:
        """
        Get semantic types for concepts.

        Returns dict mapping concept_id to list of {"tui": ..., "sty": ...}
        """
        await self._ensure_initialized()

        if not self._has_types or not concept_ids:
            return {cid: [] for cid in concept_ids}

        id_list = list(dict.fromkeys(concept_ids))

        rows = await self._fetch_semantic_type_rows(id_list)

        res: dict[str, list[dict[str, str]]] = {cid: [] for cid in id_list}
        for row in rows:
            res[row["concept_id"]].append({"tui": row["type_id"], "sty": row["type_name"]})

        return res

    async def get_narrower_concepts(
        self,
        concept_id: str,
        max_depth: int | None = 10,
        filter_ontologies: list[str] | None = None,
        max_ids: int | None = None,
    ) -> list[str]:
        """
        Get all narrower (descendant) concept IDs using recursive traversal.

        Uses the hierarchy edges to walk down the tree/DAG from the given concept.

        Args:
            concept_id: Starting concept ID (broader term)
            max_depth: Maximum depth to traverse (1 = direct children only, None = all descendants)
            filter_ontologies: Only follow edges from these ontologies (e.g., ["UMLS", "CHEBI"])
            max_ids: Maximum number of concept IDs to return (None = no limit)

        Returns:
            List of descendant concept IDs ordered by depth (shallowest first),
            excludes the starting concept
        """
        await self._ensure_initialized()

        if not self._has_edges:
            return []

        cache_key = None
        if self._expansion_cache is not None:
            cache_key = ExpansionCache.make_key(
                concept_id,
                max_depth=max_depth,
                filter_ontologies=filter_ontologies,
                max_ids=max_ids,
            )
            cached = self._expansion_cache.get(cache_key)
            if cached is not None:
                return cached

        params: dict[str, Any] = {"concept_id": concept_id, "max_depth": max_depth}

        # Build ontology filter clause
        ontology_filter = ""
        if filter_ontologies:
            ont_placeholders = []
            for i, ont in enumerate(filter_ontologies):
                key = f"ont{i}"
                params[key] = ont
                ont_placeholders.append(f":{key}")
            ontologies_sql = ", ".join(ont_placeholders)
            ontology_filter = f" AND e.ontology IN ({ontologies_sql})"

        # Build optional LIMIT clause
        limit_clause = ""
        if max_ids is not None:
            params["max_ids"] = max_ids
            limit_clause = "\nLIMIT :max_ids"

        # PostgreSQL recursive CTE with named parameters
        # Use CAST() instead of :: to avoid conflicts with SQLAlchemy named params
        # UNION (not UNION ALL) deduplicates on (concept_id, depth) during recursion
        # GROUP BY with MIN(depth) gets shortest path depth for each concept
        query = dedent(
            f"""
            WITH RECURSIVE walk(concept_id, depth) AS (
                SELECT CAST(:concept_id AS VARCHAR), 0

                UNION

                SELECT e.child_id, w.depth + 1
                FROM walk w
                JOIN {self._edges_table} e ON e.parent_id = w.concept_id
                WHERE (CAST(:max_depth AS INTEGER) IS NULL OR w.depth < :max_depth){ontology_filter}
            )
            SELECT concept_id, MIN(depth) AS min_depth
            FROM walk
            WHERE concept_id != :concept_id
            GROUP BY concept_id
            ORDER BY min_depth, concept_id{limit_clause}
            """
        )

        rows = await self._fetch_rows(query, params)

        result = [r["concept_id"] for r in rows]
        if self._expansion_cache is not None and cache_key is not None:
            self._expansion_cache.set(cache_key, result)
        return result

    def cache_stats(self) -> dict[str, Any] | None:
        """
        Get normalization cache statistics.

        Returns:
            Dict with size, maxsize, hits, misses, and hit_rate,
            or None if caching is disabled.
        """
        if self._cache is None:
            return None
        return self._cache.stats()

    def expansion_cache_stats(self) -> dict[str, Any] | None:
        """
        Get entity expansion cache statistics.

        Returns:
            Dict with size, maxsize, hits, misses, and hit_rate,
            or None if caching is disabled.
        """
        if self._expansion_cache is None:
            return None
        return self._expansion_cache.stats()

    def clear_cache(self) -> None:
        """Clear all cached entries."""
        if self._cache is not None:
            self._cache.clear()
        if self._expansion_cache is not None:
            self._expansion_cache.clear()

    async def close(self) -> None:
        """
        Close the engine and any owned resources.

        Note: Only call this if you want to close the engine. If the engine
        is managed externally, the caller should close it instead.
        """
        await self._engine.dispose()
        if self._owned_resource is not None:
            await self._owned_resource.close()

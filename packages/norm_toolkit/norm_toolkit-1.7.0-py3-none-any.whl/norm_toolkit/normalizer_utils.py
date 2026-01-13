"""
Shared helpers for normalizer implementations.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from textwrap import dedent
from typing import Any, Literal

from lvg_norm import lvg_normalize
from sqlalchemy import RowMapping

from norm_toolkit.constants import (
    EXACT_BUMP,
    ISPREF_WEIGHT,
    RANK_MULTIPLIER,
    STT_WEIGHT,
    TTY_WEIGHT,
)
from norm_toolkit.models import ConceptInfo, SemanticType


def _coerce_synonyms_list(
    strings: Sequence[str],
    synonyms: Sequence[Sequence[str] | None] | None,
) -> list[list[str]] | None:
    if synonyms is None:
        return None
    if not isinstance(synonyms, Sequence) or isinstance(synonyms, (str, bytes)):
        raise TypeError("synonyms must be a sequence of sequences aligned with strings")
    if len(synonyms) != len(strings):
        raise ValueError("synonyms must have the same length as strings")
    out: list[list[str]] = []
    for i, syns in enumerate(synonyms):
        if syns is None:
            out.append([])
            continue
        if not isinstance(syns, Sequence) or isinstance(syns, (str, bytes)):
            raise ValueError(f"synonyms[{i}] must be a sequence of strings")
        out.append(list(syns))
    return out


def build_normalized_string_map(
    strings: Sequence[str],
    synonyms: Sequence[Sequence[str] | None] | None = None,
) -> dict[str, tuple[str, ...]]:
    """
    Build a mapping of input string -> normalized string variants.

    Normalized variants are deduplicated while preserving order.
    Duplicate input strings will collapse to the last entry.
    Synonyms must be aligned with `strings` when provided.
    """
    synonyms_list = _coerce_synonyms_list(strings, synonyms)
    syns_iter = synonyms_list if synonyms_list is not None else [None] * len(strings)

    q_to_nstrs: dict[str, tuple[str, ...]] = {}
    for s, syns in zip(strings, syns_iter):
        nstrs = list(lvg_normalize(s) or [])
        if syns:
            for syn in syns:
                nstrs.extend(lvg_normalize(syn) or [])
        q_to_nstrs[s] = tuple(dict.fromkeys(nstrs))
    return q_to_nstrs


def build_normalized_query_map(
    strings: Sequence[str],
    synonyms: Sequence[Sequence[str] | None] | None = None,
    *,
    query_keys: Sequence[str] | None = None,
) -> tuple[dict[str, tuple[str, ...]], list[list[str]] | None]:
    """
    Build a mapping of query key -> normalized string variants.

    Normalized variants are deduplicated while preserving order.
    Synonyms must be aligned with `strings` when provided.
    """
    if query_keys is None:
        query_keys = list(strings)
    if len(query_keys) != len(strings):
        raise ValueError("query_keys must have the same length as strings")

    synonyms_list = _coerce_synonyms_list(strings, synonyms)
    syns_iter = synonyms_list if synonyms_list is not None else [None] * len(strings)

    q_to_nstrs: dict[str, tuple[str, ...]] = {}
    for key, s, syns in zip(query_keys, strings, syns_iter):
        nstrs = list(lvg_normalize(s) or [])
        if syns:
            for syn in syns:
                nstrs.extend(lvg_normalize(syn) or [])
        q_to_nstrs[key] = tuple(dict.fromkeys(nstrs))
    return q_to_nstrs, synonyms_list


def build_query_rows(
    q_to_nstrs: Mapping[str, Sequence[str]],
    *,
    allow_partial: bool,
) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Build query rows for qmap and qwords."""
    qmap_rows: list[tuple[str, str]] = []
    qword_rows: list[tuple[str, str, str]] = []
    for q, nstrs in q_to_nstrs.items():
        for nstr in dict.fromkeys(nstrs):
            if not nstr:
                continue
            qmap_rows.append((q, nstr))
            if allow_partial:
                for word in dict.fromkeys(nstr.split()):
                    if word:
                        qword_rows.append((q, nstr, word))
    return qmap_rows, qword_rows


def build_pref_join(
    values: Sequence[str] | None,
    *,
    column_expr: str,
    alias: str,
    value_col: str,
    values_sql_builder: Callable[[Sequence[str]], str],
) -> tuple[str, str]:
    """Build a preference join and bump expression from a VALUES clause."""
    if not values:
        return "", "0"
    vals = values_sql_builder(values)
    join = f"LEFT JOIN (VALUES {vals}) AS {alias}({value_col}) ON {column_expr} = {alias}.{value_col}"
    bump = f"CASE WHEN {alias}.{value_col} IS NULL THEN 0 ELSE 1 END"
    return join, bump


def build_ontology_filter_clauses(
    filter_ontologies: Sequence[str] | None,
    exclude_ontologies: Sequence[str] | None,
    *,
    values_sql_builder: Callable[[Sequence[str]], str],
    atoms_alias: str = "a",
    nw_alias: str = "nw",
) -> tuple[str, str]:
    """Build WHERE and nw filter clauses for ontology include/exclude lists."""
    ontology_filter_exprs: list[str] = []
    nw_filter_exprs: list[str] = []
    if filter_ontologies:
        vals = values_sql_builder(filter_ontologies)
        ontology_filter_exprs.append(f"{atoms_alias}.ontology IN ({vals})")
        nw_filter_exprs.append(f"{nw_alias}.ontology IN ({vals})")
    if exclude_ontologies:
        vals = values_sql_builder(exclude_ontologies)
        ontology_filter_exprs.append(f"{atoms_alias}.ontology NOT IN ({vals})")
        nw_filter_exprs.append(f"{nw_alias}.ontology NOT IN ({vals})")
    combined_where = f"WHERE {' AND '.join(ontology_filter_exprs)}" if ontology_filter_exprs else ""
    nw_filter_clause = f" AND {' AND '.join(nw_filter_exprs)}" if nw_filter_exprs else ""
    return combined_where, nw_filter_clause


def build_hits_agg_expr(
    *,
    kind: Literal["duckdb", "postgres"],
    score_expr: str,
    total_score_expr: str,
) -> str:
    """Build the hits aggregation expression for the lookup query."""
    fields = [
        ("global_identifier", "concept_id"),
        ("identifier", "identifier"),
        ("nstr", "NSTR"),
        ("name", "str"),
        ("source", "source"),
        ("ontology", "ontology"),
        ("name_type", "name_type"),
        ("score", score_expr),
        ("total_score", total_score_expr),
        ("match_type", "CASE WHEN is_exact THEN 'exact' ELSE 'partial' END"),
    ]

    if kind == "duckdb":
        fields_sql = ",\n".join(f"'{key}': {value}" for key, value in fields)
        return dedent(
            f"""
            LIST({{
                {fields_sql}
            }} ORDER BY total_score DESC, concept_id) AS hits
            """
        ).strip()

    if kind == "postgres":
        fields_sql = ",\n".join(f"'{key}', {value}" for key, value in fields)
        return dedent(
            f"""
            JSON_AGG(
                JSON_BUILD_OBJECT(
                    {fields_sql}
                ) ORDER BY total_score DESC, concept_id
            ) AS hits
            """
        ).strip()

    raise ValueError(f"Unsupported hits agg kind: {kind}")


def _format_with_clause(ctes: Sequence[str | None]) -> str:
    entries = [cte.strip() for cte in ctes if cte and cte.strip()]
    if not entries:
        return ""
    return "WITH\n" + ",\n".join(entries) + "\n"


def build_lookup_sql(
    *,
    with_ctes: Sequence[str],
    ns_table: str,
    nw_table: str,
    atoms_table: str,
    tty_join: str,
    combined_where: str,
    nw_filter_clause: str,
    stt_bump_expr: str,
    tty_bump_expr: str,
    min_word_hits: int | None,
    min_coverage: float,
    coverage_weight: int,
    top_k: int | None,
    ont_top_k: int | None,
    partial_enabled: bool,
    coverage_cast: str,
    hits_agg_expr: str,
) -> str:
    """Build the unified lookup SQL for exact/partial matching."""
    if (top_k is None) == (ont_top_k is None):
        raise ValueError("Exactly one of top_k or ont_top_k must be set.")
    min_hits_sql = str(min_word_hits) if min_word_hits is not None else "0"
    cov_sql = f"{min_coverage:.6f}"
    dedup_order = "rank DESC, ispref_bump DESC, stt_bump DESC, tty_bump DESC, concept_id"
    score_expr = (
        f"rank*{RANK_MULTIPLIER} + ispref_bump*{ISPREF_WEIGHT} + stt_bump*{STT_WEIGHT}"
        f" + tty_bump*{TTY_WEIGHT} + ROUND(coverage * {coverage_weight})"
    )
    exact_score_expr = f"({score_expr} + {EXACT_BUMP})::INTEGER"
    partial_score_expr = f"({score_expr})::INTEGER"
    cand_cols_template = dedent(
        f"""
        {{q_alias}}.Q, {{q_alias}}.NSTR,
        a.concept_id,
        a.identifier,
        a.str,
        a.source,
        a.ontology,
        a.name_type,
        a.ispref,
        a.rank,
        CASE WHEN a.ispref='Y' THEN 1 ELSE 0 END AS ispref_bump,
        {stt_bump_expr} AS stt_bump,
        {tty_bump_expr} AS tty_bump,
        {{coverage_expr}} AS coverage
        """
    ).strip()

    exact_cte = dedent(
        f"""
        cand_exact AS (
            SELECT
                {cand_cols_template.format(q_alias="q", coverage_expr="1.0")}
            FROM qmap q
            JOIN {ns_table} ns ON ns.nstr = q.NSTR
            JOIN {atoms_table} a
                ON a.concept_id = ns.concept_id
                AND a.name_id = ns.name_id
            {tty_join}
            {combined_where}
        ),
        dedup_exact AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY Q, concept_id
                    ORDER BY {dedup_order}
                ) AS rnc
            FROM cand_exact
        ),
        scored_exact AS (
            SELECT
                Q, NSTR, concept_id, identifier, str, source, ontology, name_type, ispref, rank,
                {exact_score_expr} AS total_score,
                TRUE AS is_exact
            FROM dedup_exact
            WHERE rnc = 1
        )
        """
    ).strip()

    partial_cte = ""
    union_partial = ""
    if partial_enabled:
        partial_cte = dedent(
            f"""
            qn AS (
                SELECT Q, NSTR, COUNT(DISTINCT NWD) AS need
                FROM qwords
                GROUP BY Q, NSTR
            ),
            hits AS (
                SELECT qw.Q, qw.NSTR, nw.string_id, nw.concept_id,
                       COUNT(DISTINCT qw.NWD) AS hits
                FROM qwords qw
                JOIN {nw_table} nw ON nw.nwd = qw.NWD{nw_filter_clause}
                GROUP BY qw.Q, qw.NSTR, nw.string_id, nw.concept_id
            ),
            good AS (
                SELECT h.Q, h.NSTR, h.string_id, h.concept_id, h.hits, qn.need,
                    CAST(h.hits AS {coverage_cast})/NULLIF(qn.need,0) AS coverage
                FROM hits h
                JOIN qn ON qn.Q = h.Q AND qn.NSTR = h.NSTR
                WHERE h.hits >= GREATEST({min_hits_sql}, CAST(CEIL(qn.need * {cov_sql}) AS INTEGER))
            ),
            cand_partial AS (
                SELECT
                    {cand_cols_template.format(q_alias="g", coverage_expr="COALESCE(g.coverage, 0.0)")}
                FROM good g
                JOIN {atoms_table} a ON a.string_id = g.string_id
                {tty_join}
                {combined_where}
            ),
            dedup_partial AS (
                SELECT *,
                    ROW_NUMBER() OVER (
                        PARTITION BY Q, concept_id
                        ORDER BY {dedup_order}
                    ) AS rnc
                FROM cand_partial
            ),
            scored_partial AS (
                SELECT
                    Q, NSTR, concept_id, identifier, str, source, ontology, name_type, ispref, rank,
                    {partial_score_expr} AS total_score,
                    FALSE AS is_exact
                FROM dedup_partial
                WHERE rnc = 1
            )
            """
        ).strip()
        union_partial = "UNION ALL SELECT * FROM scored_partial"

    scored_cte = dedent(
        f"""
        scored AS (
            SELECT * FROM scored_exact
            {union_partial}
        )
        """
    ).strip()
    dedup_concept_cte = dedent(
        """
        dedup_concept AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY Q, concept_id ORDER BY total_score DESC) AS rcid
            FROM scored
        )
        """
    ).strip()
    if ont_top_k is None:
        best_cte = dedent(
            """
            best AS (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY Q ORDER BY total_score DESC, concept_id) AS rn
                FROM dedup_concept
                WHERE rcid = 1
            )
            """
        ).strip()
        topk_cte = dedent(
            f"""
            topk AS (
                SELECT * FROM best WHERE rn <= {top_k}
            )
            """
        ).strip()
    else:
        best_cte = dedent(
            """
            best AS (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY Q, ontology ORDER BY total_score DESC, concept_id) AS rn_ont
                FROM dedup_concept
                WHERE rcid = 1
            )
            """
        ).strip()
        topk_cte = dedent(
            f"""
            topk AS (
                SELECT * FROM best WHERE rn_ont <= {ont_top_k}
            )
            """
        ).strip()
    agg_cte = dedent(
        f"""
        agg AS (
            SELECT
                Q,
                {hits_agg_expr}
            FROM topk
            GROUP BY Q
        )
        """
    ).strip()

    cte_entries = [*with_ctes, exact_cte]
    if partial_enabled:
        cte_entries.append(partial_cte)
    cte_entries.extend([scored_cte, dedup_concept_cte, best_cte, topk_cte, agg_cte])

    with_clause = _format_with_clause(cte_entries)
    select_sql = dedent(
        """
        SELECT
            aq.Q AS input_string,
            agg.hits
        FROM allq aq
        LEFT JOIN agg ON agg.Q = aq.Q
        ORDER BY aq.idx;
        """
    )
    return f"{with_clause}{select_sql}"


def build_concept_names_sql(
    *,
    idmap_cte: str | None,
    atoms_table: str,
    tty_join: str,
    tty_bump: str,
    stt_bump: str,
) -> str:
    """Build SQL for preferred names and synonyms."""
    name_ctes = dedent(
        f"""
        name_cand AS (
            SELECT
                c.concept_id, a.str, a.source AS sab, a.ontology AS ontology,
                a.name_type AS tty, a.ispref, a.stt, a.rank,
                CASE WHEN a.ispref='Y' THEN 1 ELSE 0 END AS ispref_bump,
                {stt_bump} AS stt_bump,
                {tty_bump} AS tty_bump,
                a.identifier
            FROM idmap c
            JOIN {atoms_table} a ON a.concept_id = c.concept_id
            {tty_join}
        ),
        name_best AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY concept_id
                    ORDER BY tty_bump DESC, ispref_bump DESC, stt_bump DESC, rank DESC, str
                ) AS rn
            FROM name_cand
        ),
        chosen AS (
            SELECT concept_id, str AS preferred_name, sab AS name_sab, tty AS name_tty, identifier, ontology AS name_ontology
            FROM name_best WHERE rn=1
        ),
        syn_rank AS (
            SELECT sc.*,
                ROW_NUMBER() OVER (
                    PARTITION BY sc.concept_id, LOWER(sc.str)
                    ORDER BY sc.tty_bump DESC, sc.ispref_bump DESC,
                        sc.stt_bump DESC, sc.rank DESC, sc.str
                ) AS rstr
            FROM name_cand sc
        ),
        syn_best_uniq AS (
            SELECT s.concept_id, s.str, s.tty_bump, s.ispref_bump, s.stt_bump, s.rank
            FROM syn_rank s
            LEFT JOIN chosen ch ON ch.concept_id = s.concept_id
            WHERE s.rstr = 1 AND NOT (s.str = ch.preferred_name)
        ),
        syn_agg AS (
            SELECT concept_id,
                ARRAY_AGG(
                    str ORDER BY
                        tty_bump DESC, ispref_bump DESC, stt_bump DESC, rank DESC, str
                ) AS synonyms
            FROM syn_best_uniq
            GROUP BY concept_id
        )
        """
    ).strip()

    with_clause = _format_with_clause([idmap_cte, name_ctes])
    select_sql = dedent(
        """
        SELECT c.concept_id,
            ch.preferred_name, ch.name_sab, ch.name_tty, ch.identifier, ch.name_ontology,
            sa.synonyms
        FROM idmap c
        LEFT JOIN chosen   ch ON ch.concept_id = c.concept_id
        LEFT JOIN syn_agg  sa ON sa.concept_id = c.concept_id
        ORDER BY c.concept_id;
        """
    )
    return f"{with_clause}{select_sql}"


def build_definitions_sql(
    *,
    idmap_cte: str | None,
    defs_table: str,
    def_pref_join: str,
    def_pref_bump: str,
) -> str:
    """Build SQL for preferred definitions."""
    def_ctes = dedent(
        f"""
        def_cand AS (
            SELECT
                d.concept_id, d.source AS sab, d.def_text,
                {def_pref_bump} AS def_pref_bump,
                length(d.def_text) AS def_len
            FROM {defs_table} d
            JOIN idmap c ON c.concept_id = d.concept_id
            {def_pref_join}
        ),
        def_best AS (
            SELECT *,
                ROW_NUMBER() OVER (
                    PARTITION BY concept_id
                    ORDER BY def_pref_bump DESC, def_len DESC
                ) AS drn
            FROM def_cand
        )
        """
    ).strip()

    with_clause = _format_with_clause([idmap_cte, def_ctes])
    select_sql = dedent(
        """
        SELECT concept_id, def_text, sab AS def_sab
        FROM def_best
        WHERE drn = 1;
        """
    )
    return f"{with_clause}{select_sql}"


def build_semantic_types_sql(
    *,
    idmap_cte: str | None,
    types_table: str,
) -> str:
    """Build SQL for semantic type lookup."""
    with_clause = _format_with_clause([idmap_cte])
    select_sql = dedent(
        f"""
        SELECT DISTINCT t.concept_id, t.type_id, t.type_name, t.type_tree
        FROM {types_table} t
        JOIN idmap c ON c.concept_id = t.concept_id
        ORDER BY t.concept_id, t.type_tree, t.type_id;
        """
    )
    return f"{with_clause}{select_sql}"


def init_concept_info_map(concept_ids: Sequence[str]) -> tuple[list[str], dict[str, ConceptInfo]]:
    """Return deduped concept IDs and initialized ConceptInfo entries."""
    id_list = list(dict.fromkeys(concept_ids))
    res: dict[str, ConceptInfo] = {}
    for cid in id_list:
        res[cid] = ConceptInfo(
            concept_id=cid,
            identifier=None,
            source=None,
            ontology=None,
            preferred_name=None,
            name_type=None,
            description=None,
            def_source=None,
            synonyms=[],
            semantic_types=[],
        )
    return id_list, res


def apply_concept_name_rows(
    res: dict[str, ConceptInfo],
    rows: Iterable[Mapping[str, Any] | RowMapping],
) -> None:
    """Populate ConceptInfo preferred names and synonyms from query rows."""
    for row in rows:
        cid = row["concept_id"]
        ent = res.get(cid)
        if ent is None:
            continue

        if row.get("preferred_name") is not None:
            ent.preferred_name = row["preferred_name"]
            ent.source = row.get("name_sab")
            ent.ontology = row.get("name_ontology")
            ent.name_type = row.get("name_tty")
            ent.identifier = row.get("identifier")

        synonyms = row.get("synonyms")
        if isinstance(synonyms, list):
            ent.synonyms = list(dict.fromkeys(synonyms))


def apply_definition_rows(
    res: dict[str, ConceptInfo],
    rows: Iterable[Mapping[str, Any] | RowMapping],
) -> None:
    """Populate ConceptInfo definitions from query rows."""
    for row in rows:
        cid = row["concept_id"]
        ent = res.get(cid)
        if ent is None:
            continue
        def_text = row.get("def_text")
        if def_text:
            ent.description = def_text
            ent.def_source = row.get("def_sab")


def apply_semantic_type_rows(
    res: dict[str, ConceptInfo],
    rows: Iterable[Mapping[str, Any] | RowMapping],
) -> None:
    """Populate ConceptInfo semantic types from query rows."""
    for row in rows:
        cid = row["concept_id"]
        ent = res.get(cid)
        if ent is None:
            continue
        type_id = row.get("type_id")
        type_name = row.get("type_name")
        if type_id and type_name:
            ent.semantic_types.append(SemanticType(type_id=type_id, type_name=type_name))

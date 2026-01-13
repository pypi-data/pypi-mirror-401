"""
LRU caches for normalized string lookups and entity expansion results.

Caches at the normalized string level to avoid repeated DB round trips
for the same normalized forms.
"""

from __future__ import annotations

import hashlib
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass(frozen=True)
class CacheKey:
    """Immutable cache key for normalized string lookup results."""

    nstrs_hash: str  # Hash of sorted normalized strings
    top_k: int | None
    ont_top_k: int | None
    prefer_ttys: tuple[str, ...] | None
    filter_ontologies: tuple[str, ...] | None
    exclude_ontologies: tuple[str, ...] | None
    allow_partial: bool
    min_coverage: float
    min_word_hits: int | None
    coverage_weight: int


@dataclass(frozen=True)
class ExpansionCacheKey:
    """Immutable cache key for entity expansion results."""

    concept_id: str
    max_depth: int | None
    filter_ontologies: tuple[str, ...] | None
    max_ids: int | None


class LRUCache(Generic[K, V]):
    """
    LRU cache with basic hit/miss statistics.

    Uses an OrderedDict for O(1) LRU eviction.
    """

    def __init__(self, maxsize: int = 10000) -> None:
        """
        Initialize the cache.

        Args:
            maxsize: Maximum number of entries to cache. When exceeded,
                the least recently used entries are evicted.
        """
        self._cache: OrderedDict[K, V] = OrderedDict()
        self._maxsize = maxsize
        self._hits = 0
        self._misses = 0

    def get(self, key: K) -> V | None:
        """
        Get cached value for a key.

        Args:
            key: Cache key to look up

        Returns:
            Cached value if found, None if not in cache
        """
        if key in self._cache:
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._hits += 1
            return self._cache[key]
        self._misses += 1
        return None

    def set(self, key: K, value: V) -> None:
        """
        Store a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self._maxsize:
                # Remove oldest item (LRU eviction)
                self._cache.popitem(last=False)
        self._cache[key] = value

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def size(self) -> int:
        """Current number of cached entries."""
        return len(self._cache)

    @property
    def hit_rate(self) -> float:
        """Cache hit rate (0.0 to 1.0)."""
        total = self._hits + self._misses
        return self._hits / total if total > 0 else 0.0

    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with size, maxsize, hits, misses, and hit_rate
        """
        return {
            "size": self.size,
            "maxsize": self._maxsize,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self.hit_rate,
        }


class NormalizerCache(LRUCache[CacheKey, list[dict[str, Any]]]):
    """
    LRU cache for normalized string lookup results.

    Caches the fully enriched hits for a given tuple of normalized strings
    and query parameters.
    """

    @staticmethod
    def make_key(
        nstrs: tuple[str, ...],
        *,
        top_k: int | None,
        ont_top_k: int | None,
        prefer_ttys: list[str] | None,
        filter_ontologies: list[str] | None,
        exclude_ontologies: list[str] | None,
        allow_partial: bool,
        min_coverage: float,
        min_word_hits: int | None,
        coverage_weight: int,
    ) -> CacheKey:
        """
        Create a cache key from normalized strings and query parameters.

        Args:
            nstrs: Tuple of normalized strings for the query
            top_k: Maximum number of results per query
            ont_top_k: Maximum number of results per ontology
            prefer_ttys: Preferred term types
            filter_ontologies: Include only these ontologies
            exclude_ontologies: Exclude these ontologies
            allow_partial: Whether partial matching is enabled
            min_coverage: Minimum coverage threshold
            min_word_hits: Minimum word hits required
            coverage_weight: Weight for coverage in scoring

        Returns:
            Immutable CacheKey instance
        """
        # Hash the normalized strings tuple for compact storage
        # Sort to ensure consistent hashing regardless of order
        nstrs_str = "\0".join(sorted(nstrs))
        nstrs_hash = hashlib.md5(nstrs_str.encode(), usedforsecurity=False).hexdigest()

        return CacheKey(
            nstrs_hash=nstrs_hash,
            top_k=top_k,
            ont_top_k=ont_top_k,
            prefer_ttys=tuple(prefer_ttys) if prefer_ttys else None,
            filter_ontologies=tuple(filter_ontologies) if filter_ontologies else None,
            exclude_ontologies=tuple(exclude_ontologies) if exclude_ontologies else None,
            allow_partial=allow_partial,
            min_coverage=min_coverage,
            min_word_hits=min_word_hits,
            coverage_weight=coverage_weight,
        )


class ExpansionCache(LRUCache[ExpansionCacheKey, list[str]]):
    """
    LRU cache for entity expansion results.

    Caches expanded concept IDs for a given concept and traversal parameters.
    """

    @staticmethod
    def make_key(
        concept_id: str,
        *,
        max_depth: int | None,
        filter_ontologies: list[str] | None,
        max_ids: int | None,
    ) -> ExpansionCacheKey:
        """
        Create a cache key from entity expansion parameters.

        Args:
            concept_id: Starting concept ID
            max_depth: Maximum depth to traverse
            filter_ontologies: Ontologies to include
            max_ids: Maximum number of IDs to return

        Returns:
            Immutable ExpansionCacheKey instance
        """
        return ExpansionCacheKey(
            concept_id=concept_id,
            max_depth=max_depth,
            filter_ontologies=tuple(filter_ontologies) if filter_ontologies else None,
            max_ids=max_ids,
        )

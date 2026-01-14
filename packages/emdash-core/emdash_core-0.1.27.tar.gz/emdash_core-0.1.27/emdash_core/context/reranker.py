"""Re-ranker for filtering context items by query relevance.

Uses a cross-encoder model to score context items against the current query,
keeping only the most relevant items to save tokens in the LLM context.
"""

import os
from typing import Optional

# Disable tokenizers parallelism to avoid fork warnings when running in threads
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from .models import ContextItem
from ..utils.logger import log

# Model singleton to avoid reloading
_reranker_model = None
_model_load_attempted = False


def get_reranker_model():
    """Get or load the re-ranker model (singleton).

    Returns:
        CrossEncoder model or None if not available
    """
    global _reranker_model, _model_load_attempted

    if _model_load_attempted:
        return _reranker_model

    _model_load_attempted = True

    # Check if re-ranking is enabled
    if os.getenv("CONTEXT_RERANK_ENABLED", "true").lower() != "true":
        log.debug("Context re-ranking disabled via CONTEXT_RERANK_ENABLED")
        return None

    try:
        from sentence_transformers import CrossEncoder

        model_name = os.getenv(
            "CONTEXT_RERANK_MODEL", "mixedbread-ai/mxbai-rerank-xsmall-v1"
        )
        log.info(f"Loading re-ranker model: {model_name}")
        _reranker_model = CrossEncoder(model_name)
        log.info("Re-ranker model loaded successfully")
        return _reranker_model
    except ImportError:
        log.warning("sentence-transformers not installed, re-ranking disabled")
        return None
    except Exception as e:
        log.warning(f"Failed to load re-ranker model: {e}")
        return None


def item_to_text(item: ContextItem) -> str:
    """Convert a ContextItem to text for re-ranking.

    Args:
        item: Context item to convert

    Returns:
        Text representation for scoring
    """
    parts = [item.qualified_name]

    if item.entity_type:
        parts.append(f"({item.entity_type})")

    if item.description:
        parts.append(f": {item.description[:200]}")

    if item.file_path:
        # Just include the filename, not full path
        filename = os.path.basename(item.file_path)
        parts.append(f" [file: {filename}]")

    return " ".join(parts)


def rerank_context_items(
    items: list[ContextItem],
    query: str,
    top_k: Optional[int] = None,
    top_percent: Optional[float] = None,
) -> list[ContextItem]:
    """Re-rank context items by relevance to query.

    Uses a cross-encoder model to score each item against the query,
    then returns the top K or top N% most relevant items.

    Args:
        items: List of context items to re-rank
        query: The user's query/task description
        top_k: Keep top K items (default from env: CONTEXT_RERANK_TOP_K=20)
        top_percent: Keep top N% items (overrides top_k if set)

    Returns:
        Filtered and sorted list of context items (most relevant first)
    """
    import time

    original_count = len(items)

    if not items:
        return items

    if not query or not query.strip():
        log.debug("No query provided for re-ranking, returning original items")
        return items

    model = get_reranker_model()
    if model is None:
        log.debug("Re-ranker model not available, returning original items")
        return items

    try:
        start_time = time.time()

        # Convert items to text for scoring
        texts = [item_to_text(item) for item in items]

        # Create query-document pairs
        pairs = [(query, text) for text in texts]

        # Score all pairs
        scores = model.predict(pairs)

        # Combine items with scores
        scored_items = list(zip(items, scores))

        # Sort by score descending
        scored_items.sort(key=lambda x: x[1], reverse=True)

        # Determine how many to keep
        if top_percent is not None:
            keep_count = max(1, int(len(items) * top_percent))
        elif top_k is not None:
            keep_count = min(top_k, len(items))
        else:
            # Default from environment
            default_top_k = int(os.getenv("CONTEXT_RERANK_TOP_K", "20"))
            keep_count = min(default_top_k, len(items))

        duration_ms = (time.time() - start_time) * 1000

        # Log statistics
        if scored_items:
            max_score = scored_items[0][1]
            min_score = scored_items[-1][1]
            filtered_count = original_count - keep_count
            log.info(
                f"Re-ranked context: {original_count} -> {keep_count} items "
                f"(filtered {filtered_count}) in {duration_ms:.0f}ms | "
                f"scores [{min_score:.3f}-{max_score:.3f}] | "
                f"query: '{query[:40]}...'"
            )

        # Return top items (without scores)
        return [item for item, score in scored_items[:keep_count]]

    except Exception as e:
        log.warning(f"Re-ranking failed: {e}, returning original items")
        return items


def get_rerank_scores(
    items: list[ContextItem], query: str
) -> list[tuple[ContextItem, float]]:
    """Get re-rank scores for context items without filtering.

    Useful for debugging and analysis.

    Args:
        items: List of context items
        query: Query to score against

    Returns:
        List of (item, score) tuples sorted by score descending
    """
    if not items or not query:
        return [(item, 0.0) for item in items]

    model = get_reranker_model()
    if model is None:
        return [(item, 0.0) for item in items]

    try:
        texts = [item_to_text(item) for item in items]
        pairs = [(query, text) for text in texts]
        scores = model.predict(pairs)

        scored = list(zip(items, scores))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    except Exception as e:
        log.warning(f"Failed to get rerank scores: {e}")
        return [(item, 0.0) for item in items]

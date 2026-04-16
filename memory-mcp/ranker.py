"""
Hybrid 3-factor ranker: FTS5 BM25 + recency + importance.

Weights:
  - FTS5 BM25 score  : 0.4
  - Recency (30d decay): 0.3
  - Importance (normalized): 0.3
"""

import math
from datetime import datetime, timezone


def score_result(
    fts_rank: float,
    created_at: str,
    importance: float,
    max_importance: float,
) -> float:
    """Compute hybrid score for a single memory result.

    Args:
        fts_rank: FTS5 rank value (negative; lower = better match).
        created_at: ISO datetime string for when the memory was created.
        importance: Numeric importance score for this memory.
        max_importance: Maximum importance across all memories (for normalization).

    Returns:
        Combined score in [0, 1], higher is better.
    """
    # FTS5 returns negative rank; normalize to (0, 1]
    fts_score = 1.0 / (1.0 + abs(fts_rank))

    # Recency: exponential decay, 30-day half-life
    try:
        created = datetime.fromisoformat(created_at)
        # Handle both naive and aware datetimes
        if created.tzinfo is None:
            now = datetime.utcnow()
        else:
            now = datetime.now(timezone.utc)
        age_days = (now - created).total_seconds() / 86400.0
    except (ValueError, TypeError):
        age_days = 30.0
    recency_score = math.exp(-age_days / 30.0)

    # Importance: normalize against max
    imp_score = importance / max(max_importance, 1.0)

    return 0.4 * fts_score + 0.3 * recency_score + 0.3 * imp_score


def decay_importance(importance: float, days_since_access: float) -> float:
    """ByteRover AKL daily decay: multiply by 0.995 per day.

    Args:
        importance: Current importance score.
        days_since_access: Days since last access.

    Returns:
        Decayed importance score.
    """
    return importance * (0.995 ** days_since_access)

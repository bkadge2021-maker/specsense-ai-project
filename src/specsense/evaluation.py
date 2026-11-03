from __future__ import annotations
from .models import Recommendation

def evaluate_recommendations(results: list[Recommendation], expected_ids: set[str]) -> dict[str, float]:
    """Small offline evaluation helper for hit-rate and top-1 correctness."""
    returned = {r.product.id for r in results}
    return {
        "hit_rate": len(returned & expected_ids) / max(1, len(expected_ids)),
        "top1_correct": float(bool(results) and results[0].product.id in expected_ids),
    }

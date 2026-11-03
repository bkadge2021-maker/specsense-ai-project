from .models import Recommendation, Product

def enrich_recommendations(results: list[Recommendation], catalog: list[Product]) -> list[Recommendation]:
    """Attach catalog-provided review snippets; no external review data is fabricated."""
    for result in results:
        result.insights = result.product.review_snippets[:2]
    return results

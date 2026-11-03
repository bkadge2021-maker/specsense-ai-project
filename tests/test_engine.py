from src.specsense.catalog import load_catalog
from src.specsense.engine import recommend
from src.specsense.models import UserProfile

def test_budget_and_laptop_query():
    catalog = load_catalog()
    results = recommend(
        "lightweight laptop under ₹30k for coding and battery backup",
        catalog,
        UserProfile(budget=30000, max_weight=1.8),
    )
    assert results
    assert all(r.product.category == "laptop" for r in results)
    assert results[0].score >= results[-1].score

def test_category_fallback():
    results = recommend("something useful under 10000", load_catalog())
    assert results

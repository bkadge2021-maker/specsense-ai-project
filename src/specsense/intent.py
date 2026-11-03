from __future__ import annotations
import re
from .models import ParsedIntent, UserProfile

def parse_intent(query: str, profile: UserProfile | None = None) -> ParsedIntent:
    """Lightweight deterministic parser; replaceable by an LLM-backed extractor."""
    q = query.lower()
    intent = ParsedIntent()
    category_map = {
        "laptop": ["laptop", "notebook", "computer"],
        "phone": ["phone", "smartphone", "mobile"],
        "headphones": ["headphone", "earbuds", "earphones"],
    }
    for category, words in category_map.items():
        if any(word in q for word in words):
            intent.category = category
            break

    budget_match = re.search(r"(?:under|below|less than|max(?:imum)?|budget(?: of)?)\\s*₹?\\s*([\\d,]+)\\s*(k| lakh)?", q)
    if budget_match:
        amount = float(budget_match.group(1).replace(",", ""))
        suffix = budget_match.group(2)
        intent.budget = amount * (1000 if suffix == "k" else 100000 if suffix == "lakh" else 1)

    weight_match = re.search(r"(?:under|below|less than)\\s*(\\d+(?:\\.\\d+)?)\\s*kg", q)
    if weight_match:
        intent.max_weight = float(weight_match.group(1))
    elif "lightweight" in q or "light weight" in q:
        intent.max_weight = 1.8

    battery_match = re.search(r"(\\d+)\\s*(?:hours?|hrs?)\\s*(?:of\\s*)?(?:battery|backup)", q)
    if battery_match:
        intent.min_battery = float(battery_match.group(1))
    elif "battery" in q or "battery backup" in q:
        intent.min_battery = 7

    ram_match = re.search(r"(\\d+)\\s*gb\\s*ram", q)
    if ram_match:
        intent.min_ram = int(ram_match.group(1))

    terms = {
        "coding": ["coding", "programming", "developer"],
        "travel": ["travel", "commute", "portable"],
        "gaming": ["gaming", "games"],
        "eco-friendly": ["eco-friendly", "sustainable", "recycled"],
        "low-light": ["low light", "low-light", "night photography"],
        "content creation": ["editing", "content creation", "video editing"],
    }
    for tag, words in terms.items():
        if any(w in q for w in words):
            intent.use_cases.append(tag)
    soft = ["lightweight", "long battery life", "travel-friendly", "good display",
            "good in low light", "eco-friendly", "quiet", "durable"]
    intent.soft_preferences = [s for s in soft if s in q]
    intent.keywords = [w for w in ["fast", "portable", "bright", "durable", "premium"] if w in q]

    if profile:
        if intent.budget is None:
            intent.budget = profile.budget
        if intent.max_weight is None:
            intent.max_weight = profile.max_weight
    return intent

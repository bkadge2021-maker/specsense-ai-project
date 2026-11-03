from __future__ import annotations
from .models import Product, UserProfile, Recommendation
from .intent import parse_intent

def recommend(query: str, catalog: list[Product], profile: UserProfile | None = None) -> list[Recommendation]:
    intent = parse_intent(query, profile)
    candidates = [p for p in catalog if not intent.category or p.category.lower() == intent.category]
    if not candidates:
        candidates = catalog[:]

    ranked: list[Recommendation] = []
    for p in candidates:
        score = 45.0
        hard, soft, tradeoffs, unmet = [], [], [], []
        if intent.budget is not None:
            if p.price <= intent.budget:
                score += 20
                hard.append(f"Within budget (₹{p.price:,.0f} ≤ ₹{intent.budget:,.0f})")
            else:
                score -= 35
                unmet.append(f"Above your budget by ₹{p.price-intent.budget:,.0f}")
        if intent.max_weight is not None:
            if p.weight_kg <= intent.max_weight:
                score += 10
                hard.append(f"Weight is {p.weight_kg:.2f} kg")
            else:
                score -= 12
                tradeoffs.append(f"Weighs {p.weight_kg:.2f} kg, above your {intent.max_weight:.1f} kg preference")
        if intent.min_battery is not None:
            if p.battery_hours is not None and p.battery_hours >= intent.min_battery:
                score += 10
                hard.append(f"Battery rated for {p.battery_hours:g} hours")
            else:
                unmet.append(f"Battery target of {intent.min_battery:g}+ hours is not confirmed")
                score -= 8
        if intent.min_ram is not None:
            if p.ram_gb is not None and p.ram_gb >= intent.min_ram:
                score += 8
                hard.append(f"{p.ram_gb} GB RAM meets your target")
            else:
                unmet.append(f"Does not meet the {intent.min_ram} GB RAM target")
                score -= 10
        for use in intent.use_cases:
            if use in p.purpose_tags:
                score += 7
                soft.append(f"Catalog tags support {use}")
            elif use == "coding" and p.ram_gb and p.ram_gb >= 8:
                score += 3
                soft.append("RAM capacity is suitable for entry-level coding workloads")
            else:
                tradeoffs.append(f"No explicit catalog evidence for {use}")
        if "eco-friendly" in intent.soft_preferences:
            if p.eco_friendly:
                score += 6
                soft.append("Eco-conscious product attribute")
            else:
                tradeoffs.append("No eco-friendly attribute listed")
        if "low-light" in intent.use_cases:
            if p.low_light_camera:
                score += 7
                soft.append("Low-light camera feature listed")
            else:
                tradeoffs.append("No dedicated low-light camera feature listed")
        if not hard and not soft:
            soft.append("General catalog relevance; add more detail for a tighter match")
        ranked.append(Recommendation(
            product=p, score=max(0, min(100, score)),
            hard_matches=hard, soft_matches=soft, tradeoffs=tradeoffs, unmet_needs=unmet
        ))
    return sorted(ranked, key=lambda r: (r.score, -r.product.price), reverse=True)[:5]

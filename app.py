from __future__ import annotations

import pandas as pd
import streamlit as st

from src.specsense.catalog import load_catalog
from src.specsense.engine import recommend
from src.specsense.insights import enrich_recommendations
from src.specsense.models import UserProfile

st.set_page_config(page_title="SpecSense AI", page_icon="✦", layout="wide")

st.markdown("""
<style>
    .block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem;}
    .hero {padding: 1.7rem 1.9rem; border-radius: 20px; background: linear-gradient(120deg,#111827,#243b63); color:white; margin-bottom:1.2rem;}
    .hero h1 {font-size:2.35rem; margin:0 0 .35rem 0; letter-spacing:-.04em;}
    .hero p {color:#dbeafe; margin:0; font-size:1.02rem;}
    .eyebrow {text-transform:uppercase; letter-spacing:.15em; font-size:.72rem; color:#93c5fd; font-weight:700;}
    .metric {background:#f8fafc; border:1px solid #e2e8f0; padding:1rem; border-radius:14px;}
    .muted {color:#64748b;}
    div[data-testid="stMetric"] {background:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Conversational product discovery</div>
  <h1>✦ SpecSense AI</h1>
  <p>Turn everyday language into clear, explainable product recommendations.</p>
</div>
""", unsafe_allow_html=True)

catalog = load_catalog()
with st.sidebar:
    st.header("Your preferences")
    budget = st.number_input("Maximum budget (₹)", min_value=0, value=30000, step=1000)
    max_weight = st.number_input("Preferred maximum weight (kg)", min_value=0.0, value=1.8, step=0.1)
    profile_age = st.number_input("Age (optional)", min_value=0, max_value=120, value=0)
    st.caption("These preferences are used as context, not as hard requirements unless stated in your request.")
    st.divider()
    st.caption("Demo catalog · 12 sample products")

st.subheader("What are you looking for?")
query = st.text_area(
    "Describe your ideal product in your own words",
    value="I need a lightweight laptop under ₹30k for coding, with good battery backup and a clear display.",
    height=110,
    label_visibility="collapsed",
    placeholder="Example: I need something lightweight for travel, good in low light, and eco-friendly…",
)
col_a, col_b = st.columns([1, 4])
with col_a:
    run = st.button("Find my matches  →", type="primary", use_container_width=True)
with col_b:
    st.caption("Tip: Include your budget, must-have specifications, and softer preferences.")

if run or "results" not in st.session_state:
    profile = UserProfile(age=profile_age or None, budget=budget or None, max_weight=max_weight or None)
    results = recommend(query, catalog, profile)
    st.session_state["results"] = enrich_recommendations(results, catalog)
    st.session_state["query"] = query

results = st.session_state["results"]
st.divider()
if not results:
    st.warning("No products were found in the demo catalog.")
else:
    best = results[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Products evaluated", len(catalog))
    c2.metric("Relevant matches", len(results))
    c3.metric("Top match score", f"{best.score:.0f}/100")
    st.subheader("Your best matches")
    st.caption("Ranked by fit to your stated needs. Scores are guidance, not a guarantee of real-world performance.")

    for idx, item in enumerate(results, 1):
        product = item.product
        with st.container(border=True):
            left, right = st.columns([3, 1])
            with left:
                st.markdown(f"### {idx}. {product.name}")
                st.markdown(f"**₹{product.price:,.0f}**  ·  {product.category}  ·  {product.weight_kg:.2f} kg")
                st.write(product.description)
            with right:
                st.metric("Fit score", f"{item.score:.0f}/100")
                st.progress(min(int(item.score), 100))
            st.markdown("**Why this matches**")
            if item.hard_matches:
                st.write("✓ " + " · ".join(item.hard_matches))
            if item.soft_matches:
                st.write("✦ " + " · ".join(item.soft_matches))
            if item.tradeoffs:
                st.markdown("**Trade-offs**")
                for value in item.tradeoffs:
                    st.write("– " + value)
            if item.unmet_needs:
                st.markdown("**Needs not fully met**")
                for value in item.unmet_needs:
                    st.write("– " + value)
            if item.insights:
                st.markdown("**Customer / market insights**")
                for value in item.insights:
                    st.write("• " + value)

    with st.expander("How SpecSense interpreted your request"):
        st.write(f"**Original request:** {st.session_state.get('query', query)}")
        st.write("The engine extracts budget, product category, weight, battery, memory, processor and use-case signals. Explicit limits are treated as hard constraints where possible; qualitative preferences contribute to ranking.")
    with st.expander("Compare all recommended products"):
        table = [{
            "Product": r.product.name,
            "Price": r.product.price,
            "Weight (kg)": r.product.weight_kg,
            "Battery (hrs)": r.product.battery_hours,
            "RAM (GB)": r.product.ram_gb,
            "Score": round(r.score, 1),
        } for r in results]
        st.dataframe(pd.DataFrame(table), use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("<p class='muted' style='text-align:center'>SpecSense AI · Explainable matching over structured catalog data</p>", unsafe_allow_html=True)

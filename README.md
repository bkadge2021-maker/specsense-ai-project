# SpecSense AI

**Conversational, context-aware and explainable product recommendations** over a structured product catalog.

SpecSense translates natural-language needs into product constraints, ranks catalog items, and explains hard matches, soft matches, trade-offs and unmet needs. It is designed as a clean starter project that can be extended with Gemini or OpenAI for richer intent extraction.

## What is included

- Natural-language preference input through a Streamlit interface
- Constraint extraction for category, budget, weight, battery and RAM
- Hybrid matching: structured filters + soft preference scoring
- Explainability for every recommendation
- Gap detection through unmet-needs and trade-off messages
- Review snippets sourced only from the local sample catalog
- Pydantic data validation and a small offline evaluation helper
- Modular Python package and tests

## Quick start

Requires Python 3.12+.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

Open the local URL printed by Streamlit.

## Example query

> I need a lightweight laptop under ₹30k for coding, with good battery backup.

The app will rank laptop records in `data/products.csv` and explain:
- **Hard matches:** budget, weight, battery and RAM constraints supported by catalog fields
- **Soft matches:** use-case tags and qualitative attributes
- **Trade-offs:** preferences for which the catalog has no supporting evidence
- **Unmet needs:** requirements that a product does not satisfy or cannot verify

## Project structure

```text
specsense-ai/
├── app.py
├── data/
│   └── products.csv
├── src/
│   └── specsense/
│       ├── catalog.py
│       ├── engine.py
│       ├── evaluation.py
│       ├── insights.py
│       ├── intent.py
│       └── models.py
├── tests/
│   └── test_engine.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Data format

Replace `data/products.csv` with your own catalog. Keep these columns:

| Field | Meaning |
|---|---|
| `id`, `name`, `category` | Product identity |
| `price`, `weight_kg` | Numeric constraints |
| `battery_hours`, `ram_gb`, `storage_gb` | Optional technical specs |
| `purpose_tags` | Pipe-separated tags such as `coding|travel` |
| `eco_friendly`, `low_light_camera` | Boolean attributes |
| `description` | Catalog description |
| `review_snippets` | Pipe-separated review excerpts supplied by your dataset |

Do not present missing catalog data as verified product facts.

## Architecture

```text
User request + profile
        │
        ▼
Intent extraction (intent.py)
        │ ParsedIntent
        ▼
Hybrid matching engine (engine.py)
        │ Ranked candidates + score factors
        ▼
Explainability / gap detection
        │
        ▼
Catalog-backed review enrichment
        │
        ▼
Streamlit recommendation UI
```

## Add an LLM provider

The current parser is deterministic so the demo runs without API credentials. To use Gemini or OpenAI:

1. Add the selected provider SDK to `requirements.txt`.
2. Store the API key in `.env` (never commit it).
3. Implement an LLM extraction adapter that returns the `ParsedIntent` Pydantic schema.
4. Validate model output before passing it to `recommend`.
5. Keep deterministic validation and scoring as the source of truth for hard constraints.

Suggested LLM responsibilities:
- Resolve ambiguous phrasing into structured preferences
- Identify soft intent such as "good for coding" or "travel-friendly"
- Ask a follow-up when a critical constraint is ambiguous

Do **not** let an LLM invent catalog specifications, review quotes, stock status or offers.

## Run tests

```bash
pytest -q
```

## Important demo limitations

- The included catalog is synthetic sample data, not live inventory.
- Review snippets are illustrative catalog fields and are not real customer endorsements.
- Availability, offers and real-world review enrichment require trusted external data sources.
- Scores are heuristic ranking signals, not calibrated probabilities.
- The included parser supports common phrasing and should be expanded for production use.

## GitHub submission checklist

- [ ] Replace sample catalog with permitted, accurate company data
- [ ] Add your own screenshots to `docs/` and update this README
- [ ] Add LLM extraction adapter and provider-specific setup
- [ ] Add tests for parsing, constraints, ranking and explanation correctness
- [ ] Configure secrets in deployment environment
- [ ] Create a public GitHub repository and push this project

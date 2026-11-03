from pathlib import Path
import pandas as pd
from .models import Product

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "products.csv"

def load_catalog(path: str | Path = CATALOG_PATH) -> list[Product]:
    frame = pd.read_csv(path).fillna("")
    products = []
    for row in frame.to_dict(orient="records"):
        tags = [x.strip() for x in str(row.get("purpose_tags", "")).split("|") if x.strip()]
        reviews = [x.strip() for x in str(row.get("review_snippets", "")).split("|") if x.strip()]
        def optional_float(value):
            return float(value) if value != "" else None
        def optional_int(value):
            return int(float(value)) if value != "" else None
        products.append(Product(
            id=str(row["id"]), name=str(row["name"]), category=str(row["category"]),
            price=float(row["price"]), weight_kg=float(row["weight_kg"]),
            battery_hours=optional_float(row.get("battery_hours", "")),
            ram_gb=optional_int(row.get("ram_gb", "")),
            storage_gb=optional_int(row.get("storage_gb", "")),
            processor=str(row.get("processor", "")) or None,
            display=str(row.get("display", "")) or None,
            purpose_tags=tags, eco_friendly=str(row.get("eco_friendly", "")).lower() == "true",
            low_light_camera=str(row.get("low_light_camera", "")).lower() == "true",
            description=str(row.get("description", "")), review_snippets=reviews
        ))
    return products

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float = Field(ge=0)
    weight_kg: float = Field(ge=0)
    battery_hours: Optional[float] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    processor: Optional[str] = None
    display: Optional[str] = None
    purpose_tags: list[str] = []
    eco_friendly: bool = False
    low_light_camera: bool = False
    description: str = ""
    review_snippets: list[str] = []

class UserProfile(BaseModel):
    age: Optional[int] = None
    budget: Optional[float] = None
    max_weight: Optional[float] = None
    context_tags: list[str] = []

class ParsedIntent(BaseModel):
    category: Optional[str] = None
    budget: Optional[float] = None
    max_weight: Optional[float] = None
    min_battery: Optional[float] = None
    min_ram: Optional[int] = None
    use_cases: list[str] = []
    soft_preferences: list[str] = []
    keywords: list[str] = []

class Recommendation(BaseModel):
    product: Product
    score: float
    hard_matches: list[str] = []
    soft_matches: list[str] = []
    tradeoffs: list[str] = []
    unmet_needs: list[str] = []
    insights: list[str] = []

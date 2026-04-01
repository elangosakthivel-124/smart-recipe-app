from pydantic import BaseModel
from typing import List, Optional

class RecipeBase(BaseModel):
    id: int
    title: str
    image: Optional[str]
    readyInMinutes: Optional[int]
    servings: Optional[int]
    sourceUrl: Optional[str]

class RecipeSearchResult(BaseModel):
    results: List[RecipeBase]
    totalResults: int

class RecipeDetail(RecipeBase):
    summary: Optional[str]
    instructions: Optional[str]
    nutrition: Optional[dict]
    ingredients: List[dict] = []

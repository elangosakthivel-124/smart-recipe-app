from fastapi import APIRouter, Query
from app.services.spoonacular import SpoonacularService
from app.schemas.recipe import RecipeSearchResult

router = APIRouter()
service = SpoonacularService()

@router.get("/recipes/search")
async def search_recipes(
    query: str = Query(..., description="Search query or ingredients"),
    number: int = 12,
    diet: str = None
):
    results = await service.search_recipes(query, number, diet)
    return results

import httpx
from fastapi import HTTPException
from app.core.config import settings

class SpoonacularService:
    def __init__(self):
        self.api_key = settings.SPOONACULAR_API_KEY
        self.base_url = settings.SPOONACULAR_BASE_URL

    async def search_recipes(self, query: str, number: int = 12, diet: str = None):
        async with httpx.AsyncClient() as client:
            params = {
                "apiKey": self.api_key,
                "query": query,
                "number": number,
                "addRecipeInformation": True,
                "addRecipeNutrition": True,
            }
            if diet:
                params["diet"] = diet

            response = await client.get(f"{self.base_url}/recipes/complexSearch", params=params)
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Spoonacular API error")
            
            return response.json()

    async def get_recipe_details(self, recipe_id: int):
        async with httpx.AsyncClient() as client:
            params = {"apiKey": self.api_key}
            response = await client.get(
                f"{self.base_url}/recipes/{recipe_id}/information",
                params=params
            )
            return response.json()

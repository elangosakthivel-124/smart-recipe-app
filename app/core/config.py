from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Recipe Generator"
    API_V1_STR: str = "/api/v1"
    SPOONACULAR_API_KEY: str
    SPOONACULAR_BASE_URL: str = "https://api.spoonacular.com"
    GROQ_API_KEY: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()

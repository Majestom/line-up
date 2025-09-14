import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    reqres_api_key: str = os.getenv("REQRES_API_KEY", "")
    reqres_base_url: str = "https://reqres.in/api"

    # Server Configuration
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    node_env: str = os.getenv("NODE_ENV", "development")

    # Application Configuration
    service_name: str = "user-api"
    version: str = "1.0.0"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

# Global settings instance
settings = Settings()
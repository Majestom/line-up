from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel, ValidationError, HttpUrl
from typing import Dict, Optional
import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timezone


load_dotenv()

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="User API Service", version="1.0.0")

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class UserResponse(BaseModel):
    data: UserData

# Pydantic models for external API response validation
class ReqResUserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl

class ReqResResponse(BaseModel):
    data: ReqResUserData
    support: Optional[Dict] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    external_api_status: str
    environment: str

REQRES_BASE_URL = "https://reqres.in/api"
REQRES_API_KEY = os.getenv("REQRES_API_KEY")

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "User API Service is running"}

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring and load balancer probes.

    Checks the status of the service and its dependencies.

    Returns:
        HealthResponse: Service health information including external API status
    """
    # Check external API availability
    external_api_status = "unknown"
    try:
        headers = {"x-api-key": REQRES_API_KEY} if REQRES_API_KEY else {}
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{REQRES_BASE_URL}/users/1", headers=headers)
            external_api_status = "healthy" if response.status_code == 200 else "degraded"
    except Exception:
        external_api_status = "unhealthy"

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.0.0",
        external_api_status=external_api_status,
        environment=os.getenv("NODE_ENV", "development")
    )

@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int = Path(..., ge=1, le=12, description="User ID from reqres.in API (1-12)")
) -> UserResponse:
    """
    Fetch user data from reqres.in API and return only the user information.

    This endpoint acts as a proxy to the reqres.in API, fetching user data
    and reformatting it to expose only the essential user information.

    Args:
        user_id: User ID (1-12) - corresponds to available users in reqres.in demo data

    Returns:
        UserResponse: User data with id, email, first_name, last_name, and avatar

    Raises:
        422: Validation Error - if user_id is not between 1-12
        404: User not found
        503: External API unavailable
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Add API key if available
    if REQRES_API_KEY:
        headers["x-api-key"] = REQRES_API_KEY

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{REQRES_BASE_URL}/users/{user_id}", headers=headers)
            response.raise_for_status()

            reqres_data = response.json()

            # Validate external API response with Pydantic
            try:
                reqres_response = ReqResResponse.model_validate(reqres_data)
            except ValidationError as e:
                logging.error(f"Invalid response from external API: {e}")
                raise HTTPException(
                    status_code=503,
                    detail="External API returned invalid data format"
                )

            # Transform to our internal model
            return UserResponse(
                data=UserData(
                    id=reqres_response.data.id,
                    email=reqres_response.data.email,
                    first_name=reqres_response.data.first_name,
                    last_name=reqres_response.data.last_name,
                    avatar=str(reqres_response.data.avatar)
                )
            )

        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP Status Error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            elif e.response.status_code == 401:
                logging.error(f"API authentication failed. API key configured: {bool(REQRES_API_KEY)}")
                raise HTTPException(
                    status_code=503,
                    detail="External API is temporarily unavailable due to authentication issues. Please try again later."
                )
            else:
                raise HTTPException(
                    status_code=503,
                    detail=f"External API returned an error (HTTP {e.response.status_code}). Please try again later."
                )
        except httpx.RequestError as e:
            logging.error(f"Request Error: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to external API. Please check your internet connection or try again later."
            )
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching user data. Please try again later."
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
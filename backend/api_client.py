import httpx
import logging
from fastapi import HTTPException
from pydantic import ValidationError

from config import settings
from models import ReqResResponse, UserResponse, UserData

logger = logging.getLogger(__name__)

class ReqResAPIClient:
    def __init__(self):
        self.base_url = settings.reqres_base_url
        self.api_key = settings.reqres_api_key

    def _get_headers(self) -> dict:
        """Get HTTP headers for API requests"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Add API key if available
        if self.api_key:
            headers["x-api-key"] = self.api_key

        return headers

    async def get_user(self, user_id: int) -> UserResponse:
        """
        Fetch user data from reqres.in API and return formatted response.

        Args:
            user_id: User ID to fetch (1-12)

        Returns:
            UserResponse: Formatted user data

        Raises:
            HTTPException: For various error conditions
        """
        headers = self._get_headers()
        url = f"{self.base_url}/users/{user_id}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()

                reqres_data = response.json()

                # Validate external API response with Pydantic
                try:
                    reqres_response = ReqResResponse.model_validate(reqres_data)
                except ValidationError as e:
                    logger.error("Invalid response from external API", extra={
                        "validation_error": str(e),
                        "user_id": user_id,
                        "external_api_url": url
                    })
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
                logger.error("HTTP Status Error from external API", extra={
                    "status_code": e.response.status_code,
                    "response_text": e.response.text,
                    "user_id": user_id,
                    "external_api_url": url
                })
                if e.response.status_code == 404:
                    raise HTTPException(status_code=404, detail="User not found")
                elif e.response.status_code == 401:
                    logger.error("API authentication failed", extra={
                        "api_key_configured": bool(self.api_key),
                        "user_id": user_id,
                        "external_api_url": url
                    })
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
                logger.error("Request Error connecting to external API", extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "user_id": user_id,
                    "external_api_url": url
                })
                raise HTTPException(
                    status_code=503,
                    detail="Unable to connect to external API. Please check your internet connection or try again later."
                )
            except Exception as e:
                logger.error("Unexpected error while fetching user data", extra={
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "user_id": user_id,
                    "external_api_url": url
                })
                raise HTTPException(
                    status_code=500,
                    detail="An unexpected error occurred while fetching user data. Please try again later."
                )

    async def check_health(self) -> str:
        """
        Check if the external API is healthy.

        Returns:
            str: "healthy", "degraded", or "unhealthy"
        """
        try:
            headers = self._get_headers()
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/users/1", headers=headers)
                return "healthy" if response.status_code == 200 else "degraded"
        except Exception:
            return "unhealthy"

# Global client instance
reqres_client = ReqResAPIClient()
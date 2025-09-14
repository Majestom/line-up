from fastapi import APIRouter, Path

from models import UserResponse
from api_client import reqres_client

router = APIRouter()

@router.get("/user/{user_id}", response_model=UserResponse)
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
    return await reqres_client.get_user(user_id)
from pydantic import BaseModel, HttpUrl
from typing import Dict, Optional

# Internal API models
class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class UserResponse(BaseModel):
    data: UserData

# External API response validation models
class ReqResUserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl

class ReqResResponse(BaseModel):
    data: ReqResUserData
    support: Optional[Dict] = None

# Health check model
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    external_api_status: str
    environment: str
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="User API Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
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

REQRES_BASE_URL = "https://reqres.in/api"

@app.get("/")
async def root():
    return {"message": "User API Service is running"}

@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Fetch user data from reqres.in API and return only the user information.
    
    This endpoint acts as a proxy to the reqres.in API, fetching user data
    and reformatting it to expose only the essential user information.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": "reqres-free-v1"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{REQRES_BASE_URL}/users/{user_id}", headers=headers)
            response.raise_for_status()
            
            reqres_data = response.json()
            
            if "data" not in reqres_data:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_data = reqres_data["data"]
            
            return UserResponse(
                data=UserData(
                    id=user_data["id"],
                    email=user_data["email"],
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    avatar=user_data["avatar"]
                )
            )
            
        except httpx.HTTPStatusError as e:
            print(f"HTTP Status Error: {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="User not found")
            elif e.response.status_code == 401:
                raise HTTPException(
                    status_code=503, 
                    detail="External API is currently unavailable (authentication required). Please try again later."
                )
            else:
                raise HTTPException(
                    status_code=503, 
                    detail=f"External API returned an error (HTTP {e.response.status_code}). Please try again later."
                )
        except httpx.RequestError as e:
            print(f"Request Error: {str(e)}")
            raise HTTPException(
                status_code=503, 
                detail="Unable to connect to external API. Please check your internet connection or try again later."
            )
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail="An unexpected error occurred while fetching user data. Please try again later."
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
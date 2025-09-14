from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from middleware import setup_logging, add_request_id_middleware
from health import router as health_router
from users import router as users_router

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="User API Service",
    version=settings.version,
    description="A FastAPI service that proxies requests to the reqres.in API"
)

# Add middleware
app.middleware("http")(add_request_id_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "User API Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
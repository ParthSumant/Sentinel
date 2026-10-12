from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Sentinel sustainability monitoring and action API.",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Sentinel"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "status": "running",
    }


@app.get("/api/v1/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
    }

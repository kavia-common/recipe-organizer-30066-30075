from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.session import init_db

app = FastAPI(
    title="Recipe Organizer Backend",
    description="REST API for managing users, recipes, categories, tags, and saved recipes.",
    version="0.1.0",
    openapi_tags=[
        {"name": "health", "description": "Service health and diagnostics"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize database on application startup.
    In development, this will create tables if they do not exist.
    """
    init_db(create_all_in_dev=True)


@app.get("/", tags=["health"], summary="Health Check")
def health_check():
    """Simple health check endpoint."""
    return {"message": "Healthy"}

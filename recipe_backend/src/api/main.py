from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from src.db.session import init_db
from src.api.routers.auth import router as auth_router
from src.api.routers.users import router as users_router
from src.api.routers.recipes import router as recipes_router
from src.api.routers.taxonomy import router as taxonomy_router
from src.api.routers.search import router as search_router

openapi_tags = [
    {"name": "health", "description": "Service health and diagnostics"},
    {"name": "auth", "description": "Authentication endpoints"},
    {"name": "users", "description": "User profile management"},
    {"name": "recipes", "description": "Recipe CRUD operations"},
    {"name": "taxonomy", "description": "Tags and categories"},
    {"name": "search", "description": "Recipe search"},
]

app = FastAPI(
    title="Recipe Organizer Backend",
    description="REST API for managing users, recipes, categories, tags, and saved recipes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS configuration - allow frontend origin from env or default to localhost:3000
frontend_origin = os.getenv("FRONTEND_ORIGIN") or os.getenv("SITE_URL") or "http://localhost:3000"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
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


# Register routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(taxonomy_router)
app.include_router(search_router)

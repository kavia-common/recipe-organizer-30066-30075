# Smoke Test Notes

This document outlines expected environment configuration, CORS checks, and a sequence of API smoke tests. It also captures endpoint/schema mismatches found between frontend assumptions and backend implementation.

## Environment

Backend `.env`:
- DATABASE_URL=sqlite:///./recipes.db
- ENV=development
- JWT_SECRET_KEY=<set>
- JWT_ALGORITHM=HS256
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
- FRONTEND_ORIGIN=http://localhost:3000
- SITE_URL=http://localhost:3000

Frontend `.env`:
- REACT_APP_API_BASE_URL=http://localhost:3001

FastAPI main config uses FRONTEND_ORIGIN or SITE_URL for CORS; both included above. Default fallback is http://localhost:3000.

## CORS

Backend sets:
- allow_origins: [http://localhost:3000]
- allow_credentials: true
- allow_methods/headers: "*"

This permits the React app to make authorized requests with Bearer tokens.

## API Smoke Tests (curl)

Base URL: http://localhost:3001

1) Health:
- GET /
- Expect 200 {"message":"Healthy"}

2) Register:
- POST /auth/register
  body: {"email":"u1@example.com","password":"Pw123456","full_name":"User One"}
- Expect 200 {access_token, token_type}

3) Login:
- POST /auth/login
  body: {"email":"u1@example.com","password":"Pw123456"}
- Expect 200 {access_token, token_type}
- Save TOKEN

4) Me:
- GET /users/me with Authorization: Bearer ${TOKEN}
- Expect 200 user profile

5) Taxonomy:
- POST /taxonomy/categories with bearer token
  {"name":"Lunch","description":"Midday meals"} -> 201
- POST /taxonomy/tags with bearer token
  {"name":"quick"} -> 201

6) Create Recipe (auth required):
- POST /recipes with bearer token
  {
    "title":"Ocean Salad",
    "description":"Fresh greens",
    "instructions":"Chop\nMix\nServe",
    "ingredients":"Lettuce\nCitrus\nOlive oil",
    "category_id": <category_id>,
    "tag_ids": [<tag_id>]
  }
- Expect 201 with RecipePublic

7) List Recipes:
- GET /recipes
- Expect 200 { total, limit, offset, items: [...] }

8) Search:
- GET /search?q=salad&limit=10&offset=0
- Expect 200 { total, items: [...] }

9) Recipe Detail:
- GET /recipes/{id}
- Expect 200 RecipePublic

10) Update Recipe:
- PATCH /recipes/{id} with bearer token, e.g. {"description":"Updated"}
- Expect 200 updated resource

11) Delete Recipe:
- DELETE /recipes/{id} with bearer token
- Expect 204

12) Favorites (not implemented):
- Endpoints like POST/DELETE /recipes/{id}/favorite and GET /users/me/favorites are NOT implemented. Consider as future work.

## Frontend-Backend Mismatches and Fixes

- Frontend had endpoints.recipes.search="/recipes/search" and "my" and "mine" routes which don't exist. Fixed to use backend "/search" and removed "my" endpoints.
- AuthContext previously mocked tokens; updated to call real /auth/register and /auth/login and store access_token.
- Home page now uses /search backend when possible with fallback mock data.
- RecipeDetail now fetches /recipes/{id} and normalizes fields with fallback.
- Create/Edit now uses backend schema {title, description, instructions, ingredients, category_id, tag_ids} and PATCH for update.

## OpenAPI

The backend includes a script at src/api/generate_openapi.py. If the openapi.json needs regeneration after API changes, run this script in the backend container environment. For follow-up:
- Regenerate openapi.json if any of the above changes are reflected in the API signatures.

```bash
# Note for follow-up agent (don't run here):
python -m src.api.generate_openapi
```

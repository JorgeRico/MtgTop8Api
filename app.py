from fastapi import FastAPI
from errors.errors import notFound
from codes.codes import HTTP_200
from starlette.middleware.cors import CORSMiddleware
from routers import router_decks, router_leagues, router_players, router_tournaments
import os

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url = None,
    exception_handlers={
        404: notFound,
    }
)

app.include_router(router_tournaments.router)
app.include_router(router_decks.router)
app.include_router(router_leagues.router)
app.include_router(router_players.router)

allowed_origins = os.getenv('ALLOWED_ORIGINS', 'https://mtg-stats.vercel.app,http://localhost:3000').split(',')
origins = [o.strip() for o in allowed_origins if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
    expose_headers=["*"]
)

API_VERSION = "1.0.0"

@app.get("/", status_code=HTTP_200, description="API version info")
async def root():
    return {
        "name": "MTG Stats API",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", status_code=HTTP_200, description="Health endpoint")
async def index():
    return { "message": "It works !!!!" }

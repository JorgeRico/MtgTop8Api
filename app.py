from fastapi import FastAPI
from errors.errors import notFound
from codes.codes import HTTP_200
from starlette.middleware.cors import CORSMiddleware
from routers import router_decks, router_leagues, router_players, router_tournaments
import os

if os.getenv('ENV') == 'development': 
    app = FastAPI(
        exception_handlers={
            404: notFound,
        }
    )
else:
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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/health", status_code=HTTP_200, description="Health endpoint")
async def index():
    return { "message": "It works !!!!" }



# from fastapi import FastAPI
# from supabase import create_client, Client
# app = FastAPI()

# url = 'https://akcrfttlllzxeqbfrblj.supabase.co'
# key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFrY3JmdHRsbGx6eGVxYmZyYmxqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxMTUwNDgsImV4cCI6MjA3MzY5MTA0OH0.5ePOOVBOaiJFCf9JppOR-ZadusPvBgHULJTiUIBn6WE'

# supabase: Client = create_client(url, key)

# @app.get("/leagues")
# def themes():
#     themes = supabase.table('leagues').select('*').execute()
#     return themes

# @app.get("/tournaments/")
# def monsters(theme : str = "demo-theme-1"):
#     monsters = supabase.table('monsters').select('*').eq('monsterTheme',theme).execute()
#     return monsters
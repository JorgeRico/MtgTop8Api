from fastapi import FastAPI
from errors.errors import notFound
from codes.codes import HTTP_200
from starlette.middleware.cors import CORSMiddleware
from routers import router_decks, router_leagues, router_players, router_tournaments

app = FastAPI(exception_handlers={
    404: notFound
})

app.include_router(router_tournaments.router)
app.include_router(router_decks.router)
app.include_router(router_leagues.router)
app.include_router(router_players.router)

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["*"]
# )

@app.get("/health", status_code=HTTP_200, description="Health endpoint")
async def index():
    return { "message": "It works !!!!" }

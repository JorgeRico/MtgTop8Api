from fastapi import FastAPI, HTTPException, Path
from typing import Any
from db.queries import Queries
from models.league import League
from models.tournament import Tournament, TournamentData
from models.player import Player, PlayerData
from models.card import Card, MAINDECK_CARD, SIDEBOARD_CARD
from models.deck import Deck
from models.stats import TournamentStats, LeagueStats, CardStats, STATS_LIMIT
from errors.errors import notFound
from codes.codes import HTTP_200, HTTP_404
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(exception_handlers={
    404: notFound
})

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

# ---------------------------------------------
# League endpoints
# ---------------------------------------------
@app.get("/leagues", response_model=list[League], status_code=HTTP_200, description="Leagues info")
async def getLeagueData() -> Any:
    query  = Queries()
    result = query.getLeagues()

    if result is None or id is None:
        raise HTTPException(status_code=HTTP_404, detail="League not found")

    return result

@app.get("/leagues/{id}", response_model=League, status_code=HTTP_200, description="League info")
async def getLeagueData(id: int = Path(gt = 0, title="Id League", description="League resource identifier")) -> Any:
    query  = Queries()
    result = query.getLeagueData(id)

    if result is None or id is None:
        raise HTTPException(status_code=HTTP_404, detail="League not found")

    return result

@app.get("/leagues/{id}/tournaments", response_model=list[Tournament], status_code=HTTP_200, description="League Tournaments list")
async def getLeagueTournamentsData(id: int = Path(gt = 0, title="Id League", description="League resource identifier"), skip: int = 0, limit: int = 10) -> Any:
    query  = Queries()
    result = query.getLeagueTournaments(id, skip, limit)
    
    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result

# ---------------------------------------------
# Tournament endpoints
# ---------------------------------------------
@app.get("/tournaments/{id}", response_model=Tournament, status_code=HTTP_200, description="Tournament info")
async def getTournament(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = Queries()
    result = query.getTournaments(id)
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result

@app.get("/tournaments/{id}/players", response_model=list[Player], status_code=HTTP_200, description="Tournament players list")
async def getTournamentPlayers(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = Queries()
    result = query.getTournamentPlayers(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result

@app.get("/tournaments/{id}/decks", response_model=list[Deck], status_code=HTTP_200, description="Tournament decks")
async def getTournamentDecks(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = Queries()
    result = query.getTournamentDecks(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result

@app.get("/tournaments/{id}/data", response_model=TournamentData, status_code=HTTP_200, description="Tournament info, players and decks")
async def getTournamentData(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    tournament = await getTournament(str(id))
    players    = await getTournamentPlayers(str(id))

    for player in players:
        cards = await getDeckCards(player['idDeck'])
        player.update({'deck' : cards})

    if tournament == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")
    if len(players) == 0:
        raise HTTPException(status_code=HTTP_404, detail="Item with no players")

    return TournamentData(tournament=tournament, players=players)

# ---------------------------------------------
# Player endpoints
# ---------------------------------------------
@app.get("/players/{id}", response_model=Player, status_code=HTTP_200, description="Player info")
async def getPlayer(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = Queries()
    result = query.getPlayer(id)

    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result

@app.get("/players/{id}/data", response_model=PlayerData, status_code=HTTP_200, description="Player info and deck list")
async def getPlayerDeckData(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = Queries()
    result = query.getPlayerDeckData(id)

    cards = await getDeckCards(result['idDeck'])
    result.update({'deck' : cards})
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")
    if len(cards) == None:
        raise HTTPException(status_code=HTTP_404, detail="Item with no cards")

    return result

@app.get("/players/{id}/decks", response_model=Deck, status_code=HTTP_200, description="Player deck list")
async def getPlayerDeck(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = Queries()
    result = query.getPlayerDeck(id)
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result


# ---------------------------------------------
# Deck endpoints
# ---------------------------------------------
@app.get("/decks/{id}/cards", response_model=list[Card], status_code=HTTP_200, description="Deck cards list")
async def getDeckCards(id: int = Path(gt = 0, title="Id Deck", description="Deck resource identifier")) -> Any:
    query  = Queries()
    result = query.getDeckCards(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


# ---------------------------------------------
# League Stats endpoints
# ---------------------------------------------
@app.get("/leagues/{id}/stats", response_model=LeagueStats, status_code=HTTP_200, description="League Stats")
async def getTop10LeagueCards(id: int = Path(gt = 0, title="Id League", description="League resource identifier")):
    query = Queries()
    top10 = query.getTopLeagueCards(id, STATS_LIMIT)

    if len(top10) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = Queries()
    mb    = query.getMainboardLeagueCards(id, MAINDECK_CARD, STATS_LIMIT)

    if len(mb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = Queries()
    sb    = query.getSideboardLeagueCards(id, SIDEBOARD_CARD, STATS_LIMIT)

    if len(sb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    query   = Queries()
    players = query.getLeaguePlayers(id, STATS_LIMIT)

    if len(players) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return LeagueStats(top10=top10, mb=mb, sb=sb, players=players)


# ---------------------------------------------
# League Cards Stats endpoints
# ---------------------------------------------
@app.get("/leagues/{id}/cards/stats", response_model=CardStats, status_code=HTTP_200, description="League Cards Stats")
async def getLeagueCards(id: int = Path(gt = 0, title="Id League", description="League resource identifier")):
    query         = Queries()
    creatures     = query.getTopLeagueCardSingleType(id, 'creature', STATS_LIMIT)
    query         = Queries()
    instants      = query.getTopLeagueCardSingleType(id, 'instant', STATS_LIMIT)
    query         = Queries()
    sorceries     = query.getTopLeagueCardSingleType(id, 'sorcery', STATS_LIMIT)
    query         = Queries()
    planeswalkers = query.getTopLeagueCardSingleType(id, 'planeswalker', STATS_LIMIT)
    query         = Queries()
    artifacts     = query.getTopLeagueCardSingleType(id, 'artifact', STATS_LIMIT)
    query         = Queries()
    enchantments  = query.getTopLeagueCardSingleType(id, 'enchantment', STATS_LIMIT)
    query         = Queries()
    lands         = query.getTopLeagueCardSingleType(id, 'land', STATS_LIMIT)

    return CardStats(creatures=creatures, instants=instants, sorceries=sorceries, planeswalkers=planeswalkers, artifacts=artifacts, enchantments=enchantments, lands=lands)
    

# ---------------------------------------------
# Tournament Stats endpoints
# ---------------------------------------------
@app.get("/tournaments/{id}/stats", response_model=TournamentStats, status_code=HTTP_200, description="Tournament stats")
async def getTournamentStats(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")):
    query = Queries()
    top10 = query.getTournamentTopCards(id, STATS_LIMIT)
    if len(top10) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = Queries()
    mb    = query.getTournamentMainboardCards(id, MAINDECK_CARD, STATS_LIMIT)
    if len(mb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = Queries()
    sb    = query.getTournamentSideoardCards(id, SIDEBOARD_CARD, STATS_LIMIT)
    if len(sb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return TournamentStats(top10=top10, mb=mb, sb=sb)

# ---------------------------------------------
# Tournament Card Stats endpoints
# ---------------------------------------------
@app.get("/tournaments/{id}/cards/stats", response_model=CardStats, status_code=HTTP_200, description="Tournament Card Stats")
async def getTournamentCards(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")):
    query         = Queries()
    creatures     = query.getTopTournamentCardSingleType(id, 'creature', STATS_LIMIT)
    query         = Queries()
    instants      = query.getTopTournamentCardSingleType(id, 'instant', STATS_LIMIT)
    query         = Queries()
    sorceries     = query.getTopTournamentCardSingleType(id, 'sorcery', STATS_LIMIT)
    query         = Queries()
    planeswalkers = query.getTopTournamentCardSingleType(id, 'planeswalker', STATS_LIMIT)
    query         = Queries()
    artifacts     = query.getTopTournamentCardSingleType(id, 'artifact', STATS_LIMIT)
    query         = Queries()
    enchantments  = query.getTopTournamentCardSingleType(id, 'enchantment', STATS_LIMIT)
    query         = Queries()
    lands         = query.getTopTournamentCardSingleType(id, 'land', STATS_LIMIT)

    return CardStats(creatures=creatures, instants=instants, sorceries=sorceries, planeswalkers=planeswalkers, artifacts=artifacts, enchantments=enchantments, lands=lands)
    

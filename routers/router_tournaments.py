from fastapi import APIRouter, HTTPException, Path
from schemas.tournament import Tournament
from queries.tournaments import TournamentQueries
from schemas.player import PlayerWithDeck
from codes.codes import HTTP_200, HTTP_404, TOP, MAINBOARD, SIDEBOARD
from typing import Any
from schemas.stats import Stats, Stats, STATS_LIMIT
from schemas.card import MAINDECK_CARD, SIDEBOARD_CARD
from cachetools import cached, TTLCache

router = APIRouter(
    prefix = "/tournaments",
    tags   = ["Tournaments"]
)

cache = TTLCache(maxsize=100, ttl=300)  # Cache size of 100 items, expires after 5 minutes


@cached(cache)
@router.get("/{id}", response_model=Tournament, status_code=HTTP_200, description="Tournament info")
async def getTournament(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = TournamentQueries()
    result = query.getTournaments(id)
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result


@cached(cache)
@router.get("/{id}/players", response_model=list[PlayerWithDeck], status_code=HTTP_200, description="Tournament players list")
async def getTournamentPlayersWithDecks(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = TournamentQueries()
    result = query.getTournamentPlayers(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


@cached(cache)
@router.get("/{id}/stats/{options}", response_model=Stats, status_code=HTTP_200, description="Tournament Stats")
async def getTopTournamentStats(id: int = Path(gt = 0, title="Id League", description="Tournament resource identifier"), options: str = Path(title="Tournament Options", description="Tournament resource options")):
    query = TournamentQueries()

    if options == TOP:
        result = query.getTournamentTopCards(id, STATS_LIMIT)
    if options == MAINBOARD:
        result = query.getTournamentCardsByBoardType(id, MAINDECK_CARD, STATS_LIMIT)
    if options == SIDEBOARD:
        result = query.getTournamentCardsByBoardType(id, SIDEBOARD_CARD, STATS_LIMIT)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return Stats(stats=result)


@cached(cache)
@router.get("/{id}/cards/{cardType}/stats", response_model=Stats, status_code=HTTP_200, description="Tournament Cards Stats")
async def getTournamentCardStatsByType(id: int = Path(gt = 0, title="Id League", description="Tournament resource identifier"), cardType: str = Path(title="Card Type", description="Card Type to search")):
    query = TournamentQueries()
    cards = query.getTopTournamentCardByType(id, cardType, STATS_LIMIT)

    return Stats(stats=cards)
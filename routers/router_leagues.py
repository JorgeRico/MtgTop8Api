from fastapi import APIRouter, HTTPException, Path
from schemas.league import League
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.stats import LeagueStats, SingleCardStats, STATS_LIMIT
from schemas.card import MAINDECK_CARD, SIDEBOARD_CARD
from schemas.tournament import Tournament
from queries.leagues import LeagueQueries
from cachetools import cached, TTLCache

router = APIRouter(
    prefix = "/leagues",
    tags   = ["Leagues"]
)

cache = TTLCache(maxsize=100, ttl=300)  # Cache size of 100 items, expires after 5 minutes


@cached(cache)
@router.get("/current", response_model=list[League], status_code=HTTP_200, description="Leagues info")
async def getLeagueData() -> Any:
    query  = LeagueQueries()
    result = query.getCurrentLeagues()

    if result is None or id is None:
        raise HTTPException(status_code=HTTP_404, detail="League not found")

    return result


@cached(cache)
@router.get("/past", response_model=list[League], status_code=HTTP_200, description="Leagues info")
async def getLeagueData() -> Any:
    query  = LeagueQueries()
    result = query.getPastLeagues()

    if result is None or id is None:
        raise HTTPException(status_code=HTTP_404, detail="League not found")

    return result


@cached(cache)
@router.get("/{id}", response_model=League, status_code=HTTP_200, description="League info")
async def getLeagueData(id: int = Path(gt = 0, title="Id League", description="League resource identifier")) -> Any:
    query  = LeagueQueries()
    result = query.getLeagueData(id)

    if result is None or id is None:
        raise HTTPException(status_code=HTTP_404, detail="League not found")

    return result


@cached(cache)
@router.get("/{id}/tournaments", response_model=list[Tournament], status_code=HTTP_200, description="League Tournaments list")
async def getLeagueTournamentsData(id: int = Path(gt = 0, title="Id League", description="League resource identifier"), skip: int = 0, limit: int = 10) -> Any:
    query  = LeagueQueries()
    result = query.getLeagueTournaments(id, skip, limit)
    
    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


@cached(cache)
@router.get("/{id}/stats/{options}", response_model=LeagueStats, status_code=HTTP_200, description="League Stats")
async def getTop10LeagueCards(id: int = Path(gt = 0, title="Id League", description="League resource identifier"), options: str = Path(title="League Options", description="League resource options")):
    query = LeagueQueries()

    if options == 'top':
        result = query.getTopLeagueCards(id, STATS_LIMIT)
    if options == "mainboard":
        result = query.getMainboardLeagueCards(id, MAINDECK_CARD, STATS_LIMIT)
    if options == "sideboard":
        result = query.getSideboardLeagueCards(id, SIDEBOARD_CARD, STATS_LIMIT)
    if options == "players":
        result = query.getLeaguePlayers(id, STATS_LIMIT)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return LeagueStats(stats=result)


@cached(cache)
@router.get("/{id}/cards/{cardType}/stats", response_model=SingleCardStats, status_code=HTTP_200, description="League Cards Stats")
async def getLeagueCardsByType(id: int = Path(gt = 0, title="Id League", description="League resource identifier"), cardType: str = Path(title="Card Type", description="Card Type to search")):
    query = LeagueQueries()
    cards = query.getTopLeagueCardSingleType(id, cardType, STATS_LIMIT)

    return SingleCardStats(cards=cards)
    
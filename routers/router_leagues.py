from fastapi import APIRouter, HTTPException, Path
from schemas.league import League
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.stats import LeagueStats, CardStats, STATS_LIMIT
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
@router.get("/{id}/stats", response_model=LeagueStats, status_code=HTTP_200, description="League Stats")
async def getTop10LeagueCards(id: int = Path(gt = 0, title="Id League", description="League resource identifier")):
    query = LeagueQueries()
    top10 = query.getTopLeagueCards(id, STATS_LIMIT)

    if len(top10) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = LeagueQueries()
    mb    = query.getMainboardLeagueCards(id, MAINDECK_CARD, STATS_LIMIT)

    if len(mb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = LeagueQueries()
    sb    = query.getSideboardLeagueCards(id, SIDEBOARD_CARD, STATS_LIMIT)

    if len(sb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    query   = LeagueQueries()
    players = query.getLeaguePlayers(id, STATS_LIMIT)

    if len(players) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return LeagueStats(top10=top10, mb=mb, sb=sb, players=players)


@cached(cache)
@router.get("/{id}/cards/stats", response_model=CardStats, status_code=HTTP_200, description="League Cards Stats")
async def getLeagueCards(id: int = Path(gt = 0, title="Id League", description="League resource identifier")):
    query         = LeagueQueries()
    creatures     = query.getTopLeagueCardSingleType(id, 'creature', STATS_LIMIT)
    query         = LeagueQueries()
    instants      = query.getTopLeagueCardSingleType(id, 'instant', STATS_LIMIT)
    query         = LeagueQueries()
    sorceries     = query.getTopLeagueCardSingleType(id, 'sorcery', STATS_LIMIT)
    query         = LeagueQueries()
    planeswalkers = query.getTopLeagueCardSingleType(id, 'planeswalker', STATS_LIMIT)
    query         = LeagueQueries()
    artifacts     = query.getTopLeagueCardSingleType(id, 'artifact', STATS_LIMIT)
    query         = LeagueQueries()
    enchantments  = query.getTopLeagueCardSingleType(id, 'enchantment', STATS_LIMIT)
    query         = LeagueQueries()
    lands         = query.getTopLeagueCardSingleType(id, 'land', STATS_LIMIT)

    return CardStats(creatures=creatures, instants=instants, sorceries=sorceries, planeswalkers=planeswalkers, artifacts=artifacts, enchantments=enchantments, lands=lands)
    
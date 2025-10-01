from fastapi import APIRouter, HTTPException, Path
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.player import Player
# from queries.mysql.players import PlayerQueries
from queries.supabase.players import PlayerQueries
from cachetools import cached, TTLCache

router = APIRouter(
    prefix = "/players",
    tags   = ["Players"]
)

cache = TTLCache(maxsize=100, ttl=300)  # Cache size of 100 items, expires after 5 minutes


@cached(cache)
@router.get("/{id}", response_model=Player, status_code=HTTP_200, description="Player info")
async def getPlayer(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = await query.getPlayer(id)

    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result


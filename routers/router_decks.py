from fastapi import APIRouter, HTTPException, Path
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.card import Card
from queries.decks import DeckQueries
from cachetools import cached, TTLCache

router = APIRouter(
    prefix = "/decks",
    tags   = ["Decks"]
)

cache = TTLCache(maxsize=100, ttl=300)  # Cache size of 100 items, expires after 5 minutes


@cached(cache)
@router.get("/{id}/cards", response_model=list[Card], status_code=HTTP_200, description="Deck cards list")
async def getDeckCards(id: int = Path(gt = 0, title="Id Deck", description="Deck resource identifier")) -> Any:
    query  = DeckQueries()
    result = query.getDeckCards(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


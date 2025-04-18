from fastapi import APIRouter, HTTPException, Path
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.player import Player, PlayerDataWithDeck
from schemas.deck import Deck
from queries.players import PlayerQueries
from queries.decks import DeckQueries
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
    result = query.getPlayer(id)

    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result


@cached(cache)
@router.get("/{id}/data", response_model=PlayerDataWithDeck, status_code=HTTP_200, description="Player info and deck list")
async def getPlayerDeckData(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = query.getPlayerDeckData(id)

    query = DeckQueries()
    cards = query.getDeckCards(result['idDeck'])
    result.update({'deck' : cards})
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")
    if len(cards) == None:
        raise HTTPException(status_code=HTTP_404, detail="Item with no cards")

    return result


@cached(cache)
@router.get("/{id}/decks", response_model=Deck, status_code=HTTP_200, description="Player deck list")
async def getPlayerDeck(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = query.getPlayerDeck(id)
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result

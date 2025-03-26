from fastapi import APIRouter, HTTPException, Path
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.player import Player, PlayerData
from routers.router_decks import getDeckCards
from schemas.deck import Deck
from queries.players import PlayerQueries

router = APIRouter(
    prefix = "/players",
    tags   = ["Players"]
)

# ---------------------------------------------
# Player endpoints
# ---------------------------------------------
@router.get("/{id}", response_model=Player, status_code=HTTP_200, description="Player info")
async def getPlayer(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = query.getPlayer(id)

    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result

@router.get("/{id}/data", response_model=PlayerData, status_code=HTTP_200, description="Player info and deck list")
async def getPlayerDeckData(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = query.getPlayerDeckData(id)

    cards = await getDeckCards(result['idDeck'])
    result.update({'deck' : cards})
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")
    if len(cards) == None:
        raise HTTPException(status_code=HTTP_404, detail="Item with no cards")

    return result

@router.get("/{id}/decks", response_model=Deck, status_code=HTTP_200, description="Player deck list")
async def getPlayerDeck(id: int = Path(gt = 0, title="Id Player", description="Player resource identifier")) -> Any:
    query  = PlayerQueries()
    result = query.getPlayerDeck(id)
    
    if result == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")

    return result

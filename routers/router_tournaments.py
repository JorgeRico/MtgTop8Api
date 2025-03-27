from fastapi import APIRouter, HTTPException, Path
from schemas.tournament import Tournament, TournamentData
from queries.tournaments import TournamentQueries
from queries.decks import DeckQueries
from codes.codes import HTTP_200, HTTP_404
from typing import Any
from schemas.player import Player
from schemas.deck import Deck
from schemas.stats import TournamentStats, CardStats, STATS_LIMIT
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
@router.get("/{id}/players", response_model=list[Player], status_code=HTTP_200, description="Tournament players list")
async def getTournamentPlayers(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = TournamentQueries()
    result = query.getTournamentPlayers(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


@cached(cache)
@router.get("/{id}/decks", response_model=list[Deck], status_code=HTTP_200, description="Tournament decks")
async def getTournamentDecks(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query  = TournamentQueries()
    result = query.getTournamentDecks(id)

    if len(result) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return result


@cached(cache)
@router.get("/{id}/data", response_model=TournamentData, status_code=HTTP_200, description="Tournament info, players and decks")
async def getTournamentData(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")) -> Any:
    query      = TournamentQueries()
    tournament = query.getTournaments(str(id))
    query      = TournamentQueries()
    players    = query.getTournamentPlayers(str(id))

    for player in players:
        query = DeckQueries()
        cards = query.getDeckCards(player['idDeck'])
        player.update({'deck' : cards})

    if tournament == None:
        raise HTTPException(status_code=HTTP_404, detail="Item not found")
    if len(players) == 0:
        raise HTTPException(status_code=HTTP_404, detail="Item with no players")

    return TournamentData(tournament=tournament, players=players)


@cached(cache)
@router.get("/{id}/stats", response_model=TournamentStats, status_code=HTTP_200, description="Tournament stats")
async def getTournamentStats(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")):
    query = TournamentQueries()
    top10 = query.getTournamentTopCards(id, STATS_LIMIT)
    if len(top10) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = TournamentQueries()
    mb    = query.getTournamentMainboardCards(id, MAINDECK_CARD, STATS_LIMIT)
    if len(mb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")
    
    query = TournamentQueries()
    sb    = query.getTournamentSideoardCards(id, SIDEBOARD_CARD, STATS_LIMIT)
    if len(sb) == 0:
        raise HTTPException(status_code=HTTP_404, detail="No items found")

    return TournamentStats(top10=top10, mb=mb, sb=sb)


@cached(cache)
@router.get("/{id}/cards/stats", response_model=CardStats, status_code=HTTP_200, description="Tournament Card Stats")
async def getTournamentCards(id: int = Path(gt = 0, title="Id Tournament", description="Tournament resource identifier")):
    query         = TournamentQueries()
    creatures     = query.getTopTournamentCardSingleType(id, 'creature', STATS_LIMIT)
    query         = TournamentQueries()
    instants      = query.getTopTournamentCardSingleType(id, 'instant', STATS_LIMIT)
    query         = TournamentQueries()
    sorceries     = query.getTopTournamentCardSingleType(id, 'sorcery', STATS_LIMIT)
    query         = TournamentQueries()
    planeswalkers = query.getTopTournamentCardSingleType(id, 'planeswalker', STATS_LIMIT)
    query         = TournamentQueries()
    artifacts     = query.getTopTournamentCardSingleType(id, 'artifact', STATS_LIMIT)
    query         = TournamentQueries()
    enchantments  = query.getTopTournamentCardSingleType(id, 'enchantment', STATS_LIMIT)
    query         = TournamentQueries()
    lands         = query.getTopTournamentCardSingleType(id, 'land', STATS_LIMIT)

    return CardStats(creatures=creatures, instants=instants, sorceries=sorceries, planeswalkers=planeswalkers, artifacts=artifacts, enchantments=enchantments, lands=lands)
    

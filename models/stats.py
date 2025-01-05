from pydantic import BaseModel
from models.card import TopCard
from models.player import PlayerStats

STATS_LIMIT = 15

class CardStats(BaseModel):
    creatures     : list[TopCard]
    instants      : list[TopCard]
    sorceries     : list[TopCard]
    planeswalkers : list[TopCard]
    artifacts     : list[TopCard]
    enchantments  : list[TopCard]
    lands         : list[TopCard]

class TournamentStats(BaseModel):
    top10 : list[TopCard]
    mb    : list[TopCard]
    sb    : list[TopCard]

class LeagueStats(BaseModel):
    top10     : list[TopCard]
    mb        : list[TopCard]
    sb        : list[TopCard]
    players   : list[PlayerStats]

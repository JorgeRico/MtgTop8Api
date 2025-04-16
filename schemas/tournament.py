from pydantic import BaseModel
from schemas.player import PlayerData

class Tournament(BaseModel):
    id       : int
    name     : str
    date     : str
    idLeague : int
    players  : int

class TournamentData(BaseModel):
    tournament : Tournament
    players    : list[PlayerData]
from pydantic import BaseModel
from models.player import PlayerData

class Tournament(BaseModel):
    id       : int
    name     : str
    date     : str
    idLeague : int

class TournamentData(BaseModel):
    tournament : Tournament
    players    : list[PlayerData]
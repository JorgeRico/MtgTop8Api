from pydantic import BaseModel
class Tournament(BaseModel):
    id       : int
    name     : str
    date     : str
    idLeague : int
    players  : int
    format   : int

class IdTournament(BaseModel):
    id : int
from pydantic import BaseModel

class League(BaseModel):
    id       : int
    name     : str
    isLegacy : int
    current  : int
    year     : int

class IdLeague(BaseModel):
    id : int

class HomeLeagues(BaseModel):
    current : list[League]
    past    : list[League]
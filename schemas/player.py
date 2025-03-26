from pydantic import BaseModel
from schemas.card import Card

class Player(BaseModel):
    id       : int 
    name     : str
    position : int
    idDeck   : int

class PlayerData(BaseModel):
    id       : int 
    name     : str
    position : int
    idDeck   : int
    deck     : list[Card]

class PlayerStats(BaseModel):
    num  : int 
    name : str
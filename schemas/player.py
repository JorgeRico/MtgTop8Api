from pydantic import BaseModel

class Player(BaseModel):
    id       : int 
    name     : str
    position : int
    idDeck   : int

class PlayerWithDeck(BaseModel):
    id       : int 
    name     : str
    position : int
    idDeck   : int
    deckName : str

class PlayerStats(BaseModel):
    num  : int 
    name : str
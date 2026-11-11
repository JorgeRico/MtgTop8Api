from pydantic import BaseModel, Field


class Player(BaseModel):
    id       : int = Field(gt=0)
    name     : str = Field(min_length=1)
    position : int = Field(ge=0)
    idDeck   : int = Field(gt=0)


class PlayerWithDeck(BaseModel):
    id       : int = Field(gt=0)
    name     : str = Field(min_length=1)
    position : int = Field(ge=0)
    idDeck   : int = Field(gt=0)
    deckName : str = Field(min_length=1)


class PlayerStats(BaseModel):
    num  : int = Field(ge=0)
    name : str = Field(min_length=1)

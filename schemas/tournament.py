from pydantic import BaseModel, Field


class Tournament(BaseModel):
    id         : int = Field(gt=0)
    name       : str = Field(min_length=1)
    date       : str = Field(min_length=1)
    idLeague   : int = Field(gt=0)
    players    : int = Field(ge=0)
    format     : int = Field(ge=0)
    leagueName : str = Field(min_length=1)
    year       : int = Field(ge=1900, le=2100)


class IdTournament(BaseModel):
    id : int = Field(gt=0)

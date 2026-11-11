from pydantic import BaseModel, Field


class League(BaseModel):
    id             : int = Field(gt=0)
    name           : str = Field(min_length=1)
    isLegacy       : int = Field(ge=0, le=1)
    current        : int = Field(ge=0, le=1)
    year           : int = Field(ge=1900, le=2100)
    location       : str | None = None
    locationName   : str | None = None
    classification : str | None = None


class IdLeague(BaseModel):
    id : int = Field(gt=0)


class HomeLeagues(BaseModel):
    current : list[League]
    past    : list[League]


class HomePastLeagues(BaseModel):
    leagues : list[League]
    total   : int = Field(ge=0)


class LeagueAverage(BaseModel):
    average : int = Field(ge=0)

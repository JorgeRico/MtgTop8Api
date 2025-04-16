from pydantic import BaseModel

class League(BaseModel):
    id       : int
    name     : str
    isLegacy : int
    current  : int
    year     : int

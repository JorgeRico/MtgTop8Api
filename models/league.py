from pydantic import BaseModel

class League(BaseModel):
    id   : int
    name : str

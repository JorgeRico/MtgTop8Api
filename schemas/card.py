from pydantic import BaseModel, Field

MAINDECK_CARD  = "md"
SIDEBOARD_CARD = "sb"

class Card(BaseModel):
    id       : int = Field(gt=0)
    name     : str = Field(min_length=1)
    num      : int = Field(ge=0)
    cardType : str = Field(min_length=1)
    board    : str = Field(min_length=1)
    imgUrl   : str = Field(min_length=1)

class TopCard(BaseModel):
    num    : int = Field(ge=0)
    name   : str = Field(min_length=1)
    imgUrl : str | None = None

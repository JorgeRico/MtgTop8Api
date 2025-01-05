from pydantic import BaseModel
from models.card import Card

class Deck(BaseModel):
    id   : int
    name : str

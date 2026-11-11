from pydantic import BaseModel, Field
from schemas.card import TopCard

STATS_LIMIT = 15
class Stats(BaseModel):
    stats : list[TopCard] = Field(max_length=STATS_LIMIT)

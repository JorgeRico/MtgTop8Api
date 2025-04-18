from pydantic import BaseModel
from schemas.card import TopCard

STATS_LIMIT = 15
class Stats(BaseModel):
    stats : list[TopCard]

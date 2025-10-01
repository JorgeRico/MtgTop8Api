# from db.mysql.db import Db
from db.supabase.db import Db

class DeckQueries:

    def __init__(self):
        self.db = Db()
    
    async def getDeckCards(self, id):
        conn   = await self.db.getSupabase()
        result = conn.table('cards').select('id, name, num, cardType, board, imgUrl').eq('idDeck', str(id)).execute()

        return result.data
    
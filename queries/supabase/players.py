# from db.mysql.db import Db
from db.supabase.db import Db

class PlayerQueries:

    def __init__(self):
        self.db = Db()
    
    # get player info
    async def getPlayer(self, id):
        conn   = await self.db.getSupabase()
        result = conn.table('players').select('id, name, position, idDeck').eq('id', str(id)).execute()

        return result

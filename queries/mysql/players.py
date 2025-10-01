from db.mysql.db import Db

class PlayerQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    # get player info
    async def getPlayer(self, id):
        query  = 'SELECT id, name, position, idDeck FROM players WHERE id = ' + str(id)
        result = await self.db.getSelectSingleResultQuery(self.conn, query)

        return result

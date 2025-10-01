from db.mysql.db import Db

class DeckQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    async def getDeckCards(self, id):
        query  = 'SELECT id, name, num, cardType, board FROM cards WHERE idDeck = ' + str(id)
        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
from db.db import Db

class DeckQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    def getDeckCards(self, id):
        query  = 'SELECT id, name, num, cardType, board FROM cards WHERE idDeck = ' + str(id)
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
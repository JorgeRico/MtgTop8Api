from db.db import Db

class PlayerQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    def getPlayer(self, id):
        query  = 'SELECT id, name, position, idDeck FROM player WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    def getPlayerDeckData(self, id):
        query  = 'SELECT id, name, position, idDeck FROM player WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    def getPlayerDeck(self, id):
        query  = 'SELECT id, name FROM deck WHERE idPlayer = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result

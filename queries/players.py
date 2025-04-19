from db.db import Db

class PlayerQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    # get player info
    def getPlayer(self, id):
        query  = 'SELECT id, name, position, idDeck FROM player WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result

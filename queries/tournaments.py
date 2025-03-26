from db.db import Db

class TournamentQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    def getTournaments(self, id):
        query  = 'SELECT id, name, date, idLeague FROM tournament WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    def getTournamentPlayers(self, id):
        query  = 'SELECT id, name, position, idDeck FROM player WHERE idTournament = ' + str(id) + ' ORDER BY position ASC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTournamentDecks(self, id):
        query =  "SELECT deck.id, deck.name FROM player "
        query += "INNER JOIN tournament on tournament.id = player.idTournament "
        query += "INNER JOIN deck on deck.id = player.idDeck "
        query += "WHERE tournament.id = " + str(id) + " "

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result

    def getTournamentTopCards(self, id, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.id = " + str(id) + " "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTournamentMainboardCards(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.id = " + str(id) + " and cards.board = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTournamentSideoardCards(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.id = " + str(id) + " AND cards.board = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTopTournamentCardSingleType(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.id = " + str(id) + " "
        query += "AND cards.cardType = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
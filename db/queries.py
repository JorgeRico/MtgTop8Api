from db.db import Db

class Queries:

    def __init__(self):
        self.db    = Db()
        self.conn = self.db.connect()

    def getCurrentLeagues(self):
        query  = 'SELECT id, name, isLegacy, current FROM league where active = 1 AND current = 1 ORDER BY id DESC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getPastLeagues(self):
        query  = 'SELECT id, name, isLegacy, current FROM league where active = 1 AND current = 0 ORDER BY id DESC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getLeagueData(self, id):
        query  = 'SELECT id, name, isLegacy, current FROM league WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    def getLeagueTournaments(self, id, skip, limit):
        query  = 'SELECT id, name, date, idLeague FROM tournament WHERE idLeague = ' + str(id) + ' LIMIT ' + str(skip) + ', ' + str(limit)
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
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
    
    def getDeckCards(self, id):
        query  = 'SELECT id, name, num, cardType, board FROM cards WHERE idDeck = ' + str(id)
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTopLeagueCards(self, id, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getTopLeagueCardSingleType(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " "
        query += "AND cards.cardType = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getMainboardLeagueCards(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " and cards.board = '" + str(boardType) + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getSideboardLeagueCards(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " AND cards.board = '" + boardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    def getLeaguePlayers(self, id, limit):
        query = "SELECT COUNT(player.name) as num, player.name FROM player "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " "
        query += "GROUP BY player.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

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
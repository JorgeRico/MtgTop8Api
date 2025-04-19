from db.db import Db

class LeagueQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()

    # get active leagues - current year
    def getCurrentLeagues(self):
        query  = 'SELECT id, name, isLegacy, current, year FROM league where active = 1 AND current = 1 ORDER BY id DESC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get past leagues - other years
    def getPastLeagues(self):
        query  = 'SELECT id, name, isLegacy, current, year FROM league where active = 1 AND current = 0 ORDER BY year DESC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league info
    def getLeagueData(self, id):
        query  = 'SELECT id, name, isLegacy, current, year FROM league WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    # get league tournaments list
    def getLeagueTournaments(self, id):
        query  = 'SELECT id, name, date, idLeague, players FROM tournament WHERE idLeague = ' + str(id)
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league top cards stats
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
    
    # league card stats by card type
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
    
    # league card stats by board type
    def getLeagueCardsByBoard(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " and cards.board = '" + str(boardType) + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league player stats
    def getLeaguePlayers(self, id, limit):
        query = "SELECT COUNT(player.name) as num, player.name FROM player "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.idLeague = " + str(id) + " "
        query += "GROUP BY player.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
from db.mysql.db import Db

class LeagueQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()

    # get active leagues - current year
    async def getCurrentLeagues(self):
        query  = 'SELECT id, name, isLegacy, current, year FROM leagues where active = 1 AND current = 1 ORDER BY id DESC'
        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get past leagues - other years
    async def getPastLeagues(self):
        query  = 'SELECT id, name, isLegacy, current, year FROM leagues where active = 1 AND current = 0 ORDER BY year DESC'
        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league info
    async def getLeagueData(self, id):
        query  = 'SELECT id, name, isLegacy, current, year FROM leagues WHERE id = ' + str(id)
        result = await self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    # get league tournaments list
    async def getLeagueTournaments(self, id):
        query = 'SELECT tournaments.id as id, tournaments.name as name, tournaments.date as date, tournaments.idLeague as idLeague, tournaments.players as players, leagues.isLegacy as format FROM tournaments '
        query += 'INNER JOIN leagues on leagues.id = tournaments.idLeague '
        query += 'WHERE tournaments.idLeague = ' + str(id)

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league top cards stats
    async def getTopLeagueCards(self, id, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.idLeague = " + str(id) + " "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # league card stats by card type
    async def getTopLeagueCardSingleType(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.idLeague = " + str(id) + " "
        query += "AND cards.cardType = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # league card stats by board type
    async def getLeagueCardsByBoard(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.idLeague = " + str(id) + " and cards.board = '" + str(boardType) + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get league player stats
    async def getLeaguePlayers(self, id, limit):
        query = "SELECT COUNT(players.name) as num, players.name FROM players "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.idLeague = " + str(id) + " "
        query += "GROUP BY players.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
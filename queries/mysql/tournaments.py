from db.mysql.db import Db

class TournamentQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    # get tournament info
    async def getTournaments(self, id):
        query = 'SELECT tournaments.id as id, tournaments.name as name, tournaments.date as date, tournaments.idLeague as idLeague, tournaments.players as players, leagues.isLegacy as format FROM tournaments '
        query += 'INNER JOIN leagues on leagues.id = tournaments.idLeague '
        query += 'WHERE tournaments.id = ' + str(id)

        result = await self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    # get tournament players and deckname
    async def getTournamentPlayers(self, id):
        query = 'SELECT players.id as id, players.name as name, players.position as position, players.idDeck as idDeck, decks.name as deckName FROM players '
        query += 'INNER JOIN decks on decks.id = players.idDeck '
        query += 'WHERE players.idTournament = ' + str(id) + ' ORDER BY players.position ASC'

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result

    # get tournament top card stats list
    async def getTournamentTopCards(self, id, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.id = " + str(id) + " "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get tournament card stats list by board type
    async def getTournamentCardsByBoardType(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.id = " + str(id) + " and cards.board = '" + boardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get tournament card stats list by card type
    async def getTopTournamentCardByType(self, id, cardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN players ON players.idDeck = cards.idDeck "
        query += "INNER JOIN tournaments ON tournaments.id = players.idTournament "
        query += "WHERE tournaments.id = " + str(id) + " "
        query += "AND cards.cardType = '" + cardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = await self.db.getSelectListResultQuery(self.conn, query)

        return result
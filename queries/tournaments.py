from db.db import Db

class TournamentQueries:

    def __init__(self):
        self.db   = Db()
        self.conn = self.db.connect()
    
    # get tournament info
    def getTournaments(self, id):
        query  = 'SELECT id, name, date, idLeague, players FROM tournament WHERE id = ' + str(id)
        result = self.db.getSelectSingleResultQuery(self.conn, query)

        return result
    
    # get tournament players and deckname
    def getTournamentPlayers(self, id):
        query  = 'SELECT player.id as id, player.name as name, player.position as position, player.idDeck as idDeck, deck.name as deckName FROM player '
        query  += 'INNER JOIN deck on deck.id = player.idDeck '
        query  += 'WHERE player.idTournament = ' + str(id) + ' ORDER BY player.position ASC'
        result = self.db.getSelectListResultQuery(self.conn, query)

        return result

    # get tournament top card stats list
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
    
    # get tournament card stats list by board type
    def getTournamentCardsByBoardType(self, id, boardType, limit):
        query = "SELECT SUM(cards.num) as num, cards.name FROM cards "
        query += "INNER JOIN player ON player.idDeck = cards.idDeck "
        query += "INNER JOIN tournament ON tournament.id = player.idTournament "
        query += "WHERE tournament.id = " + str(id) + " and cards.board = '" + boardType + "' "
        query += "GROUP BY cards.name "
        query += "ORDER BY num desc "
        query += "LIMIT " + str(limit) + ";"

        result = self.db.getSelectListResultQuery(self.conn, query)

        return result
    
    # get tournament card stats list by card type
    def getTopTournamentCardByType(self, id, cardType, limit):
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
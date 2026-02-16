# from db.mysql.db import Db
from db.supabase.db import Db

class TournamentQueries:

    def __init__(self):
        self.db = Db()

    # get all tournaments
    async def getAllTournaments(self):
        conn   = await self.db.getSupabase()
        result = conn.table('tournaments').select('id').order("id", desc=True).execute()
        
        return result.data
    
    # get tournament info
    async def getTournaments(self, idTournament):
        conn   = await self.db.getSupabase()
        result = conn.table('tournaments').select('id, name, date, idLeague, players, leagues(isLegacy, year, name)').eq('id', str(idTournament)).order("id", desc=True).execute()
        
        # data conversion - compatibillity with mysql old results
        item = {
            'id'         : result.data[0]['id'], 
            'name'       : result.data[0]['name'], 
            'date'       : result.data[0]['date'], 
            'idLeague'   : result.data[0]['idLeague'], 
            'players'    : result.data[0]['players'], 
            'format'     : result.data[0]['leagues']['isLegacy'],
            'year'       : result.data[0]['leagues']['year'],
            'leagueName' : result.data[0]['leagues']['name']
        }
        
        return item

    # get tournament players and deckname
    async def getTournamentPlayers(self, idTournament):
        conn   = await self.db.getSupabase()
        result = conn.table('players').select('id, name, position, idDeck, decks(name)').eq('idTournament', str(idTournament)).order("position", desc=False).execute()
        
        # data conversion - compatibillity with mysql old results
        values = []
        for i in result.data:
            item = {
                'id'       : i['id'], 
                'name'     : i['name'], 
                'position' : i['position'], 
                'idDeck'   : i['idDeck'], 
                'deckName' : i['decks']['name']
            }
            values.append(item)

        return values
    
    # get tournament top card stats list
    async def getTournamentTopCards(self, idTournament, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idTournament)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').in_('idDeck', idDecks).order('name', desc=False).execute()

        return self.groupAndReorderData(result.data, limit)
    
    # get tournament card stats list by board type
    async def getTournamentCardsByBoardType(self, idTournament, boardType, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idTournament)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').eq('board', boardType).in_('idDeck', idDecks).order('name', desc=False).execute()


        return self.groupAndReorderData(result.data, limit)
    
    # get tournament card stats list by card type
    async def getTopTournamentCardByType(self, idTournament, cardType, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idTournament)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').eq('cardType', cardType).in_('idDeck', idDecks).order('name', desc=False).execute()

        return self.groupAndReorderData(result.data, limit)
    
    # get tournament idDecks
    def getIdDecks(self, conn, idTournament):
        result = conn.table('players').select('idDeck, tournaments()').eq('idTournament', str(idTournament)).execute()

        idDecks = []
        for i in result.data:
            idDecks.append(i['idDeck'])

        return idDecks

    # process data
    def groupAndReorderData(self, result, limit):
        allCards = []
        for item in result:
            if item['name'] not in allCards:
                allCards.append(item['name'])

        finalResult = []
        for item in allCards:
            total = 0
            img   = ""

            for xitem in result:
                if xitem['name'] == item:
                    total = total + int(xitem['num'])
                    img   = xitem['imgUrl']

            item = {
                "name"   : item,
                "num"    : total,
                "imgUrl" : img
            }

            finalResult.append(item)

        values = sorted(finalResult, key=lambda x: (x['num'], x['name']))
        reverse = values[::-1]
        result  = reverse[0:limit]

        return result
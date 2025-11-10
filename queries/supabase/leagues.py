# from db.mysql.db import Db
from db.supabase.db import Db
from collections import Counter

class LeagueQueries:

    def __init__(self):
        self.db = Db()

    # get all leagues
    async def getAllIdLeagues(self):
        conn   = await self.db.getSupabase()
        result = conn.table('leagues').select('id').eq('active', 1).order("id", desc=True).execute()

        return result.data

    # get active leagues - current year
    async def getCurrentLeagues(self):
        conn   = await self.db.getSupabase()
        result = conn.table('leagues').select('id, name, isLegacy, current, year').eq('active', 1).eq('current', 1).order("id", desc=True).execute()

        return result.data
    
    # get past leagues - other years
    async def getPastLeagues(self):
        conn   = await self.db.getSupabase()
        result = conn.table('leagues').select('id, name, isLegacy, current, year').eq('active', 1).eq('current', 0).order("year", desc=True).execute()

        return result.data
    
    # get league info
    async def getLeagueData(self, id):
        conn   = await self.db.getSupabase()
        result = conn.table('leagues').select('id, name, isLegacy, current, year').eq('id', str(id)).execute()

        return result.data[0]
    
    # get league tournaments list
    async def getLeagueTournaments(self, id):
        conn   = await self.db.getSupabase()
        result = conn.table('tournaments').select('id, name, date, idLeague, players, leagues(isLegacy)').eq('idLeague', str(id)).order('datetime', desc=True).execute()
        
        # data conversion - compatibillity with mysql old results
        values = []
        for i in result.data:
            item = {
                'id'       : i['id'], 
                'name'     : i['name'], 
                'date'     : i['date'], 
                'idLeague' : i['idLeague'], 
                'players'  : i['players'], 
                'format'   : i['leagues']['isLegacy']
            }
            values.append(item)

        return values
    
    # get league top cards stats
    async def getTopLeagueCards(self, idLeague, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idLeague)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').in_('idDeck', idDecks).order('name', desc=False).execute()

        return self.groupAndReorderData(result.data, limit)
    
    # league card stats by card type
    async def getTopLeagueCardSingleType(self, idLeague, cardType, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idLeague)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').eq('cardType', cardType).in_('idDeck', idDecks).order('name', desc=False).execute()

        return self.groupAndReorderData(result.data, limit)
    
    # league card stats by board type
    async def getLeagueCardsByBoard(self, idLeague, boardType, limit):
        conn    = await self.db.getSupabase()
        idDecks = self.getIdDecks(conn, idLeague)

        # python needs other query to solve 2 joins
        result = conn.table('cards').select('num, name, imgUrl').eq('board', boardType).in_('idDeck', idDecks).order('name', desc=False).execute()

        return self.groupAndReorderData(result.data, limit)
    
    # get league player stats
    async def getLeaguePlayers(self, idLeague, limit):
        conn          = await self.db.getSupabase()
        idTournaments = self.getIdTournaments(conn, idLeague)

        # python needs other query to solve 2 joins
        result = conn.table('players').select('name').in_('idTournament', idTournaments).execute()

        # count and group items
        allResults = []
        for i in result.data:
            allResults.append(i['name'])

        res = [[x,allResults.count(x)] for x in set(allResults)]
        finalResult = []
        for i in res:
            item = {
                "name" : i[0],
                "num"  : i[1]
            }
            finalResult.append(item)

        values = sorted(finalResult, key=lambda x: (x['num'], x['name']))
        reverse = values[::-1]
        result  = reverse[0:limit]

        return result
    
    # get tournament idDecks
    def getIdDecks(self, conn, idLeague):
        result = conn.table('players').select('idDeck, tournaments()').eq('tournaments.idLeague', str(idLeague)).execute()

        idDecks = []
        for i in result.data:
            idDecks.append(i['idDeck'])

        return idDecks
    
    def getIdTournaments(self, conn, idLeague):
        result = conn.table('tournaments').select('id').eq('idLeague', int(idLeague)).execute()

        idTournaments = []
        for i in result.data:
            idTournaments.append(i['id'])

        return idTournaments

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
                "name" : item,
                "num"  : total,
                "imgUrl" : img
            }

            finalResult.append(item)

        values = sorted(finalResult, key=lambda x: (x['num'], x['name']))
        reverse = values[::-1]
        result  = reverse[0:limit]

        return result
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()


class Db:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.url = os.environ.get('SUPABASE_URL')
        self.key = os.environ.get('SUPABASE_KEY')
        self.supabase = create_client(self.url, self.key)
        self._initialized = True

    async def getSupabase(self):
        return self.supabase

    # select query
    def getTableDataQuery(self, table, options):
        response = self.supabase.table(table).select(options).execute()
        return response.data

    # select with where condition
    def getTableDataQueryWhere(self, table, options, whereKey, whereValue):
        response = self.supabase.table(table).select(options).eq(whereKey, whereValue).execute()
        return response.data

    # insert query
    def insert(self, table, query):
        try:
            return self.supabase.table(table).insert(query).execute()
        except Exception as error:
            return str(error)

    # update query
    def update(self, table, query, conditionKey, conditionValue):
        return self.supabase.table(table).update(query).eq(conditionKey, conditionValue).execute()

    # delete query
    def delete(self, table, conditionKey, conditionValue):
        self.supabase.table(table).delete().eq(conditionKey, conditionValue).execute()

import mysql.connector
from mysql.connector import Error

class Db:

    def __init__(self):
        self.hostName     = 'app-database'
        self.portName     = '3308'
        self.databaseName = 'app-database'
        self.userName     = 'user'
        self.passwordText = 'password'

    def connect(self):
        try:
            return mysql.connector.connect(
                host     = self.hostName,
                user     = self.userName,
                password = self.passwordText,
                database = self.databaseName
            )   
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
    
    def getSelectListResultQuery(self, conn, query):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()

            return result
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
    
    def getSelectSingleResultQuery(self, conn, query):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            return result
        except Error as e:
            print("Error while connecting to MySQL %s" %e)
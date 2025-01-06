import pymysql.cursors
import os
class Db:

    def __init__(self):
        self.hostName     = os.getenv('HOSTNAME')
        self.portName     = os.getenv('PORT')
        self.databaseName = os.getenv('DATABASE')
        self.userName     = os.getenv('USER')
        self.passwordText = os.getenv('PASSWORD')

    def connect(self):
        try:
            return pymysql.connect(
                host        = self.hostName,
                user        = self.userName,
                password    = self.passwordText,
                database    = self.databaseName,
                cursorclass = pymysql.cursors.DictCursor
            )   
        except Exception as e:
            print("Error while connecting to MySQL %s" %e)
    
    def getSelectListResultQuery(self, conn, query):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()

            return result
        except Exception as e:
            print("Error while connecting to MySQL %s" %e)
    
    def getSelectSingleResultQuery(self, conn, query):
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            return result
        except Exception as e:
            print("Error while connecting to MySQL %s" %e)
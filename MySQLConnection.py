import mysql.connector

"""Change MySQL information"""

class Connection():
    def __init__(self):
        self.connection = None
        self.cursor = None

    def ConnectToMySQL(self, db:str):
        connection = mysql.connector.connect(
        host='localhost',
        database = db,
        user ='root',
        password='CHANGEME')
        self.connection = connection

        return self.connection
    
    def MakeCursor(self):
        self.cursor = self.connection.cursor(dictionary=True)
        return self.cursor
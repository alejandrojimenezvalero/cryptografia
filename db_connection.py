import os
import mysql.connector


class dbConnection():

    def __init__(self):
        password = os.getenv('MYSQL_PASSWORD')
        con = mysql.connector.connect(
            host="sql11.freesqldatabase.com",
            user="sql11653150",
            password=password,
            database="sql11653150"
        )
        self.con = con


    def closeConnection(self):
        self.con.close()


    def insertUser(self, data):
        cursor = self.con.cursor()
        consult = "INSERT INTO User (Name, Second_Name, Email, Password) VALUES (%s, %s, %s, %s)"
        cursor.execute(consult, data)
        self.con.commit()


    def insertForum(self, data):
        cursor = self.con.cursor()
        consult = "INSERT INTO Forums (Name, Password) VALUES (%s, %s)"
        cursor.execute(consult, data)
        self.con.commit()


    def insertMsg(self, data):
        cursor = self.con.cursor()
        consult = "INSERT INTO Messages (Data, id_user, id_forum) VALUES (%s, %s, %s)"
        cursor.execute(consult, data)
        self.con.commit()

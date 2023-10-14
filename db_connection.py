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

    def findUser(self, email):
        cursor = self.con.cursor()
        query = "SELECT * FROM User WHERE Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
    def findPassword(self, email):
        cursor = self.con.cursor()
        query = "SELECT Password FROM User WHERE Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def findForum(self, forum_name):
        cursor = self.con.cursor()
        query = "SELECT * FROM Forums WHERE Name = %s"
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def showForums(self, email):
        mycursor = self.con.cursor()

        forum_list = []

        # We get the id from the user
        mycursor.execute("SELECT id_user FROM User WHERE Email = %s", (email,))
        id_user = mycursor.fetchone()

        # Verify if the user exists
        if id_user:
            # We get the id's of the forums the user has access to
            mycursor.execute("SELECT id_forum FROM UsersForums WHERE id_user = %s", (id_user[0],))
            id_forums = mycursor.fetchall()

            if id_forums:
                # We get the forums names
                for forum_id in id_forums:
                    mycursor.execute("SELECT Name FROM Forums WHERE id_forum = %s", (forum_id[0],))
                    forum_name = mycursor.fetchone()
                    if forum_name:
                        print(f"Forum name: {forum_name[0]}")
                        forum_list.append(forum_name)
            else:
                print("You don\'t belong to any forum")
                return 0
        else:
            print(f"There's no id associated to the email: {email}.")
            return 0

        return forum_list

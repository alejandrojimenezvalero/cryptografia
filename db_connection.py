import os
import mysql.connector
import sqlite3


class dbConnection():

    def __init__(self, option):
        # We add this self.option parameter because some querys have differences between qlite3 and mysql-connector
        self.option = option
        if self.option == 'localhost':
            self.con = sqlite3.connect('local_database.db', check_same_thread=False)
        elif self.option == 'online':

            password = os.getenv('MYSQL_PASSWORD')
            self.con = mysql.connector.connect(
                host="sql11.freesqldatabase.com",
                user="sql11653150",
                password=password,
                database="sql11653150"
            )

    def selectQuery(self, query):
        if self.option == 'localhost':
            return query.replace('@', '?')
        elif self.option == 'online':
            return query.replace('@', '%s')


    def closeConnection(self):
        """We close connection with the database"""
        self.con.close()
        return 0

    def update0(self, mutex):
        """This function is used to update in certain contexts of the execution"""
        mutex.acquire()
        try:
            self.con.commit()
        finally:
            mutex.release()
        return 0

    def insertUser(self, data):
        """We insert a user in the database"""
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO User (Name, Second_Name, Email, Password, Salt) VALUES (@, @, @, @, @)")
            cursor.execute(query, data)
            self.con.commit()
            return 0
        except:
            print("The length of your name, second name or email exceed the maximum length allowed")
            return -1


    def insertForum(self, data, email):
        """We insert a Forum in the database"""
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO Forums (Name, Password, Salt) VALUES (@, @, @)")
            cursor.execute(query, data)
            self.con.commit()
            self.joinUserForum(email, data[0])
            return 0
        except:
            print("The length of the name, password exceed the maximum length allowed")
            return -1


    def insertMessage(self, data, mutex):
        """We insert the message a user sent to a forum"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO Messages (Message, id_user, id_forum) VALUES (@, @, @)")
            cursor.execute(query, data)
            self.con.commit()
        finally:
            mutex.release()
        return 0

    def joinUserForum(self, email, forum_name):
        """We add the relationship User-Forum"""

        cursor = self.con.cursor()
        cursor.execute(self.selectQuery("SELECT id_user FROM User WHERE Email = @"), (email,))
        id_user = cursor.fetchone()[0]

        cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
        id_forum = cursor.fetchone()[0]

        query = self.selectQuery("INSERT INTO UsersForums (id_user, id_forum) VALUES (@, @)")
        data = [id_user, id_forum]
        cursor.execute(query, data)

        self.con.commit()
        return 0

    def fetchUser(self, email):
        """We check if a user exists or not"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT * FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def fetchPasswordUser(self, email):
        """We fetch the password of the user"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Password FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None
    def fetchUserSalt(self, email):
        """We fetch the password's salt of the user"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Salt FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchForum(self, forum_name):
        """We fetch if a forum exists or not"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT * FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def fetchPasswordForum(self, forum_name):
        """We fetch the password of the forum"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Password FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchForumSalt(self, forum_name ):
        """We fetch the password' salt of the forum"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Salt FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None
    def showForums(self, email):
        """We show all the forums the user has access to"""
        cursor = self.con.cursor()

        forum_list = []

        # We get the id from the user
        cursor.execute(self.selectQuery("SELECT id_user FROM User WHERE Email = @"), (email,))
        id_user = cursor.fetchone()

        # Verify if the user exists
        if id_user:
            # We get the id's of the forums the user has access to
            cursor.execute(self.selectQuery("SELECT id_forum FROM UsersForums WHERE id_user = @"), (id_user[0],))
            id_forums = cursor.fetchall()

            if id_forums:
                # We get the forums names
                for forum_id in id_forums:
                    cursor.execute(self.selectQuery("SELECT Name FROM Forums WHERE id_forum = @"), (forum_id[0],))
                    forum_name = cursor.fetchone()[0]
                    if forum_name:
                        print(f"Forum name: {forum_name}")
                        forum_list.append(forum_name)
            else:
                print("You don\'t belong to any forum")
        else:
            print(f"There's no id associated to the email: {email}.")
            return 0

        return forum_list

    def showMessages(self, forum_name, mutex):
        """We get all the messages of the forum and who wrote them"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()

            cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
            forum_id = cursor.fetchone()[0]

            # We get the name and second name of the user who wrote the message
            query = self.selectQuery("SELECT m.Message, u.Name, u.Second_Name "
                                     "FROM Messages m "
                                     "JOIN User u ON m.id_user = u.id_user "
                                     "WHERE m.id_forum = @")
            cursor.execute(query, (forum_id,))
            result = cursor.fetchall()
        finally:
            mutex.release()

        return result

    def consultIdUser(self, email, mutex):
        mutex.acquire()
        try:
            cursor = self.con.cursor()
            cursor.execute(self.selectQuery("SELECT id_user FROM User WHERE Email = @"), (email,))
            user_id = cursor.fetchone()[0]
        finally:
            mutex.release()

        return user_id

    def consultIdForum(self, forum_name, mutex):
        mutex.acquire()
        try:
            cursor = self.con.cursor()

            cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
            forum_id = cursor.fetchone()[0]
        finally:
            mutex.release()

        return forum_id
"""
def fetch_data(self, table, condition_column, condition_value):
    "Función genérica para recuperar datos de la base de datos"
    cursor = self.con.cursor()
    query = f"SELECT * FROM {table} WHERE {condition_column} = @"
    cursor.execute(query, (condition_value,))
    result = cursor.fetchall()
    if len(result) > 0:
        return result[0][0] if result[0][0] else True
    else:
        return None

def fetchUser(self, email):
    "Comprobamos si existe un usuario o no"
    return self.fetch_data("User", "Email", email)

def fetchPasswordUser(self, email):
    "Recuperamos la contraseña del usuario"
    return self.fetch_data("User", "Email", email)

def fetchForum(self, forum_name):
    "Comprobamos si existe un foro o no"
    return self.fetch_data("Forums", "Name", forum_name)

def fetchPasswordForum(self, forum_name):
    "Recuperamos la contraseña del foro"
    return self.fetch_data("Forums", "Name", forum_name)
"""
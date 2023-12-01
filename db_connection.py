"""
This module manages the establishment of a connection with the database
It handles the configuration, connection, and all interactions with the database, along with other related operations
"""
import os
import mysql.connector
import sqlite3


class dbConnection():
    """This class establishes the connection with the database and manages all the operations related to it"""

    def __init__(self, option):
        # We add this self.option parameter because some query's have differences between sqlite3 and mysql-connector
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
        """This function selects the correct syntax of the query depending on the chosen option"""
        if self.option == 'localhost':
            return query.replace('@', '?')
        elif self.option == 'online':
            return query.replace('@', '%s')


    def closeConnection(self):
        """This function closes connection with the database"""
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
        """This function inserts a user in the database"""
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO User (Name, Second_Name, Email, Password, Private_key, Salt) VALUES (@, @, @, @, @, @)")
            cursor.execute(query, data)
            self.con.commit()
            return 0
        except:
            print("The length of your name, second name or email exceed the maximum length allowed")
            return -1

    def insertForum(self, data):
        """This function inserts a Forum in the database"""
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO Forums (Name, Password, Salt) VALUES (@, @, @)")
            cursor.execute(query, data)
            self.con.commit()
            return 0
        except:
            print("The length of the name, password exceed the maximum length allowed")
            return -1

    def insertMessage(self, data, mutex):
        """This function inserts the message a user sent to a forum"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()
            query = self.selectQuery("INSERT INTO Messages (Message, id_user, id_forum, Salt) VALUES (@, @, @, @)")
            cursor.execute(query, data)
            self.con.commit()
        except:
            print("Message exceeds app capacity")
        finally:
            mutex.release()
        return 0

    def joinUserForum(self, email, forum_name, role):
        """This function adds the relationship User-Forum"""

        cursor = self.con.cursor()
        cursor.execute(self.selectQuery("SELECT id_user FROM User WHERE Email = @"), (email,))
        id_user = cursor.fetchone()[0]

        cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
        id_forum = cursor.fetchone()[0]

        cursor.execute(self.selectQuery("SELECT id FROM Roles WHERE role = @"), (role,))
        id_role = cursor.fetchone()[0]

        query = self.selectQuery("INSERT INTO UsersForums (id_user, id_forum, id_role) VALUES (@, @, @)")
        data = [id_user, id_forum, id_role]
        cursor.execute(query, data)

        self.con.commit()
        return 0

    def fetchUserId(self, email):
        """This function checks if a user exists or not"""
        query = self.selectQuery("SELECT id_user FROM User WHERE Email = @")
        try:
            cursor = self.con.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                return result[0]
        except Exception as e:
            print(f"Error getting user ID by email: {e}")

        return None

    def fetchUserNameAndSecondName(self, email):
        """Esta función obtiene el nombre y el segundo nombre de un usuario dado su correo electrónico."""
        query = self.selectQuery("SELECT Name, Second_name FROM User WHERE Email = @")
        try:
            cursor = self.con.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                return result  # Retorna una tupla (Name, Second_name)
        except Exception as e:
            print(f"Error obteniendo el nombre y segundo nombre del usuario por correo electrónico: {e}")

        return None

    def fetchForumId(self, forum_name):
        query = self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @")

        try:
            cursor = self.con.cursor()
            cursor.execute(query, (forum_name,))
            result = cursor.fetchone()

            if result:
                return result[0]
        except Exception as e:
            print(f"Error getting forum ID by name: {e}")

        return None

    def fetchPasswordUser(self, email):
        """This function fetchs the password of the user"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Password FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchPrivateKeyUser(self, email):
        """This function fetchs the password of the user"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Private_key FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchPublicKey(self, user_to_fetch_id):
        try:
            # Conectar a la base de datos
            cursor = self.con.cursor()
            query = self.selectQuery("SELECT public_key_pem_text FROM PublicKeys WHERE id_user = @")
            # Consultar la clave pública del usuario en base a su ID
            cursor.execute(query, (user_to_fetch_id,))
            result = cursor.fetchone()

            if result:
                # Obtener la representación PEM de la clave pública
                return result[0]
            else:
                print(f"No se encontró la clave pública para el usuario con ID {user_to_fetch_id}")
                return None
        except Exception as e:
            print(f"Error al recuperar la clave pública: {e}")
            return None

    def fetchUserSalt(self, email):
        """This function fetchs the password's salt of the user"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Salt FROM User WHERE Email = @")
        cursor.execute(query, (email,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchForumExists(self, forum_name):
        """This function fetchs if a forum exists or not"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT * FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def fetchPasswordForum(self, forum_name):
        """This function fetches the password of the forum"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Password FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchForumSalt(self, forum_name ):
        """This function fetches the password's salt of the forum"""
        cursor = self.con.cursor()
        query = self.selectQuery("SELECT Salt FROM Forums WHERE Name = @")
        cursor.execute(query, (forum_name,))
        result = cursor.fetchall()[0][0]
        if len(result) > 0:
            return result
        else:
            return None

    def fetchRole(self, id_user, id_forum):
        cursor = self.con.cursor()

        # Consulta para obtener el nombre del rol
        cursor.execute(self.selectQuery('''SELECT Roles.role FROM UsersForums 
                                            JOIN Roles ON UsersForums.id_role = Roles.id 
                                            WHERE UsersForums.id_user = @ AND UsersForums.id_forum = @'''),
                       (id_user, id_forum,))
        role_name = cursor.fetchone()

        return role_name[0] if role_name[0] else None

    def fetchInvitations(self, id_user):
        query = self.selectQuery('''
            SELECT Forums.Name , Invitations.Message_invitation, Invitations.Signature, Invitations.id_sender
            FROM Invitations
            JOIN Forums ON Invitations.id_forum_origin = Forums.id_forum
            JOIN User ON Invitations.id_user_destination = User.id_user
            WHERE Invitations.id_user_destination = @''')

        try:
            cursor = self.con.cursor()
            cursor.execute(query, (id_user,))
            invitations = cursor.fetchall()
            return invitations
        except Exception as e:
            print(f"Error fetching invitations: {e}")
            return None

    def sendInvitation(self, message, signature, user_destination_email, forum_origin_name, id_sender):
        # Get user id from users name
        user_destination_id = self.fetchUserId(user_destination_email)

        if user_destination_id is None:
            print("Error: User destination not found.")
            return

        # Get forum id form forums name
        forum_origin_id = self.fetchForumId(forum_origin_name)

        if forum_origin_id is None:
            print("Error: Forum origin not found.")
            return

        query = self.selectQuery("INSERT INTO Invitations (Message_invitation, Signature, id_user_destination, id_forum_origin, id_sender) VALUES (@, @, @, @, @)")
        values = (message, signature, user_destination_id, forum_origin_id, id_sender)

        try:
            cursor = self.con.cursor()
            cursor.execute(query, values)
            self.con.commit()
            print("Invitation sent successfully.")
        except Exception as e:
            print(f"Error sending invitation: {e}")

    def deleteInvitation(self, id_user, forum_name):
        # Obtener el ID del foro a partir del nombre del foro
        forum_id = self.fetchForumId(forum_name)

        if forum_id is None:
            print("Error: Forum not found.")
            return

        # Eliminar la invitación en la tabla Invitations
        query = self.selectQuery("DELETE FROM Invitations WHERE id_user_destination = ? AND id_forum_origin = @")
        values = (id_user, forum_id)

        try:
            cursor = self.con.cursor()
            cursor.execute(query, values)
            self.con.commit()
            print("Invitation deleted successfully.")
        except Exception as e:
            print(f"Error deleting invitation: {e}")

    def showForums(self, email):
        """This function shows all the forums the user has access to and the role he has"""
        cursor = self.con.cursor()

        forum_list = []
        forum_list_admin = []

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
                    role = self.fetchRole(id_user[0], forum_id[0])
                    if forum_name:
                        print(f"Forum name: {forum_name} (Role: {role})")
                        forum_list.append(forum_id[0])
                        if role == "admin":
                            forum_list_admin.append(forum_name)
            else:
                print("You don\'t belong to any forum")
        else:
            print(f"There's no id associated to the email: {email}.")
            return 0

        return forum_list, forum_list_admin

    def showMessages(self, forum_name, mutex):
        """This function gets all the messages of the forum and who wrote them"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()

            cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
            forum_id = cursor.fetchone()[0]

            # We get the name and second name of the user who wrote the message
            query = self.selectQuery("SELECT m.id_message, m.Message, m.Salt, u.Name, u.Second_Name "
                                     "FROM Messages m "
                                     "JOIN User u ON m.id_user = u.id_user "
                                     "WHERE m.id_forum = @")
            cursor.execute(query, (forum_id,))
            result = cursor.fetchall()
        finally:
            mutex.release()

        return result

    def consultIdUser(self, email, mutex):
        """This function consults the id of a user"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()
            cursor.execute(self.selectQuery("SELECT id_user FROM User WHERE Email = @"), (email,))
            user_id = cursor.fetchone()[0]
        finally:
            mutex.release()

        return user_id

    def consultIdForum(self, forum_name, mutex):
        """This function consults the id of a forum"""
        mutex.acquire()
        try:
            cursor = self.con.cursor()

            cursor.execute(self.selectQuery("SELECT id_forum FROM Forums WHERE Name = @"), (forum_name,))
            forum_id = cursor.fetchone()[0]
        finally:
            mutex.release()

        return forum_id

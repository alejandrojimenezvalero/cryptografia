"""This module handles the creation of the database and necessary tables"""
import sqlite3

def create_tables():
    con = sqlite3.connect('local_database.db')
    cursor = con.cursor()

    cursor.execute('DROP TABLE IF EXISTS User')
    cursor.execute('DROP TABLE IF EXISTS Forums')
    cursor.execute('DROP TABLE IF EXISTS Roles')
    cursor.execute('DROP TABLE IF EXISTS UsersForums')
    cursor.execute('DROP TABLE IF EXISTS Invitations')
    cursor.execute('DROP TABLE IF EXISTS Messages')
    cursor.execute('DROP TABLE IF EXISTS PublicKeys')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL CHECK(LENGTH(Name) <= 15),
            Second_Name TEXT CHECK(LENGTH(Second_Name) <= 15),
            Email TEXT UNIQUE CHECK(LENGTH(Second_Name) <= 30),
            Password TEXT CHECK(LENGTH(Password) <= 100),
            Private_key TEXT,
            Salt TEXT CHECK(LENGTH(Salt) <= 24)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Forums (
            id_forum INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL UNIQUE CHECK(LENGTH(Name) <= 15),
            Password TEXT CHECK(LENGTH(Password) <= 100),
            Salt TEXT CHECK(LENGTH(Salt) <= 24)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Roles (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO Roles (role) VALUES (?)
    ''', [('admin',), ('user',)])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UsersForums (
            id_user INTEGER,
            id_forum INTEGER,
            id_role INTEGER,
            FOREIGN KEY (id_user) REFERENCES User(id_user) ON DELETE CASCADE,
            FOREIGN KEY (id_forum) REFERENCES Forums(id_forum) ON DELETE CASCADE,
            FOREIGN KEY (id_role) REFERENCES Roles(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Invitations (
            id_message INTEGER PRIMARY KEY AUTOINCREMENT,
            Message_invitation TEXT NOT NULL,
            Signature TEXT,
            id_user_destination INTEGER,
            id_sender INTEGER,
            id_forum_origin INTEGER,
            FOREIGN KEY (id_user_destination) REFERENCES User(id_user) ON DELETE SET NULL,
            FOREIGN KEY (id_sender) REFERENCES User(id_user) ON DELETE SET NULL,
            FOREIGN KEY (id_forum_origin) REFERENCES Forums(id_forum) ON DELETE CASCADE,
            UNIQUE (id_user_destination, id_forum_origin)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Messages (
            id_message INTEGER PRIMARY KEY AUTOINCREMENT,
            Message TEXT CHECK(LENGTH(Message) <= 200) NOT NULL,
            id_user INTEGER,
            id_forum INTEGER,
            Salt TEXT CHECK(LENGTH(Salt) <= 24),
            FOREIGN KEY (id_user) REFERENCES User(id_user) ON DELETE SET NULL,
            FOREIGN KEY (id_forum) REFERENCES Forums(id_forum) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PublicKeys (
            id_user INTEGER PRIMARY KEY,
            public_key_pem_text TEXT,
            FOREIGN KEY (id_user) REFERENCES User(id_user)
        )
    ''')

    con.commit()
    con.close()

def insert_data():
    con = sqlite3.connect('local_database.db')
    cursor = con.cursor()

    # Insert data into User table
    cursor.execute('INSERT INTO User (Name, Email, Password, Salt) VALUES (?, ?, ?, ?)',
                   ('John Doe', 'john@example.com', 'hashed_password', 'salt123'))

    # Insert data into Forums table
    cursor.execute('INSERT INTO Forums (Name, Password, Salt) VALUES (?, ?, ?)',
                   ('Discussion', 'forum_password', 'salt456'))

    # Insert data into UsersForums table
    cursor.execute('INSERT INTO UsersForums (id_user, id_forum, id_role) VALUES (?, ?, ?)',
                   (1, 1, 2))  # Assuming 'user' role has id 2 and 'admin' role has id 1

    # Insert data into Messages table
    cursor.execute('INSERT INTO Messages (Message, id_user, id_forum, Salt) VALUES (?, ?, ?, ?)',
                   ('Hello, world!', 1, 1, 'salt789'))

    con.commit()
    con.close()

def fetch_data():
    con = sqlite3.connect('local_database.db')
    cursor = con.cursor()

    # Retrieve data from User table
    cursor.execute('SELECT * FROM User')
    users = cursor.fetchall()
    print("Users:")
    print(users)

    # Retrieve data from Forums table
    cursor.execute('SELECT * FROM Forums')
    forums = cursor.fetchall()
    print("\nForums:")
    print(forums)

    # Retrieve data from Roles table
    cursor.execute('SELECT * FROM Roles')
    users_forums = cursor.fetchall()
    print("\nRoles:")
    print(users_forums)

    # Retrieve data from UsersForums table
    cursor.execute('SELECT * FROM UsersForums')
    users_forums = cursor.fetchall()
    print("\nUsersForums:")
    print(users_forums)

    # Retrieve data from Invitations table
    cursor.execute('SELECT * FROM Invitations')
    users_forums = cursor.fetchall()
    print("\nInvitations:")
    print(users_forums)

    # Retrieve data from Messages table
    cursor.execute('SELECT * FROM Messages')
    messages = cursor.fetchall()
    print("\nMessages:")
    print(messages)

    cursor.execute('SELECT * FROM PublicKeys')
    messages = cursor.fetchall()
    print("\nPublicKeys:")
    print(messages)

    con.close()

if __name__ == "__main__":
    create_tables()
    #insert_data()
    fetch_data()

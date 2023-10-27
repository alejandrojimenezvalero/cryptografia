"""This module handles the creation of the database and necessary tables"""
import sqlite3

con = sqlite3.connect('local_database.db')

cursor = con.cursor()

cursor.execute('DROP TABLE IF EXISTS User')
cursor.execute('DROP TABLE IF EXISTS Forums')
cursor.execute('DROP TABLE IF EXISTS UsersForums')
cursor.execute('DROP TABLE IF EXISTS Messages')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL CHECK(LENGTH(Name) <= 15),
        Second_Name TEXT CHECK(LENGTH(Second_Name) <= 15),
        Email TEXT UNIQUE CHECK(LENGTH(Second_Name) <= 30),
        Password TEXT CHECK(LENGTH(Password) <= 100),
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
    CREATE TABLE IF NOT EXISTS UsersForums (
        id_user INTEGER,
        id_forum INTEGER,
        FOREIGN KEY (id_user) REFERENCES User(id_user) ON DELETE CASCADE,
        FOREIGN KEY (id_forum) REFERENCES Forum(id_forum) ON DELETE CASCADE
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
        FOREIGN KEY (id_forum) REFERENCES Forum(id_forum) ON DELETE CASCADE
    )
''')

con.commit()

con.close()

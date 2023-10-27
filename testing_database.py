"""This module conducts testing procedures for the database functionality"""
import sqlite3

con = sqlite3.connect('local_database.db')

cursor = con.cursor()
cursor.execute("SELECT * FROM User")
rows = cursor.fetchall()
print('------------User Table-------------')
# Imprimir los resultados por pantalla
for row in rows:
    print(row)
print('-----------------------------------')

cursor.execute("SELECT * FROM Forums")
rows = cursor.fetchall()
print('------------Forum Table------------')
# Imprimir los resultados por pantalla
for row in rows:
    print(row)
print('-----------------------------------')

cursor.execute("SELECT * FROM UsersForums")
rows = cursor.fetchall()
print('---------UsersForums Table----------')
# Imprimir los resultados por pantalla
for row in rows:
    print(row)
print('-----------------------------------')

cursor.execute("SELECT * FROM Messages")
rows = cursor.fetchall()
print('----------Messages Table-----------')
# Imprimir los resultados por pantalla
for row in rows:
    print(row)
print('-----------------------------------')


con.close()

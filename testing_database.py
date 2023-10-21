import sqlite3

con = sqlite3.connect('local_database.db')

cursor = con.cursor()
"""
data = ['Edu', 'Al', 'AMDK', 'sadnas']
data2= ['Edu', 'Al', 'AMDKdsad', 'sadnas']
consult = "INSERT INTO User (Name, Second_Name, Email, Password) VALUES (?, ?, ?, ?)"
cursor.execute(consult, data)
cursor.execute(consult, data2)
"""
cursor.execute("SELECT * FROM User")
filas = cursor.fetchall()

# Imprimir los resultados por pantalla
for fila in filas:
    print(fila)


con.close()
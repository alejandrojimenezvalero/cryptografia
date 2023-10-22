import keyboard
import sqlite3

# Conectarse a la base de datos
conn = sqlite3.connect('local_database.db')
cursor = conn.cursor()

# Seleccionar todas las filas de la tabla User
cursor.execute("SELECT * FROM Messages")
rows = cursor.fetchall()

# Imprimir todas las filas
for row in rows:
    print(row)

# Cerrar la conexión
conn.close()


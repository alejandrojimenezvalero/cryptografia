from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os
import sqlite3

# Función para insertar la clave pública en la base de datos
def insert_public_key_to_database(user_id, public_key_pem, database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Comprobar si ya existe una clave pública para el usuario
    cursor.execute('SELECT id_user FROM PublicKeys WHERE id_user = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        print(f"Ya existe una clave pública para el usuario con ID {user_id}")
    else:
        # Insertar la clave pública en la tabla PublicKeys
        cursor.execute('''
                    INSERT INTO PublicKeys (id_user, public_key_pem_text)
                    VALUES (?, ?)
                ''', (user_id, public_key_pem))

        print(f"Clave pública insertada para el usuario con ID {user_id}")

    # Guardar los cambios y cerrar la conexión
    connection.commit()
    connection.close()

# Ruta de los certificados
certs_folder = 'AC1/nuevoscerts'
database_path = 'local_database.db'

# Iterar sobre los archivos en la carpeta de certificados
for cert_filename in os.listdir(certs_folder):
    cert_path = os.path.join(certs_folder, cert_filename)

    # Abrir el certificado en modo binario y leer su contenido
    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()

    try:
        # Analizar el certificado
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # Obtener el ID del usuario desde el certificado
        user_id = int(cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value)

        # Obtener la clave pública en formato PEM
        public_key_pem = cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # Insertar la clave pública en la base de datos
        insert_public_key_to_database(user_id, public_key_pem, database_path)

    except Exception as e:
        print(f"Error al procesar el certificado {cert_filename}: {e}")

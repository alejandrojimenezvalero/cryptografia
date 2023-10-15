from cryptography.fernet import Fernet
import hmac
import hashlib

def initialize_password():
    key = b'GX0wOFAFYIohW8EIKfIyc0c4w-NMQg5nT2cDqr7zeHk='
    cipher_suite = Fernet(key)
    return cipher_suite


def password_encryption(password):
    # we generate the key
    # we create out a Fernet object
    cipher_suite = initialize_password()
    # to convert plain text to cipher text
    encrypted_pass = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_pass


def password_decryption(encrypted_value):
    cipher_suite = initialize_password()
    decrypted_value = cipher_suite.decrypt(encrypted_value).decode()
    return decrypted_value


def initialize_msg(message):
    # Generar una clave secreta aleatoria de 32 bytes (256 bits)
    key = b"0y\xb8\x811r\xa4U\xadv\xa1\xf8\x08HL\x87\xbb\x93g\xddY\xe5\x14\xcfZ'\x06\x0c\xd7\x14\xa8E"
    encoded_message = message.encode()
    return key, encoded_message


def encrypt_message(message):
    """We use this function when we wan to send an authenticated message"""
    k, encoded_message = initialize_msg(message)
    # Crear el HMAC utilizando SHA-256
    hmac_obj = hmac.new(k, digestmod=hashlib.sha256)
    # Actualizar el objeto HMAC con los datos que deseas autenticar
    hmac_obj.update(encoded_message)
    # Obtener el valor HMAC (resumen autenticado): este es el valor que se le pasa
    valor_hmac = hmac_obj.digest()
    return valor_hmac

def decrypt_message(message, valor_hmac):
    """We use this function when we received an authenticated message"""
    k, encoded_message = initialize_msg(message)
    # Crear un objeto HMAC con la clave secreta y SHA-256
    hmac_receptor = hmac.new(k, digestmod=hashlib.sha256)
    # Actualizar el objeto HMAC con los datos recibidos
    hmac_receptor.update(encoded_message)
    # Verificar si el valor HMAC calculado coincide con el valor HMAC recibido
    if hmac.compare_digest(valor_hmac, hmac_receptor.digest()):
        #En este caso el mensaje no ha sido manipulado
        print("Los datos son auténticos e íntegros (la verificación HMAC es exitosa).")
        return 0
    else:
        print("Los datos no son auténticos o no son íntegros (la verificación HMAC falló).")
        return -1

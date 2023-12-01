"""
This module handles encryption and decryption operations using AES and AES-GCM encryption standards
It also manages the validation process for ensuring the consistency of the second password with the first one
"""
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import re


def check_password():
    """This function checks if the password and the confirmation match"""
    while True:
        print('Enter the password (it must contain at least 1 uppercase letter, 1 digit, '
              '1 of the following symbols ($,%,&,@), and be at least 8 characters long:')
        pass1 = input()

        if pass1 == '!exit':
            return -1

        if is_valid_password(pass1):
            while True:
                print('Confirm your password:')
                pass2 = input()
                if pass1 == pass2:
                    return pass1
                else:
                    print('The passwords don\'t match')
        else:
            print("Your password doesn't match the required standards")

def is_valid_password(password):
    """Check if the password meets the required standards"""
    return re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', password)


def initialize_data(key, salt):
    """Initializes data encryption using the provided key and salt."""
    # We use key stretching to prevent brute force attacks
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    k = base64.urlsafe_b64encode(kdf.derive(key))
    cipher_suite = Fernet(k)
    return cipher_suite


def generate_salt():
    """This function generates a random salt"""
    salt = os.urandom(16)
    return salt


def encode_salt(salt):
    """This function encodes the salt"""
    return base64.b64encode(salt).decode('utf-8')


def decode_salt(encoded_salt):
    """This function decodes the salt"""
    return base64.b64decode(encoded_salt.encode())


def data_encryption(data, key, salt):
    """This function encrypts a piece of data using a key and a salt"""
    k = key.encode()
    cipher_suite = initialize_data(k, salt)
    encrypted_data = cipher_suite.encrypt(data.encode()).decode()
    return encrypted_data


def data_decryption(data, key, salt):
    """This function decrypts a piece of data using a key and a salt"""
    # We fetch de password salt
    k = key.encode()
    cipher_suite = initialize_data(k, salt)
    try:
        decrypted_data = cipher_suite.decrypt(data.encode()).decode()
        return decrypted_data
    except:
        return -1


def generate_private_key():
    user_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return user_private_key


def private_key_to_pem(user_private_key):
    private_pem = user_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    return private_pem


def load_private_key_from_pem(pem_bytes, password=None):
    try:
        # Cargar la clave privada desde la representación PEM
        private_key = serialization.load_pem_private_key(
            pem_bytes,
            password=password,
            backend=default_backend()
        )
        return private_key
    except Exception as e:
        print(f"Error al cargar la clave privada desde PEM: {e}")
        return None

def load_public_key_from_pem(recipient_public_key_pem):
    recipient_public_key = serialization.load_pem_public_key(
        recipient_public_key_pem.encode(),
        backend=default_backend()
    )
    return recipient_public_key

def encrypt_and_sign(message, recipient_public_key, sender_private_key):
    """
    Cifra un mensaje con la clave pública del destinatario y firma el mensaje con la clave privada del emisor.

    Parameters:
    - message: Mensaje a cifrar y firmar.
    - recipient_public_key: Clave pública del destinatario.
    - sender_private_key: Clave privada del emisor.

    Returns:
    - ciphertext: Mensaje cifrado y firmado.
    """
    # Cifrar el mensaje con la clave pública del destinatario
    ciphertext = recipient_public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Firmar el mensaje con la clave privada del emisor
    signature = sender_private_key.sign(
        ciphertext,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Combinar el mensaje cifrado y la firma
    print(ciphertext)
    print(type(ciphertext))
    print(signature)
    print(type(signature))

    return ciphertext, signature

def verify_signature_and_decrypt(ciphertext, signature, sender_public_key_pem, recipient_private_key):
    """
    Verifica la firma del mensaje utilizando la clave pública del emisor y descifra el mensaje con la clave privada del destinatario.

    Parameters:
    - ciphertext: Mensaje cifrado y firmado.
    - sender_public_key: Clave pública del emisor.
    - recipient_private_key: Clave privada del destinatario.

    Returns:
    - message: Mensaje descifrado.
    """
    sender_public_key = load_public_key_from_pem(sender_public_key_pem)

    print(ciphertext)
    print(type(ciphertext))
    print(signature)
    print(type(signature))
    print(type(sender_public_key))

    try:
        sender_public_key.verify(
            signature,
            ciphertext,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("La firma es válida.")
    except Exception as e:
        print(f"La firma no es válida: {e}")
        return None

    try:
        decrypted_message = recipient_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()
    except Exception as e:
        print(f"Error al descifrar el mensaje: {e}")
        return None




import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re


def check_password(pass1, pass2):
    while pass1 != pass2:
        print('Enter the password (it must contain at least 1 mayus, 1 digit, '
              '1 of the following symbols ($,%,&,@) :')
        pass1 = input()
        while not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)) and pass1 != '!exit':

            if not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)):
                print("Your password doesn\'t match required standards")
            pass1 = input()

        if pass1 == '!exit':
            return -1

        print('Confirm your password:')
        pass2 = input()
        if pass1 != pass2:
            print('The passwords doesn\'t match')
        else:
            return pass1

def initialize_data(key, salt):
    # We use key stretching to prevent brute force attacks
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    k = base64.urlsafe_b64encode(kdf.derive(key))
    cipher_suite = Fernet(k)
    return cipher_suite

def generate_salt():
    salt = os.urandom(16)
    return salt
def encode_salt(salt):
    return base64.b64encode(salt).decode('utf-8')

def decode_salt(encoded_salt):
    return base64.b64decode(encoded_salt.encode())

def data_encryption(password, key, salt):
    k = key.encode()
    cipher_suite = initialize_data(k, salt)
    encrypted_data = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_data


def data_decryption(encrypted_value, key, salt):
    # We fetch de password salt
    k = key.encode()
    cipher_suite = initialize_data(k, salt)
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_value.encode()).decode()
        return decrypted_data
    except:
        return -1

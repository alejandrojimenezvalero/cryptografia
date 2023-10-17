from cryptography.fernet import Fernet
import hmac
import hashlib
import base64
import re


def check_password(pass1):
    while not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)):

        if not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)):
            print("Your password doesn\'t match required standards")
        pass1 = input()
    return pass1

def initialize_data(key):
    key_32_bytes = hashlib.sha256(key.encode()).digest()
    encoded_key = base64.urlsafe_b64encode(key_32_bytes)
    cipher_suite = Fernet(encoded_key)
    return cipher_suite


def data_encryption(password, key):
    cipher_suite = initialize_data(key)
    encrypted_data = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_data


def data_decryption(encrypted_value, key):
    cipher_suite = initialize_data(key)
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_value.encode()).decode()
        return decrypted_data
    except:
        return -1



def initialize_msg(message, key):
    # We use the password of the Forum as a key to encrypt the message
    key_32_bytes = hashlib.sha256(key.encode()).digest()
    encoded_key = base64.urlsafe_b64encode(key_32_bytes)
    encoded_message = message.encode()
    return encoded_key, encoded_message

def auth_message(message, key, stored_hmac):
    """We use this function when we received an authenticated message"""
    hmac_value = generate_hmac(key, message)
    # Check if the HMAC stored is equal to the HMAC of the actual message in order to see if it has been manipulated
    if hmac.compare_digest(stored_hmac, hmac_value):
        # In this case the message has not been manipulated
        return 0
    else:
        return -1
def generate_hmac(message, key):
    k, encoded_message = initialize_msg(message, key)
    # We create an HMAC with the message
    hmac_receptor = hmac.new(k, digestmod=hashlib.sha256)
    hmac_receptor.update(encoded_message)
    hmac_value = hmac_receptor.digest()
    return hmac_value

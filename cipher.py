from cryptography.fernet import Fernet
import hmac
import hashlib
import base64

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
    decrypted_data = cipher_suite.decrypt(encrypted_value.encode()).decode()
    return decrypted_data


def initialize_msg(message, key):
    # We use the password of the Forum as a key to encrypt the message
    key_32_bytes = hashlib.sha256(key.encode()).digest()
    encoded_key = base64.urlsafe_b64encode(key_32_bytes)
    encoded_message = message.encode()
    return encoded_key, encoded_message


def auth_send_message(message, key):
    """We use this function when we want to send an authenticated message"""
    k, encoded_message = initialize_msg(message, key)
    # We generate HMAC object using sha-226 algorithm
    hmac_obj = hmac.new(k, digestmod=hashlib.sha256)
    # Update to HMAC object with the message as an argument
    hmac_obj.update(encoded_message)
    # We obtain HMAC value
    valor_hmac = hmac_obj.digest()
    # We encrypt the message to storage it ciphered in the database
    return valor_hmac

def auth_received_message(message, stored_hmac):
    """We use this function when we received an authenticated message"""
    k, encoded_message = initialize_msg(message)
    # We create an HMAC with the message
    hmac_receptor = hmac.new(k, digestmod=hashlib.sha256)
    hmac_receptor.update(encoded_message)
    # Check if the HMAC stored is equal to the HMAC of the actual message in order to see if it has been manipulated
    if hmac.compare_digest(stored_hmac, hmac_receptor.digest()):
        # In this case the message has not been manipulated
        return 0
    else:
        print("This message is no longer available, it has been manipulated")
        return -1

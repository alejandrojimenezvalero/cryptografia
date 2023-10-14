from cryptography.fernet import Fernet


def initialize():
    key = b'GX0wOFAFYIohW8EIKfIyc0c4w-NMQg5nT2cDqr7zeHk='
    cipher_suite = Fernet(key)
    return cipher_suite


def password_encryption(password):
    # we generate the key
    # we create out a Fernet object
    cipher_suite = initialize()
    # to convert plain text to cipher text
    encrypted_pass = cipher_suite.encrypt(password.encode()).decode()
    return encrypted_pass


def password_decryption(encrypted_value):
    cipher_suite = initialize()
    decrypted_value = cipher_suite.decrypt(encrypted_value).decode()
    return decrypted_value

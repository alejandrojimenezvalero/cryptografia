"""This module handles the sign-up functionality for the application users"""
import cipher
import re
import time
from certificate_management_users import ManageCertificates


def sign(user):
    """This function manages the sign-up option"""

    print('You are now trying to sign up, if u want exit, please type \'!exit\'')
    time.sleep(1)
    data = None
    print('Name (max 15 chars): ')
    user.name = input()

    print('Second Name (max 15 chars): ')
    user.second_name = input()
    print('Email (max 30 chars): ')
    user.email = input()

    while user.email != '!exit':

        # We check if the email follow the regular expression
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        while not re.match(regex, user.email):
            if not re.match(regex, user.email):
                print('The email doesn\'t follow the required parameters')
                time.sleep(1)
                print('Email:')
            user.email = input()

        # We check if the email is already in use

        if not user.connectionDb.fetchUserId(user.email):

            pass1 = cipher.check_password()

            # We encode the password
            # We are going to use Fernet for symmetric encryption
            if pass1 == -1:
                return -1
            salt = cipher.generate_salt()
            # We generate the private key
            user.private_key = cipher.generate_private_key()
            # We get the pem format of the private key
            pem_private_key = cipher.private_key_to_pem(user.private_key)
            print(pem_private_key)
            # We cipher the pem format
            ciphered_pem_private_key = cipher.data_encryption(pem_private_key, pass1, salt)
            ciphered_password = cipher.data_encryption(pass1, pass1, salt)
            encoded_salt = cipher.encode_salt(salt)
            data = [user.name, user.second_name, user.email, ciphered_password, ciphered_pem_private_key, encoded_salt]
            # We leave the while pass1 != pass2 loop
            # We leave the while True loop
            break
        else:
            print('Sorry that email name is already in use, you should try log in, type !exit to go back')
            time.sleep(1)
            print('Email: ')
        user.email = input()

    if user.email != '!exit':

        res = user.connectionDb.insertUser(data)
        user.id = user.connectionDb.fetchUserId(user.email)
        ManageCertificates(user).generate_certificate_request(user.private_key)
        if res == 0:
            print('Account has been created successfully')
        time.sleep(1)
    user.reset_attributes()
    return -1

"""This module handles the sign-up functionality for the application users"""
import cipher
import re
import time


def sign(user):
    """This function manages the sign-up option"""

    print('You are now trying to sign up, if u want exit, please type \'!exit\'')
    time.sleep(1)
    data = None
    print('Name (max 15 chars): ')
    name = input()

    print('Second Name (max 15 chars): ')
    sec_name = input()
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

        if not user.connectionDb.fetchUser(user.email):
            pass1, pass2 = 0, 1
            pass1 = cipher.check_password(pass1, pass2)

            # We encode the password
            # We are going to use Fernet for symmetric encryption
            if pass1 == -1:
                return -1
            salt = cipher.generate_salt()
            ciphered_password = cipher.data_encryption(pass1, pass1, salt)
            encoded_salt = cipher.encode_salt(salt)
            data = [name, sec_name, user.email, ciphered_password, encoded_salt]
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
        if res == 0:
            print('Account has been created successfully')
        time.sleep(1)
    return -1

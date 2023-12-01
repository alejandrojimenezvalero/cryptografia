"""This module handles the log-in functionality for the application users"""
import time
import forums_menu
import cipher
from certificate_management_users import ManageCertificates


def log(user):
    """This function manages the log-in option"""

    print('You are now trying to log in, if u want exit, please type \'!exit\'')
    time.sleep(1)
    # We add a counter to so that the user can only try the password 3 times
    c = 3
    while user.email != '!exit':
        print('Please enter your email:')
        user.email = input().lower()

        # Check if the email is in the DB and if not tell de user that he has to sign up

        if user.connectionDb.fetchUserId(user.email):
            print('Please enter your password:')
            while c > 0:
                password = input()

                # Check if the password is correct
                salt = cipher.decode_salt(user.connectionDb.fetchUserSalt(user.email))

                db_password = cipher.data_decryption(user.connectionDb.fetchPasswordUser(user.email), password, salt)


                if password == db_password:
                    pem_private_key = cipher.data_decryption(user.connectionDb.fetchPrivateKeyUser(user.email),
                                                              password, salt)
                    user.private_key = cipher.load_private_key_from_pem(pem_private_key.encode())
                    user.id = user.connectionDb.fetchUserId(user.email)
                    user.name, user.second_name = user.connectionDb.fetchUserNameAndSecondName(user.email)
                    if ManageCertificates(user).check_user_is_certified():
                        forums_menu.start(user)
                    user.reset_attributes()
                    return -1
                else:
                    c -= 1
                    print('Wrong password, please try again:')

            print('Sorry you have exhausted your 3 attempts, you are being redirected to the home page')
            # We add 5 seconds of time sleep so the brute force algorithm it's not efficient
            time.sleep(5)
            user.reset_attributes()
            return -1
        else:
            if user.email != '!exit':
                print('User doesn\'t exist')
            time.sleep(1)
            user.reset_attributes()
            return -1

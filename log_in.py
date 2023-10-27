"""This module handles the log-in functionality for the application users"""
import time
import forums_menu
import cipher


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


        if user.connectionDb.fetchUser(user.email):
            print('Please enter your password:')
            while c > 0:
                password = input()

                # Check if the password is correct
                salt = cipher.decode_salt(user.connectionDb.fetchUserSalt(user.email))

                db_password = cipher.data_decryption(user.connectionDb.fetchPasswordUser(user.email), password, salt)

                if password == db_password:
                    forums_menu.start(user)
                    return -1
                else:
                    c -= 1
                    print('Wrong password, please try again:')

            print('Sorry you have exhausted your 3 attempts, you are being redirected to the home page')
            # We add 5 seconds of time sleep so the brute force algorithm it's not efficient
            time.sleep(5)
            return -1
        else:
            if user.email != '!exit':
                print('User doesn\'t exist')
            user.email = None
            time.sleep(1)
            return -1

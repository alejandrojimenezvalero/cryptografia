import time
import forums_menu
import cipher


def log(user):
    print('You are now trying to log in, if u want exit, please type \'!exit\'')
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
                db_password = cipher.data_decryption(user.connectionDb.fetchPasswordUser(user.email), password)

                if password == db_password:
                    forums_menu.start(user)
                    return -1
                else:
                    c -= 1
                    print('Wrong password, please try again:')

            print('Sorry you have exhausted your 3 attempts, you are being redirecting to the home page')
            # We add 5 seconds of time sleep so the brute force algoritm it's not efficient
            time.sleep(5)
            return -1
        else:
            print('User doesn\'t exist')
        return -1

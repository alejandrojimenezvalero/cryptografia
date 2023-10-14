import time
import forums_menu


def log(con):
    print('You are now trying to log in, if u want exit, please type \'!exit\'')
    # We add a counter to so that the user can only try the password 3 times
    c = 3
    email = None
    while email != '!exit':
        print('Please enter your email:')
        email = input().lower()

        # Check if the email is in the DB and if not tell de user that he has to sign up

        if email:
            print('Please enter your password:')
            while c > 0:
                password = input()

                # Check if the password is correct

                if password:
                    forums_menu.start(con, email)
                    return -1
                else:
                    c -= 1
                    print('Wrong password, please try again:')

            print('Sorry you have exhausted your 3 attempts, you are being redirecting to the home page')
            # We add 5 seconds of time sleep so the brute force algoritm it's not efficient
            time.sleep(5)
            return -1
        else:
            print('Please enter your email:')

    return -1

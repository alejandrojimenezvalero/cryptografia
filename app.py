"""This module initializes the application and sets up the necessary components"""
from user_log import User
import log_in
import sign_up
import time
from transitions import print_slow
from display_image import show_notification_with_image

def createApp():
    """This function contains the precise logic for initializing the app"""
    #show_notification_with_image("logo.png", 7)
    try:
        print_slow('Would you like to chat online (temporary unavailable) or localhost?')
        option = input()
        while option != 'localhost':
            if option == 'online':
                print('Sorry the online version is temporary unavailable')
            print_slow('Please, type \'localhost\' or \'online\'')
            option = input()


        print_slow('Welcome to echoSpace, what do you want to do?\n'
              + '1. If you want to Sign Up, please type \'S\'\n'
              + '2. If you want to Log In, please type \'L\'\n'
              + '3. If you want to Exit, please type \'E\'\n')

        # We establish connection with the database
        user = User(option)

        action = input().lower()
        res = None
    except KeyboardInterrupt:
        print('Closing echoSpace')
        time.sleep(3)
        return -1
    try:
        while action != 'e':
            if action == 'l':
                res = log_in.log(user)

            elif action == 's':
                res = sign_up.sign(user)
            else:
                print('Please type \'S\' (sign up), \'L\' (log in) or \'E\' (exit)')

            if res == -1:
                print('-------------------------------')
                print('You have been redirected to the home page')
                print('Please type \'S\' (sign up), \'L\' (log in) or \'E\' (exit)')
            action = input().lower()

        # User wants to exit, and we close the connection with the database
        user.connectionDb.closeConnection()
        return 0

    except KeyboardInterrupt:
        # We close the connection with the database
        user.connectionDb.closeConnection()
        print('Closing echoSpace')
        time.sleep(3)
        return -1

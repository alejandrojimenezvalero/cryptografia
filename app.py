from user_log import User
import log_in
import sign_up

def createApp():

    print('Would you like to chat online (temporary unavailable) or localhost?')
    option = input()
    while option != 'localhost':
        if option == 'online':
            print('Sorry the online version is temporary unavailable')
        print('Please, type \'localhost\' or \'online\'')
        option = input()


    print('Welcome ForumLand, what do you want to do?\n'
          + '1. If you want to Sign Up, please type \'S\'\n'
          + '2. If you want to Log In, please type \'L\'\n'
          + '3. If you want to Exit, please type \'E\'\n')

    # We establish connection with the database
    user = User(option)

    action = input().lower()
    res = None
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
        return -1

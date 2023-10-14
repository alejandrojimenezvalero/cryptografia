from db_connection import dbConnection
import log_in
import sign_up

def createApp():
    print('Welcome ForumLand, what do you want to do?\n'
          + '1. If you want to Sign Up, please type \'S\'\n'
          + '2. If you want to Log In, please type \'L\'\n'
          + '3. If you want to Exit, please type \'E\'\n')

    # We establish connection with the database
    con = dbConnection()

    action = input().lower()
    res = None
    try:
        while action != 'e':
            if action == 'l':
                res = log_in.log(con)

            elif action == 's':
                res = sign_up.sign(con)
            else:
                print('Please type \'S\' (sign up), \'L\' (log in) or \'E\' (exit)')

            if res == -1:
                print('-------------------------------')
                print('You have been redirected to the home page')
                print('Please type \'S\' (sign up), \'L\' (log in) or \'E\' (exit)')
            action = input().lower()

        # User wants to exit, and we close the connection with the database
        con.closeConnection()
        return 0

    except KeyboardInterrupt:
        # We close the connection with the database
        #con.closeConnection()
        return -1

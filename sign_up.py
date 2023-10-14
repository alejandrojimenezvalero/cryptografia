import re


def sign(con):
    print('You are now trying to sign up, if u want exit, please type \'!exit\'')

    print('Name: ')
    name = input()

    print('Second Name: ')
    sec_name = input()

    while True:

        print('Email: ')
        email = input()
        # We check if the email follow the regular expression
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        while not re.match(regex, email):
            email = input()
            if not re.match(regex, email):
                print('The email doesn\'t follow the required parameters')
                print('Email:')

        # We check if the email is already in use

        if not email:
            pass1, pass2 = None, None
            while pass1 != pass2:
                print('Password:')
                pass1 = input()
                print('Repeat your password:')
                pass2 = input()
                if pass1 != pass2:
                    print('The passwords doesn\'t match')
                else:
                    # We encode the password

                    # We leave the while pass1 != pass2 loop
                    break
            # We leave the while True loop
            break
        else:
            print('Sorry that email name is already in use')

    # We create the account
    print('Account has been created successfully')
    return -1

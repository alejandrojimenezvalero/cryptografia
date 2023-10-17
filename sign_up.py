import cipher


def sign(user):
    print('You are now trying to sign up, if u want exit, please type \'!exit\'')
    data = None
    print('Name: ')
    name = input()

    print('Second Name: ')
    sec_name = input()
    print('Email: ')
    user.email = input()

    while user.email != '!exit':

        # We check if the email follow the regular expression
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        while not re.match(regex, user.email):
            if not re.match(regex, user.email):
                print('The email doesn\'t follow the required parameters')
                print('Email:')
            user.email = input()

        # We check if the email is already in use

        if not user.connectionDb.fetchUser(user.email):
            pass1, pass2 = 0, 1
            while pass1 != pass2:
                print('Enter the password for your account (it must contain at least 1 mayus, 1 digit, '
                      '1 of the following symbols ($,%,&,@) :')
                pass1 = input()
                pass1 = cipher.check_password(pass1)

                print('Confirm your password:')
                pass2 = input()
                if pass1 != pass2:
                    print('The passwords doesn\'t match')
                else:
                    # We encode the password
                    # We are going to use Fernet for symetric encription
                    ciphered_password = cipher.data_encryption(pass1, pass1)
                    data = [name, sec_name, user.email, ciphered_password]
                    # We leave the while pass1 != pass2 loop
                    break
            # We leave the while True loop
            break
        else:
            print('Sorry that email name is already in use, you should try log in, type !exit to go back')
            print('Email: ')
        user.email = input()

    if user.email != '!exit':

        user.connectionDb.insertUser(data)

        print('Account has been created successfully')
    return -1

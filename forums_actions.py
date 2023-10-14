import forum_chat
import re
import cipher


def access(con, forum_list):
    while True:
        print('Please, enter the  name of the forum you want to access')
        forum_name = input()

        # We check if the user belongs to the forum
        if forum_name in forum_list:
            print('Please, enter your password:')
            c = 3
            # We check if the password is correct
            while c > 0:

                password = input()

                # Check if the password is correct

                if password:
                    res = forum_chat.start(con, forum_name)
                    # You went out the live_chat, and you are going back to the forum menu
                    return res
                else:
                    c -= 1
                    print('Wrong password, please try again:')
            # We break the while True loop because of a wrong password, and you log_out
            break

        else:
            print('You don\'t have access to the forum' + forum_name)
    return -1


def create(con):
    forum_data = []
    while True:
        print('Please, enter the  name of the forum you want to create:')
        forum_name = input()

        # We check if the name is already in use
        if not con.findForum(forum_name):
            print('Create the password of the forum:')

            pass1, pass2 = 0, 1

            while pass1 != pass2:
                print('Enter the password for your forum (it must contain at least 1 mayus, 1 digit, '
                      '1 of the following symbols ($,%,&,@) :')
                pass1 = input()
                while not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)):

                    if not (re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[$%&@])[A-Za-z\d$%&@]{8,}$', pass1)):
                        print("Your password doesn\'t match required standards")
                    pass1 = input()

                print('Confirm your password:')
                pass2 = input()
                if pass1 != pass2:
                    print('The passwords doesn\'t match')
                else:
                    # We encode the password
                    # We are going to use Fernet for symetric encription
                    ciphered_password = cipher.password_encryption(pass1)
                    forum_data = [forum_name, ciphered_password]
                    # We leave the while pass1 != pass2 loop
                    break
            # We leave the while True loop
            break
        else:
            print('Sorry that forum name is already in use')

    # We create the forum

    con.insertForum(forum_data)
    print('Forum has been created successfully')
    return 1

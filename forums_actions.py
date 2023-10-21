import forum_chat
import re
import cipher


def access(user, forum_list):
    while True:
        print('Please, enter the  name of the forum you want to access')
        forum_name = input()

        # We check if the user belongs to the forum
        if forum_name not in forum_list:
            print('You don\'t have access to the forum: ' + forum_name)

        print('Please, enter your password:')
        c = 3
        # We check if the password is correct
        while c > 0:

            password = input()

            # Check if the password is correct
            db_password = cipher.data_decryption(user.connectionDb.fetchPasswordForum(forum_name), password)

            if password == db_password:
                if forum_name not in forum_list:
                    user.connectionDb.joinUserForum(user.email, forum_name)
                # We save the forum were the user will be sending messages
                user.usingForum = forum_name
                user.cypherKeyForum = password
                res = forum_chat.start(user)
                # You went out the live_chat, and you are going back to the forum menu
                return res
            else:
                c -= 1
                print('Wrong password, please try again:')
        # We break the while True loop because of a wrong password, and you log_out
        break

    return -1


def create(user):
    forum_data = []
    while True:
        print('Please, enter the  name of the forum you want to create:')
        forum_name = input()

        # We check if the name is already in use
        if not user.connectionDb.fetchForum(forum_name):
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
                    ciphered_password = cipher.data_encryption(pass1, pass1)
                    forum_data = [forum_name, ciphered_password]
                    # We leave the while pass1 != pass2 loop
                    break
            # We leave the while True loop
            break
        else:
            print('Sorry that forum name is already in use')

    # We create the forum

    user.connectionDb.insertForum(forum_data, user.email)
    print('Forum has been created successfully')
    return 1

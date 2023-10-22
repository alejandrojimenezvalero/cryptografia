import forum_chat
import re
import cipher
import time


def access(user, forum_list):
    while True:
        print('Please, enter the  name of the forum you want to access')
        forum_name = input()

        while not user.connectionDb.fetchForum(forum_name) and forum_name != '!exit':
            print("That forum doesn\'t exist, you may want to create it")
            forum_name = input()

        if forum_name == '!exit':
            break

        # We check if the user belongs to the forum
        if forum_name not in forum_list:
            print('You don\'t have access to the forum: ' + forum_name)
            time.sleep(1)

        print('Please, enter your password:')
        c = 3
        # We check if the password is correct
        while c > 0:

            password = input()
            salt = cipher.decode_salt(user.connectionDb.fetchForumSalt(forum_name))
            # Check if the password is correct
            db_password = cipher.data_decryption(user.connectionDb.fetchPasswordForum(forum_name), password, salt)

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

            pass1 = cipher.check_password(pass1, pass2)

            if pass1 == -1:
                return -1

            # We encode the password
            # We are going to use Fernet for symetric encription
            salt = cipher.generate_salt()
            ciphered_password = cipher.data_encryption(pass1, pass1, salt)
            encoded_salt = cipher.encode_salt(salt)
            forum_data = [forum_name, ciphered_password, encoded_salt]
            # We leave the while pass1 != pass2 loop
            # We leave the while True loop
            break
        else:
            print('Sorry that forum name is already in use')

    # We create the forum
    res = user.connectionDb.insertForum(forum_data, user.email)
    if res == 0:
        print('Forum has been created successfully')
    time.sleep(1)
    return 1

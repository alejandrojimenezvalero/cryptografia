"""This module facilitates the creation or access of a forum"""
import forum_chat
import cipher
import time
import plyer
from plyer.platforms.win.notification import Notification
from transitions import print_slow


def access(user, forum_list):
    """This function manages the access logic to a forum"""
    while True:
        print('Please, enter the  name of the forum you want to access')
        forum_name = input()

        while not user.connectionDb.fetchForumExists(forum_name) and forum_name != '!exit':
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
                    user.connectionDb.joinUserForum(user.email, forum_name, "user")
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
    """This function manages the creation logic of a forum"""
    forum_data = []
    while True:
        print('Please, enter the  name of the forum you want to create:')
        forum_name = input()

        # We check if the name is already in use
        if  forum_name == '!exit':
            return -1
        elif not user.connectionDb.fetchForumExists(forum_name):
            print('Create the password of the forum:')

            pass1 = cipher.check_password()

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
    res = user.connectionDb.insertForum(forum_data)
    user.connectionDb.joinUserForum(user.email, forum_name, "admin")
    if res == 0:
        print('Forum has been created successfully')
    time.sleep(1)
    return 1

def display_notification(message):
    try:
        plyer.notification.notify(
            title='Forum Invitation',
            message=message,
            app_name='ForumApp'
        )
    except Exception as e:
        print(f"Error displaying notification: {e}")


def check_inbox(user):
    invitations = user.connectionDb.fetchInvitations(user.id)

    if not invitations:
        print_slow("No invitations in your inbox.")
        return 1
    print_slow("You have invitations for the following forums")
    c = 1
    print("-" * 40)
    for invitation in invitations:
        print(f"{c}. Forum Name: {invitation[0]}")
        print("-" * 40)
        c += 1

    print_slow("You can only see the invitation message once")
    print_slow("Which forum invitation you want to open?")

    forum_name = None
    complete_invitation = None
    while forum_name not in [invitation[0] for invitation in invitations]:
        forum_name = input("Please, enter the forum name or type !exit: ")

        if forum_name == '!exit':
            return 1

    for invitation in invitations:
        if invitation[0] == forum_name:
            complete_invitation = invitation

    sender_public_key_pem = user.connectionDb.fetchPublicKey(complete_invitation[3])
    ciphered_message = complete_invitation[1]
    signature = complete_invitation[2]
    decrypted_message = cipher.verify_signature_and_decrypt(ciphered_message,signature, sender_public_key_pem, user.private_key)
    if decrypted_message == None:
        print("Error decrypting invitation")
        user.connectionDb.deleteInvitation(user.id, forum_name)
        return -1
    else:
        display_notification(decrypted_message)
    user.connectionDb.deleteInvitation(user.id, forum_name)

    return 1


def invite(user, forum_list_admin):
    # in future versions, the app only will ask for the username
    user_to_fetch = None
    while not user.connectionDb.fetchUserId(user_to_fetch) and user_to_fetch != "!exit":
        print("Please, enter the email of the user you want to invite or type \'!exit\'")
        user_to_fetch = input()
    user_to_fetch_id = user.connectionDb.fetchUserId(user_to_fetch)
    if user_to_fetch == "!exit":
        print("You are being redirected to the forum menu")
        time.sleep(2)
        return 1

    print("You can invite to the following forums:")
    c = 1
    for forum_name in forum_list_admin:
        print(c, ". ", forum_name)
        c += 1
    forum_to_invite = None
    while (forum_to_invite not in forum_list_admin) and forum_to_invite != "!exit":
        print("Select the name of the forum or type !exit")
        forum_to_invite = input()

    if forum_to_invite == "!exit":
        print("You are being redirected to the forum menu")
        time.sleep(2)
        return 1

    confirmation = False
    message = None
    while not confirmation and message != "!exit":
        print("Please, write the password of the forum and we will send the invitation with the password, this invitation will be ciphered or type !exit")
        message = input()
        print("Make sure the password is correct")
        print("Do you want to invite ", user_to_fetch, " to the forum ", forum_to_invite, "? (y/n)")
        confirmation = input().lower()
    if message == "!exit":
        print("You are being redirected to the forum menu")
        time.sleep(2)
        return 1

    destination_user_public_key_pem = user.connectionDb.fetchPublicKey(user_to_fetch_id)
    destination_user_public_key = cipher.load_public_key_from_pem(destination_user_public_key_pem)
    ciphered_message, signature = cipher.encrypt_and_sign(message, destination_user_public_key, user.private_key)
    user.connectionDb.sendInvitation(ciphered_message, signature, user_to_fetch, forum_to_invite, user.id)
    return 1


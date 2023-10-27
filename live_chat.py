"""
This module manages the live chat feature.
Enables concurrent communication between users through two separate threads of execution
"""
import threading
import time
import keyboard
import cipher

def showBdMessages(user, mutex, exit_flag):
    """This function shows the messages of the forum"""
    print("Showing the new messages of the forum...")
    shown_messages = set()
    last_shown_index = 0
    while not exit_flag.is_set():
        try:
            user.connectionDb.update0(mutex)
            db_messages = user.connectionDb.showMessages(user.usingForum, mutex)
            for i in range(last_shown_index, len(db_messages)):
                id, message, salt, name, second_name = db_messages[i]
                decoded_salt = cipher.decode_salt(salt)
                decoded_message = cipher.data_decryption(message,user.cypherKeyForum, decoded_salt)
                if id not in shown_messages:
                    print(f"{name} {second_name}: {decoded_message}\n")
                    shown_messages.add(id)
            last_shown_index = len(db_messages)
        except:
            exit_flag.set()


def block_while_insert(user, message, mutex):
    """This function blocks the input option while the message is in the sending process"""
    keyboard.hook(lambda e: keyboard.block_key(e.name))

    id_user = user.connectionDb.consultIdUser(user.email, mutex)
    id_forum = user.connectionDb.consultIdForum(user.usingForum, mutex)
    salt = cipher.generate_salt()
    ciphered_message = cipher.data_encryption(message, user.cypherKeyForum, salt)
    encoded_salt = cipher.encode_salt(salt)
    data = [ciphered_message, id_user, id_forum, encoded_salt]
    user.connectionDb.insertMessage(data, mutex)

    keyboard.unhook_all()

def waitUserMessage(user, mutex, exit_flag):
    """This function listens for user input from the console"""
    time.sleep(1)
    while not exit_flag.is_set():
        # We add a time.sleep of 0.1 seconds, so it doesn't interrupt any
        try:
            message = input()
            if message.lower() == "!exit":
                exit_flag.set()
            else:
                if len(message) > 79:
                    message = message[:79]
                block_while_insert(user, message, mutex)
        except:
            exit_flag.set()
    return -1


def chat(user):
    """Manages the execution flow using two threads for concurrent operations"""
    exit_flag = threading.Event()
    mutex = threading.Lock()

    show_messages_thread = threading.Thread(target=showBdMessages, args=(user, mutex, exit_flag, ))
    wait_messages_thread = threading.Thread(target=waitUserMessage, args=(user, mutex, exit_flag, ))

    # Start threads
    show_messages_thread.start()
    wait_messages_thread.start()

    # Join threads
    show_messages_thread.join()
    wait_messages_thread.join()

    print("You are leaving the chat, please wait.")
    time.sleep(5)
    return 1

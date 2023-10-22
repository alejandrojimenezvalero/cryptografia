import threading
import time
import keyboard


def showBdMessages(user, mutex, exit_flag):
    print("Showing the new messages of the forum...")
    shown_messages = set()
    last_shown_index = 0
    while not exit_flag.is_set():
        try:
            time.sleep(0.01)
            user.connectionDb.update0(mutex)
            db_messages = user.connectionDb.showMessages(user.usingForum, mutex)
            for i in range(last_shown_index, len(db_messages)):
                message, name, second_name = db_messages[i]
                if (message, name, second_name) not in shown_messages:
                    print(f"{name} {second_name}: {message}\n")
                    shown_messages.add((message, name, second_name))
            last_shown_index = len(db_messages)
        except:
            exit_flag.set()


def block_while_insert(user, message, mutex):
    keyboard.hook(lambda e: keyboard.block_key(e.name))

    id_user = user.connectionDb.consultIdUser(user.email, mutex)
    id_forum = user.connectionDb.consultIdForum(user.usingForum, mutex)
    data = [message, id_user, id_forum]
    user.connectionDb.insertMessage(data, mutex)

    keyboard.unhook_all()

def waitUserMessage(user, mutex, exit_flag):
    time.sleep(1)
    while not exit_flag.is_set():
        # We add a time.sleep of 0.1 seconds, so it doesn't interrupt any
        #time.sleep(2)
        try:
            message = input()
            if message.lower() == "!exit":
                exit_flag.set()
            else:
                block_while_insert(user, message, mutex)
        except:
            exit_flag.set()
    return -1


def chat(user):
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

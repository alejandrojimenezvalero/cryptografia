import threading
import time

def showBdMessages(user, mutex):
    print("Showing the new messages of the forum...")
    shown_messages = set()
    while True:
        user.connectionDb.update0(mutex)
        db_messages = user.connectionDb.showMessages(user.usingForum, mutex)
        for (message, name, second_name) in db_messages:
            if (message, name, second_name) not in shown_messages:
                print(f"{name} {second_name}: {message}\n")
                shown_messages.add((message, name, second_name))


def waitUserMessage(user, mutex):
    time.sleep(1)
    while True:
        # We add a time.sleep of 0.1 seconds, so it doesn't interrupt any
        #time.sleep(2)
        message = input()
        if message.lower() == "!exit":
            break
        id_user = user.connectionDb.consultIdUser(user.email, mutex)
        id_forum = user.connectionDb.consultIdForum(user.usingForum, mutex)
        data = [message, id_user, id_forum]
        user.connectionDb.insertMessage(data, mutex)

def chat(user):
    mutex = threading.Lock()

    show_messages_thread = threading.Thread(target=showBdMessages, args=(user, mutex, ))
    wait_messages_thread = threading.Thread(target=waitUserMessage, args=(user, mutex, ))

    # Start threads
    show_messages_thread.start()
    wait_messages_thread.start()

    # Join threads
    show_messages_thread.join()
    wait_messages_thread.join()

    print("You are leaving the chat, please wait.")
    time.sleep(5)
    return 1

import threading
import time

def showBdMessages(con, forum_name, mutex):
    print("Showing the new messages of the forum...")
    shown_messages = set()
    while True:
        con.update0(mutex)
        db_messages = con.showMessages(forum_name, mutex)
        for (message, name, second_name) in db_messages:
            if (message, name, second_name) not in shown_messages:
                print(f"{name} {second_name}: {message}\n")
                shown_messages.add((message, name, second_name))


def waitUserMessage(con, email, forum_name, mutex):
    time.sleep(1)
    while True:
        # We add a time.sleep of 0.1 seconds, so it doesn't interrupt any
        #time.sleep(2)
        message = input()
        if message.lower() == "!exit":
            break
        id_user = con.consultIdUser(email, mutex)
        id_forum = con.consultIdForum(forum_name, mutex)
        data = [message, id_user, id_forum]
        con.insertMessage(data, mutex)

def chat(con, email, forum_name):
    mutex = threading.Lock()

    show_messages_thread = threading.Thread(target=showBdMessages, args=(con, forum_name, mutex, ))
    wait_messages_thread = threading.Thread(target=waitUserMessage, args=(con, email, forum_name, mutex, ))

    # Start threads
    show_messages_thread.start()
    wait_messages_thread.start()

    # Join threads
    show_messages_thread.join()
    wait_messages_thread.join()

    print("You are leaving the chat, please wait.")
    time.sleep(5)
    return 1

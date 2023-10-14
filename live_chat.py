import threading
import time


print('Welcome ')


def showBdMessages(con, forum_name):
    print("Showing the new messages of the forum...")
    while True:
        pass


def waitUserMessage(con, forum_name):
    while True:
        message = input("-> ")
        if message.lower() == "!exit":
            break


def chat(con, forum_name):
    show_messages_thread = threading.Thread(target=showBdMessages, args=(forum_name, con,))
    wait_messages_thread = threading.Thread(target=waitUserMessage, args=(forum_name, con,))

    # Start threads
    show_messages_thread.start()
    wait_messages_thread.start()

    # Join threads
    show_messages_thread.join()
    wait_messages_thread.join()

    print("You are leaving the chat, please wait.")
    time.sleep(5)
    return 1

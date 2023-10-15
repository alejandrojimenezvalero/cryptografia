import live_chat


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def start(con, email, forum_name):

    # We check the number of messages of the forum
    """
    print('There are x messages on the forum: ' + forum_name)
    print('How many messages you want to see?: ')
    num_msg = None
    while True:
        num_msg = input()
        if not is_int(num_msg):
            print('Please, enter a valid number of messages')
        else:
            num_msg = int(num_msg)
            break

    # We show the number of messages the user asked for
    """
    res = live_chat.chat(con, email, forum_name)
    return res

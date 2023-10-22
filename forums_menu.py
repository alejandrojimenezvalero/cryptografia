import forums_actions
import time


def start(user):

    # First we have to show all the Forums the user has access to
    while True:
        print('You have access to the following forums:')
        time.sleep(1)

        # We show the forums
        forum_list = user.connectionDb.showForums(user.email)
        time.sleep(1)

        print('What do you want to do?\n'
              + '1. If you want to access a forum, please type !access\n'
              + '2. If you want to create a forum, please type !create\n'
              + '3. If you want to Exit, please type !exit\n')

        action_forum = None
        res = None
        while action_forum != '!exit':

            action_forum = input().lower()
            if action_forum == '!access':
                res = forums_actions.access(user, forum_list)
            elif action_forum == '!create':
                res = forums_actions.create(user)
            elif action_forum != '!exit':
                print('Please use !access, !create or !exit')

            if res == 1:
                # if res==1, you come back from access or create, either ways you stay on the forum menu
                print('Welcome back to the forum menu.')
                time.sleep(1)
                break
            elif res == -1:
                # if res==-1, you have entered a wrong password, and you must log_out automatically
                break
        if res != 1:
            break
    return -1

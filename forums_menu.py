"""This module manages the forum menu display for users, showcasing the forums they are part of"""
import forums_actions
import time


import time
import forums_actions  # Asumo que hay un módulo forums_actions que contiene las funciones access, create, e invite

import time
import forums_actions  # Asumo que hay un módulo forums_actions que contiene las funciones access, create e invite

def start(user):
    """This function allows the user to create a new forum or access an already created one"""
    show_menu = True
    forum_list = []
    is_admin = False

    while True:
        if show_menu:
            print('You have access to the following forums:')
            time.sleep(1)

            forum_list, forum_list_admin = user.connectionDb.showForums(user.email)
            time.sleep(1)

            if len(forum_list_admin) > 0:
                is_admin = True

            menu_text = ('What do you want to do?\n'
                         + '1. If you want to access a forum, please type !access\n'
                         + '2. If you want to create a forum, please type !create\n'
                         + '3. If you want to send an invitation to a forum, please type !invite\n'
                         + '4. If you want to check your inbox type !inbox\n'
                         + '5. If you want to Exit, please type !exit\n' if is_admin else
                         'What do you want to do?\n'
                         + '1. If you want to access a forum, please type !access\n'
                         + '2. If you want to create a forum, please type !create\n'
                         + '3. If you want to check your inbox type !inbox\n'
                         + '4. If you want to Exit, please type !exit\n')

            print(menu_text)
            show_menu = False

        action_forum = input().lower()
        res = None

        if action_forum == '!access':
            res = forums_actions.access(user, forum_list)
        elif action_forum == '!create':
            res = forums_actions.create(user)
            forum_list, forum_list_admin = user.connectionDb.showForums(user.email)
            if len(forum_list_admin) > 0:
                is_admin = True
        elif action_forum == '!inbox':
            res = forums_actions.check_inbox(user)
        elif action_forum == '!invite' and is_admin:
            res = forums_actions.invite(user, forum_list_admin)
        elif action_forum != '!exit' and is_admin:
            print('Please use !access, !create, !invite, or !exit')
        elif action_forum != '!exit' and not is_admin:
            print('Please use !access, !create, or !exit')

        if res == 1:
            print('Welcome back to the forum menu.')
            time.sleep(1)
        elif res == -1 or action_forum == "!exit":
            break

    return -1



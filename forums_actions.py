import forum_chat


def access(con):
    while True:
        print('Please, enter the  name of the forum you want to access')
        forum_name = input()

        # We check if the user belongs to the forum

        if forum_name:
            print('Please, enter your password:')
            c = 3
            # We check if the password is correct
            while c > 0:

                password = input()

                # Check if the password is correct

                if password:
                    res = forum_chat.start(con, forum_name)
                    # You went out the live_chat, and you are going back to the forum menu
                    return res
                else:
                    c -= 1
                    print('Wrong password, please try again:')
            # We break the while True loop because of a wrong password, and you log_out
            break

        else:
            print('You don\'t have access to the forum' + forum_name)
    return -1


def create(con):
    while True:
        print('Please, enter the  name of the forum you want to create:')
        forum_name = input()

        # We check if the name is already in use

        if not forum_name:
            print('Create the password of the forum:')
            pass1, pass2 = None, None
            while pass1 != pass2:
                print('Please, Enter your password:')
                pass1 = input()
                print('Repeat your password:')
                pass2 = input()
                if pass1 != pass2:
                    print('The passwords doesn\'t match')
                else:
                    # We encode the password

                    # We leave the while pass1 != pass2 loop
                    break
            # We leave the while True loop
            break
        else:
            print('Sorry that forum name is already in use')

    # We create the forum
    print('Forum has been created successfully')
    return 1

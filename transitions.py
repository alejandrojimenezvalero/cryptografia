import keyboard
import time
import sys


def block_keyboard():
    keys_to_block = list(range(1, 127))

    for key in keys_to_block:
        keyboard.block_key(key)

    special_keys = ['enter', 'esc', 'backspace', 'delete', 'tab']
    for key in special_keys:
        keyboard.block_key(key)

def unblock_keyboard():
    keyboard.unhook_all()

def print_slow(text):
    block_keyboard()
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)

    # Print a new line at the end
    print()

    unblock_keyboard()  # Unblock keyboard events

"""This module initializes the live chat functionality for the application"""
import live_chat


def start(user):
    """This function initializes the chat"""
    res = live_chat.chat(user)
    return res

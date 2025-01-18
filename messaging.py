# messaging.py

from db import messages_collection
import streamlit as st
from datetime import datetime

def send_message(sender, recipient, message):
    """
    Sends a message from the sender to the recipient.

    :param sender: Username of the sender.
    :param recipient: Username of the recipient.
    :param message: Content of the message.
    """
    messages_collection.insert_one({
        "sender": sender,
        "recipient": recipient,
        "message": message,
        "timestamp": datetime.utcnow(),
        "read": False  # Indicates if the message has been read
    })
    st.success("Message sent!")

def get_messages(username, selected_user):
    """
    Retrieves all messages between the logged-in user and the selected user.

    :param username: Logged-in user's username.
    :param selected_user: The user with whom to chat.
    :return: List of message dictionaries sorted by timestamp.
    """
    messages = messages_collection.find({
        "$or": [
            {"sender": username, "recipient": selected_user},
            {"sender": selected_user, "recipient": username}
        ]
    }).sort("timestamp", 1)  # Sort messages from oldest to newest
    return list(messages)
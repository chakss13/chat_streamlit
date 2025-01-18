# messaging.py

from db import cursor, conn
from datetime import datetime

def send_message(sender, recipient, message):
    """
    Sends a message from the sender to the recipient.
    
    Args:
        sender (str): The username of the sender.
        recipient (str): The username of the recipient.
        message (str): The message content.
        
    Returns:
        tuple: (bool, str) indicating success status and a message.
    """
    if conn is None or cursor is None:
        return False, "Database connection is not available."
    
    # Check if the recipient exists
    cursor.execute("SELECT username FROM users WHERE username = %s", (recipient,))
    if not cursor.fetchone():
        return False, "Recipient not found."

    # Insert the message into the database
    cursor.execute(
        "INSERT INTO messages (sender, recipient, message, read) VALUES (%s, %s, %s, %s)",
        (sender, recipient, message, False)
    )
    return True, "Message sent successfully."

def get_messages(username, selected_user):
    """
    Retrieves all messages between the logged-in user and the selected user.
    
    Args:
        username (str): The username of the logged-in user.
        selected_user (str): The username of the user to chat with.
        
    Returns:
        list: A list of message dictionaries.
    """
    if conn is None or cursor is None:
        return []
    
    cursor.execute('''
        SELECT sender, recipient, message, timestamp 
        FROM messages 
        WHERE (sender = %s AND recipient = %s) OR (sender = %s AND recipient = %s)
        ORDER BY timestamp ASC
    ''', (username, selected_user, selected_user, username))
    
    messages = cursor.fetchall()
    return messages

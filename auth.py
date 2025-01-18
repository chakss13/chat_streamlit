# auth.py

from db import cursor, conn
from utils import hash_password, check_password

def register_user(username, password):
    """
    Registers a new user in the database.
    
    Args:
        username (str): The desired username.
        password (str): The plain text password.
        
    Returns:
        tuple: (bool, str) indicating success status and a message.
    """
    # Check if the username already exists
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return False, "Username already exists."

    # Hash the password and insert the new user
    hashed_pwd = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, password, status) VALUES (%s, %s, %s)",
        (username, hashed_pwd, "Available")
    )
    return True, "User registered successfully."

def authenticate_user(username, password):
    """
    Authenticates a user by verifying the username and password.
    
    Args:
        username (str): The user's username.
        password (str): The plain text password.
        
    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    # Retrieve the hashed password for the given username
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user and check_password(password, user['password']):
        return True
    return False

def get_all_users(current_username):
    """
    Retrieves all registered users except the current user.
    
    Args:
        current_username (str): The username of the current logged-in user.
        
    Returns:
        list: A list of usernames.
    """
    cursor.execute("SELECT username FROM users WHERE username != %s", (current_username,))
    users = cursor.fetchall()
    return [user['username'] for user in users]

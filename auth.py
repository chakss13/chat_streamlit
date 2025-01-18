# auth.py

from db import users_collection
from utils import hash_password, check_password

def register_user(username, password):
    """
    Registers a new user by adding their credentials to the database.

    :param username: Desired username.
    :param password: Desired password.
    :return: Tuple indicating success status and a message.
    """
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        return False, "Username already exists."

    # Hash the user's password before storing it
    hashed_pwd = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_pwd,
        "status": "Available",  # Default status
        "avatar": ""            # Placeholder for user avatar
    })
    return True, "User registered successfully."

def authenticate_user(username, password):
    """
    Authenticates a user by verifying their credentials.

    :param username: Entered username.
    :param password: Entered password.
    :return: Boolean indicating if authentication is successful.
    """
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user['password']):
        return True
    return False
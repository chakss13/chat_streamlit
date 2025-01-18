# utils.py

import bcrypt

def hash_password(password):
    """
    Hashes a password using bcrypt.

    :param password: Plain text password.
    :return: Hashed password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password, hashed):
    """
    Verifies a password against the hashed version.

    :param password: Plain text password entered by the user.
    :param hashed: Hashed password stored in the database.
    :return: Boolean indicating if the password matches.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
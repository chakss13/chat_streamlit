# utils.py

import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """
    Checks a password against the hashed version.
    
    Args:
        password (str): The plain text password.
        hashed (str): The hashed password to compare against.
        
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

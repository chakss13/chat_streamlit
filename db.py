# db.py
import os
import psycopg2
from psycopg2.extras import DictCursor

# It's recommended to set DATABASE_URL as an environment variable for security
DATABASE_URL = os.getenv()

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=DictCursor)
    print("Connected to PostgreSQL successfully!")
except Exception as e:
    print(f"Failed to connect to PostgreSQL: {e}")
    cursor = None
    conn = None

def create_tables():
    if conn is None or cursor is None:
        print("No database connection.")
        return
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                status VARCHAR(50),
                avatar TEXT
            );
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender VARCHAR(255) NOT NULL,
                recipient VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read BOOLEAN DEFAULT FALSE
            );
        ''')
    print("Tables are set up successfully.")

create_tables()

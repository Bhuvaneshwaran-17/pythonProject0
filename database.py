import psycopg2
from psycopg2.extras import Json

DB_CONFIG = {
    "host": "localhost",
    "dbname": "NextMove",
    "user": "postgres",
    "password": "Bhuvi@2024",
    "port": 5432
}


def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)

    # Create tables if they don't exist
    with conn.cursor() as cursor:
        # Table for storing action sequences with user_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                action_name VARCHAR(255) NOT NULL,
                next_action_name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table for storing individual user actions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_actions (
                id SERIAL PRIMARY KEY,
                action_name VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB
            )
        """)

        conn.commit()

    return conn
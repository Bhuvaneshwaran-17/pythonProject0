import psycopg2
from psycopg2.extras import Json

DB_CONFIG = {
    "host": "dpg-ctb7t4hopnds73el0qe0-a.oregon-postgres.render.com",
    "dbname": "db_for_nextaction",
    "user": "db_for_nextaction_user",
    "password": "6uRdStT8KBNgyz9qvhgYDALeHnBzOUFB",
    "port": 5432,
    "sslmode": "require"  # Important for Render PostgreSQL
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # Create tables if they don't exist
        with conn.cursor() as cursor:
            # Table for storing action sequences with user_id
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255),
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
                    user_id VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata JSONB
                )
            """)
            conn.commit()
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

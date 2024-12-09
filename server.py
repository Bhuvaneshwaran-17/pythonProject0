from flask import Flask, jsonify, request
from supabase import create_client, Client
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Initialize Flask app
app = Flask(__name__)

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    try:
        # Initialize connection to Supabase Postgres database using environment variables
        connection = psycopg2.connect(
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT, 
            dbname=DB_NAME
        )
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute("SELECT * FROM action;")
        rows = cursor.fetchall()

        # Convert the result to a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/custom-query', methods=['GET'])
def custom_query():
    try:
        # Get the action_name from the request
        action_name = request.args.get('action_name')
        if not action_name:
            return jsonify({"error": "action_name parameter is required"}), 400

        # Initialize connection to Supabase Postgres database using environment variables
        connection = psycopg2.connect(
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT, 
            dbname=DB_NAME
        )
        cursor = connection.cursor()

        # Execute the SQL query with parameter substitution
        query = """
            SELECT action_name, next_action_name, COUNT(*) as frequency
            FROM action
            WHERE action_name = %s
            GROUP BY action_name, next_action_name
            ORDER BY frequency DESC, next_action_name;
        """
        cursor.execute(query, (action_name,))
        rows = cursor.fetchall()

        # Convert the result to a list of dictionaries
        columns = [desc[0] for desc in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

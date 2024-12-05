import pandas as pd
from typing import List, Dict, Union
from datetime import datetime
from database import get_db_connection


def fetch_sequences_for_action(current_action: str) -> Union[List[tuple], Dict[str, str]]:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT action_name, next_action_name, COUNT(*) as frequency
                    FROM actions 
                    WHERE action_name = %s
                    GROUP BY action_name, next_action_name
                    ORDER BY frequency DESC, next_action_name
                    """,
                    (current_action,)
                )
                data = cursor.fetchall()

        if not data:
            return {"error": "No data found for the given action."}

        return data

    except Exception as e:
        print(f"Error fetching sequences: {e}")
        return {"error": f"Database error: {e}"}


def analyze_sequences(data: List[tuple], current_action: str) -> Dict:
    if isinstance(data, dict) and "error" in data:
        return data

    # Create a DataFrame for better analysis
    df = pd.DataFrame(data, columns=['action', 'next_action', 'frequency'])
    total_occurrences = df['frequency'].sum()

    # Calculate probabilities
    sequences = []
    for _, row in df.iterrows():
        probability = row['frequency'] / total_occurrences
        sequences.append({
            'next_action': row['next_action'],
            'frequency': row['frequency'],
            'probability': round(probability * 100, 2)
        })

    return {
        'current_action': current_action,
        'total_occurrences': int(total_occurrences),
        'sequences': sequences
    }


def track_user_action(action_data: dict) -> Dict[str, str]:
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # First, get the last action to create the sequence
                if action_data.get('user_id'):
                    cursor.execute(
                        """
                        SELECT action_name 
                        FROM user_actions 
                        WHERE user_id = %s 
                        ORDER BY timestamp DESC 
                        LIMIT 1
                        """,
                        (action_data['user_id'],)
                    )
                    last_action = cursor.fetchone()

                    # If there was a previous action, record the sequence
                    if last_action:
                        cursor.execute(
                            """
                            INSERT INTO actions (action_name, next_action_name, created_at)
                            VALUES (%s, %s, %s)
                            """,
                            (last_action[0], action_data['action_name'], datetime.now())
                        )

                # Record the current action
                cursor.execute(
                    """
                    INSERT INTO user_actions (
                        action_name, 
                        user_id, 
                        timestamp, 
                        metadata
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        action_data['action_name'],
                        action_data.get('user_id'),
                        action_data.get('timestamp', datetime.now()),
                        action_data.get('metadata')
                    )
                )
                conn.commit()

        return {"status": "success", "message": "Action tracked successfully"}

    except Exception as e:
        print(f"Error tracking action: {e}")
        return {"error": f"Failed to track action: {e}"}
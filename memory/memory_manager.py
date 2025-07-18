import sqlite3
from datetime import datetime
import pandas as pd

DB_PATH = "db/emotion_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotion_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        emotion TEXT,
        intensity REAL,
        trigger TEXT,
        user_note TEXT
    )
    """)
    conn.commit()
    conn.close()

def log_emotion(emotion, intensity=None, trigger=None, user_note=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Safely convert intensity to float or set to None
        try:
            intensity_val = float(intensity) if intensity is not None else None
        except ValueError:
            intensity_val = None

        cursor.execute("""
            INSERT INTO emotion_log (date, emotion, intensity, trigger, user_note)
            VALUES (?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            emotion,
            intensity_val,
            trigger,
            user_note
        ))

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error logging emotion:", e)

def fetch_mood_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM emotion_log ORDER BY date ASC", conn)
        conn.close()
        return df
    except Exception as e:
        print("Error fetching mood history:", e)
        return None

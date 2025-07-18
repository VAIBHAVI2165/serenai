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
    conn = sqlite3.connect("db/emotion_log.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emotion_log (date, emotion, intensity, trigger, user_note)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), emotion, intensity, trigger, user_note))

    conn.commit()
    conn.close()


def fetch_mood_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM emotion_log ORDER BY date ASC", conn)
        conn.close()
        return df
    except Exception:
        return None

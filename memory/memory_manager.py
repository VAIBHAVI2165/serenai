# memory/memory_manager.py
import sqlite3
from datetime import datetime

DB_FILE = "serenai_mood.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emotion_log (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            emotion TEXT,
            confidence REAL,
            user_input TEXT
        )
    ''')
    conn.commit()
    conn.close()


def log_emotion(user_input, emotion, confidence):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO emotion_log (timestamp, emotion, confidence, user_input) VALUES (?, ?, ?, ?)",
              (timestamp, emotion, confidence, user_input))
    conn.commit()
    conn.close()

def fetch_mood_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT emotion, timestamp FROM emotion_log ORDER BY timestamp ASC")
    data = c.fetchall()
    conn.close()
    return data

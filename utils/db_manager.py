# utils/db_manager.py

import sqlite3
from datetime import datetime

# Connect to (or create) the database
def connect_db():
    conn = sqlite3.connect("db/emotion_log.db")
    return conn

# Create the emotion_log table (run only once)
def create_table():
    conn = connect_db()
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

# Add a new emotion record
def log_emotion(emotion, intensity, trigger, user_note=""):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO emotion_log (date, emotion, intensity, trigger, user_note)
    VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().isoformat(), emotion, intensity, trigger, user_note))
    conn.commit()
    conn.close()

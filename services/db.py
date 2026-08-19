import os
import mysql.connector
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_CFG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "ecoRewards"),
    "autocommit": True
}

@contextmanager
def conn_cursor():
    conn = mysql.connector.connect(**DB_CFG)
    cur = conn.cursor()
    try:
        yield conn, cur
    finally:
        cur.close()
        conn.close()

def ensure_schema():
    with conn_cursor() as (_, cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
          id VARCHAR(32) PRIMARY KEY,
          name VARCHAR(64),
          points INT DEFAULT 0,
          face_path VARCHAR(255),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
          id INT AUTO_INCREMENT PRIMARY KEY,
          user_id VARCHAR(32),
          type ENUM('credit','debit'),
          amount INT,
          bottle_type VARCHAR(32),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
          id INT AUTO_INCREMENT PRIMARY KEY,
          event VARCHAR(64),
          details TEXT,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def get_user(user_id):
    with conn_cursor() as (_, cur):
        cur.execute("SELECT id, name, points, face_path FROM users WHERE id=%s", (user_id,))
        return cur.fetchone()

def upsert_user(user_id, name, face_path):
    with conn_cursor() as (_, cur):
        cur.execute("""
        INSERT INTO users (id, name, points, face_path) VALUES (%s,%s,0,%s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), face_path=VALUES(face_path)
        """, (user_id, name, face_path))

def add_points(user_id, amount, bottle_type):
    with conn_cursor() as (_, cur):
        cur.execute("UPDATE users SET points = points + %s WHERE id=%s", (amount, user_id))
        cur.execute("INSERT INTO transactions (user_id, type, amount, bottle_type) VALUES (%s,'credit',%s,%s)",
                    (user_id, amount, bottle_type))

def deduct_points(user_id, amount, reason):
    with conn_cursor() as (_, cur):
        cur.execute("UPDATE users SET points = points - %s WHERE id=%s", (amount, user_id))
        cur.execute("INSERT INTO transactions (user_id, type, amount, bottle_type) VALUES (%s,'debit',%s,%s)",
                    (user_id, amount, reason))

def log_event(event, details):
    with conn_cursor() as (_, cur):
        cur.execute("INSERT INTO events (event, details) VALUES (%s,%s)", (event, details))
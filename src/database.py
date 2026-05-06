import sqlite3
import pandas as pd
import os

# Database Path Configuration
DB_FOLDER = "database"
DB_PATH = os.path.join(DB_FOLDER, "expenses.db")

def initialize_database():
    """Creates the database folder and transactions table if they do not exist."""
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Schema includes currency for multi-currency support
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            currency TEXT,
            method TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(date, category, amount, currency, method, note):
    """Inserts a new expense record into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        INSERT INTO transactions (date, category, amount, currency, method, note)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    conn.execute(query, (date, category, amount, currency, method, note))
    conn.commit()
    conn.close()

def load_all_data():
    """Fetches all records and returns a cleaned Pandas DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM transactions", conn)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df
import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join("database", "expenses.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
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
    conn.close()

def add_expense(date, category, amount, currency, method, note):
    conn = sqlite3.connect(DB_PATH)
    df = pd.DataFrame([[date, category, amount, currency, method, note]], 
                      columns=['date', 'category', 'amount', 'currency', 'method', 'note'])
    df.to_sql('transactions', conn, if_exists='append', index=False)
    conn.close()

def get_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM transactions", conn)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
    except:
        df = pd.DataFrame()
    conn.close()
    return df
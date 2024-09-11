import sqlite3

def initialize_database():
    conn = sqlite3.connect('banking.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')

    # Create accounts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        username TEXT,
        account_name TEXT,
        balance INTEGER,
        PRIMARY KEY (username, account_name),
        FOREIGN KEY (username) REFERENCES users(username)
    )
    ''')

    # Create transactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time TEXT NOT NULL,
        sender TEXT,
        recipient TEXT,
        amount INTEGER,
        FOREIGN KEY (sender) REFERENCES users(username),
        FOREIGN KEY (recipient) REFERENCES users(username)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
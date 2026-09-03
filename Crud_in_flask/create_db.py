import os
import sqlite3

def init_db(db_path: str = None):
    """Initialize SQLite database with products table schema."""
    script_dir = os.path.dirname(__file__)
    if db_path is None:
        db_path = os.path.join(script_dir, 'database.db')

    sql_path = os.path.join(script_dir, 'database.sql')
    connection = sqlite3.connect(db_path)

    if os.path.exists(sql_path):
        with open(sql_path, 'r', encoding='utf-8') as f:
            connection.executescript(f.read())

    cur = connection.cursor()
    cur.execute("INSERT INTO products (title, price) VALUES (?, ?)", ('Keyboard', 120))
    cur.execute("INSERT INTO products (title, price) VALUES (?, ?)", ('Monitor 4k', 111))
    connection.commit()
    connection.close()
    print(f"Initialized database schema at '{db_path}'.")

if __name__ == '__main__':
    init_db()


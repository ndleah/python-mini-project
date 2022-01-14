import sqlite3

connection = sqlite3.connect('database.db')


with open('database.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO products (title, price) VALUES (?, ?)",
            ('Keyboard', 120)
            )

cur.execute("INSERT INTO products (title, price) VALUES (?, ?)",
            ('Monitor 4k', 111)
            )

connection.commit()
connection.close()

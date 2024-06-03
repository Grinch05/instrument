import sqlite3

def create_db():
    conn = sqlite3.connect('shoe_store.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shoes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  size INTEGER,
                  price REAL,
                  model TEXT,
                  country TEXT,
                  image BLOB)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT,
                  role TEXT)''')
    conn.commit()
    conn.close()

def add_default_users():
    conn = sqlite3.connect('shoe_store.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
              ('admin', 'admin', 'admin'))
    c.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
              ('user', 'user', 'user'))
    conn.commit()
    conn.close()

create_db()
add_default_users()

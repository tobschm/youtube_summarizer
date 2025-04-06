import sqlite3

class Database:
    conn = None
    c = None

    def __init__(self):
        # create a database connection (file is created if it doesn't exist)
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        # Create table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
            Name TEXT NOT NULL,
            Api_key TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        self.conn.close()

    def add_entry(self, name, api_key):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute("INSERT OR REPLACE INTO api_keys (Name, Api_key) VALUES (?, ?)", (name, api_key))
        self.conn.commit()
        self.conn.close()

    def remove_entry(self, name):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM api_keys WHERE Name=?", (name,))
        self.conn.commit()
        self.conn.close()

    def get_api_key(self, name):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT Api_key FROM api_keys WHERE Name=?", (name,))
        api_key = self.c.fetchone()
        if api_key:
            api_key = api_key[0]
        else:
            api_key = None
        self.conn.close()
        return api_key

    def get_all_entries(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM api_keys")
        entries = self.c.fetchall()
        self.conn.close()
        return entries
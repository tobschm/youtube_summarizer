import sqlite3
import sys
import os

class Database:
    conn = None
    c = None
    db_path = None

    def get_db_path(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            app_data = os.path.join(os.path.expanduser("~"), ".youtube_summarizer")
            os.makedirs(app_data, exist_ok=True)
            return os.path.join(app_data, 'database.db')
        else:
            # Running in dev mode
            return 'database.db'

    def __init__(self):
        # create a database connection (file is created if it doesn't exist)
        self.db_path = self.get_db_path()
        self.conn = sqlite3.connect(self.db_path)
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
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.c.execute("INSERT OR REPLACE INTO api_keys (Name, Api_key) VALUES (?, ?)", (name, api_key))
        self.conn.commit()
        self.conn.close()

    def remove_entry(self, name):
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.c.execute("DELETE FROM api_keys WHERE Name=?", (name,))
        self.conn.commit()
        self.conn.close()

    def get_api_key(self, name):
        self.conn = sqlite3.connect(self.db_path)
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
        self.conn = sqlite3.connect(self.db_path)
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM api_keys")
        entries = self.c.fetchall()
        self.conn.close()
        return entries
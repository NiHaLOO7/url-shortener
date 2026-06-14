import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="urls.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT NOT NULL,
                long_url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_long_url ON urls(long_url)
        """)
        conn.commit()
        conn.close()

    def save_url(self, long_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO urls 
                       (short_code, 
                       long_url, 
                       created_at) 
                       VALUES (?, ?, ?)""", 
                       ('', long_url, 
                       datetime.now().isoformat())
                    )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def update_short_code(self, id, short_code):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE urls 
                       SET short_code = ? 
                       WHERE id = ?
                       """, 
                       (short_code, 
                       id)
                    )
        conn.commit()
        conn.close()
    
    def get_long_url(self, id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT long_url FROM urls 
                       WHERE id = ?
                       """, 
                       (id,)
                    )
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def get_short_code(self, long_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT short_code FROM urls 
                       WHERE long_url = ? AND short_code != ''
                       """, 
                       (long_url,)
                    )
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
    
    def get_all_urls(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT long_url FROM urls 
                       """
                    )
        rows = cursor.fetchall()
        conn.close()
        return rows

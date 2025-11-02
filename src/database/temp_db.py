# src/database/temp_db.py
import sqlite3
import os

class TempDatabase:
    def __init__(self, path):
        self.path = path
        self.conn = None

    def connect(self):
        if "fail" in self.path:
            raise ConnectionError("No se pudo conectar a la base de datos temporal.")
        self.conn = sqlite3.connect(self.path)
        return True

    def insert_demo_data(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS demo (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO demo (name) VALUES ('Alice'), ('Bob')")
        self.conn.commit()

    def fetch_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM demo")
        return cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

    def cleanup(self):
        """Elimina el archivo de base de datos temporal."""
        if os.path.exists(self.path):
            os.remove(self.path)

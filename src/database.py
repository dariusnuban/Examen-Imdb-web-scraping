import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="films_imdb.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
       
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                genre TEXT,
                duration TEXT,
                director TEXT,
                rating REAL,
                rating_count INTEGER,
                link TEXT UNIQUE,
                budget,
                origine,
                date_scraping TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    
    def insert_film(self, title, year, genre, duration, director, rating, count, link):
        try:
            # La requête SQL doit correspondre au nombre de colonnes et de paramètres
            self.cursor.execute('''
                INSERT INTO films (title, year, genre, duration, director, rating, rating_count, link, date_scraping)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, year, genre, duration, director, rating, count, link, datetime.now().isoformat()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def close(self):
        self.conn.close()
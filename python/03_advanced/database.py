# database.py
# Работа с базой данных SQLite

import sqlite3
import json
from datetime import datetime

class Database:
    def __init__(self, db_name='snake_game.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """Создание таблиц"""
        # Таблица рекордов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                game_time INTEGER,
                food_eaten INTEGER
            )
        ''')
        
        # Таблица настроек
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT DEFAULT 'Player',
                difficulty TEXT DEFAULT 'medium',
                sound_enabled BOOLEAN DEFAULT 1,
                music_enabled BOOLEAN DEFAULT 1,
                show_grid BOOLEAN DEFAULT 1,
                control_scheme TEXT DEFAULT 'arrows'
            )
        ''')
        
        # Таблица достижений
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                condition TEXT,
                unlocked BOOLEAN DEFAULT 0
            )
        ''')
        
        # Вставка достижений по умолчанию
        achievements = [
            ('first_blood', 'Первая еда', 'Съесть первое яблоко'),
            ('snake_master', 'Мастер змейка', 'Набрать 100 очков'),
            ('speed_demon', 'Демон скорости', 'Достичь максимальной скорости'),
            ('invincible', 'Неуязвимый', 'Съесть 10 бонусов подряд'),
            ('wall_killer', 'Разрушитель стен', 'Пройти уровень со стенами'),
            ('golden_feast', 'Золотой пир', 'Съесть 5 золотых яблок')
        ]
        
        for ach in achievements:
            try:
                self.cursor.execute('''
                    INSERT INTO achievements (name, description, condition)
                    VALUES (?, ?, ?)
                ''', ach)
            except sqlite3.IntegrityError:
                pass
                
        self.conn.commit()
        
    def save_score(self, player_name, score, difficulty, game_time, food_eaten):
        """Сохранение результата"""
        self.cursor.execute('''
            INSERT INTO high_scores (player_name, score, difficulty, game_time, food_eaten)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_name, score, difficulty, game_time, food_eaten))
        self.conn.commit()
        
    def

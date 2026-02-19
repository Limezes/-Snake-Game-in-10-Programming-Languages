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
        
    def get_high_scores(self, difficulty=None, limit=10):
        """Получение рекордов"""
        if difficulty:
            self.cursor.execute('''
                SELECT player_name, score, difficulty, date, game_time, food_eaten
                FROM high_scores
                WHERE difficulty = ?
                ORDER BY score DESC
                LIMIT ?
            ''', (difficulty, limit))
        else:
            self.cursor.execute('''
                SELECT player_name, score, difficulty, date, game_time, food_eaten
                FROM high_scores
                ORDER BY score DESC
                LIMIT ?
            ''', (limit,))
            
        return self.cursor.fetchall()
        
    def get_player_stats(self, player_name):
        """Получение статистики игрока"""
        self.cursor.execute('''
            SELECT 
                COUNT(*) as games_played,
                MAX(score) as best_score,
                AVG(score) as avg_score,
                SUM(food_eaten) as total_food
            FROM high_scores
            WHERE player_name = ?
        ''', (player_name,))
        
        return self.cursor.fetchone()
        
    def save_settings(self, settings):
        """Сохранение настроек"""
        self.cursor.execute('''
            UPDATE settings SET
                player_name = ?,
                difficulty = ?,
                sound_enabled = ?,
                music_enabled = ?,
                show_grid = ?,
                control_scheme = ?
            WHERE id = 1
        ''', (
            settings.get('player_name', 'Player'),
            settings.get('difficulty', 'medium'),
            settings.get('sound_enabled', 1),
            settings.get('music_enabled', 1),
            settings.get('show_grid', 1),
            settings.get('control_scheme', 'arrows')
        ))
        
        if self.cursor.rowcount == 0:
            self.cursor.execute('''
                INSERT INTO settings (player_name, difficulty, sound_enabled, 
                                     music_enabled, show_grid, control_scheme)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                settings.get('player_name', 'Player'),
                settings.get('difficulty', 'medium'),
                settings.get('sound_enabled', 1),
                settings.get('music_enabled', 1),
                settings.get('show_grid', 1),
                settings.get('control_scheme', 'arrows')
            ))
            
        self.conn.commit()
        
    def load_settings(self):
        """Загрузка настроек"""
        self.cursor.execute('SELECT * FROM settings WHERE id = 1')
        result = self.cursor.fetchone()
        
        if result:
            return {
                'player_name': result[2],
                'difficulty': result[3],
                'sound_enabled': bool(result[4]),
                'music_enabled': bool(result[5]),
                'show_grid': bool(result[6]),
                'control_scheme': result[7]
            }
        else:
            return {
                'player_name': 'Player',
                'difficulty': 'medium',
                'sound_enabled': True,
                'music_enabled': True,
                'show_grid': True,
                'control_scheme': 'arrows'
            }
            
    def unlock_achievement(self, achievement_name):
        """Разблокировка достижения"""
        self.cursor.execute('''
            UPDATE achievements
            SET unlocked = 1
            WHERE name = ? AND unlocked = 0
        ''', (achievement_name,))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False
        
    def get_achievements(self):
        """Получение всех достижений"""
        self.cursor.execute('SELECT name, description, unlocked FROM achievements')
        return self.cursor.fetchall()
        
    def __del__(self):
        """Закрытие соединения"""
        if hasattr(self, 'conn'):
            self.conn.close()

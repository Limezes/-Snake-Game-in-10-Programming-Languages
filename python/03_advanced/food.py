# food.py
# Классы еды

import random
import pygame
from config import *

class Food:
    def __init__(self, snake_positions, walls=None, food_type='normal'):
        self.type = food_type
        self.properties = FOOD_TYPES[food_type].copy()
        self.position = self.generate_position(snake_positions, walls)
        self.lifetime = 300 if food_type != 'normal' else None  # Кадров жизни для бонусной еды
        self.age = 0
        
    def generate_position(self, snake_positions, walls=None):
        """Генерация случайной позиции"""
        max_attempts = 1000
        attempts = 0
        
        while attempts < max_attempts:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            if (x, y) not in snake_positions:
                if walls is None or (x, y) not in walls:
                    return (x, y)
                    
            attempts += 1
            
        # Если не нашли свободное место, возвращаем None
        return None
        
    def update(self):
        """Обновление состояния еды"""
        if self.lifetime is not None:
            self.age += 1
            if self.age >= self.lifetime:
                return False  # Еда исчезла
        return True  # Еда еще существует
        
    def draw(self, screen, offset_x, offset_y):
        """Отрисовка еды"""
        if self.position is None:
            return
            
        x = offset_x + self.position[0] * CELL_SIZE
        y = offset_y + self.position[1] * CELL_SIZE
        
        # Эффект мигания для бонусной еды
        if self.lifetime and self.lifetime - self.age < 60:
            if (pygame.time.get_ticks() // 150) % 2:
                return
                
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        
        if self.type == 'normal':
            pygame.draw.rect(screen, self.properties['color'], rect)
            pygame.draw.circle(screen, YELLOW, 
                              (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 
                              CELL_SIZE // 3)
        elif self.type == 'bonus':
            # Звезда
            pygame.draw.rect(screen, self.properties['color'], rect)
            points = [
                (x + CELL_SIZE // 2, y + 2),
                (x + CELL_SIZE - 4, y + CELL_SIZE - 4),
                (x + 2, y + CELL_SIZE - 8)
            ]
            pygame.draw.polygon(screen, YELLOW, points)
        elif self.type == 'speed':
            # Молния
            pygame.draw.rect(screen, self.properties['color'], rect)
            lightning = [
                (x + CELL_SIZE // 2, y + 2),
                (x + CELL_SIZE - 4, y + CELL_SIZE // 2),
                (x + CELL_SIZE // 2 + 4, y + CELL_SIZE // 2 + 2),
                (x + CELL_SIZE // 2 - 4, y + CELL_SIZE - 4)
            ]
            pygame.draw.lines(screen, YELLOW, False, lightning, 3)
        elif self.type == 'slow':
            # Черепаха
            pygame.draw.rect(screen, self.properties['color'], rect)
            pygame.draw.ellipse(screen, YELLOW, 
                               (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8))
        elif self.type == 'golden':
            # Корона
            pygame.draw.rect(screen, self.properties['color'], rect)
            crown_points = [
                (x + CELL_SIZE // 2, y + 2),
                (x + 2, y + CELL_SIZE - 4),
                (x + CELL_SIZE - 2, y + CELL_SIZE - 4)
            ]
            pygame.draw.polygon(screen, YELLOW, crown_points)

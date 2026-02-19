# snake.py
# Класс змейки

import pygame
from config import *

class Snake:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.reset()
        
    def reset(self):
        """Сброс змейки"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        
        self.positions = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_flag = 0
        self.speed_modifier = 1.0
        self.speed_modifier_duration = 0
        self.invulnerable = False
        self.invulnerable_duration = 0
        
    def move(self):
        """Движение змейки"""
        # Применяем следующее направление, если оно не противоположное
        if (self.next_direction[0] != -self.direction[0] or 
            self.next_direction[1] != -self.direction[1]):
            self.direction = self.next_direction
            
        head = self.positions[0]
        x, y = head
        
        new_head = (x + self.direction[0], y + self.direction[1])
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если не нужно расти
        if self.grow_flag > 0:
            self.grow_flag -= 1
        else:
            self.positions.pop()
            
        # Обновление эффектов
        self.update_effects()
        
    def update_effects(self):
        """Обновление временных эффектов"""
        if self.speed_modifier_duration > 0:
            self.speed_modifier_duration -= 1
        else:
            self.speed_modifier = 1.0
            
        if self.invulnerable_duration > 0:
            self.invulnerable_duration -= 1
        else:
            self.invulnerable = False
            
    def grow(self, amount=1):
        """Увеличение длины змейки"""
        self.grow_flag += amount
        
    def change_direction(self, new_direction):
        """Изменение направления"""
        self.next_direction = new_direction
        
    def apply_speed_boost(self, multiplier, duration):
        """Применение ускорения"""
        self.speed_modifier = multiplier
        self.speed_modifier_duration = duration
        
    def apply_invulnerability(self, duration):
        """Применение неуязвимости"""
        self.invulnerable = True
        self.invulnerable_duration = duration
        
    def check_self_collision(self):
        """Проверка столкновения с собой"""
        if self.invulnerable:
            return False
        return self.positions[0] in self.positions[1:]
        
    def check_wall_collision(self, walls):
        """Проверка столкновения со стенами"""
        if self.invulnerable:
            return False
            
        head = self.positions[0]
        
        # Столкновение с границами
        if (head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
            
        # Столкновение со стенами уровня
        if head in walls:
            return True
            
        return False
        
    def draw(self, screen, offset_x, offset_y):
        """Отрисовка змейки"""
        for i, pos in enumerate(self.positions):
            x = offset_x + pos[0] * CELL_SIZE
            y = offset_y + pos[1] * CELL_SIZE
            
            # Выбор цвета (мигание при неуязвимости)
            if self.invulnerable and (pygame.time.get_ticks() // 200) % 2:
                color = WHITE
            else:
                color = GREEN if i == 0 else DARK_GREEN
                
            rect = pygame.Rect(x, y, CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
            # Глаза для головы
            if i == 0:
                eye_size = 3
                if self.direction == RIGHT:
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE - 6, y + 6), eye_size)
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE - 6, y + CELL_SIZE - 6), eye_size)
                elif self.direction == LEFT:
                    pygame.draw.circle(screen, BLACK, (x + 6, y + 6), eye_size)
                    pygame.draw.circle(screen, BLACK, (x + 6, y + CELL_SIZE - 6), eye_size)
                elif self.direction == UP:
                    pygame.draw.circle(screen, BLACK, (x + 6, y + 6), eye_size)
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE - 6, y + 6), eye_size)
                elif self.direction == DOWN:
                    pygame.draw.circle(screen, BLACK, (x + 6, y + CELL_SIZE - 6), eye_size)
                    pygame.draw.circle(screen, BLACK, (x + CELL_SIZE - 6, y + CELL_SIZE - 6), eye_size)

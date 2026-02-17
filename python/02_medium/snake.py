#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Змейка на Pygame с графическим интерфейсом
Управление: стрелки, пауза - пробел
"""

import pygame
import random
import sys
from config import *

class Snake:
    """Класс змейки"""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Сброс змейки к начальному состоянию"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow_flag = False
        
    def move(self):
        """Движение змейки"""
        head = self.positions[0]
        x, y = head
        
        if self.direction == RIGHT:
            x += CELL_SIZE
        elif self.direction == LEFT:
            x -= CELL_SIZE
        elif self.direction == UP:
            y -= CELL_SIZE
        elif self.direction == DOWN:
            y += CELL_SIZE
            
        new_head = (x, y)
        
        # Вставка новой головы
        self.positions.insert(0, new_head)
        
        # Удаление хвоста, если не нужно расти
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False
            
    def grow(self):
        """Увеличение длины змейки"""
        self.grow_flag = True
        
    def check_collision(self):
        """Проверка столкновения с собой"""
        return self.positions[0] in self.positions[1:]
        
    def change_direction(self, new_direction):
        """Изменение направления"""
        # Запрет разворота на 180 градусов
        if (new_direction == RIGHT and self.direction != LEFT) or \
           (new_direction == LEFT and self.direction != RIGHT) or \
           (new_direction == UP and self.direction != DOWN) or \
           (new_direction == DOWN and self.direction != UP):
            self.direction = new_direction
            
    def draw(self, screen):
        """Отрисовка змейки"""
        for i, pos in enumerate(self.positions):
            color = GREEN if i == 0 else DARK_GREEN  # Голова ярче
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Граница

class Food:
    """Класс еды"""
    
    def __init__(self, snake_positions):
        self.position = self.generate_position(snake_positions)
        self.color = RED
        
    def generate_position(self, snake_positions):
        """Генерация случайной позиции для еды"""
        while True:
            x = random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            
            if (x, y) not in snake_positions:
                return (x, y)
                
    def draw(self, screen):
        """Отрисовка еды"""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.circle(screen, YELLOW, 
                          (self.position[0] + CELL_SIZE // 2, 
                           self.position[1] + CELL_SIZE // 2), 
                          CELL_SIZE // 3)

class Game:
    """Основной класс игры"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Змейка - Версия 2.0")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        """Сброс игры"""
        self.snake = Snake()
        self.food = Food(self.snake.positions)
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_over = False
        self.paused = False
        self.high_score = self.load_high_score()
        
    def load_high_score(self):
        """Загрузка рекорда"""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except:
            return 0
            
    def save_high_score(self):
        """Сохранение рекорда"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
                
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                    
                if event.key == pygame.K_SPACE and not self.game_over:
                    self.paused = not self.paused
                    
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                    
                if not self.game_over and not self.paused:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(RIGHT)
                        
        return True
        
    def update(self):
        """Обновление состояния игры"""
        if self.game_over or self.paused:
            return
            
        self.snake.move()
        
        # Проверка столкновения со стенами
        head = self.snake.positions[0]
        if (head[0] < 0 or head[0] >= SCREEN_WIDTH or
            head[1] < 0 or head[1] >= SCREEN_HEIGHT):
            self.game_over = True
            self.save_high_score()
            return
            
        # Проверка столкновения с собой
        if self.snake.check_collision():
            self.game_over = True
            self.save_high_score()
            return
            
        # Проверка поедания еды
        if head == self.food.position:
            self.snake.grow()
            self.food = Food(self.snake.positions)
            self.score += 10
            
            # Увеличение скорости
            if self.speed < MAX_SPEED:
                self.speed += SPEED_INCREMENT
                
    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y), 1)
            
    def draw(self):
        """Отрисовка игры"""
        self.screen.fill(BLACK)
        
        # Сетка
        self.draw_grid()
        
        # Змейка и еда
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Информация
        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        high_score_text = self.small_font.render(f"Рекорд: {self.high_score}", True, WHITE)
        speed_text = self.small_font.render(f"Скорость: {int(self.speed)}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 50))
        self.screen.blit(speed_text, (10, 75))
        
        if self.paused:
            pause_text = self.font.render("ПАУЗА", True, YELLOW)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
            
        if self.game_over:
            # Затемнение экрана
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, RED)
            restart_text = self.small_font.render("Нажмите R для рестарта", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

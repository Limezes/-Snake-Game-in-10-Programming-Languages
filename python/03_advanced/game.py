# game.py
# Основной игровой класс

import pygame
import sys
import random
from enum import Enum
from config import *
from snake import Snake
from food import Food
from database import Database

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    HIGH_SCORES = 5
    SETTINGS = 6
    ACHIEVEMENTS = 7

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Змейка - Продвинутая версия")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.db = Database()
        self.settings = self.db.load_settings()
        
        self.state = GameState.MENU
        self.difficulty = self.settings['difficulty']
        self.player_name = self.settings['player_name']
        
        self.reset_game()
        self.load_sounds()
        
        self.animation_frame = 0
        self.particles = []
        
    def reset_game(self):
        """Сброс игры"""
        self.snake = Snake(self.difficulty)
        self.walls = self.generate_walls() if DIFFICULTY_LEVELS[self.difficulty]['walls'] else []
        self.foods = []
        self.bonus_timer = 0
        self.score = 0
        self.food_eaten = 0
        self.game_time = 0
        self.level = 1
        
        # Создание первой еды
        self.spawn_food('normal')
        
        # Настройки сложности
        diff_config = DIFFICULTY_LEVELS[self.difficulty]
        self.speed = diff_config['initial_speed']
        self.max_speed = diff_config['max_speed']
        self.speed_increment = diff_config['speed_increment']
        self.bonus_chance = diff_config['bonus_food_chance']
        
    def generate_walls(self):
        """Генерация стен для уровня"""
        walls = []
        
        if self.level == 1:
            # Простой уровень - стены по краям
            for x in range(GRID_WIDTH):
                walls.append((x, 0))
                walls.append((x, GRID_HEIGHT - 1))
            for y in range(GRID_HEIGHT):
                walls.append((0, y))
                walls.append((GRID_WIDTH - 1, y))
        elif self.level == 2:
            # Лабиринт
            for i in range(GRID_WIDTH // 4, GRID_WIDTH * 3 // 4):
                walls.append((i, GRID_HEIGHT // 2))
        elif self.level == 3:
            # Спираль
            center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
            for r in range(3, 10, 2):
                for x in range(center_x - r, center_x + r + 1):
                    walls.append((x, center_y - r))
                    walls.append((x, center_y + r))
                for y in range(center_y - r + 1, center_y + r):
                    walls.append((center_x - r, y))
                    walls.append((center_x + r, y))
                    
        return list(set(walls))  # Убираем дубликаты
        
    def spawn_food(self, food_type='normal'):
        """Создание еды"""
        food = Food(self.snake.positions, self.walls, food_type)
        if food.position is not None:
            self.foods.append(food)
            
    def load_sounds(self):
        """Загрузка звуков"""
        try:
            self.sounds = {
                'eat': pygame.mixer.Sound('sounds/eat.wav'),
                'bonus': pygame.mixer.Sound('sounds/bonus.wav'),
                'game_over': pygame.mixer.Sound('sounds/game_over.wav'),
                'level_up': pygame.mixer.Sound('sounds/level_up.wav')
            }
        except:
            self.sounds = {}
            
    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if self.settings['sound_enabled'] and sound_name in self.sounds:
            self.sounds[sound_name].play()
            
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    self.handle_menu_keys(event.key)
                elif self.state == GameState.PLAYING:
                    self.handle_game_keys(event.key)
                elif self.state == GameState.PAUSED:
                    self.handle_paused_keys(event.key)
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_keys(event.key)
                elif self.state == GameState.HIGH_SCORES:
                    self.handle_high_scores_keys(event.key)
                elif self.state == GameState.SETTINGS:
                    self.handle_settings_keys(event.key)
                elif self.state == GameState.ACHIEVEMENTS:
                    self.handle_achievements_keys(event.key)
                    
        return True
        
    def handle_menu_keys(self, key):
        """Обработка клавиш в меню"""
        if key == pygame.K_RETURN:
            self.state = GameState.PLAYING
            self.reset_game()
        elif key == pygame.K_h:
            self.state = GameState.HIGH_SCORES
        elif key == pygame.K_s:
            self.state = GameState.SETTINGS
        elif key == pygame.K_a:
            self.state = GameState.ACHIEVEMENTS
        elif key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    def handle_game_keys(self, key):
        """Обработка клавиш во время игры"""
        if key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED
        elif key == pygame.K_SPACE:
            self.state = GameState.PAUSED
        elif key == pygame.K_UP or key == pygame.K_w:
            self.snake.change_direction(UP)
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.snake.change_direction(DOWN)
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.snake.change_direction(LEFT)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.snake.change_direction(RIGHT)
            
    def handle_paused_keys(self, key):
        """Обработка клавиш на паузе"""
        if key == pygame.K_ESCAPE or key == pygame.K_SPACE:
            self.state = GameState.PLAYING
        elif key == pygame.K_m:
            self.state = GameState.MENU
            
    def handle_game_over_keys(self, key):
        """Обработка клавиш при окончании игры"""
        if key == pygame.K_r:
            self.reset_game()
            self.state = GameState.PLAYING
        elif key == pygame.K_m:
            self.state = GameState.MENU
        elif key == pygame.K_s:
            # Сохранение результата
            self.db.save_score(
                self.player_name,
                self.score,
                self.difficulty,
                self.game_time,
                self.food_eaten
            )
            self.state = GameState.HIGH_SCORES
            
    def handle_high_scores_keys(self, key):
        """Обработка клавиш в таблице рекордов"""
        if key == pygame.K_ESCAPE or key == pygame.K_m:
            self.state = GameState.MENU
            
    def handle_settings_keys(self, key):
        """Обработка клавиш в настройках"""
        if key == pygame.K_ESCAPE or key == pygame.K_m:
            self.db.save_settings(self.settings)
            self.state = GameState.MENU
        elif key == pygame.K_UP:
            self.cycle_difficulty(-1)
        elif key == pygame.K_DOWN:
            self.cycle_difficulty(1)
            
    def handle_achievements_keys(self, key):
        """Обработка клавиш в достижениях"""
        if key == pygame.K_ESCAPE or key == pygame.K_m:
            self.state = GameState.MENU
            
    def cycle_difficulty(self, direction):
        """Циклическое переключение сложности"""
        difficulties = list(DIFFICULTY_LEVELS.keys())
        current_index = difficulties.index(self.settings['difficulty'])
        new_index = (current_index + direction) % len(difficulties)
        self.settings['difficulty'] = difficulties[new_index]
        
    def update(self):
        """Обновление состояния игры"""
        if self.state != GameState.PLAYING:
            return
            
        self.game_time += 1
        self.animation_frame += 1
        
        # Движение змейки
        self.snake.move()
        
        # Проверка столкновений
        if self.snake.check_self_collision():
            self.game_over()
            return
            
        if self.snake.check_wall_collision(self.walls):
            self.game_over()
            return
            
        # Проверка поедания еды
        head = self.snake.positions[0]
        for food in self.foods[:]:
            if head == food.position:
                self.eat_food(food)
                self.foods.remove(food)
                break
                
        # Обновление еды
        for food in self.foods[:]:
            if not food.update():
                self.foods.remove(food)
                
        # Спавн новой еды
        if len(self.foods) < 3:
            if random.random() < 0.01:  # 1% шанс на бонусную еду
                food_type = random.choice(['bonus', 'speed', 'slow', 'golden'])
                self.spawn_food(food_type)
            else:
                self.spawn_food('normal')
                
        # Бонусная еда по таймеру
        self.bonus_timer += 1
        if self.bonus_timer > 500 and random.random() < self.bonus_chance:
            self.spawn_food('bonus')
            self.bonus_timer = 0
            
        # Обновление частиц
        self.update_particles()
        
    def eat_food(self, food):
        """Обработка поедания еды"""
        self.score += food.properties['points']
        self.food_eaten += 1
        self.play_sound('eat')
        
        # Эффект поедания
        self.create_particles(food.position)
        
        # Рост змейки
        self.snake.grow()
        
        # Специальные эффекты
        if food.type == 'speed':
            self.snake.apply_speed_boost(1.5, 100)
        elif food.type == 'slow':
            self.snake.apply_speed_boost(0.5, 100)
        elif food.type == 'golden':
            self.snake.apply_invulnerability(100)
            self.play_sound('bonus')
            
        # Увеличение скорости
        if self.speed < self.max_speed:
            self.speed += self.speed_increment
            
        # Проверка достижений
        self.check_achievements()
        
        # Повышение уровня
        if self.score > self.level * 200:
            self.level_up()
            
    def level_up(self):
        """Повышение уровня"""
        self.level += 1
        self.play_sound('level_up')
        
        if DIFFICULTY_LEVELS[self.difficulty]['walls']:
            self.walls = self.generate_walls()
            
    def check_achievements(self):
        """Проверка достижений"""
        if self.score >= 100:
            self.db.unlock_achievement('snake_master')
            
        if self.speed >= self.max_speed:
            self.db.unlock_achievement('speed_demon')
            
    def game_over(self):
        """Окончание игры"""
        self.state = GameState.GAME_OVER
        self.play_sound('game_over')
        
    def create_particles(self, position):
        """Создание частиц"""
        x = position[0] * CELL_SIZE + CELL_SIZE // 2
        y = position[1] * CELL_SIZE + CELL_SIZE // 2
        
        for _ in range(10):
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': 30,
                'color': random.choice([RED, YELLOW, ORANGE])
            })
            
    def update_particles(self):
        """Обновление частиц"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self):
        """Отрисовка частиц"""
        for particle in self.particles:
            alpha = particle['life'] / 30
            color = [int(c * alpha) for c in particle['color']]
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), 3)
            
    def draw_grid(self):
        """Отрисовка сетки"""
        if not self.settings['show_grid']:
            return
            
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
            
    def draw_walls(self):
        """Отрисовка стен"""
        for wall in self.walls:
            x = wall[0] * CELL_SIZE
            y = wall[1] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, DARK_GREEN, rect, 2)
            
    def draw_menu(self):
        """Отрисовка меню"""
        self.screen.fill(BLACK)
        
        title = self.font_large.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        options = [
            ("Нажмите ENTER", "Начать игру"),
            ("Нажмите H", "Таблица рекордов"),
            ("Нажмите S", "Настройки"),
            ("Нажмите A", "Достижения"),
            ("Нажмите ESC", "Выход")
        ]
        
        y = 300
        for key, desc in options:
            key_text = self.font_small.render(key, True, YELLOW)
            desc_text = self.font_small.render(desc, True, WHITE)
            
            key_rect = key_text.get_rect(right=SCREEN_WIDTH//2 - 20, y=y)
            desc_rect = desc_text.get_rect(left=SCREEN_WIDTH//2 + 20, y=y)
            
            self.screen.blit(key_text, key_rect)
            self.screen.blit(desc_text, desc_rect)
            
            y += 50
            
    def draw_game(self):
        """Отрисовка игры"""
        self.screen.fill(BLACK)
        
        self.draw_grid()
        self.draw_walls()
        self.snake.draw(self.screen, 0, 0)
        
        for food in self.foods:
            food.draw(self.screen, 0, 0)
            
        self.draw_particles()
        
        # Информация
        info_y = 10
        score_text = self.font_small.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, info_y))
        
        level_text = self.font_small.render(f"Уровень: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, info_y + 30))
        
        speed_text = self.font_small.render(f"Скорость: {int(self.speed)}", True, WHITE)
        self.screen.blit(speed_text, (10, info_y + 60))
        
        # Бонусы
        if self.snake.speed_modifier != 1.0:
            boost_text = self.font_small.render("УСКОРЕНИЕ!", True, BLUE)
            self.screen.blit(boost_text, (SCREEN_WIDTH - 150, info_y))
            
        if self.snake.invulnerable:
            inv_text = self.font_small.render("НЕУЯЗВИМ!", True, PURPLE)
            self.screen.blit(inv_text, (SCREEN_WIDTH - 150, info_y + 30))
            
    def draw_pause(self):
        """Отрисовка паузы"""
        # Затемнение экрана
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("ПАУЗА", True, YELLOW)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_small.render("Нажмите ПРОБЕЛ для продолжения", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        self.screen.blit(continue_text, continue_rect)
        
        menu_text = self.font_small.render("Нажмите M для выхода в меню", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
        self.screen.blit(menu_text, menu_rect)
        
    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        # Затемнение экрана
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("ИГРА ОКОНЧЕНА", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Счёт: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        self.screen.blit(score_text, score_rect)
        
        food_text = self.font_small.render(f"Съедено: {self.food_eaten}", True, WHITE)
        food_rect = food_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
        self.screen.blit(food_text, food_rect)
        
        time_text = self.font_small.render(f"Время: {self.game_time // 60} сек", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        self.screen.blit(time_text, time_rect)
        
        restart_text = self.font_small.render("Нажмите R для рестарта", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
        self.screen.blit(restart_text, restart_rect)
        
        save_text = self.font_small.render("Нажмите S для сохранения", True, YELLOW)
        save_rect = save_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
        self.screen.blit(save_text, save_rect)
        
        menu_text = self.font_small.render("Нажмите M для выхода в меню", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 160))
        self.screen.blit(menu_text, menu_rect)
        
    def draw_high_scores(self):
        """Отрисовка таблицы рекордов"""
        self.screen.fill(BLACK)
        
        title = self.font_large.render("ТАБЛИЦА РЕКОРДОВ", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Заголовки
        headers = ["Игрок", "Счёт", "Сложность", "Время", "Еда"]
        x_positions = [200, 350, 450, 600, 700]
        
        for i, header in enumerate(headers):
            text = self.font_small.render(header, True, YELLOW)
            self.screen.blit(text, (x_positions[i], 120))
            
        # Рекорды
        scores = self.db.get_high_scores(limit=15)
        y = 170
        
        for i, score in enumerate(scores):
            if i >= 10:
                break
                
            color = GREEN if i == 0 else WHITE
            
            name_text = self.font_small.render(score[0], True, color)
            self.screen.blit(name_text, (200, y))
            
            score_text = self.font_small.render(str(score[1]), True, color)
            self.screen.blit(score_text, (350, y))
            
            diff_text = self.font_small.render(score[2], True, color)
            self.screen.blit(diff_text, (450, y))
            
            time_text = self.font_small.render(f"{score[4]//60}c", True, color)
            self.screen.blit(time_text, (600, y))
            
            food_text = self.font_small.render(str(score[5]), True, color)
            self.screen.blit(food_text, (700, y))
            
            y += 35
            
        back_text = self.font_small.render("Нажмите ESC для возврата", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
        
    def draw_settings(self):
        """Отрисовка настроек"""
        self.screen.fill(BLACK)
        
        title = self.font_large.render("НАСТРОЙКИ", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        y = 150
        settings_items = [
            ("Игрок:", self.settings['player_name']),
            ("Сложность:", self.settings['difficulty'].capitalize()),
            ("Звук:", "Вкл" if self.settings['sound_enabled'] else "Выкл"),
            ("Музыка:", "Вкл" if self.settings['music_enabled'] else "Выкл"),
            ("Сетка:", "Вкл" if self.settings['show_grid'] else "Выкл"),
            ("Управление:", self.settings['control_scheme'])
        ]
        
        for label, value in settings_items:
            label_text = self.font_medium.render(label, True, WHITE)
            value_text = self.font_medium.render(str(value), True, YELLOW)
            
            label_rect = label_text.get_rect(right=SCREEN_WIDTH//2 - 20, y=y)
            value_rect = value_text.get_rect(left=SCREEN_WIDTH//2 + 20, y=y)
            
            self.screen.blit(label_text, label_rect)
            self.screen.blit(value_text, value_rect)
            
            y += 60
            
        back_text = self.font_small.render("Нажмите ESC для сохранения и возврата", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
        
    def draw_achievements(self):
        """Отрисовка достижений"""
        self.screen.fill(BLACK)
        
        title = self.font_large.render("ДОСТИЖЕНИЯ", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        achievements = self.db.get_achievements()
        y = 120
        
        for name, desc, unlocked in achievements:
            color = GREEN if unlocked else GRAY
            symbol = "✓" if unlocked else "○"
            
            name_text = self.font_medium.render(f"{symbol} {name}", True, color)
            desc_text = self.font_small.render(desc, True, WHITE)
            
            self.screen.blit(name_text, (50, y))
            self.screen.blit(desc_text, (50, y + 35))
            
            y += 70
            
        back_text = self.font_small.render("Нажмите ESC для возврата", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
        
    def draw(self):
        """Основная отрисовка"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()
        elif self.state == GameState.HIGH_SCORES:
            self.draw_high_scores()
        elif self.state == GameState.SETTINGS:
            self.draw_settings()
        elif self.state == GameState.ACHIEVEMENTS:
            self.draw_achievements()
            
        pygame.display.flip()
        
    def run(self):
        """Главный игровой цикл"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed * self.snake.speed_modifier)
            
        pygame.quit()
        sys.exit()

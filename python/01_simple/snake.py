#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простая консольная змейка с использованием библиотеки curses
Управление: стрелки или WASD, Q - выход
"""

import curses
import random
import time

class SimpleSnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_game()
        
    def setup_game(self):
        # Настройка экрана
        curses.curs_set(0)  # Скрыть курсор
        self.stdscr.nodelay(1)  # Неблокирующий ввод
        self.stdscr.timeout(100)  # Таймаут в миллисекундах
        
        # Цвета
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Змейка
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Еда
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Стены
        
        # Размеры поля
        self.height, self.width = self.stdscr.getmaxyx()
        self.height -= 2  # Оставляем место для информации
        self.width -= 2
        
        # Начальные параметры игры
        self.reset_game()
        
    def reset_game(self):
        """Сброс игры к начальному состоянию"""
        # Змейка
        self.snake = [
            [self.height // 2, self.width // 2],
            [self.height // 2, self.width // 2 - 1],
            [self.height // 2, self.width // 2 - 2]
        ]
        
        # Направление движения (вправо)
        self.direction = curses.KEY_RIGHT
        self.score = 0
        self.game_over = False
        
        # Создание еды
        self.create_food()
        
    def create_food(self):
        """Создание еды в случайном месте"""
        while True:
            self.food = [
                random.randint(1, self.height - 2),
                random.randint(1, self.width - 2)
            ]
            if self.food not in self.snake:
                break
                
    def draw_border(self):
        """Отрисовка границ поля"""
        for i in range(self.width + 1):
            self.stdscr.addch(0, i, '═', curses.color_pair(3))
            self.stdscr.addch(self.height, i, '═', curses.color_pair(3))
        
        for i in range(self.height + 1):
            self.stdscr.addch(i, 0, '║', curses.color_pair(3))
            self.stdscr.addch(i, self.width, '║', curses.color_pair(3))
        
        self.stdscr.addch(0, 0, '╔', curses.color_pair(3))
        self.stdscr.addch(0, self.width, '╗', curses.color_pair(3))
        self.stdscr.addch(self.height, 0, '╚', curses.color_pair(3))
        self.stdscr.addch(self.height, self.width, '╝', curses.color_pair(3))
        
    def draw(self):
        """Отрисовка всех элементов игры"""
        self.stdscr.clear()
        self.draw_border()
        
        # Отрисовка змейки
        for i, segment in enumerate(self.snake):
            if i == 0:  # Голова
                self.stdscr.addch(segment[0], segment[1], '●', curses.color_pair(1))
            else:
                self.stdscr.addch(segment[0], segment[1], '○', curses.color_pair(1))
        
        # Отрисовка еды
        self.stdscr.addch(self.food[0], self.food[1], '★', curses.color_pair(2))
        
        # Информация
        info = f" Счёт: {self.score} | Q - выход "
        self.stdscr.addstr(self.height + 1, 0, info, curses.color_pair(3))
        
        if self.game_over:
            game_over_msg = " ИГРА ОКОНЧЕНА! Нажмите R для рестарта "
            self.stdscr.addstr(self.height // 2, (self.width - len(game_over_msg)) // 2, 
                              game_over_msg, curses.A_BOLD)
        
        self.stdscr.refresh()
        
    def update(self):
        """Обновление состояния игры"""
        # Получение ввода
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            return False
            
        if self.game_over:
            if key == ord('r') or key == ord('R'):
                self.reset_game()
            return True
            
        # Изменение направления
        if key in [curses.KEY_UP, ord('w'), ord('W')] and self.direction != curses.KEY_DOWN:
            self.direction = curses.KEY_UP
        elif key in [curses.KEY_DOWN, ord('s'), ord('S')] and self.direction != curses.KEY_UP:
            self.direction = curses.KEY_DOWN
        elif key in [curses.KEY_LEFT, ord('a'), ord('A')] and self.direction != curses.KEY_RIGHT:
            self.direction = curses.KEY_LEFT
        elif key in [curses.KEY_RIGHT, ord('d'), ord('D')] and self.direction != curses.KEY_LEFT:
            self.direction = curses.KEY_RIGHT
            
        # Движение змейки
        head = self.snake[0].copy()
        
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
            
        # Проверка на столкновение со стенами
        if (head[0] <= 0 or head[0] >= self.height or
            head[1] <= 0 or head[1] >= self.width):
            self.game_over = True
            return True
            
        # Проверка на поедание еды
        if head == self.food:
            self.snake.insert(0, head)
            self.score += 10
            self.create_food()
        else:
            self.snake.insert(0, head)
            self.snake.pop()
            
        # Проверка на столкновение с собой
        if self.snake[0] in self.snake[1:]:
            self.game_over = True
            
        return True
        
    def run(self):
        """Главный игровой цикл"""
        running = True
        while running:
            running = self.update()
            self.draw()
            time.sleep(0.05)  # Небольшая задержка

def main(stdscr):
    game = SimpleSnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)

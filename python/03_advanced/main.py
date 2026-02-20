#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Snake Game - Продвинутая версия
Главный файл запуска
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game

def main():
    """Точка входа"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

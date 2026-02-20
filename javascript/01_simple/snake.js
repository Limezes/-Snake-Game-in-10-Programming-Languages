#!/usr/bin/env node

/**
 * Простая консольная змейка для Node.js
 * Управление: WASD, Q - выход
 * 
 * Запуск: node snake.js
 */

const readline = require('readline');

readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

class SimpleSnakeGame {
    constructor(width = 20, height = 10) {
        this.width = width;
        this.height = height;
        this.reset();
        this.setupInput();
    }

    reset() {
        // Создание змейки
        this.snake = [
            { x: Math.floor(this.width / 2), y: Math.floor(this.height / 2) }
        ];
        this.direction = 'RIGHT';
        this.nextDirection = 'RIGHT';
        this.score = 0;
        this.gameOver = false;
        this.gameLoop = null;
        
        // Создание еды
        this.createFood();
    }

    createFood() {
        while (true) {
            this.food = {
                x: Math.floor(Math.random() * this.width),
                y: Math.floor(Math.random() * this.height)
            };
            
            // Проверка, что еда не на змейке
            if (!this.snake.some(segment => 
                segment.x === this.food.x && segment.y === this.food.y)) {
                break;
            }
        }
    }

    setupInput() {
        process.stdin.on('keypress', (str, key) => {
            if (key.ctrl && key.name === 'c') {
                process.exit();
            }

            if (key.name === 'q') {
                process.exit();
            }

            if (this.gameOver) {
                if (key.name === 'r') {
                    this.reset();
                }
                return;
            }

            // Управление
            switch (key.name) {
                case 'w': this.nextDirection = 'UP'; break;
                case 's': this.nextDirection = 'DOWN'; break;
                case 'a': this.nextDirection = 'LEFT'; break;
                case 'd': this.nextDirection = 'RIGHT'; break;
            }
        });
    }

    move() {
        // Проверка и применение направления
        const opposite = {
            'UP': 'DOWN',
            'DOWN': 'UP',
            'LEFT': 'RIGHT',
            'RIGHT': 'LEFT'
        };

        if (this.nextDirection !== opposite[this.direction]) {
            this.direction = this.nextDirection;
        }

        // Новая голова
        const head = { ...this.snake[0] };
        
        switch (this.direction) {
            case 'UP': head.y--; break;
            case 'DOWN': head.y++; break;
            case 'LEFT': head.x--; break;
            case 'RIGHT': head.x++; break;
        }

        // Проверка столкновения со стенами
        if (head.x < 0 || head.x >= this.width || 
            head.y < 0 || head.y >= this.height) {
            this.gameOver = true;
            return;
        }

        // Добавление новой головы
        this.snake.unshift(head);

        // Проверка поедания еды
        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.createFood();
        } else {
            this.snake.pop();
        }

        // Проверка столкновения с собой
        const headCollision = this.snake.slice(1).some(segment => 
            segment.x === head.x && segment.y === head.y
        );

        if (headCollision) {
            this.gameOver = true;
        }
    }

    render() {
        console.clear();
        
        // Верхняя граница
        let output = '┌' + '─'.repeat(this.width) + '┐\n';

        // Игровое поле
        for (let y = 0; y < this.height; y++) {
            output += '│';
            for (let x = 0; x < this.width; x++) {
                if (this.snake[0].x === x && this.snake[0].y === y) {
                    output += '●'; // Голова
                } else if (this.snake.slice(1).some(s => s.x === x && s.y === y)) {
                    output += '○'; // Тело
                } else if (this.food.x === x && this.food.y === y) {
                    output += '★'; // Еда
                } else {
                    output += ' ';
                }
            }
            output += '│\n';
        }

        // Нижняя граница
        output += '└' + '─'.repeat(this.width) + '┘\n';
        
        // Информация
        output += `\n Счёт: ${this.score}\n`;
        output += ` Управление: WASD | Q - выход | R - рестарт\n`;

        if (this.gameOver) {
            output += `\n 🎮 ИГРА ОКОНЧЕНА! Нажмите R для рестарта\n`;
        }

        console.log(output);
    }

    start() {
        console.log('=== КОНСОЛЬНАЯ ЗМЕЙКА ===\n');
        this.gameLoop = setInterval(() => {
            if (!this.gameOver) {
                this.move();
            }
            this.render();
        }, 150);
    }
}

// Запуск игры
const game = new SimpleSnakeGame();
game.start();

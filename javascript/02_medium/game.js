/**
 * Змейка на Canvas
 * Управление: Стрелки или WASD
 */

class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.scoreElement = document.getElementById('score');
        this.highScoreElement = document.getElementById('highScore');
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.difficultySelect = document.getElementById('difficulty');
        
        // Размеры
        this.gridSize = 20;
        this.cellSize = this.canvas.width / this.gridSize;
        
        // Состояние игры
        this.reset();
        this.loadHighScore();
        this.setupEventListeners();
        this.draw();
    }
    
    reset() {
        this.snake = [
            { x: 10, y: 10 },
            { x: 9, y: 10 },
            { x: 8, y: 10 }
        ];
        this.direction = 'RIGHT';
        this.nextDirection = 'RIGHT';
        this.score = 0;
        this.gameOver = false;
        this.isRunning = false;
        this.isPaused = false;
        this.speed = this.getSpeedFromDifficulty();
        this.gameLoop = null;
        this.createFood();
        this.updateScore();
        
        // Обновление кнопок
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
        this.pauseBtn.textContent = 'Пауза';
    }
    
    getSpeedFromDifficulty() {
        const speeds = {
            'easy': 150,
            'medium': 100,
            'hard': 70
        };
        return speeds[this.difficultySelect.value];
    }
    
    createFood() {
        while (true) {
            this.food = {
                x: Math.floor(Math.random() * this.gridSize),
                y: Math.floor(Math.random() * this.gridSize)
            };
            
            if (!this.snake.some(segment => 
                segment.x === this.food.x && segment.y === this.food.y)) {
                break;
            }
        }
    }
    
    loadHighScore() {
        this.highScore = localStorage.getItem('snakeHighScore') || 0;
        this.highScoreElement.textContent = this.highScore;
    }
    
    saveHighScore() {
        if (this.score > this.highScore) {
            this.highScore = this.score;
            localStorage.setItem('snakeHighScore', this.highScore);
            this.highScoreElement.textContent = this.highScore;
        }
    }
    
    updateScore() {
        this.scoreElement.textContent = this.score;
    }
    
    setupEventListeners() {
        // Кнопки
        this.startBtn.addEventListener('click', () => this.start());
        this.pauseBtn.addEventListener('click', () => this.togglePause());
        this.resetBtn.addEventListener('click', () => this.reset());
        
        // Клавиатура
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Изменение сложности
        this.difficultySelect.addEventListener('change', () => {
            if (!this.isRunning) {
                this.speed = this.getSpeedFromDifficulty();
            }
        });
    }
    
    handleKeyPress(e) {
        const key = e.key.toLowerCase();
        
        // Пробел - пауза
        if (key === ' ') {
            e.preventDefault();
            if (this.isRunning) {
                this.togglePause();
            }
            return;
        }
        
        if (!this.isRunning || this.isPaused || this.gameOver) return;
        
        // Стрелки и WASD
        const keyMap = {
            'arrowup': 'UP', 'w': 'UP',
            'arrowdown': 'DOWN', 's': 'DOWN',
            'arrowleft': 'LEFT', 'a': 'LEFT',
            'arrowright': 'RIGHT', 'd': 'RIGHT'
        };
        
        if (keyMap[key]) {
            e.preventDefault();
            this.nextDirection = keyMap[key];
        }
    }
    
    start() {
        if (this.gameOver) {
            this.reset();
        }
        
        this.isRunning = true;
        this.isPaused = false;
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        
        if (this.gameLoop) {
            clearInterval(this.gameLoop);
        }
        
        this.gameLoop = setInterval(() => this.update(), this.speed);
    }
    
    togglePause() {
        if (!this.isRunning || this.gameOver) return;
        
        this.isPaused = !this.isPaused;
        this.pauseBtn.textContent = this.isPaused ? 'Продолжить' : 'Пауза';
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
        if (head.x < 0 || head.x >= this.gridSize || 
            head.y < 0 || head.y >= this.gridSize) {
            this.gameOver = true;
            return;
        }

        // Добавление новой головы
        this.snake.unshift(head);

        // Проверка поедания еды
        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.createFood();
            this.updateScore();
            
            // Проверка рекорда
            if (this.score > this.highScore) {
                this.saveHighScore();
            }
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
    
    update() {
        if (this.gameOver || this.isPaused || !this.isRunning) return;
        
        this.move();
        this.draw();
        
        if (this.gameOver) {
            clearInterval(this.gameLoop);
            this.gameLoop = null;
            this.isRunning = false;
            this.startBtn.disabled = false;
            this.pauseBtn.disabled = true;
            this.saveHighScore();
        }
    }
    
    draw() {
        // Очистка canvas
        this.ctx.fillStyle = '#2c3e50';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Рисование сетки
        this.ctx.strokeStyle = '#34495e';
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i <= this.gridSize; i++) {
            this.ctx.beginPath();
            this.ctx.moveTo(i * this.cellSize, 0);
            this.ctx.lineTo(i * this.cellSize, this.canvas.height);
            this.ctx.stroke();
            
            this.ctx.beginPath();
            this.ctx.moveTo(0, i * this.cellSize);
            this.ctx.lineTo(this.canvas.width, i * this.cellSize);
            this.ctx.stroke();
        }
        
        // Рисование змейки
        this.snake.forEach((segment, index) => {
            const x = segment.x * this.cellSize;
            const y = segment.y * this.cellSize;
            const padding = index === 0 ? 2 : 4; // Голова больше
            
            // Градиент для головы
            if (index === 0) {
                const gradient = this.ctx.createRadialGradient(
                    x + this.cellSize/2, y + this.cellSize/2, 2,
                    x + this.cellSize/2, y + this.cellSize/2, this.cellSize/2
                );
                gradient.addColorStop(0, '#27ae60');
                gradient.addColorStop(1, '#229954');
                
                this.ctx.fillStyle = gradient;
            } else {
                this.ctx.fillStyle = index % 2 === 0 ? '#27ae60' : '#229954';
            }
            
            this.ctx.fillRect(
                x + padding/2, 
                y + padding/2, 
                this.cellSize - padding, 
                this.cellSize - padding
            );
            
            // Глаза для головы
            if (index === 0) {
                this.ctx.fillStyle = 'white';
                const eyeSize = 3;
                
                if (this.direction === 'RIGHT') {
                    this.ctx.fillRect(x + this.cellSize - 8, y + 5, eyeSize, eyeSize);
                    this.ctx.fillRect(x + this.cellSize - 8, y + this.cellSize - 8, eyeSize, eyeSize);
                } else if (this.direction === 'LEFT') {
                    this.ctx.fillRect(x + 5, y + 5, eyeSize, eyeSize);
                    this.ctx.fillRect(x + 5, y + this.cellSize - 8, eyeSize, eyeSize);
                } else if (this.direction === 'UP') {
                    this.ctx.fillRect(x + 5, y + 5, eyeSize, eyeSize);
                    this.ctx.fillRect(x + this.cellSize - 8, y + 5, eyeSize, eyeSize);
                } else if (this.direction === 'DOWN') {
                    this.ctx.fillRect(x + 5, y + this.cellSize - 8, eyeSize, eyeSize);
                    this.ctx.fillRect(x + this.cellSize - 8, y + this.cellSize - 8, eyeSize, eyeSize);
                }
            }
        });
        
        // Рисование еды
        if (this.food) {
            const x = this.food.x * this.cellSize;
            const y = this.food.y * this.cellSize;
            
            // Градиент для еды
            const gradient = this.ctx.createRadialGradient(
                x + this.cellSize/2, y + this.cellSize/2, 2,
                x + this.cellSize/2, y + this.cellSize/2, this.cellSize/2
            );
            gradient.addColorStop(0, '#e74c3c');
            gradient.addColorStop(1, '#c0392b');
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(
                x + this.cellSize/2, 
                y + this.cellSize/2, 
                this.cellSize/2 - 2, 
                0, 
                Math.PI * 2
            );
            this.ctx.fill();
            
            // Блик
            this.ctx.fillStyle = 'rgba(255,255,255,0.5)';
            this.ctx.beginPath();
            this.ctx.arc(
                x + this.cellSize/2 - 2, 
                y + this.cellSize/2 - 2, 
                2, 
                0, 
                Math.PI * 2
            );
            this.ctx.fill();
        }
        
        // Сообщение о конце игры
        if (this.gameOver) {
            this.ctx.fillStyle = 'rgba(0,0,0,0.7)';
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.ctx.fillStyle = 'white';
            this.ctx.font = 'bold 24px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('ИГРА ОКОНЧЕНА', this.canvas.width/2, this.canvas.height/2);
            
            this.ctx.font = '16px Arial';
            this.ctx.fillText(`Счёт: ${this.score}`, this.canvas.width/2, this.canvas.height/2 + 40);
        }
    }
}

// Запуск игры после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});


#include "../include/snake.h"
#include <iostream>
#include <cstdlib>
#include <thread>
#include <chrono>
#include <conio.h>
#include <random>

using namespace std;

SnakeGame::SnakeGame() {
    reset();
}

void SnakeGame::reset() {
    snake.clear();
    snake.push_back({WIDTH / 2, HEIGHT / 2});
    snake.push_back({WIDTH / 2 - 1, HEIGHT / 2});
    snake.push_back({WIDTH / 2 - 2, HEIGHT / 2});
    
    dir = RIGHT;
    nextDir = RIGHT;
    score = 0;
    gameOver = false;
    running = true;
    
    createFood();
}

void SnakeGame::createFood() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> disX(0, WIDTH - 1);
    uniform_int_distribution<> disY(0, HEIGHT - 1);
    
    do {
        food = {disX(gen), disY(gen)};
    } while (find(snake.begin(), snake.end(), food) != snake.end());
}

void SnakeGame::move() {
    // Проверка направления
    if ((dir == UP && nextDir != DOWN) ||
        (dir == DOWN && nextDir != UP) ||
        (dir == LEFT && nextDir != RIGHT) ||
        (dir == RIGHT && nextDir != LEFT)) {
        dir = nextDir;
    }
    
    // Новая голова
    auto head = snake.front();
    
    switch (dir) {
        case UP:    head.second--; break;
        case DOWN:  head.second++; break;
        case LEFT:  head.first--; break;
        case RIGHT: head.first++; break;
    }
    
    // Проверка столкновения со стенами
    if (head.first < 0 || head.first >= WIDTH || 
        head.second < 0 || head.second >= HEIGHT) {
        gameOver = true;
        return;
    }
    
    // Добавление новой головы
    snake.push_front(head);
    
    // Проверка поедания еды
    if (head == food) {
        score += 10;
        createFood();
    } else {
        snake.pop_back();
    }
    
    // Проверка столкновения с собой
    for (size_t i = 1; i < snake.size(); i++) {
        if (snake[i] == head) {
            gameOver = true;
            break;
        }
    }
}

void SnakeGame::clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void SnakeGame::render() {
    clearScreen();
    
    cout << "=== КОНСОЛЬНАЯ ЗМЕЙКА НА C++ ===\n\n";
    
    // Верхняя граница
    cout << "┌";
    for (int i = 0; i < WIDTH; i++) cout << "─";
    cout << "┐\n";
    
    // Игровое поле
    for (int y = 0; y < HEIGHT; y++) {
        cout << "│";
        for (int x = 0; x < WIDTH; x++) {
            auto head = snake.front();
            if (head.first == x && head.second == y) {
                cout << "●"; // Голова
            } else if (find(snake.begin() + 1, snake.end(), make_pair(x, y)) != snake.end()) {
                cout << "○"; // Тело
            } else if (food.first == x && food.second == y) {
                cout << "★"; // Еда
            } else {
                cout << " ";
            }
        }
        cout << "│\n";
    }
    
    // Нижняя граница
    cout << "└";
    for (int i = 0; i < WIDTH; i++) cout << "─";
    cout << "┘\n";
    
    // Информация
    cout << "\n Счёт: " << score << "\n";
    cout << " Управление: WASD | Q - выход | R - рестарт\n";
    
    if (gameOver) {
        cout << "\n 🎮 ИГРА ОКОНЧЕНА! Нажмите R для рестарта\n";
    }
}

void SnakeGame::handleInput(char key) {
    if (key == 'q' || key == 'Q') {
        running = false;
        return;
    }
    
    if (gameOver) {
        if (key == 'r' || key == 'R') {
            reset();
        }
        return;
    }
    
    switch (key) {
        case 'w': case 'W': nextDir = UP; break;
        case 's': case 'S': nextDir = DOWN; break;
        case 'a': case 'A': nextDir = LEFT; break;
        case 'd': case 'D': nextDir = RIGHT; break;
    }
}

void SnakeGame::start() {
    cout << "=== КОНСОЛЬНАЯ ЗМЕЙКА НА C++ ===\n";
    cout << "Нажмите любую клавишу для начала...\n";
    _getch();
    
    while (running) {
        if (!gameOver) {
            move();
        }
        render();
        
        // Проверка ввода
        if (_kbhit()) {
            char key = _getch();
            handleInput(key);
        }
        
        this_thread::sleep_for(chrono::milliseconds(INITIAL_SPEED));
    }
}

int main() {
    SnakeGame game;
    game.start();
    return 0;
}

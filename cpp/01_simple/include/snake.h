#ifndef SNAKE_H
#define SNAKE_H

#include <deque>
#include <utility>

class SnakeGame {
private:
    static const int WIDTH = 20;
    static const int HEIGHT = 10;
    static const int INITIAL_SPEED = 150;
    
    std::deque<std::pair<int, int>> snake;
    std::pair<int, int> food;
    enum Direction { UP, DOWN, LEFT, RIGHT } dir, nextDir;
    int score;
    bool gameOver;
    bool running;
    
    void createFood();
    void move();
    void render();
    void handleInput(char key);
    void clearScreen();
    
public:
    SnakeGame();
    void reset();
    void start();
};

#endif // SNAKE_H

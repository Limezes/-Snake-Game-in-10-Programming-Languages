#include "../include/Game.h"
#include <iostream>
#include <random>

Game::Game() 
    : window(sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT), "Snake Game - SFML"),
      level(1),
      speed(100.0f),
      gameOver(false),
      paused(false) {
    
    window.setFramerateLimit(60);
    
    // Загрузка шрифта
    if (!font.loadFromFile("resources/fonts/arial.ttf")) {
        std::cerr << "Не удалось загрузить шрифт!\n";
    }
    
    // Настройка текста
    scoreText.setFont(font);
    scoreText.setCharacterSize(24);
    scoreText.setFillColor(sf::Color::White);
    scoreText.setPosition(10, WINDOW_HEIGHT - 80);
    
    levelText.setFont(font);
    levelText.setCharacterSize(24);
    levelText.setFillColor(sf::Color::White);
    levelText.setPosition(10, WINDOW_HEIGHT - 50);
    
    gameOverText.setFont(font);
    gameOverText.setCharacterSize(48);
    gameOverText.setFillColor(sf::Color::Red);
    gameOverText.setString("GAME OVER");
    gameOverText.setPosition(
        WINDOW_WIDTH / 2 - gameOverText.getLocalBounds().width / 2,
        WINDOW_HEIGHT / 2 - 50
    );
    
    reset();
}

void Game::reset() {
    snake.reset();
    food.respawn({snake.getBody().begin(), snake.getBody().end()});
    scoreManager.resetScore();
    level = 1;
    speed = 100.0f;
    gameOver = false;
}

void Game::processEvents() {
    sf::Event event;
    while (window.pollEvent(event)) {
        if (event.type == sf::Event::Closed) {
            window.close();
        }
        
        if (event.type == sf::Event::KeyPressed) {
            if (event.key.code == sf::Keyboard::Escape) {
                window.close();
            }
            
            if (event.key.code == sf::Keyboard::Space) {
                if (gameOver) {
                    reset();
                } else {
                    paused = !paused;
                }
            }
            
            if (!gameOver && !paused) {
                switch (event.key.code) {
                    case sf::Keyboard::Up:
                    case sf::Keyboard::W:
                        snake.setDirection(Snake::UP);
                        break;
                    case sf::Keyboard::Down:
                    case sf::Keyboard::S:
                        snake.setDirection(Snake::DOWN);
                        break;
                    case sf::Keyboard::Left:
                    case sf::Keyboard::A:
                        snake.setDirection(Snake::LEFT);
                        break;
                    case sf::Keyboard::Right:
                    case sf::Keyboard::D:
                        snake.setDirection(Snake::RIGHT);
                        break;
                }
            }
        }
    }
}

void Game::update() {
    if (gameOver || paused) return;
    
    snake.updateEffects();
    snake.move();
    
    // Проверка столкновения со стенами
    auto head = snake.getHead();
    if (head.x < 0 || head.x >= GRID_SIZE || 
        head.y < 0 || head.y >= GRID_SIZE) {
        gameOver = true;
        return;
    }
    
    // Проверка столкновения с едой
    if (head == food.getPosition()) {
        snake.grow();
        scoreManager.addScore(food.getPoints());
        
        // Проверка повышения уровня
        if (scoreManager.getCurrentScore() / 100 + 1 > level) {
            levelUp();
        }
        
        food.respawn({snake.getBody().begin(), snake.getBody().end()});
    }
    
    // Проверка столкновения с собой
    if (snake.checkSelfCollision() && !snake.isInvincible()) {
        gameOver = true;
    }
    
    // Обновление еды
    food.update();
    if (food.isExpired()) {
        food.respawn({snake.getBody().begin(), snake.getBody().end()});
    }
}

void Game::levelUp() {
    level++;
    if (speed > 30) {
        speed -= 10;
    }
}

void Game::render() {
    window.clear(sf::Color(30, 30, 40));
    
    // Рисование сетки
    sf::RectangleShape gridLine(sf::Vector2f(1, WINDOW_HEIGHT - 100));
    gridLine.setFillColor(sf::Color(50, 50, 70));
    
    for (int i = 0; i <= GRID_SIZE; i++) {
        gridLine.setPosition(i * CELL_SIZE, 0);
        window.draw(gridLine);
    }
    
    gridLine.setSize(sf::Vector2f(WINDOW_WIDTH, 1));
    for (int i = 0; i <= GRID_SIZE; i++) {
        gridLine.setPosition(0, i * CELL_SIZE);
        window.draw(gridLine);
    }
    
    // Рисование змейки
    snake.draw(window, CELL_SIZE);
    
    // Рисование еды
    food.draw(window, CELL_SIZE);
    
    // Обновление текста
    scoreText.setString("Счёт: " + std::to_string(scoreManager.getCurrentScore()));
    levelText.setString("Уровень: " + std::to_string(level) + 
                       " | Скорость: " + std::to_string(static_cast<int>(1000.0f / speed)));
    
    window.draw(scoreText);
    window.draw(levelText);
    
    if (gameOver) {
        window.draw(gameOverText);
        
        sf::Text restartText;
        restartText.setFont(font);
        restartText.setCharacterSize(24);
        restartText.setFillColor(sf::Color::White);
        restartText.setString("Нажмите ПРОБЕЛ для рестарта");
        restartText.setPosition(
            WINDOW_WIDTH / 2 - restartText.getLocalBounds().width / 2,
            WINDOW_HEIGHT / 2 + 20
        );
        window.draw(restartText);
    } else if (paused) {
        sf::Text pauseText;
        pauseText.setFont(font);
        pauseText.setCharacterSize(48);
        pauseText.setFillColor(sf::Color::Yellow);
        pauseText.setString("ПАУЗА");
        pauseText.setPosition(
            WINDOW_WIDTH / 2 - pauseText.getLocalBounds().width / 2,
            WINDOW_HEIGHT / 2 - 50
        );
        window.draw(pauseText);
    }
    
    window.display();
}

void Game::run() {
    sf::Clock clock;
    
    while (window.isOpen()) {
        processEvents();
        
        if (clock.getElapsedTime().asMilliseconds() > speed / snake.getSpeedMultiplier()) {
            update();
            clock.restart();
        }
        
        render();
    }
}

int main() {
    Game game;
    game.run();
    return 0;
}

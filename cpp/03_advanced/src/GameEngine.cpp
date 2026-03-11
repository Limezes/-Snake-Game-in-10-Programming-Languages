#include "../include/GameEngine.h"
#include <QDateTime>

GameEngine::GameEngine(QObject *parent) 
    : QObject(parent),
      difficulty(Difficulty::MEDIUM),
      state(GameState::MENU),
      score(0),
      level(1),
      highScore(0),
      foodEaten(0) {
    
    // Настройка таймеров
    gameTimer.setInterval(100); // Базовая скорость
    connect(&gameTimer, &QTimer::timeout, this, &GameEngine::update);
    
    powerUpTimer.setInterval(5000); // Спавн power-up каждые 5 секунд
    connect(&powerUpTimer, &QTimer::timeout, this, &GameEngine::spawnPowerUp);
    
    // Загрузка звуков
    eatSound.setSource(QUrl::fromLocalFile(":/sounds/eat.wav"));
    gameOverSound.setSource(QUrl::fromLocalFile(":/sounds/gameover.wav"));
    levelUpSound.setSource(QUrl::fromLocalFile(":/sounds/levelup.wav"));
    
    eatSound.setVolume(50);
    gameOverSound.setVolume(50);
    levelUpSound.setVolume(50);
}

void GameEngine::startGame() {
    snake.reset();
    foods.clear();
    walls.clear();
    powerUps.clear();
    
    score = 0;
    level = 1;
    foodEaten = 0;
    
    generateWalls();
    spawnFood();
    
    state = GameState::PLAYING;
    gameTimer.start();
    powerUpTimer.start();
    
    emit gameStateChanged(state);
}

void GameEngine::pauseGame() {
    if (state == GameState::PLAYING) {
        state = GameState::PAUSED;
        gameTimer.stop();
        powerUpTimer.stop();
        emit gameStateChanged(state);
    }
}

void GameEngine::resumeGame() {
    if (state == GameState::PAUSED) {
        state = GameState::PLAYING;
        gameTimer.start();
        powerUpTimer.start();
        emit gameStateChanged(state);
    }
}

void GameEngine::restartGame() {
    startGame();
}

void GameEngine::setDifficulty(Difficulty diff) {
    difficulty = diff;
    
    switch (diff) {
        case Difficulty::EASY:
            gameTimer.setInterval(150);
            break;
        case Difficulty::MEDIUM:
            gameTimer.setInterval(100);
            break;
        case Difficulty::HARD:
            gameTimer.setInterval(70);
            break;
        case Difficulty::EXPERT:
            gameTimer.setInterval(50);
            break;
    }
}

void GameEngine::generateWalls() {
    if (difficulty == Difficulty::EASY || difficulty == Difficulty::MEDIUM) {
        return;
    }
    
    // Генерация стен в зависимости от уровня
    for (int i = 0; i < level * 2; i++) {
        int x = QRandomGenerator::global()->bounded(GRID_WIDTH);
        int y = QRandomGenerator::global()->bounded(GRID_HEIGHT);
        
        if (!snake.checkPosition(QPoint(x, y))) {
            walls.append(Wall(x, y));
        }
    }
}

void GameEngine::spawnFood() {
    QVector<QPoint> occupied = snake.getBody();
    
    for (const auto& wall : walls) {
        occupied.append(wall.getPosition());
    }
    
    Food food;
    food.respawn(occupied);
    foods.append(food);
}

void GameEngine::spawnPowerUp() {
    if (powerUps.size() < 3 && QRandomGenerator::global()->bounded(100) < 30) {
        QVector<QPoint> occupied = snake.getBody();
        
        for (const auto& wall : walls) {
            occupied.append(wall.getPosition());
        }
        
        for (const auto& food : foods) {
            occupied.append(food.getPosition());
        }
        
        PowerUp powerUp;
        powerUp.spawn(occupied);
        powerUps.append(powerUp);
    }
}

void GameEngine::moveSnake(Direction dir) {
    if (state != GameState::PLAYING) return;
    
    snake.setDirection(dir);
}

void GameEngine::update() {
    snake.updateEffects();
    snake.move();
    
    checkCollisions();
    
    // Обновление еды
    for (auto& food : foods) {
        food.update();
    }
    
    // Удаление просроченной еды
    foods.erase(std::remove_if(foods.begin(), foods.end(),
        [](const Food& f) { return f.isExpired(); }), foods.end());
    
    // Обновление power-ups
    for (auto& powerUp : powerUps) {
        powerUp.update();
    }
    
    powerUps.erase(std::remove_if(powerUps.begin(), powerUps.end(),
        [](const PowerUp& p) { return p.isExpired(); }), powerUps.end());
    
    // Спавн новой еды при необходимости
    if (foods.size() < 3) {
        spawnFood();
    }
}

void GameEngine::checkCollisions() {
    QPoint head = snake.getHead();
    
    // Проверка стен
    if (head.x() < 0 || head.x() >= GRID_WIDTH || 
        head.y() < 0 || head.y() >= GRID_HEIGHT) {
        gameOver();
        return;
    }
    
    // Проверка столкновения со стенами
    for (const auto& wall : walls) {
        if (wall.getPosition() == head) {
            gameOver();
            return;
        }
    }
    
    // Проверка еды
    for (auto it = foods.begin(); it != foods.end();) {
        if (it->getPosition() == head) {
            snake.grow();
            score += it->getPoints();
            foodEaten++;
            eatSound.play();
            
            emit scoreChanged(score);
            emit foodEaten(*it);
            
            // Применение эффекта еды
            switch (it->getType()) {
                case FoodType::SPEED:
                    snake.setSpeedMultiplier(1.5f, 300);
                    break;
                case FoodType::SLOW:
                    snake.setSpeedMultiplier(0.5f, 300);
                    break;
                case FoodType::GOLDEN:
                    snake.setInvincible(true, 500);
                    break;
                default:
                    break;
            }
            
            it = foods.erase(it);
            
            // Проверка повышения уровня
            if (score > level * 100) {
                levelUp();
            }
        } else {
            ++it;
        }
    }
    
    // Проверка power-ups
    for (auto it = powerUps.begin(); it != powerUps.end();) {
        if (it->getPosition() == head) {
            emit powerUpCollected(*it);
            
            // Применение эффекта power-up
            switch (it->getType()) {
                case PowerUpType::SPEED_BOOST:
                    snake.setSpeedMultiplier(2.0f, it->getDuration());
                    break;
                case PowerUpType::INVINCIBILITY:
                    snake.setInvincible(true, it->getDuration());
                    break;
                case PowerUpType::SLOW_TIME:
                    snake.setSpeedMultiplier(0.3f, it->getDuration());
                    break;
                case PowerUpType::EXTRA_LIFE:
                    // Дополнительная жизнь
                    break;
                case PowerUpType::SCORE_MULTIPLIER:
                    score *= 2;
                    emit scoreChanged(score);
                    break;
            }
            
            it = powerUps.erase(it);
        } else {
            ++it;
        }
    }
    
    // Проверка столкновения с собой
    if (snake.checkSelfCollision()) {
        gameOver();
    }
}

void GameEngine::levelUp() {
    level++;
    levelUpSound.play();
    emit levelChanged(level);
    
    // Увеличение сложности
    if (difficulty == Difficulty::HARD || difficulty == Difficulty::EXPERT) {
        generateWalls();
    }
    
    if (gameTimer.interval() > 30) {
        gameTimer.setInterval(gameTimer.interval() - 5);
    }
}

void GameEngine::gameOver() {
    state = GameState::GAME_OVER;
    gameTimer.stop();
    powerUpTimer.stop();
    gameOverSound.play();
    
    if (score > highScore) {
        highScore = score;
    }
    
    emit gameStateChanged(state);
}

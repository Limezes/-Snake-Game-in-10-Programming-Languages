#include "../include/Snake.h"
#include <random>

Snake::Snake() : color(sf::Color::Green), invincible(false), 
                 speedMultiplier(1.0f), invincibleTimer(0), speedTimer(0) {
    reset();
}

void Snake::reset() {
    body.clear();
    body.push_back({10, 10});
    body.push_back({9, 10});
    body.push_back({8, 10});
    dir = RIGHT;
    nextDir = RIGHT;
    invincible = false;
    speedMultiplier = 1.0f;
    invincibleTimer = 0;
    speedTimer = 0;
}

void Snake::move() {
    // Проверка направления
    if ((dir == UP && nextDir != DOWN) ||
        (dir == DOWN && nextDir != UP) ||
        (dir == LEFT && nextDir != RIGHT) ||
        (dir == RIGHT && nextDir != LEFT)) {
        dir = nextDir;
    }
    
    // Новая голова
    sf::Vector2i head = body.front();
    
    switch (dir) {
        case UP:    head.y--; break;
        case DOWN:  head.y++; break;
        case LEFT:  head.x--; break;
        case RIGHT: head.x++; break;
    }
    
    // Добавление новой головы
    body.push_front(head);
    body.pop_back();
}

void Snake::grow() {
    body.push_back(body.back());
}

void Snake::setDirection(Direction newDir) {
    nextDir = newDir;
}

void Snake::setInvincible(bool inv, int duration) {
    invincible = inv;
    invincibleTimer = duration;
}

void Snake::setSpeedMultiplier(float mult, int duration) {
    speedMultiplier = mult;
    speedTimer = duration;
}

void Snake::updateEffects() {
    if (invincibleTimer > 0) {
        invincibleTimer--;
        if (invincibleTimer <= 0) {
            invincible = false;
        }
    }
    
    if (speedTimer > 0) {
        speedTimer--;
        if (speedTimer <= 0) {
            speedMultiplier = 1.0f;
        }
    }
}

bool Snake::checkSelfCollision() const {
    if (invincible) return false;
    
    auto head = body.front();
    for (size_t i = 1; i < body.size(); i++) {
        if (body[i] == head) {
            return true;
        }
    }
    return false;
}

bool Snake::checkPosition(const sf::Vector2i& pos) const {
    for (const auto& segment : body) {
        if (segment == pos) {
            return true;
        }
    }
    return false;
}

void Snake::draw(sf::RenderWindow& window, int cellSize) const {
    for (size_t i = 0; i < body.size(); i++) {
        sf::RectangleShape rect(sf::Vector2f(cellSize - 2, cellSize - 2));
        rect.setPosition(body[i].x * cellSize + 1, body[i].y * cellSize + 1);
        
        if (i == 0) {
            // Голова
            if (invincible) {
                float pulse = (sinf(invincibleTimer * 0.1f) + 1.0f) * 0.5f;
                rect.setFillColor(sf::Color(255, 255, 0, 255 * pulse));
            } else {
                rect.setFillColor(sf::Color(50, 255, 50));
            }
            rect.setOutlineColor(sf::Color::White);
            rect.setOutlineThickness(1);
        } else {
            // Тело
            float opacity = 1.0f - (i * 0.05f);
            if (opacity < 0.3f) opacity = 0.3f;
            rect.setFillColor(sf::Color(0, 200, 0, 255 * opacity));
        }
        
        window.draw(rect);
        
        // Глаза для головы
        if (i == 0) {
            sf::CircleShape eye(2);
            eye.setFillColor(sf::Color::White);
            
            switch (dir) {
                case RIGHT:
                    eye.setPosition(body[i].x * cellSize + cellSize - 8, 
                                   body[i].y * cellSize + 5);
                    window.draw(eye);
                    eye.setPosition(body[i].x * cellSize + cellSize - 8, 
                                   body[i].y * cellSize + cellSize - 9);
                    window.draw(eye);
                    break;
                case LEFT:
                    eye.setPosition(body[i].x * cellSize + 4, 
                                   body[i].y * cellSize + 5);
                    window.draw(eye);
                    eye.setPosition(body[i].x * cellSize + 4, 
                                   body[i].y * cellSize + cellSize - 9);
                    window.draw(eye);
                    break;
                case UP:
                    eye.setPosition(body[i].x * cellSize + 5, 
                                   body[i].y * cellSize + 4);
                    window.draw(eye);
                    eye.setPosition(body[i].x * cellSize + cellSize - 9, 
                                   body[i].y * cellSize + 4);
                    window.draw(eye);
                    break;
                case DOWN:
                    eye.setPosition(body[i].x * cellSize + 5, 
                                   body[i].y * cellSize + cellSize - 8);
                    window.draw(eye);
                    eye.setPosition(body[i].x * cellSize + cellSize - 9, 
                                   body[i].y * cellSize + cellSize - 8);
                    window.draw(eye);
                    break;
            }
        }
    }
}

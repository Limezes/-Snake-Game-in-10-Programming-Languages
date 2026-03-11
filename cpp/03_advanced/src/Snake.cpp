#include "../include/Snake.h"
#include <QRandomGenerator>

Snake::Snake() : direction(Direction::RIGHT), nextDirection(Direction::RIGHT),
                 invincible(false), speedMultiplier(1.0f),
                 invincibleTimer(0), speedTimer(0),
                 color(50, 200, 50), headColor(50, 255, 50) {
    reset();
}

void Snake::reset() {
    body.clear();
    body.append(QPoint(10, 10));
    body.append(QPoint(9, 10));
    body.append(QPoint(8, 10));
    
    direction = Direction::RIGHT;
    nextDirection = Direction::RIGHT;
    invincible = false;
    speedMultiplier = 1.0f;
    invincibleTimer = 0;
    speedTimer = 0;
}

void Snake::move() {
    // Проверка направления
    if ((direction == Direction::UP && nextDirection != Direction::DOWN) ||
        (direction == Direction::DOWN && nextDirection != Direction::UP) ||
        (direction == Direction::LEFT && nextDirection != Direction::RIGHT) ||
        (direction == Direction::RIGHT && nextDirection != Direction::LEFT)) {
        direction = nextDirection;
    }
    
    // Новая голова
    QPoint head = body.first();
    
    switch (direction) {
        case Direction::UP:    head.ry()--; break;
        case Direction::DOWN:  head.ry()++; break;
        case Direction::LEFT:  head.rx()--; break;
        case Direction::RIGHT: head.rx()++; break;
    }
    
    // Добавление новой головы
    body.prepend(head);
    body.removeLast();
}

void Snake::grow() {
    body.append(body.last());
}

void Snake::setDirection(Direction dir) {
    nextDirection = dir;
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
    
    QPoint head = body.first();
    for (int i = 1; i < body.size(); i++) {
        if (body[i] == head) {
            return true;
        }
    }
    return false;
}

bool Snake::checkPosition(const QPoint& pos) const {
    return body.contains(pos);
}

bool Snake::checkHeadPosition(const QPoint& pos) const {
    return !body.isEmpty() && body.first() == pos;
}

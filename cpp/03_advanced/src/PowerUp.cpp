#include "../include/PowerUp.h"
#include <QRandomGenerator>

PowerUp::PowerUp() : duration(0), lifetime(300), age(0) {}

void PowerUp::spawn(const QVector<QPoint>& occupiedPositions) {
    int maxAttempts = 100;
    
    do {
        position.rx() = QRandomGenerator::global()->bounded(20);
        position.ry() = QRandomGenerator::global()->bounded(20);
    } while (occupiedPositions.contains(position) && maxAttempts-- > 0);
    
    // Случайный тип power-up
    int r = QRandomGenerator::global()->bounded(5);
    type = static_cast<PowerUpType>(r);
    
    switch (type) {
        case PowerUpType::SPEED_BOOST:
            color = QColor(0, 255, 255);
            duration = 500;
            break;
        case PowerUpType::INVINCIBILITY:
            color = QColor(255, 255, 0);
            duration = 500;
            break;
        case PowerUpType::SLOW_TIME:
            color = QColor(255, 0, 255);
            duration = 500;
            break;
        case PowerUpType::EXTRA_LIFE:
            color = QColor(255, 100, 100);
            duration = 0;
            break;
        case PowerUpType::SCORE_MULTIPLIER:
            color = QColor(255, 200, 0);
            duration = 0;
            break;
    }
    
    age = 0;
}

void PowerUp::update() {
    age++;
}

bool PowerUp::isExpired() const {
    return age >= lifetime;
}

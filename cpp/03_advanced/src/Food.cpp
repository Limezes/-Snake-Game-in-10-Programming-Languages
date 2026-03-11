#include "../include/Food.h"
#include <QRandomGenerator>

Food::Food() : type(FoodType::NORMAL), points(10), 
               color(255, 50, 50), lifetime(0), age(0) {}

void Food::respawn(const QVector<QPoint>& occupiedPositions) {
    int maxAttempts = 100;
    
    do {
        position.rx() = QRandomGenerator::global()->bounded(20);
        position.ry() = QRandomGenerator::global()->bounded(20);
    } while (occupiedPositions.contains(position) && maxAttempts-- > 0);
    
    // Случайный тип еды
    int r = QRandomGenerator::global()->bounded(100);
    
    if (r < 70) {
        type = FoodType::NORMAL;
        points = 10;
        color = QColor(255, 50, 50);
        lifetime = 0;
    } else if (r < 85) {
        type = FoodType::BONUS;
        points = 50;
        color = QColor(255, 215, 0);
        lifetime = 300;
    } else if (r < 93) {
        type = FoodType::SPEED;
        points = 20;
        color = QColor(50, 150, 255);
        lifetime = 0;
    } else if (r < 98) {
        type = FoodType::SLOW;
        points = 20;
        color = QColor(150, 50, 255);
        lifetime = 0;
    } else {
        type = FoodType::GOLDEN;
        points = 100;
        color = QColor(255, 215, 0);
        lifetime = 0;
    }
    
    age = 0;
}

void Food::update() {
    if (lifetime > 0) {
        age++;
    }
}

bool Food::isExpired() const {
    return lifetime > 0 && age >= lifetime;
}

#ifndef FOOD_H
#define FOOD_H

#include <QPoint>
#include <QColor>

enum class FoodType {
    NORMAL,
    BONUS,
    SPEED,
    SLOW,
    GOLDEN
};

class Food {
private:
    QPoint position;
    FoodType type;
    int points;
    QColor color;
    int lifetime;
    int age;
    
public:
    Food();
    
    void respawn(const QVector<QPoint>& occupiedPositions);
    void update();
    bool isExpired() const;
    
    // Геттеры
    QPoint getPosition() const { return position; }
    FoodType getType() const { return type; }
    int getPoints() const { return points; }
    QColor getColor() const { return color; }
    
    // Сеттеры
    void setPosition(const QPoint& pos) { position = pos; }
};

#endif // FOOD_H

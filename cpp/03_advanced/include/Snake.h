#ifndef SNAKE_H
#define SNAKE_H

#include <QVector>
#include <QPoint>
#include <QColor>

enum class Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT
};

class Snake {
private:
    QVector<QPoint> body;
    Direction direction;
    Direction nextDirection;
    
    bool invincible;
    float speedMultiplier;
    int invincibleTimer;
    int speedTimer;
    
    QColor color;
    QColor headColor;

public:
    Snake();
    
    void reset();
    void move();
    void grow();
    void setDirection(Direction dir);
    void setInvincible(bool inv, int duration);
    void setSpeedMultiplier(float mult, int duration);
    void updateEffects();
    
    // Геттеры
    const QVector<QPoint>& getBody() const { return body; }
    QPoint getHead() const { return body.isEmpty() ? QPoint() : body.first(); }
    Direction getDirection() const { return direction; }
    bool isInvincible() const { return invincible; }
    float getSpeedMultiplier() const { return speedMultiplier; }
    QColor getColor() const { return color; }
    QColor getHeadColor() const { return headColor; }
    
    // Проверки
    bool checkSelfCollision() const;
    bool checkPosition(const QPoint& pos) const;
    bool checkHeadPosition(const QPoint& pos) const;
};

#endif // SNAKE_H

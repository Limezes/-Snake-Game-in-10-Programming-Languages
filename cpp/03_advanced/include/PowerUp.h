#ifndef POWERUP_H
#define POWERUP_H

#include <QPoint>
#include <QColor>

enum class PowerUpType {
    SPEED_BOOST,
    INVINCIBILITY,
    SLOW_TIME,
    EXTRA_LIFE,
    SCORE_MULTIPLIER
};

class PowerUp {
private:
    QPoint position;
    PowerUpType type;
    QColor color;
    int duration;
    int lifetime;
    int age;
    
public:
    PowerUp();
    
    void spawn(const QVector<QPoint>& occupiedPositions);
    void update();
    bool isExpired() const;
    
    // Геттеры
    QPoint getPosition() const { return position; }
    PowerUpType getType() const { return type; }
    QColor getColor() const { return color; }
    int getDuration() const { return duration; }
};

#endif // POWERUP_H

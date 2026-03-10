#ifndef WALL_H
#define WALL_H

#include <QPoint>
#include <QColor>

class Wall {
private:
    QPoint position;
    QColor color;
    bool destructible;

public:
    Wall(int x, int y, bool destructible = false);
    
    QPoint getPosition() const { return position; }
    QColor getColor() const { return color; }
    bool isDestructible() const { return destructible; }
    void setDestructible(bool d) { destructible = d; }
};

#endif // WALL_H

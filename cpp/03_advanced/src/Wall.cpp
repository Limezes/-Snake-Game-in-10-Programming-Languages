#include "../include/Wall.h"

Wall::Wall(int x, int y, bool destructible) 
    : position(x, y), destructible(destructible) {
    
    if (destructible) {
        color = QColor(150, 100, 50);
    } else {
        color = QColor(100, 100, 120);
    }
}

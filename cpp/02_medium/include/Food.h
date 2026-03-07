
#ifndef FOOD_H
#define FOOD_H

#include <SFML/Graphics.hpp>
#include <vector>

enum class FoodType {
    NORMAL,
    BONUS,
    SPEED,
    SLOW,
    GOLDEN
};

class Food {
private:
    sf::Vector2i position;
    FoodType type;
    int points;
    sf::Color color;
    float lifetime;
    float age;
    
public:
    Food();
    void respawn(const std::vector<sf::Vector2i>& occupiedPositions);
    void update();
    bool isExpired() const;
    
    sf::Vector2i getPosition() const { return position; }
    int getPoints() const { return points; }
    FoodType getType() const { return type; }
    void draw(sf::RenderWindow& window, int cellSize) const;
};

#endif // FOOD_H

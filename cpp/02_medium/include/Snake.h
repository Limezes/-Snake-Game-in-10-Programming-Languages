#ifndef SNAKE_H
#define SNAKE_H

#include <SFML/Graphics.hpp>
#include <deque>

class Snake {
private:
    std::deque<sf::Vector2i> body;
    enum Direction { UP, DOWN, LEFT, RIGHT } dir, nextDir;
    sf::Color color;
    bool invincible;
    float speedMultiplier;
    int invincibleTimer;
    int speedTimer;
    
public:
    Snake();
    void reset();
    void move();
    void grow();
    void setDirection(Direction newDir);
    void setInvincible(bool inv, int duration);
    void setSpeedMultiplier(float mult, int duration);
    void updateEffects();
    
    const std::deque<sf::Vector2i>& getBody() const { return body; }
    sf::Vector2i getHead() const { return body.front(); }
    bool checkSelfCollision() const;
    bool checkPosition(const sf::Vector2i& pos) const;
    void draw(sf::RenderWindow& window, int cellSize) const;
    
    bool isInvincible() const { return invincible; }
    float getSpeedMultiplier() const { return speedMultiplier; }
};

#endif // SNAKE_H

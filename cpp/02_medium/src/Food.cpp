#include "../include/Food.h"
#include <random>

Food::Food() : type(FoodType::NORMAL), points(10), 
               color(sf::Color::Red), lifetime(0), age(0) {
    respawn({});
}

void Food::respawn(const std::vector<sf::Vector2i>& occupiedPositions) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static std::uniform_int_distribution<> dis(0, 19);
    
    do {
        position.x = dis(gen);
        position.y = dis(gen);
    } while (std::find(occupiedPositions.begin(), occupiedPositions.end(), 
                       position) != occupiedPositions.end());
    
    // Случайный тип еды
    static std::uniform_real_distribution<> chance(0.0, 1.0);
    float r = chance(gen);
    
    if (r < 0.7f) {
        type = FoodType::NORMAL;
        points = 10;
        color = sf::Color::Red;
        lifetime = 0;
    } else if (r < 0.85f) {
        type = FoodType::BONUS;
        points = 50;
        color = sf::Color::Yellow;
        lifetime = 300; // 5 секунд при 60 FPS
    } else if (r < 0.93f) {
        type = FoodType::SPEED;
        points = 20;
        color = sf::Color::Cyan;
        lifetime = 0;
    } else if (r < 0.98f) {
        type = FoodType::SLOW;
        points = 20;
        color = sf::Color::Magenta;
        lifetime = 0;
    } else {
        type = FoodType::GOLDEN;
        points = 100;
        color = sf::Color(255, 215, 0);
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

void Food::draw(sf::RenderWindow& window, int cellSize) const {
    sf::CircleShape shape(cellSize / 2 - 2);
    shape.setPosition(position.x * cellSize + 2, position.y * cellSize + 2);
    
    // Пульсация для бонусной еды
    if (type == FoodType::BONUS) {
        float pulse = (sinf(age * 0.1f) + 1.0f) * 0.5f;
        sf::Color c = color;
        c.a = 255 * pulse;
        shape.setFillColor(c);
    } else {
        shape.setFillColor(color);
    }
    
    window.draw(shape);
    
    // Символ для особой еды
    sf::Font font;
    font.loadFromFile("resources/fonts/arial.ttf");
    
    sf::Text text;
    text.setFont(font);
    text.setCharacterSize(14);
    text.setFillColor(sf::Color::White);
    
    switch (type) {
        case FoodType::BONUS:
            text.setString("★");
            break;
        case FoodType::SPEED:
            text.setString("⚡");
            break;
        case FoodType::SLOW:
            text.setString("🐢");
            break;
        case FoodType::GOLDEN:
            text.setString("👑");
            break;
        default:
            return;
    }
    
    text.setPosition(position.x * cellSize + cellSize / 3,
                     position.y * cellSize + cellSize / 4);
    window.draw(text);
}

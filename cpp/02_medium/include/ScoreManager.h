#ifndef SCORE_MANAGER_H
#define SCORE_MANAGER_H

#include <string>

class ScoreManager {
private:
    int currentScore;
    int highScore;
    std::string playerName;
    
    void loadHighScore();
    void saveHighScore();
    
public:
    ScoreManager();
    
    void addScore(int points);
    void resetScore();
    int getCurrentScore() const { return currentScore; }
    int getHighScore() const { return highScore; }
    void setPlayerName(const std::string& name) { playerName = name; }
};

#endif // SCORE_MANAGER_H

#include "../include/ScoreManager.h"
#include <fstream>
#include <iostream>

ScoreManager::ScoreManager() : currentScore(0), highScore(0) {
    loadHighScore();
}

void ScoreManager::loadHighScore() {
    std::ifstream file("highscore.txt");
    if (file.is_open()) {
        file >> highScore;
        file.close();
    }
}

void ScoreManager::saveHighScore() {
    std::ofstream file("highscore.txt");
    if (file.is_open()) {
        file << highScore;
        file.close();
    }
}

void ScoreManager::addScore(int points) {
    currentScore += points;
    if (currentScore > highScore) {
        highScore = currentScore;
        saveHighScore();
    }
}

void ScoreManager::resetScore() {
    currentScore = 0;
}

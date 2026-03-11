
#include "../include/SettingsManager.h"

SettingsManager::SettingsManager(QObject *parent) 
    : QObject(parent), settings("MyCompany", "SnakeGame") {}

GameEngine::Difficulty SettingsManager::getDifficulty() const {
    return static_cast<GameEngine::Difficulty>(
        settings.value("difficulty", static_cast<int>(GameEngine::Difficulty::MEDIUM)).toInt()
    );
}

void SettingsManager::setDifficulty(GameEngine::Difficulty difficulty) {
    settings.setValue("difficulty", static_cast<int>(difficulty));
}

QString SettingsManager::getPlayerName() const {
    return settings.value("player_name", "Player").toString();
}

void SettingsManager::setPlayerName(const QString& name) {
    settings.setValue("player_name", name);
}

bool SettingsManager::isSoundEnabled() const {
    return settings.value("sound_enabled", true).toBool();
}

void SettingsManager::setSoundEnabled(bool enabled) {
    settings.setValue("sound_enabled", enabled);
}

bool SettingsManager::isMusicEnabled() const {
    return settings.value("music_enabled", true).toBool();
}

void SettingsManager::setMusicEnabled(bool enabled) {
    settings.setValue("music_enabled", enabled);
}

int SettingsManager::getSoundVolume() const {
    return settings.value("sound_volume", 50).toInt();
}

void SettingsManager::setSoundVolume(int volume) {
    settings.setValue("sound_volume", qBound(0, volume, 100));
}

QString SettingsManager::getUpKey() const {
    return settings.value("up_key", "Up").toString();
}

QString SettingsManager::getDownKey() const {
    return settings.value("down_key", "Down").toString();
}

QString SettingsManager::getLeftKey() const {
    return settings.value("left_key", "Left").toString();
}

QString SettingsManager::getRightKey() const {
    return settings.value("right_key", "Right").toString();
}

void SettingsManager::setControlKeys(const QString& up, const QString& down, 
                                      const QString& left, const QString& right) {
    settings.setValue("up_key", up);
    settings.setValue("down_key", down);
    settings.setValue("left_key", left);
    settings.setValue("right_key", right);
}

QColor SettingsManager::getSnakeColor() const {
    return settings.value("snake_color", QColor(50, 255, 50)).value<QColor>();
}

void SettingsManager::setSnakeColor(const QColor& color) {
    settings.setValue("snake_color", color);
}

QColor SettingsManager::getBackgroundColor() const {
    return settings.value("background_color", QColor(30, 30, 40)).value<QColor>();
}

void SettingsManager::setBackgroundColor(const QColor& color) {
    settings.setValue("background_color", color);
}

bool SettingsManager::isGridVisible() const {
    return settings.value("grid_visible", true).toBool();
}

void SettingsManager::setGridVisible(bool visible) {
    settings.setValue("grid_visible", visible);
}

int SettingsManager::getHighScore() const {
    return settings.value("high_score", 0).toInt();
}

void SettingsManager::setHighScore(int score) {
    if (score > getHighScore()) {
        settings.setValue("high_score", score);
    }
}

int SettingsManager::getTotalPlayTime() const {
    return settings.value("total_play_time", 0).toInt();
}

void SettingsManager::setTotalPlayTime(int seconds) {
    settings.setValue("total_play_time", seconds);
}

void SettingsManager::resetToDefaults() {
    settings.clear();
}

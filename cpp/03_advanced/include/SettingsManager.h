#ifndef SETTINGSMANAGER_H
#define SETTINGSMANAGER_H

#include <QObject>
#include <QSettings>
#include "GameEngine.h"

class SettingsManager : public QObject {
    Q_OBJECT

private:
    QSettings settings;
    
public:
    explicit SettingsManager(QObject *parent = nullptr);
    
    // Настройки игры
    GameEngine::Difficulty getDifficulty() const;
    void setDifficulty(GameEngine::Difficulty difficulty);
    
    QString getPlayerName() const;
    void setPlayerName(const QString& name);
    
    bool isSoundEnabled() const;
    void setSoundEnabled(bool enabled);
    
    bool isMusicEnabled() const;
    void setMusicEnabled(bool enabled);
    
    int getSoundVolume() const;
    void setSoundVolume(int volume);
    
    // Управление
    QString getUpKey() const;
    QString getDownKey() const;
    QString getLeftKey() const;
    QString getRightKey() const;
    void setControlKeys(const QString& up, const QString& down, 
                        const QString& left, const QString& right);
    
    // Внешний вид
    QColor getSnakeColor() const;
    void setSnakeColor(const QColor& color);
    
    QColor getBackgroundColor() const;
    void setBackgroundColor(const QColor& color);
    
    bool isGridVisible() const;
    void setGridVisible(bool visible);
    
    // Статистика
    int getHighScore() const;
    void setHighScore(int score);
    
    int getTotalPlayTime() const;
    void setTotalPlayTime(int seconds);
    
    // Сброс
    void resetToDefaults();
};

#endif // SETTINGSMANAGER_H

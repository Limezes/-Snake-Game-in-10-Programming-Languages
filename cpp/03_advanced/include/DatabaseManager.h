#ifndef DATABASEMANAGER_H
#define DATABASEMANAGER_H

#include <QObject>
#include <QtSql>
#include <QVector>
#include <QMap>

struct HighScore {
    int id;
    QString playerName;
    int score;
    int level;
    QString difficulty;
    QDateTime date;
    int foodEaten;
};

struct Achievement {
    QString name;
    QString description;
    bool unlocked;
    QDateTime unlockedDate;
};

class DatabaseManager : public QObject {
    Q_OBJECT

private:
    QSqlDatabase db;
    
    bool createTables();
    void insertDefaultAchievements();

public:
    explicit DatabaseManager(QObject *parent = nullptr);
    ~DatabaseManager();
    
    bool openDatabase(const QString& path);
    void closeDatabase();
    
    // Рекорды
    bool saveScore(const QString& playerName, int score, int level, 
                   const QString& difficulty, int foodEaten);
    QVector<HighScore> getHighScores(int limit = 10);
    int getPlayerRank(int score);
    
    // Достижения
    bool unlockAchievement(const QString& name);
    QVector<Achievement> getAchievements();
    bool isAchievementUnlocked(const QString& name);
    
    // Статистика
    QMap<QString, int> getStatistics();
    int getTotalGames();
    int getAverageScore();
    
signals:
    void databaseError(const QString& error);
};

#endif // DATABASEMANAGER_H

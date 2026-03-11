#include "../include/DatabaseManager.h"
#include <QSqlQuery>
#include <QSqlError>
#include <QVariant>

DatabaseManager::DatabaseManager(QObject *parent) : QObject(parent) {
    db = QSqlDatabase::addDatabase("QSQLITE");
}

DatabaseManager::~DatabaseManager() {
    closeDatabase();
}

bool DatabaseManager::openDatabase(const QString& path) {
    db.setDatabaseName(path);
    
    if (!db.open()) {
        emit databaseError("Не удалось открыть базу данных: " + db.lastError().text());
        return false;
    }
    
    return createTables();
}

void DatabaseManager::closeDatabase() {
    if (db.isOpen()) {
        db.close();
    }
}

bool DatabaseManager::createTables() {
    QSqlQuery query;
    
    // Таблица рекордов
    bool success = query.exec(
        "CREATE TABLE IF NOT EXISTS high_scores ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "player_name TEXT NOT NULL,"
        "score INTEGER NOT NULL,"
        "level INTEGER NOT NULL,"
        "difficulty TEXT NOT NULL,"
        "date DATETIME DEFAULT CURRENT_TIMESTAMP,"
        "food_eaten INTEGER DEFAULT 0"
        ")"
    );
    
    if (!success) {
        emit databaseError("Ошибка создания таблицы high_scores: " + query.lastError().text());
        return false;
    }
    
    // Таблица достижений
    success = query.exec(
        "CREATE TABLE IF NOT EXISTS achievements ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "name TEXT UNIQUE,"
        "description TEXT,"
        "unlocked BOOLEAN DEFAULT 0,"
        "unlocked_date DATETIME"
        ")"
    );
    
    if (!success) {
        emit databaseError("Ошибка создания таблицы achievements: " + query.lastError().text());
        return false;
    }
    
    // Таблица статистики
    success = query.exec(
        "CREATE TABLE IF NOT EXISTS statistics ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "total_games INTEGER DEFAULT 0,"
        "total_score INTEGER DEFAULT 0,"
        "total_food INTEGER DEFAULT 0,"
        "total_play_time INTEGER DEFAULT 0"
        ")"
    );
    
    if (!success) {
        emit databaseError("Ошибка создания таблицы statistics: " + query.lastError().text());
        return false;
    }
    
    insertDefaultAchievements();
    return true;
}

void DatabaseManager::insertDefaultAchievements() {
    QVector<QPair<QString, QString>> achievements = {
        {"first_food", "Съесть первое яблоко"},
        {"score_100", "Набрать 100 очков"},
        {"score_500", "Набрать 500 очков"},
        {"score_1000", "Набрать 1000 очков"},
        {"level_5", "Достичь 5 уровня"},
        {"level_10", "Достичь 10 уровня"},
        {"speed_demon", "Достичь максимальной скорости"},
        {"invincible", "Съесть 10 бонусов подряд"},
        {"wall_killer", "Пройти уровень со стенами"},
        {"golden_feast", "Съесть 5 золотых яблок"}
    };
    
    QSqlQuery query;
    query.prepare("INSERT OR IGNORE INTO achievements (name, description) VALUES (?, ?)");
    
    for (const auto& ach : achievements) {
        query.addBindValue(ach.first);
        query.addBindValue(ach.second);
        query.exec();
    }
}

bool DatabaseManager::saveScore(const QString& playerName, int score, int level, 
                                 const QString& difficulty, int foodEaten) {
    QSqlQuery query;
    query.prepare(
        "INSERT INTO high_scores (player_name, score, level, difficulty, food_eaten) "
        "VALUES (?, ?, ?, ?, ?)"
    );
    
    query.addBindValue(playerName);
    query.addBindValue(score);
    query.addBindValue(level);
    query.addBindValue(difficulty);
    query.addBindValue(foodEaten);
    
    if (!query.exec()) {
        emit databaseError("Ошибка сохранения результата: " + query.lastError().text());
        return false;
    }
    
    // Обновление статистики
    query.exec("SELECT total_games, total_score, total_food FROM statistics WHERE id = 1");
    
    if (query.next()) {
        int totalGames = query.value(0).toInt() + 1;
        int totalScore = query.value(1).toInt() + score;
        int totalFood = query.value(2).toInt() + foodEaten;
        
        query.prepare(
            "UPDATE statistics SET total_games = ?, total_score = ?, total_food = ? "
            "WHERE id = 1"
        );
        query.addBindValue(totalGames);
        query.addBindValue(totalScore);
        query.addBindValue(totalFood);
        query.exec();
    } else {
        query.prepare(
            "INSERT INTO statistics (id, total_games, total_score, total_food) "
            "VALUES (1, 1, ?, ?)"
        );
        query.addBindValue(score);
        query.addBindValue(foodEaten);
        query.exec();
    }
    
    return true;
}

QVector<HighScore> DatabaseManager::getHighScores(int limit) {
    QVector<HighScore> scores;
    
    QSqlQuery query;
    query.prepare(
        "SELECT id, player_name, score, level, difficulty, date, food_eaten "
        "FROM high_scores ORDER BY score DESC LIMIT ?"
    );
    query.addBindValue(limit);
    
    if (query.exec()) {
        while (query.next()) {
            HighScore hs;
            hs.id = query.value(0).toInt();
            hs.playerName = query.value(1).toString();
            hs.score = query.value(2).toInt();
            hs.level = query.value(3).toInt();
            hs.difficulty = query.value(4).toString();
            hs.date = query.value(5).toDateTime();
            hs.foodEaten = query.value(6).toInt();
            scores.append(hs);
        }
    }
    
    return scores;
}

int DatabaseManager::getPlayerRank(int score) {
    QSqlQuery query;
    query.prepare("SELECT COUNT(*) + 1 FROM high_scores WHERE score > ?");
    query.addBindValue(score);
    
    if (query.exec() && query.next()) {
        return query.value(0).toInt();
    }
    
    return -1;
}

bool DatabaseManager::unlockAchievement(const QString& name) {
    QSqlQuery query;
    query.prepare(
        "UPDATE achievements SET unlocked = 1, unlocked_date = CURRENT_TIMESTAMP "
        "WHERE name = ? AND unlocked = 0"
    );
    query.addBindValue(name);
    
    return query.exec() && query.numRowsAffected() > 0;
}

QVector<Achievement> DatabaseManager::getAchievements() {
    QVector<Achievement> achievements;
    
    QSqlQuery query("SELECT name, description, unlocked, unlocked_date FROM achievements");
    
    while (query.next()) {
        Achievement ach;
        ach.name = query.value(0).toString();
        ach.description = query.value(1).toString();
        ach.unlocked = query.value(2).toBool();
        ach.unlockedDate = query.value(3).toDateTime();
        achievements.append(ach);
    }
    
    return achievements;
}

bool DatabaseManager::isAchievementUnlocked(const QString& name) {
    QSqlQuery query;
    query.prepare("SELECT unlocked FROM achievements WHERE name = ?");
    query.addBindValue(name);
    
    if (query.exec() && query.next()) {
        return query.value(0).toBool();
    }
    
    return false;
}

QMap<QString, int> DatabaseManager::getStatistics() {
    QMap<QString, int> stats;
    
    QSqlQuery query("SELECT total_games, total_score, total_food FROM statistics WHERE id = 1");
    
    if (query.next()) {
        stats["total_games"] = query.value(0).toInt();
        stats["total_score"] = query.value(1).toInt();
        stats["total_food"] = query.value(2).toInt();
    } else {
        stats["total_games"] = 0;
        stats["total_score"] = 0;
        stats["total_food"] = 0;
    }
    
    // Средний счет
    if (stats["total_games"] > 0) {
        stats["average_score"] = stats["total_score"] / stats["total_games"];
    } else {
        stats["average_score"] = 0;
    }
    
    return stats;
}

int DatabaseManager::getTotalGames() {
    QSqlQuery query("SELECT COUNT(*) FROM high_scores");
    
    if (query.next()) {
        return query.value(0).toInt();
    }
    
    return 0;
}

int DatabaseManager::getAverageScore() {
    QSqlQuery query("SELECT AVG(score) FROM high_scores");
    
    if (query.next()) {
        return query.value(0).toInt();
    }
    
    return 0;
}

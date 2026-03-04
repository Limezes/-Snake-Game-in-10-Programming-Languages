package com.snake.utils;

import java.sql.*;
import java.util.*;

public class DatabaseManager {
    private Connection connection;
    
    public DatabaseManager() {
        try {
            connection = DriverManager.getConnection("jdbc:sqlite:snake.db");
            createTables();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    private void createTables() throws SQLException {
        // Таблица рекордов
        Statement stmt = connection.createStatement();
        stmt.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """);
        
        // Таблица достижений
        stmt.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                unlocked BOOLEAN DEFAULT 0,
                unlocked_date TIMESTAMP
            )
        """);
        
        // Таблица настроек
        stmt.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """);
        
        // Вставка начальных достижений
        insertInitialAchievements();
    }
    
    private void insertInitialAchievements() {
        String[][] achievements = {
            {"first_food", "Съесть первое яблоко"},
            {"score_100", "Набрать 100 очков"},
            {"score_500", "Набрать 500 очков"},
            {"level_5", "Достичь 5 уровня"},
            {"speed_demon", "Достичь максимальной скорости"},
            {"invincible", "Съесть 10 бонусов подряд"},
            {"wall_killer", "Пройти уровень со стенами"},
            {"golden_feast", "Съесть 5 золотых яблок"}
        };
        
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "INSERT OR IGNORE INTO achievements (name, description) VALUES (?, ?)"
            );
            
            for (String[] ach : achievements) {
                pstmt.setString(1, ach[0]);
                pstmt.setString(2, ach[1]);
                pstmt.executeUpdate();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public void saveScore(String playerName, int score, int level, String difficulty) {
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "INSERT INTO high_scores (player_name, score, level, difficulty) VALUES (?, ?, ?, ?)"
            );
            pstmt.setString(1, playerName);
            pstmt.setInt(2, score);
            pstmt.setInt(3, level);
            pstmt.setString(4, difficulty);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public List<Map<String, Object>> getHighScores(int limit) {
        List<Map<String, Object>> scores = new ArrayList<>();
        
        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(
                "SELECT * FROM high_scores ORDER BY score DESC LIMIT " + limit
            );
            
            while (rs.next()) {
                Map<String, Object> score = new HashMap<>();
                score.put("player_name", rs.getString("player_name"));
                score.put("score", rs.getInt("score"));
                score.put("level", rs.getInt("level"));
                score.put("difficulty", rs.getString("difficulty"));
                score.put("date", rs.getString("date"));
                scores.add(score);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return scores;
    }
    
    public int getHighScore() {
        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT MAX(score) FROM high_scores");
            if (rs.next()) {
                return rs.getInt(1);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return 0;
    }
    
    public void unlockAchievement(String name) {
        try {
            PreparedStatement pstmt = connection.prepareStatement(
                "UPDATE achievements SET unlocked = 1, unlocked_date = CURRENT_TIMESTAMP WHERE name = ?"
            );
            pstmt.setString(1, name);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    
    public List<Map<String, Object>> getAchievements() {
        List<Map<String, Object>> achievements = new ArrayList<>();
        
        try {
            Statement stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM achievements");
            
            while (rs.next()) {
                Map<String, Object> ach = new HashMap<>();
                ach.put("name", rs.getString("name"));
                ach.put("description", rs.getString("description"));
                ach.put("unlocked", rs.getBoolean("unlocked"));
                ach.put("unlocked_date", rs.getString("unlocked_date"));
                achievements.add(ach);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return achievements;
    }
    
    public void close() {
        try {
            if (connection != null) {
                connection.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}

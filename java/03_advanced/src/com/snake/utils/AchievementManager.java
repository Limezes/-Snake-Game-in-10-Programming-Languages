package com.snake.utils;

import com.snake.model.FoodType;
import java.util.List;
import java.util.Map;

public class AchievementManager {
    private DatabaseManager db;
    private int consecutiveBonuses;
    
    public AchievementManager(DatabaseManager db) {
        this.db = db;
        this.consecutiveBonuses = 0;
    }
    
    public void checkFoodEaten(FoodType type) {
        if (type == FoodType.BONUS) {
            consecutiveBonuses++;
            if (consecutiveBonuses >= 10) {
                db.unlockAchievement("invincible");
            }
        } else {
            consecutiveBonuses = 0;
        }
        
        // Первая еда
        db.unlockAchievement("first_food");
    }
    
    public void checkScore(int score) {
        if (score >= 100) {
            db.unlockAchievement("score_100");
        }
        if (score >= 500) {
            db.unlockAchievement("score_500");
        }
    }
    
    public void checkLevel(int level) {
        if (level >= 5) {
            db.unlockAchievement("level_5");
        }
    }
    
    public void checkSpeed(double speed) {
        if (speed >= 150) {
            db.unlockAchievement("speed_demon");
        }
    }
    
    public void checkWalls() {
        db.unlockAchievement("wall_killer");
    }
    
    public void checkGoldenFood(int count) {
        if (count >= 5) {
            db.unlockAchievement("golden_feast");
        }
    }
    
    public List<Map<String, Object>> getAllAchievements() {
        return db.getAchievements();
    }
}

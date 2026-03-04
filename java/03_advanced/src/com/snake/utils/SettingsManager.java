package com.snake.utils;



import com.snake.model.Difficulty;
import java.util.prefs.Preferences;

public class SettingsManager {
    private Preferences prefs;
    private Difficulty difficulty;
    private String playerName;
    private boolean soundEnabled;
    private boolean musicEnabled;
    private boolean wallsEnabled;
    private int highScore;
    private int maxFood;
    private double powerUpChance;
    private double cellSize;
    
    public SettingsManager() {
        prefs = Preferences.userNodeForPackage(SettingsManager.class);
        loadSettings();
    }
    
    private void loadSettings() {
        String diffName = prefs.get("difficulty", "MEDIUM");
        difficulty = Difficulty.valueOf(diffName);
        playerName = prefs.get("player_name", "Player");
        soundEnabled = prefs.getBoolean("sound_enabled", true);
        musicEnabled = prefs.getBoolean("music_enabled", true);
        wallsEnabled = prefs.getBoolean("walls_enabled", false);
        highScore = prefs.getInt("high_score", 0);
        maxFood = prefs.getInt("max_food", 5);
        powerUpChance = prefs.getDouble("powerup_chance", 0.1);
        cellSize = prefs.getDouble("cell_size", 25.0);
    }
    
    public void saveSettings() {
        prefs.put("difficulty", difficulty.name());
        prefs.put("player_name", playerName);
        prefs.putBoolean("sound_enabled", soundEnabled);
        prefs.putBoolean("music_enabled", musicEnabled);
        prefs.putBoolean("walls_enabled", wallsEnabled);
        prefs.putInt("high_score", highScore);
        prefs.putInt("max_food", maxFood);
        prefs.putDouble("powerup_chance", powerUpChance);
        prefs.putDouble("cell_size", cellSize);
    }
    
    public Difficulty getDifficulty() {
        return difficulty;
    }
    
    public void setDifficulty(Difficulty difficulty) {
        this.difficulty = difficulty;
    }
    
    public String getPlayerName() {
        return playerName;
    }
    
    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }
    
    public boolean isSoundEnabled() {
        return soundEnabled;
    }
    
    public void setSoundEnabled(boolean soundEnabled) {
        this.soundEnabled = soundEnabled;
    }
    
    public boolean isMusicEnabled() {
        return musicEnabled;
    }
    
    public void setMusicEnabled(boolean musicEnabled) {
        this.musicEnabled = musicEnabled;
    }
    
    public boolean isWallsEnabled() {
        return difficulty.hasWalls();
    }
    
    public int getHighScore() {
        return highScore;
    }
    
    public void setHighScore(int highScore) {
        if (highScore > this.highScore) {
            this.highScore = highScore;
            prefs.putInt("high_score", highScore);
        }
    }
    
    public int getMaxFood() {
        return maxFood;
    }
    
    public double getPowerUpChance() {
        return difficulty.getPowerUpChance();
    }
    
    public double getCellSize() {
        return cellSize;
    }
}

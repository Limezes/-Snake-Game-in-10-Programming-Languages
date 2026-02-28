package com.snake;

import java.io.*;
import java.util.prefs.Preferences;

public class ScoreManager {
    private static final String HIGH_SCORE_KEY = "highScore";
    private Preferences prefs;
    private int highScore;
    
    public ScoreManager() {
        prefs = Preferences.userNodeForPackage(ScoreManager.class);
        highScore = prefs.getInt(HIGH_SCORE_KEY, 0);
    }
    
    public int getHighScore() {
        return highScore;
    }
    
    public void setHighScore(int score) {
        if (score > highScore) {
            highScore = score;
            prefs.putInt(HIGH_SCORE_KEY, highScore);
            
            // Также сохраняем в файл для бэкапа
            saveToFile(score);
        }
    }
    
    private void saveToFile(int score) {
        try (PrintWriter out = new PrintWriter("highscore.txt")) {
            out.println(score);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }
    
    public void loadFromFile() {
        try (BufferedReader in = new BufferedReader(new FileReader("highscore.txt"))) {
            String line = in.readLine();
            if (line != null) {
                int fileScore = Integer.parseInt(line.trim());
                if (fileScore > highScore) {
                    highScore = fileScore;
                }
            }
        } catch (IOException e) {
            // Файл не существует - используем Preferences
        }
    }
}


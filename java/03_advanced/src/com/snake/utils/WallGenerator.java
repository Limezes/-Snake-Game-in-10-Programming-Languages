package com.snake.utils;

import com.snake.model.Wall;
import java.util.*;

public class WallGenerator {
    private int level;
    private Random random;
    
    public WallGenerator(int level) {
        this.level = level;
        this.random = new Random();
    }
    
    public List<Wall> generate() {
        List<Wall> walls = new ArrayList<>();
        
        switch (level) {
            case 1:
                // Стены по краям
                generateBorderWalls(walls);
                break;
            case 2:
                // Простой лабиринт
                generateBorderWalls(walls);
                generateSimpleMaze(walls);
                break;
            case 3:
                // Сложный лабиринт
                generateBorderWalls(walls);
                generateComplexMaze(walls);
                break;
            case 4:
                // Спираль
                generateSpiral(walls);
                break;
            default:
                // Процедурная генерация
                generateProcedural(walls);
        }
        
        return walls;
    }
    
    private void generateBorderWalls(List<Wall> walls) {
        for (int x = 0; x < 20; x++) {
            walls.add(new Wall(x, 0));
            walls.add(new Wall(x, 19));
        }
        for (int y = 1; y < 19; y++) {
            walls.add(new Wall(0, y));
            walls.add(new Wall(19, y));
        }
    }
    
    private void generateSimpleMaze(List<Wall> walls) {
        for (int i = 4; i < 16; i++) {
            walls.add(new Wall(i, 10));
        }
    }
    
    private void generateComplexMaze(List<Wall> walls) {
        for (int i = 2; i < 18; i++) {
            if (i % 3 != 0) {
                walls.add(new Wall(i, 5));
                walls.add(new Wall(i, 14));
            }
        }
    }
    
    private void generateSpiral(List<Wall> walls) {
        for (int r = 1; r < 8; r += 2) {
            for (int x = 10 - r; x <= 10 + r; x++) {
                walls.add(new Wall(x, 10 - r));
                walls.add(new Wall(x, 10 + r));
            }
            for (int y = 10 - r + 1; y < 10 + r; y++) {
                walls.add(new Wall(10 - r, y));
                walls.add(new Wall(10 + r, y));
            }
        }
    }
    
    private void generateProcedural(List<Wall> walls) {
        int wallCount = level * 5;
        
        for (int i = 0; i < wallCount; i++) {
            int x = random.nextInt(18) + 1;
            int y = random.nextInt(18) + 1;
            walls.add(new Wall(x, y));
        }
    }
}

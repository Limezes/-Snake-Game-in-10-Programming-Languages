package com.snake.model;

public enum Difficulty {
    EASY(150, false, 0.1),
    MEDIUM(100, false, 0.15),
    HARD(70, true, 0.2),
    EXPERT(50, true, 0.25);
    
    private final int speed;
    private final boolean walls;
    private final double powerUpChance;
    
    Difficulty(int speed, boolean walls, double powerUpChance) {
        this.speed = speed;
        this.walls = walls;
        this.powerUpChance = powerUpChance;
    }
    
    public int getSpeed() {
        return speed;
    }
    
    public boolean hasWalls() {
        return walls;
    }
    
    public double getPowerUpChance() {
        return powerUpChance;
    }
}

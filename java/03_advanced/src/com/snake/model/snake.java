package com.snake.model;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import java.util.*;

public class Snake {
    private LinkedList<Position> body;
    private Direction direction;
    private Direction nextDirection;
    private double speedMultiplier;
    private long speedMultiplierEndTime;
    private boolean invincible;
    private long invincibleEndTime;
    private int growCount;
    private Difficulty difficulty;
    
    public Snake(Difficulty difficulty) {
        this.difficulty = difficulty;
        reset();
    }
    
    public void reset() {
        body = new LinkedList<>();
        body.add(new Position(10, 10));
        body.add(new Position(9, 10));
        body.add(new Position(8, 10));
        
        direction = Direction.RIGHT;
        nextDirection = Direction.RIGHT;
        speedMultiplier = 1.0;
        invincible = false;
        growCount = 0;
    }
    
    public void move() {
        // Проверка направления
        if ((direction == Direction.UP && nextDirection != Direction.DOWN) ||
            (direction == Direction.DOWN && nextDirection != Direction.UP) ||
            (direction == Direction.LEFT && nextDirection != Direction.RIGHT) ||
            (direction == Direction.RIGHT && nextDirection != Direction.LEFT)) {
            direction = nextDirection;
        }
        
        // Новая голова
        Position head = body.getFirst().copy();
        
        switch (direction) {
            case UP: head.setY(head.getY() - 1); break;
            case DOWN: head.setY(head.getY() + 1); break;
            case LEFT: head.setX(head.getX() - 1); break;
            case RIGHT: head.setX(head.getX() + 1); break;
        }
        
        // Телепортация через границы (если нет стен)
        if (!difficulty.hasWalls()) {
            if (head.getX() < 0) head.setX(19);
            if (head.getX() >= 20) head.setX(0);
            if (head.getY() < 0) head.setY(19);
            if (head.getY() >= 20) head.setY(0);
        }
        
        // Добавление новой головы
        body.addFirst(head);
        
        // Удаление хвоста
        if (growCount > 0) {
            growCount--;
        } else {
            body.removeLast();
        }
        
        // Проверка временных эффектов
        long now = System.currentTimeMillis();
        if (speedMultiplierEndTime > 0 && now > speedMultiplierEndTime) {
            speedMultiplier = 1.0;
            speedMultiplierEndTime = 0;
        }
        
        if (invincibleEndTime > 0 && now > invincibleEndTime) {
            invincible = false;
            invincibleEndTime = 0;
        }
    }
    
    public boolean collidesWithItself() {
        if (invincible) return false;
        
        Position head = body.getFirst();
        for (int i = 1; i < body.size(); i++) {
            if (head.equals(body.get(i))) {
                return true;
            }
        }
        return false;
    }
    
    public boolean collidesWith(Position pos) {
        return body.stream().anyMatch(p -> p.equals(pos));
    }
    
    public void grow() {
        growCount++;
    }
    
    public void setDirection(Direction newDirection) {
        this.nextDirection = newDirection;
    }
    
    public void setSpeedMultiplier(double multiplier, long duration) {
        this.speedMultiplier = multiplier;
        this.speedMultiplierEndTime = System.currentTimeMillis() + duration;
    }
    
    public void setInvincible(boolean invincible, long duration) {
        this.invincible = invincible;
        if (invincible) {
            this.invincibleEndTime = System.currentTimeMillis() + duration;
        }
    }
    
    public void increaseSpeed() {
        // Увеличение базовой скорости с уровнем
    }
    
    public void render(GraphicsContext gc, double cellSize) {
        for (int i = 0; i < body.size(); i++) {
            Position pos = body.get(i);
            double x = pos.getX() * cellSize;
            double y = pos.getY() * cellSize;
            


            if (i == 0) {
                // Голова
                if (invincible) {
                    gc.setFill(Color.GOLD);
                } else {
                    gc.setFill(Color.rgb(50, 255, 50));
                }
                gc.fillRoundRect(x + 2, y + 2, cellSize - 4, cellSize - 4, 10, 10);
                
                // Глаза
                gc.setFill(Color.WHITE);
                double eyeSize = cellSize / 5;
                
                switch (direction) {
                    case RIGHT:
                        gc.fillOval(x + cellSize - eyeSize * 2, y + eyeSize, eyeSize, eyeSize);
                        gc.fillOval(x + cellSize - eyeSize * 2, y + cellSize - eyeSize * 2, eyeSize, eyeSize);
                        break;
                    case LEFT:
                        gc.fillOval(x + eyeSize, y + eyeSize, eyeSize, eyeSize);
                        gc.fillOval(x + eyeSize, y + cellSize - eyeSize * 2, eyeSize, eyeSize);
                        break;
                    case UP:
                        gc.fillOval(x + eyeSize, y + eyeSize, eyeSize, eyeSize);
                        gc.fillOval(x + cellSize - eyeSize * 2, y + eyeSize, eyeSize, eyeSize);
                        break;
                    case DOWN:
                        gc.fillOval(x + eyeSize, y + cellSize - eyeSize * 2, eyeSize, eyeSize);
                        gc.fillOval(x + cellSize - eyeSize * 2, y + cellSize - eyeSize * 2, eyeSize, eyeSize);
                        break;
                }
            } else {
                // Тело
                double opacity = 1.0 - (i * 0.05);
                if (opacity < 0.3) opacity = 0.3;
                
                gc.setFill(Color.rgb(0, 200, 0, opacity));
                gc.fillRoundRect(x + 3, y + 3, cellSize - 6, cellSize - 6, 5, 5);
            }
        }
    }
    
    public Position getHead() {
        return body.getFirst();
    }
    
    public double getSpeedMultiplier() {
        return speedMultiplier;
    }
    
    public boolean isInvincible() {
        return invincible;
    }
}

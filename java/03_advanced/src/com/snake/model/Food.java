package com.snake.model;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import java.util.Random;

public class Food {
    private Position position;
    private FoodType type;
    private int points;
    private long spawnTime;
    private static final Random random = new Random();
    
    public Food(FoodType type, double canvasWidth, double canvasHeight) {
        this.type = type;
        this.points = type.getPoints();
        this.spawnTime = System.currentTimeMillis();
        
        int maxX = (int)(canvasWidth / 25);
        int maxY = (int)(canvasHeight / 25);
        
        this.position = new Position(
            random.nextInt(maxX),
            random.nextInt(maxY)
        );
    }
    
    public Position getPosition() {
        return position;
    }
    
    public int getPoints() {
        return points;
    }
    
    public FoodType getType() {
        return type;
    }
    
    public boolean isExpired() {
        if (type == FoodType.BONUS) {
            return System.currentTimeMillis() - spawnTime > 5000; // 5 секунд
        }
        return false;
    }
    
    public void render(GraphicsContext gc, double cellSize) {
        double x = position.getX() * cellSize;
        double y = position.getY() * cellSize;
        
        // Эффект пульсации для бонусной еды
        if (type == FoodType.BONUS) {
            double pulse = Math.sin(System.currentTimeMillis() / 200.0) * 0.2 + 0.8;
            gc.setGlobalAlpha(pulse);
        }
        
        // Градиент
        gc.setFill(type.getColor());
        gc.fillOval(x + 3, y + 3, cellSize - 6, cellSize - 6);
        
        // Блик
        gc.setFill(Color.WHITE);
        gc.setGlobalAlpha(0.5);
        gc.fillOval(x + 5, y + 5, cellSize / 4, cellSize / 4);
        
        gc.setGlobalAlpha(1.0);
        
        // Символ для особой еды
        if (type != FoodType.NORMAL) {
            gc.setFill(Color.WHITE);
            gc.setFont(javafx.scene.text.Font.font(14));
            gc.fillText(type.getSymbol(), x + cellSize/4, y + cellSize/1.5);
        }
    }
}

package com.snake.model;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import java.util.Random;

public class PowerUp {
    private Position position;
    private PowerUpType type;
    private long spawnTime;
    private static final Random random = new Random();
    
    public PowerUp(PowerUpType type, double canvasWidth, double canvasHeight) {
        this.type = type;
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
    
    public PowerUpType getType() {
        return type;
    }
    
    public boolean isExpired() {
        return System.currentTimeMillis() - spawnTime > 3000; // 3 секунды
    }
    
    public void render(GraphicsContext gc, double cellSize) {
        double x = position.getX() * cellSize;
        double y = position.getY() * cellSize;
        
        // Эффект вращения
        double rotation = (System.currentTimeMillis() / 100.0) % 360;
        gc.save();
        gc.translate(x + cellSize/2, y + cellSize/2);
        gc.rotate(rotation);
        
        gc.setFill(type.getColor());
        gc.fillRect(-cellSize/2 + 3, -cellSize/2 + 3, cellSize - 6, cellSize - 6);
        
        gc.setFill(Color.WHITE);
        gc.setFont(javafx.scene.text.Font.font(16));
        gc.fillText(type.getSymbol(), -cellSize/4, cellSize/4);
        
        gc.restore();
    }
}

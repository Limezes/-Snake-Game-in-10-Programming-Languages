package com.snake.model;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class Wall {
    private Position position;
    
    public Wall(int x, int y) {
        this.position = new Position(x, y);
    }
    
    public Position getPosition() {
        return position;
    }
    
    public boolean collidesWith(Position pos) {
        return position.equals(pos);
    }
    
    public void render(GraphicsContext gc, double cellSize) {
        double x = position.getX() * cellSize;
        double y = position.getY() * cellSize;
        
        gc.setFill(Color.rgb(100, 100, 120));
        gc.fillRect(x + 1, y + 1, cellSize - 2, cellSize - 2);
        
        gc.setStroke(Color.rgb(150, 150, 170));
        gc.setLineWidth(2);
        gc.strokeRect(x + 1, y + 1, cellSize - 2, cellSize - 2);
    }
}

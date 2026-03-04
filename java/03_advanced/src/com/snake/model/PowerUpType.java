package com.snake.model;

import javafx.scene.paint.Color;
import java.util.Random;

public enum PowerUpType {
    SPEED_BOOST("⚡", Color.CYAN),
    INVINCIBILITY("🛡️", Color.GOLD),
    SLOW_TIME("⏱️", Color.PURPLE),
    EXTRA_LIFE("❤️", Color.RED);
    
    private final String symbol;
    private final Color color;
    private static final Random random = new Random();
    
    PowerUpType(String symbol, Color color) {
        this.symbol = symbol;
        this.color = color;
    }
    
    public String getSymbol() {
        return symbol;
    }
    
    public Color getColor() {
        return color;
    }
    
    public static PowerUpType getRandom() {
        PowerUpType[] types = values();
        return types[random.nextInt(types.length)];
    }
}

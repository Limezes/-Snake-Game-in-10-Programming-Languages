package com.snake;

import java.util.*;
import java.io.IOException;

/**
 * Простая консольная змейка на Java
 * Управление: W A S D, Q - выход
 * Запуск: javac com/snake/SimpleSnakeGame.java && java com.snake.SimpleSnakeGame
 */
public class SimpleSnakeGame {
    private static final int WIDTH = 20;
    private static final int HEIGHT = 10;
    private static final int INITIAL_SPEED = 150;
    
    private List<Point> snake;
    private Point food;
    private Direction direction;
    private Direction nextDirection;
    private int score;
    private boolean gameOver;
    private boolean running;
    
    private enum Direction {
        UP, DOWN, LEFT, RIGHT
    }
    
    private static class Point {
        int x, y;
        
        Point(int x, int y) {
            this.x = x;
            this.y = y;
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (!(obj instanceof Point)) return false;
            Point other = (Point) obj;
            return x == other.x && y == other.y;
        }
    }
    
    public SimpleSnakeGame() {
        snake = new ArrayList<>();
        reset();
        setupInput();
    }
    
    private void reset() {
        snake.clear();
        snake.add(new Point(WIDTH / 2, HEIGHT / 2));
        snake.add(new Point(WIDTH / 2 - 1, HEIGHT / 2));
        snake.add(new Point(WIDTH / 2 - 2, HEIGHT / 2));
        
        direction = Direction.RIGHT;
        nextDirection = Direction.RIGHT;
        score = 0;
        gameOver = false;
        running = true;
        
        createFood();
    }
    
    private void createFood() {
        Random rand = new Random();
        while (true) {
            food = new Point(rand.nextInt(WIDTH), rand.nextInt(HEIGHT));
            if (!snake.contains(food)) {
                break;
            }
        }
    }
    
    private void setupInput() {
        new Thread(() -> {
            Scanner scanner = new Scanner(System.in);
            while (running) {
                try {
                    String input = scanner.nextLine().toLowerCase();
                    if (input.length() == 1) {
                        handleKey(input.charAt(0));
                    }
                } catch (Exception e) {
                    // Игнорируем ошибки ввода
                }
            }
            scanner.close();
        }).start();
    }
    
    private void handleKey(char key) {
        if (key == 'q') {
            running = false;
            System.exit(0);
        }
        
        if (gameOver) {
            if (key == 'r') {
                reset();
            }
            return;
        }
        
        switch (key) {
            case 'w': nextDirection = Direction.UP; break;
            case 's': nextDirection = Direction.DOWN; break;
            case 'a': nextDirection = Direction.LEFT; break;
            case 'd': nextDirection = Direction.RIGHT; break;
        }
    }
    
    private void move() {
        // Проверка направления
        if ((direction == Direction.UP && nextDirection != Direction.DOWN) ||
            (direction == Direction.DOWN && nextDirection != Direction.UP) ||
            (direction == Direction.LEFT && nextDirection != Direction.RIGHT) ||
            (direction == Direction.RIGHT && nextDirection != Direction.LEFT)) {
            direction = nextDirection;
        }
        
        // Новая голова
        Point head = new Point(snake.get(0).x, snake.get(0).y);
        
        switch (direction) {
            case UP: head.y--; break;
            case DOWN: head.y++; break;
            case LEFT: head.x--; break;
            case RIGHT: head.x++; break;
        }
        
        // Проверка столкновения со стенами
        if (head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT) {
            gameOver = true;
            return;
        }
        
        // Добавление новой головы
        snake.add(0, head);
        
        // Проверка поедания еды
        if (head.equals(food)) {
            score += 10;
            createFood();
        } else {
            snake.remove(snake.size() - 1);
        }
        
        // Проверка столкновения с собой
        for (int i = 1; i < snake.size(); i++) {
            if (snake.get(i).equals(head)) {
                gameOver = true;
                break;
            }
        }
    }
    
    private void render() {
        // Очистка консоли (работает в большинстве терминалов)
        try {
            if (System.getProperty("os.name").contains("Windows")) {
                new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
            } else {
                System.out.print("\033[H\033[2J");
                System.out.flush();
            }
        } catch (Exception e) {
            // Если не получается очистить, просто выводим пустые строки
            for (int i = 0; i < 50; i++) System.out.println();
        }
        
        // Верхняя граница
        System.out.print("┌");
        for (int i = 0; i < WIDTH; i++) System.out.print("─");
        System.out.println("┐");
        
        // Игровое поле
        for (int y = 0; y < HEIGHT; y++) {
            System.out.print("│");
            for (int x = 0; x < WIDTH; x++) {
                Point current = new Point(x, y);
                
                if (snake.get(0).equals(current)) {
                    System.out.print("●"); // Голова
                } else if (snake.contains(current)) {
                    System.out.print("○"); // Тело
                } else if (food.equals(current)) {
                    System.out.print("★"); // Еда
                } else {
                    System.out.print(" ");
                }
            }
            System.out.println("│");
        }
        
        // Нижняя граница
        System.out.print("└");
        for (int i = 0; i < WIDTH; i++) System.out.print("─");
        System.out.println("┘");
        
        // Информация
        System.out.println("\n Счёт: " + score);
        System.out.println(" Управление: WASD | Q - выход | R - рестарт");
        
        if (gameOver) {
            System.out.println("\n 🎮 ИГРА ОКОНЧЕНА! Нажмите R для рестарта");
        }
    }
    
    public void start() {
        System.out.println("=== КОНСОЛЬНАЯ ЗМЕЙКА НА JAVA ===\n");
        
        while (running) {
            if (!gameOver) {
                move();
            }
            render();
            
            try {
                Thread.sleep(INITIAL_SPEED);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    public static void main(String[] args) {
        SimpleSnakeGame game = new SimpleSnakeGame();
        game.start();
    }
}

package com.snake;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.Random;

public class GamePanel extends JPanel implements ActionListener, KeyListener {
    private static final int GRID_SIZE = 20;
    private static final int CELL_SIZE = 25;
    
    private SnakeGame mainFrame;
    private Timer timer;
    private ArrayList<Point> snake;
    private Point food;
    private Direction direction;
    private Direction nextDirection;
    private int score;
    private int level;
    private boolean gameOver;
    private boolean paused;
    private Color snakeColor;
    private int speed;
    
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
    
    public GamePanel(SnakeGame mainFrame) {
        this.mainFrame = mainFrame;
        this.snakeColor = Color.GREEN;
        this.speed = 100;
        
        setBackground(new Color(30, 30, 30));
        setFocusable(true);
        addKeyListener(this);
        
        reset();
    }
    
    public void reset() {
        snake = new ArrayList<>();
        snake.add(new Point(GRID_SIZE / 2, GRID_SIZE / 2));
        snake.add(new Point(GRID_SIZE / 2 - 1, GRID_SIZE / 2));
        snake.add(new Point(GRID_SIZE / 2 - 2, GRID_SIZE / 2));
        
        direction = Direction.RIGHT;
        nextDirection = Direction.RIGHT;
        score = 0;
        level = 1;
        gameOver = false;
        paused = false;
        
        createFood();
        mainFrame.updateScore(score);
        
        repaint();
    }
    
    public void newGame() {
        reset();
        if (timer != null) {
            timer.stop();
        }
        timer = new Timer(speed, this);
        timer.start();
    }
    
    public void togglePause() {
        if (!gameOver) {
            paused = !paused;
            repaint();
        }
    }
    
    public void setSpeed(int speed) {
        this.speed = speed;
        if (timer != null) {
            timer.setDelay(speed);
        }
    }
    
    public void setSnakeColor(Color color) {
        this.snakeColor = color;
        repaint();
    }
    
    public Color getSnakeColor() {
        return snakeColor;
    }
    
    private void createFood() {
        Random rand = new Random();
        while (true) {
            food = new Point(rand.nextInt(GRID_SIZE), rand.nextInt(GRID_SIZE));
            if (!snake.contains(food)) {
                break;
            }
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
        if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
            gameOver = true;
            timer.stop();
            repaint();
            return;
        }
        
        // Добавление новой головы
        snake.add(0, head);
        
        // Проверка поедания еды
        if (head.equals(food)) {
            score += 10;
            mainFrame.updateScore(score);
            
            // Повышение уровня каждые 50 очков
            if (score % 50 == 0) {
                level++;
                if (speed > 30) {
                    speed -= 10;
                    timer.setDelay(speed);
                }
            }
            
            createFood();
        } else {
            snake.remove(snake.size() - 1);
        }
        
        // Проверка столкновения с собой
        for (int i = 1; i < snake.size(); i++) {
            if (snake.get(i).equals(head)) {
                gameOver = true;
                timer.stop();
                break;
            }
        }
        
        repaint();
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
            RenderingHints.VALUE_ANTIALIAS_ON);
        
        // Рисование сетки
        g2d.setColor(new Color(50, 50, 50));
        for (int i = 0; i <= GRID_SIZE; i++) {
            g2d.drawLine(i * CELL_SIZE, 0, i * CELL_SIZE, getHeight());
            g2d.drawLine(0, i * CELL_SIZE, getWidth(), i * CELL_SIZE);
        }
        
        // Рисование змейки
        for (int i = 0; i < snake.size(); i++) {
            Point p = snake.get(i);
            int x = p.x * CELL_SIZE;
            int y = p.y * CELL_SIZE;
            
            if (i == 0) {
                // Голова
                g2d.setColor(snakeColor.brighter());
                g2d.fillRoundRect(x + 2, y + 2, 
                    CELL_SIZE - 4, CELL_SIZE - 4, 10, 10);
                
                // Глаза
                g2d.setColor(Color.WHITE);
                if (direction == Direction.RIGHT) {
                    g2d.fillOval(x + CELL_SIZE - 8, y + 5, 4, 4);
                    g2d.fillOval(x + CELL_SIZE - 8, y + CELL_SIZE - 9, 4, 4);
                } else if (direction == Direction.LEFT) {
                    g2d.fillOval(x + 4, y + 5, 4, 4);
                    g2d.fillOval(x + 4, y + CELL_SIZE - 9, 4, 4);
                } else if (direction == Direction.UP) {
                    g2d.fillOval(x + 5, y + 4, 4, 4);
                    g2d.fillOval(x + CELL_SIZE - 9, y + 4, 4, 4);
                } else if (direction == Direction.DOWN) {
                    g2d.fillOval(x + 5, y + CELL_SIZE - 8, 4, 4);
                    g2d.fillOval(x + CELL_SIZE - 9, y + CELL_SIZE - 8, 4, 4);
                }
            } else {
                // Тело
                float opacity = 1.0f - (i * 0.05f);
                if (opacity < 0.3f) opacity = 0.3f;
                
                g2d.setColor(new Color(
                    snakeColor.getRed(),
                    snakeColor.getGreen(),
                    snakeColor.getBlue(),
                    (int)(255 * opacity)
                ));
                g2d.fillRoundRect(x + 3, y + 3, 
                    CELL_SIZE - 6, CELL_SIZE - 6, 5, 5);
            }
        }
        
        // Рисование еды
        if (food != null) {
            int x = food.x * CELL_SIZE;
            int y = food.y * CELL_SIZE;
            
            // Градиент для яблока
            RadialGradientPaint gradient = new RadialGradientPaint(
                x + CELL_SIZE/2, y + CELL_SIZE/2, CELL_SIZE/2,
                new float[]{0.0f, 1.0f},
                new Color[]{Color.RED, new Color(150, 0, 0)}
            );
            g2d.setPaint(gradient);
            g2d.fillOval(x + 3, y + 3, CELL_SIZE - 6, CELL_SIZE - 6);
            
            // Листик
            g2d.setColor(Color.GREEN);
            g2d.fillOval(x + CELL_SIZE - 8, y + 2, 6, 6);
        }
        
        // Сообщения
        g2d.setFont(new Font("Arial", Font.BOLD, 20));
        g2d.setColor(Color.WHITE);
        
        if (gameOver) {
            g2d.setColor(new Color(0, 0, 0, 180));
            g2d.fillRect(0, 0, getWidth(), getHeight());
            
            g2d.setColor(Color.RED);
            g2d.setFont(new Font("Arial", Font.BOLD, 36));
            String msg = "GAME OVER";
            FontMetrics fm = g2d.getFontMetrics();
            int msgX = (getWidth() - fm.stringWidth(msg)) / 2;
            g2d.drawString(msg, msgX, getHeight() / 2 - 20);
            
            g2d.setColor(Color.WHITE);
            g2d.setFont(new Font("Arial", Font.PLAIN, 18));
            String scoreMsg = "Счёт: " + score;
            fm = g2d.getFontMetrics();
            msgX = (getWidth() - fm.stringWidth(scoreMsg)) / 2;
            g2d.drawString(scoreMsg, msgX, getHeight() / 2 + 20);
        }
        
        if (paused && !gameOver) {
            g2d.setColor(new Color(0, 0, 0, 150));
            g2d.fillRect(0, 0, getWidth(), getHeight());
            
            g2d.setColor(Color.YELLOW);
            g2d.setFont(new Font("Arial", Font.BOLD, 36));
            String msg = "ПАУЗА";
            FontMetrics fm = g2d.getFontMetrics();
            int msgX = (getWidth() - fm.stringWidth(msg)) / 2;
            g2d.drawString(msg, msgX, getHeight() / 2);
        }
    }
    
    @Override
    public void actionPerformed(ActionEvent e) {
        if (!gameOver && !paused) {
            move();
        }
    }
    
    @Override
    public void keyPressed(KeyEvent e) {
        int key = e.getKeyCode();
        
        if (key == KeyEvent.VK_SPACE) {
            togglePause();
            return;
        }
        
        if (gameOver || paused) return;
        
        if (key == KeyEvent.VK_UP || key == KeyEvent.VK_W) {
            nextDirection = Direction.UP;
        } else if (key == KeyEvent.VK_DOWN || key == KeyEvent.VK_S) {
            nextDirection = Direction.DOWN;
        } else if (key == KeyEvent.VK_LEFT || key == KeyEvent.VK_A) {
            nextDirection = Direction.LEFT;
        } else if (key == KeyEvent.VK_RIGHT || key == KeyEvent.VK_D) {
            nextDirection = Direction.RIGHT;
        }
    }
    
    @Override
    public void keyReleased(KeyEvent e) {}
    
    @Override
    public void keyTyped(KeyEvent e) {}
}

package com.snake;

import javafx.animation.AnimationTimer;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.media.Media;
import javafx.scene.media.MediaPlayer;
import java.net.URL;
import java.util.*;

import com.snake.model.*;
import com.snake.utils.*;

public class GameController implements Initializable {
    
    @FXML private Canvas gameCanvas;
    @FXML private Label scoreLabel;
    @FXML private Label levelLabel;
    @FXML private Label highScoreLabel;
    @FXML private VBox gameOverlay;
    @FXML private VBox pauseMenu;
    @FXML private VBox gameOverMenu;
    
    private GraphicsContext gc;
    private GameState gameState;
    private Snake snake;
    private List<Food> foods;
    private List<Wall> walls;
    private List<PowerUp> activePowerUps;
    private DatabaseManager dbManager;
    private SettingsManager settings;
    private AchievementManager achievements;
    private MediaPlayer backgroundMusic;
    private MediaPlayer soundEffect;
    
    private AnimationTimer gameLoop;
    private long lastUpdate = 0;
    private int score;
    private int level;
    private boolean paused;
    
    private enum GameState {
        MENU, PLAYING, PAUSED, GAME_OVER
    }
    
    @Override
    public void initialize(URL location, ResourceBundle resources) {
        gc = gameCanvas.getGraphicsContext2D();
        dbManager = new DatabaseManager();
        settings = new SettingsManager();
        achievements = new AchievementManager(dbManager);
        
        initializeGame();
        setupKeyHandlers();
        setupAudio();
        
        gameCanvas.setFocusTraversable(true);
        gameCanvas.requestFocus();
        
        // Запуск рендеринга
        startRendering();
    }
    
    private void initializeGame() {
        snake = new Snake(settings.getDifficulty());
        foods = new ArrayList<>();
        walls = new ArrayList<>();
        activePowerUps = new ArrayList<>();
        
        // Генерация стен в зависимости от уровня
        generateWalls();
        
        // Создание начальной еды
        spawnFood(FoodType.NORMAL);
        
        score = 0;
        level = 1;
        gameState = GameState.PLAYING;
        paused = false;
        
        updateLabels();
    }
    
    private void generateWalls() {
        walls.clear();
        
        if (settings.isWallsEnabled()) {
            // Генерация процедурных стен
            WallGenerator generator = new WallGenerator(level);
            walls = generator.generate();
        }
    }
    
    private void spawnFood(FoodType type) {
        if (foods.size() < settings.getMaxFood()) {
            Food food = new Food(type, gameCanvas.getWidth(), gameCanvas.getHeight());
            if (!snake.collidesWith(food.getPosition()) && 
                walls.stream().noneMatch(w -> w.collidesWith(food.getPosition()))) {
                foods.add(food);
            }
        }
    }
    
    private void spawnPowerUp() {
        if (Math.random() < settings.getPowerUpChance()) {
            PowerUpType type = PowerUpType.getRandom();
            PowerUp powerUp = new PowerUp(type, gameCanvas.getWidth(), gameCanvas.getHeight());
            if (!snake.collidesWith(powerUp.getPosition())) {
                activePowerUps.add(powerUp);
            }
        }
    }
    
    private void setupKeyHandlers() {
        gameCanvas.setOnKeyPressed(event -> {
            KeyCode code = event.getCode();
            
            if (code == KeyCode.ESCAPE) {
                togglePause();
                return;
            }
            
            if (code == KeyCode.SPACE) {
                if (gameState == GameState.GAME_OVER) {
                    restartGame();
                }
                return;
            }
            
            if (gameState != GameState.PLAYING || paused) return;
            
            // Управление змейкой
            switch (code) {
                case UP:
                case W:
                    snake.setDirection(Direction.UP);
                    break;
                case DOWN:
                case S:
                    snake.setDirection(Direction.DOWN);
                    break;
                case LEFT:
                case A:
                    snake.setDirection(Direction.LEFT);
                    break;
                case RIGHT:
                case D:
                    snake.setDirection(Direction.RIGHT);
                    break;
            }
        });
    }
    
    private void setupAudio() {
        if (settings.isMusicEnabled()) {
            try {
                URL resource = getClass().getResource("/sounds/background.mp3");
                Media media = new Media(resource.toString());
                backgroundMusic = new MediaPlayer(media);
                backgroundMusic.setCycleCount(MediaPlayer.INDEFINITE);
                backgroundMusic.setVolume(0.3);
                backgroundMusic.play();
            } catch (Exception e) {
                System.err.println("Не удалось загрузить музыку: " + e.getMessage());
            }
        }
    }
    
    private void playSound(String filename) {
        if (settings.isSoundEnabled()) {
            try {
                URL resource = getClass().getResource("/sounds/" + filename);
                Media media = new Media(resource.toString());
                soundEffect = new MediaPlayer(media);
                soundEffect.play();
            } catch (Exception e) {
                // Игнорируем ошибки звука
            }
        }
    }
    
    private void startRendering() {
        gameLoop = new AnimationTimer() {
            @Override
            public void handle(long now) {
                // Обновление игры (60 FPS)
                if (lastUpdate == 0) {
                    lastUpdate = now;
                    return;
                }
                
                if (now - lastUpdate > 16_000_000) { // ~60 FPS
                    if (gameState == GameState.PLAYING && !paused) {
                        update();
                    }
                    render();
                    lastUpdate = now;
                }
            }
        };
        gameLoop.start();
    }
    
    private void update() {
        // Движение змейки
        snake.move();
        
        // Проверка столкновений со стенами
        if (settings.isWallsEnabled()) {
            for (Wall wall : walls) {
                if (snake.getHead().equals(wall.getPosition())) {
                    gameOver();
                    return;
                }
            }
        }
        
        // Проверка столкновений с едой
        Iterator<Food> foodIterator = foods.iterator();
        while (foodIterator.hasNext()) {
            Food food = foodIterator.next();
            if (snake.getHead().equals(food.getPosition())) {
                snake.grow();
                score += food.getPoints();
                playSound("eat.wav");
                
                // Проверка достижений
                achievements.checkFoodEaten(food.getType());
                
                // Специальные эффекты
                if (food.getType() == FoodType.BONUS) {
                    spawnPowerUp();
                }
                
                foodIterator.remove();
                
                // Создание новой еды
                if (foods.size() < settings.getMaxFood()) {
                    spawnFood(FoodType.getRandom());
                }
            }
        }
        
        // Проверка power-ups
        Iterator<PowerUp> powerUpIterator = activePowerUps.iterator();
        while (powerUpIterator.hasNext()) {
            PowerUp powerUp = powerUpIterator.next();
            if (snake.getHead().equals(powerUp.getPosition())) {
                applyPowerUp(powerUp.getType());
                playSound("powerup.wav");
                powerUpIterator.remove();
            }
        }
        
        // Обновление power-ups
        activePowerUps.removeIf(PowerUp::isExpired);
        
        // Проверка столкновения с собой
        if (snake.collidesWithItself()) {
            gameOver();
            return;
        }
        
        // Повышение уровня
        if (score > level * 100) {
            levelUp();
        }
        
        // Спавн бонусной еды
        if (Math.random() < 0.01) {
            spawnFood(FoodType.BONUS);
        }
        
        updateLabels();
    }
    
    private void applyPowerUp(PowerUpType type) {
        switch (type) {
            case SPEED_BOOST:
                snake.setSpeedMultiplier(1.5, 5000);
                break;
            case INVINCIBILITY:
                snake.setInvincible(true, 3000);
                break;
            case SLOW_TIME:
                snake.setSpeedMultiplier(0.5, 3000);
                break;
            case EXTRA_LIFE:
                // Дополнительная жизнь
                break;
        }
    }
    
    private void levelUp() {
        level++;
        playSound("levelup.wav");
        
        // Увеличение сложности
        snake.increaseSpeed();
        
        // Генерация новых стен
        if (settings.isWallsEnabled()) {
            generateWalls();
        }
        
        // Проверка достижений
        achievements.checkLevel(level);
    }
    
    private void gameOver() {
        gameState = GameState.GAME_OVER;
        playSound("gameover.wav");
        
        // Сохранение результата
        dbManager.saveScore(settings.getPlayerName(), score, level, 
                           settings.getDifficulty().toString());
        
        // Обновление рекорда
        if (score > settings.getHighScore()) {
            settings.setHighScore(score);
        }
        
        gameOverlay.setVisible(true);
        gameOverMenu.setVisible(true);
    }
    
    private void restartGame() {
        initializeGame();
        gameOverlay.setVisible(false);
        gameOverMenu.setVisible(false);
        pauseMenu.setVisible(false);
    }
    
    private void togglePause() {
        if (gameState == GameState.PLAYING) {
            paused = !paused;
            gameOverlay.setVisible(paused);
            pauseMenu.setVisible(paused);
            
            if (!paused) {
                gameCanvas.requestFocus();
            }
        }
    }
    
    private void updateLabels() {
        scoreLabel.setText(String.format("Счёт: %d", score));
        levelLabel.setText(String.format("Уровень: %d", level));
        highScoreLabel.setText(String.format("Рекорд: %d", settings.getHighScore()));
    }
    
    private void render() {
        // Очистка canvas
        gc.setFill(Color.rgb(20, 20, 30));
        gc.fillRect(0, 0, gameCanvas.getWidth(), gameCanvas.getHeight());
        
        // Рисование сетки
        gc.setStroke(Color.rgb(50, 50, 70));
        gc.setLineWidth(0.5);
        
        double cellSize = settings.getCellSize();
        for (double x = 0; x < gameCanvas.getWidth(); x += cellSize) {
            gc.strokeLine(x, 0, x, gameCanvas.getHeight());
        }
        for (double y = 0; y < gameCanvas.getHeight(); y += cellSize) {
            gc.strokeLine(0, y, gameCanvas.getWidth(), y);
        }
        
        // Рисование стен
        for (Wall wall : walls) {
            wall.render(gc, cellSize);
        }
        
        // Рисование еды
        for (Food food : foods) {
            food.render(gc, cellSize);
        }
        
        // Рисование power-ups
        for (PowerUp powerUp : activePowerUps) {
            powerUp.render(gc, cellSize);
        }
        
        // Рисование змейки
        snake.render(gc, cellSize);
        
        // Эффекты
        if (snake.isInvincible()) {
            gc.setGlobalAlpha(0.3);
            gc.setFill(Color.YELLOW);
            gc.fillOval(
                snake.getHead().getX() * cellSize - cellSize/2,
                snake.getHead().getY() * cellSize - cellSize/2,
                cellSize * 2,
                cellSize * 2
            );
            gc.setGlobalAlpha(1.0);
        }
    }
    
    public void shutdown() {
        if (backgroundMusic != null) {
            backgroundMusic.stop();
        }
        if (soundEffect != null) {
            soundEffect.stop();
        }
        dbManager.close();
    }
    
    @FXML
    private void resumeGame() {
        togglePause();
    }
    
    @FXML
    private void restartFromMenu() {
        restartGame();
    }
    
    @FXML
    private void showMainMenu() {
        // Возврат в главное меню
    }
    
    @FXML
    private void showSettings() {
        // Показать настройки
    }
    
    @FXML
    private void showAchievements() {
        // Показать достижения
    }
    
    @FXML
    private void showHighScores() {
        // Показать таблицу рекордов
    }
}

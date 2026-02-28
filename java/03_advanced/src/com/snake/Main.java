package com.snake;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.text.Font;

public class Main extends Application {
    
    @Override
    public void start(Stage primaryStage) throws Exception {
        // Загрузка шрифтов
        Font.loadFont(getClass().getResourceAsStream("/fonts/PressStart2P.ttf"), 14);
        
        // Загрузка главного окна
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/MainMenu.fxml"));
        Parent root = loader.load();
        
        primaryStage.setTitle("Snake Game - JavaFX");
        primaryStage.setScene(new Scene(root, 800, 600));
        primaryStage.setResizable(false);
        primaryStage.show();
        
        // Обработка закрытия
        primaryStage.setOnCloseRequest(e -> {
            GameController controller = loader.getController();
            controller.shutdown();
        });
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}


#include <QApplication>
#include <QDir>
#include <QDebug>
#include "../include/MainWindow.h"
#include "../include/DatabaseManager.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    app.setApplicationName("Snake Game");
    app.setOrganizationName("MyCompany");
    app.setApplicationVersion("3.0.0");
    
    // Создание необходимых директорий
    QDir dir;
    if (!dir.exists("data")) {
        dir.mkdir("data");
    }
    
    // Инициализация базы данных
    DatabaseManager dbManager;
    if (!dbManager.openDatabase("data/snake.db")) {
        qWarning() << "Не удалось открыть базу данных";
    }
    
    MainWindow window;
    window.show();
    
    return app.exec();
}

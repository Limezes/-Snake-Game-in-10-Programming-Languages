cmake_minimum_required(VERSION 3.10)
project(SnakeSFML)

set(CMAKE_CXX_STANDARD 11)

# Найти SFML
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Исполнительный файл
add_executable(snake
    src/Game.cpp
    src/Snake.cpp
    src/Food.cpp
    src/ScoreManager.cpp
)

# Подключение заголовков
target_include_directories(snake PRIVATE include)

# Линковка с SFML
target_link_libraries(snake sfml-graphics sfml-window sfml-system)

# Копирование ресурсов
add_custom_command(TARGET snake POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/resources
        $<TARGET_FILE_DIR:snake>/resources
)

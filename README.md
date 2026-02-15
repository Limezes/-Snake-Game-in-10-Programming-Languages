# 🐍 Snake Game in 10 Programming Languages

[![GitHub license](https://img.shields.io/github/license/yourusername/snake-10-languages)](https://github.com/yourusername/snake-10-languages/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/snake-10-languages)](https://github.com/yourusername/snake-10-languages/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/snake-10-languages)](https://github.com/yourusername/snake-10-languages/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/snake-10-languages/pulls)
[![Made with Love](https://img.shields.io/badge/Made%20with-❤-red.svg)](https://github.com/yourusername/snake-10-languages)

<p align="center">
  <img src="assets/screenshots/snake-preview.gif" alt="Snake Game Preview" width="600">
</p>

## 📋 О проекте

Классическая игра **"Змейка" (Snake)**, реализованная на **10 различных языках программирования**. Каждая реализация проходит эволюцию от простой консольной версии до полноценной игры с графическим интерфейсом и дополнительными функциями.

### 🎯 Цель проекта

- Показать реализацию одной и той игры на разных языках
- Продемонстрировать эволюцию кода от простого к сложному
- Создать учебный ресурс для начинающих разработчиков
- Сравнить подходы и возможности разных языков

### 🎮 Правила игры

- Управляйте змейкой с помощью стрелок (или WASD)
- Съедайте красные яблоки, чтобы расти
- Не врезайтесь в стены и в собственный хвост
- Чем длиннее змейка, тем сложнее играть
- Набирайте как можно больше очков!

---

## 📁 Структура репозитория

```
snake-10-languages/
├── 📁 python/                 # Python реализации
├── 📁 javascript/             # JavaScript реализации
├── 📁 java/                   # Java реализации
├── 📁 cpp/                    # C++ реализации
├── 📁 csharp/                 # C# реализации
├── 📁 rust/                   # Rust реализации
├── 📁 go/                     # Go реализации
├── 📁 swift/                  # Swift реализации
├── 📁 kotlin/                 # Kotlin реализации
├── 📁 typescript/             # TypeScript реализации
├── 📁 assets/                 # Изображения и ресурсы
│   ├── screenshots/           # Скриншоты игры
│   └── icons/                 # Иконки для разных платформ
├── 📁 docs/                    # Документация
│   ├── tutorials/             # Туториалы по созданию
│   └── api/                    # Документация API
├── .github/                    # GitHub файлы
│   ├── workflows/              # GitHub Actions
│   └── ISSUE_TEMPLATE/         # Шаблоны для issues
├── CONTRIBUTING.md             # Правила для контрибьюторов
├── LICENSE                      # Лицензия MIT
└── README.md                    # Этот файл
```

---

## 🚀 Реализации по языкам

### 1. 🐍 Python

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://python.org)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная змейка с curses | `curses` | `python python/01_simple/snake.py` |
| **02_medium** | Графика на Pygame | `pygame` | `pip install pygame && python python/02_medium/snake.py` |
| **03_advanced** | Полноценная игра с уровнями и рекордами | `pygame`, `sqlite3`, `json` | `pip install -r python/03_advanced/requirements.txt && python python/03_advanced/main.py` |

<details>
<summary>📸 Скриншоты Python версии</summary>
<p align="center">
  <img src="assets/screenshots/python-simple.png" width="200">
  <img src="assets/screenshots/python-medium.png" width="200">
  <img src="assets/screenshots/python-advanced.png" width="200">
</p>
</details>

---

### 2. 📜 JavaScript

[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)](https://developer.mozilla.org/ru/docs/Web/JavaScript)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия для Node.js | `readline` | `node javascript/01_simple/snake.js` |
| **02_medium** | Браузерная версия на Canvas | `Canvas API` | Откройте `javascript/02_medium/index.html` |
| **03_advanced** | React + WebSocket мультиплеер | `React`, `WebSocket`, `Express` | `cd javascript/03_advanced && npm install && npm start` |

<details>
<summary>📸 Скриншоты JavaScript версии</summary>
<p align="center">
  <img src="assets/screenshots/js-simple.png" width="200">
  <img src="assets/screenshots/js-medium.png" width="200">
  <img src="assets/screenshots/js-advanced.png" width="200">
</p>
</details>

---

### 3. ☕ Java

[![Java](https://img.shields.io/badge/Java-11%2B-red?style=for-the-badge&logo=java)](https://java.com)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `Scanner` | `javac java/01_simple/Snake.java && java Snake` |
| **02_medium** | GUI на Swing | `Swing`, `AWT` | `javac java/02_medium/*.java && java SnakeGame` |
| **03_advanced** | JavaFX + многопоточность | `JavaFX`, `Threads` | `cd java/03_advanced && ./gradlew run` |

<details>
<summary>📸 Скриншоты Java версии</summary>
<p align="center">
  <img src="assets/screenshots/java-simple.png" width="200">
  <img src="assets/screenshots/java-medium.png" width="200">
  <img src="assets/screenshots/java-advanced.png" width="200">
</p>
</details>

---

### 4. ⚡ C++

[![C++](https://img.shields.io/badge/C%2B%2B-17%2B-blue?style=for-the-badge&logo=c%2B%2B)](https://isocpp.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `iostream` | `g++ cpp/01_simple/snake.cpp -o snake && ./snake` |
| **02_medium** | SFML графика | `SFML` | `g++ cpp/02_medium/*.cpp -lsfml-graphics -lsfml-window -lsfml-system -o snake && ./snake` |
| **03_advanced** | Qt + сетевая игра | `Qt5`, `Sockets` | `cd cpp/03_advanced && qmake && make && ./snake` |

<details>
<summary>📸 Скриншоты C++ версии</summary>
<p align="center">
  <img src="assets/screenshots/cpp-simple.png" width="200">
  <img src="assets/screenshots/cpp-medium.png" width="200">
  <img src="assets/screenshots/cpp-advanced.png" width="200">
</p>
</details>

---

### 5. 🔷 C#

[![C#](https://img.shields.io/badge/C%23-9.0-green?style=for-the-badge&logo=c-sharp)](https://docs.microsoft.com/ru-ru/dotnet/csharp/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `Console` | `csc csharp/01_simple/Snake.cs && ./Snake` |
| **02_medium** | WinForms приложение | `WinForms` | `dotnet run --project csharp/02_medium` |
| **03_advanced** | WPF + Unity интеграция | `WPF`, `Unity` | Откройте решение в Visual Studio |

<details>
<summary>📸 Скриншоты C# версии</summary>
<p align="center">
  <img src="assets/screenshots/csharp-simple.png" width="200">
  <img src="assets/screenshots/csharp-medium.png" width="200">
  <img src="assets/screenshots/csharp-advanced.png" width="200">
</p>
</details>

---

### 6. 🦀 Rust

[![Rust](https://img.shields.io/badge/Rust-2021-orange?style=for-the-badge&logo=rust)](https://www.rust-lang.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `std::io` | `cd rust/01_simple && cargo run` |
| **02_medium** | Piston графика | `piston_window` | `cd rust/02_medium && cargo run` |
| **03_advanced** | WebAssembly версия | `wasm-bindgen`, `web-sys` | `cd rust/03_advanced && wasm-pack build --target web` |

<details>
<summary>📸 Скриншоты Rust версии</summary>
<p align="center">
  <img src="assets/screenshots/rust-simple.png" width="200">
  <img src="assets/screenshots/rust-medium.png" width="200">
  <img src="assets/screenshots/rust-advanced.png" width="200">
</p>
</details>

---

### 7. 🔵 Go

[![Go](https://img.shields.io/badge/Go-1.17%2B-blue?style=for-the-badge&logo=go)](https://golang.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `fmt`, `time` | `cd go/01_simple && go run snake.go` |
| **02_medium** | Ebitengine графика | `ebitengine` | `cd go/02_medium && go run .` |
| **03_advanced** | Мультиплеер по сети | `websocket`, `goroutines` | `cd go/03_advanced && go run server.go` |

<details>
<summary>📸 Скриншоты Go версии</summary>
<p align="center">
  <img src="assets/screenshots/go-simple.png" width="200">
  <img src="assets/screenshots/go-medium.png" width="200">
  <img src="assets/screenshots/go-advanced.png" width="200">
</p>
</details>

---

### 8. 🍎 Swift

[![Swift](https://img.shields.io/badge/Swift-5.5-orange?style=for-the-badge&logo=swift)](https://swift.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `Foundation` | `cd swift/01_simple && swift run` |
| **02_medium** | SpriteKit игра для macOS | `SpriteKit` | Откройте Xcode проект |
| **03_advanced** | iOS приложение с GameCenter | `SwiftUI`, `GameKit` | Откройте Xcode проект и запустите на симуляторе |

<details>
<summary>📸 Скриншоты Swift версии</summary>
<p align="center">
  <img src="assets/screenshots/swift-simple.png" width="200">
  <img src="assets/screenshots/swift-medium.png" width="200">
  <img src="assets/screenshots/swift-advanced.png" width="200">
</p>
</details>

---

### 9. 🟣 Kotlin

[![Kotlin](https://img.shields.io/badge/Kotlin-1.6-purple?style=for-the-badge&logo=kotlin)](https://kotlinlang.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия | `kotlin-stdlib` | `cd kotlin/01_simple && kotlinc snake.kt -include-runtime -d snake.jar && java -jar snake.jar` |
| **02_medium** | Swing GUI | `Swing` | `cd kotlin/02_medium && ./gradlew run` |
| **03_advanced** | Compose Multiplatform | `Compose`, `Ktor` | `cd kotlin/03_advanced && ./gradlew run` |

<details>
<summary>📸 Скриншоты Kotlin версии</summary>
<p align="center">
  <img src="assets/screenshots/kotlin-simple.png" width="200">
  <img src="assets/screenshots/kotlin-medium.png" width="200">
  <img src="assets/screenshots/kotlin-advanced.png" width="200">
</p>
</details>

---

### 10. 🔷 TypeScript

[![TypeScript](https://img.shields.io/badge/TypeScript-4.5-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)

| Версия | Описание | Технологии | Команда для запуска |
|--------|----------|------------|---------------------|
| **01_simple** | Консольная версия для Deno | `Deno` | `cd typescript/01_simple && deno run --allow-all snake.ts` |
| **02_medium** | Canvas с типами | `Canvas API`, `TypeScript` | `cd typescript/02_medium && tsc && открыть index.html` |
| **03_advanced** | Angular + Firebase | `Angular`, `Firebase` | `cd typescript/03_advanced && npm install && ng serve` |

<details>
<summary>📸 Скриншоты TypeScript версии</summary>
<p align="center">
  <img src="assets/screenshots/ts-simple.png" width="200">
  <img src="assets/screenshots/ts-medium.png" width="200">
  <img src="assets/screenshots/ts-advanced.png" width="200">
</p>
</details>

---

## 📊 Сравнение реализаций

| Язык | Строк кода (simple) | Строк кода (advanced) | Сложность | Производительность |
|------|--------------------|----------------------|-----------|-------------------|
| Python | ~100 | ~1500 | Низкая | Средняя |
| JavaScript | ~120 | ~2000 | Низкая | Средняя |
| Java | ~150 | ~2500 | Средняя | Высокая |
| C++ | ~130 | ~3000 | Высокая | Очень высокая |
| C# | ~140 | ~2800 | Средняя | Высокая |
| Rust | ~160 | ~3500 | Высокая | Очень высокая |
| Go | ~110 | ~2200 | Средняя | Высокая |
| Swift | ~150 | ~4000 | Средняя | Высокая |
| Kotlin | ~130 | ~2700 | Средняя | Высокая |
| TypeScript | ~140 | ~2300 | Низкая | Средняя |

---

## 🎯 Особенности advanced версий

- ✅ **Сохранение рекордов** (локалное и облачное)
- ✅ **Разные уровни сложности**
- ✅ **Бонусные яблоки** (замедление, ускорение, очки)
- ✅ **Мультиплеер** (локальный и по сети)
- ✅ **Настройки управления**
- ✅ **Темы оформления**
- ✅ **Достижения**
- ✅ **Таблица лидеров**
- ✅ **Пауза и сохранение игры**
- ✅ **Режим "бесконечные стены"**

---

## 🚀 Быстрый старт

### Клонирование репозитория

```bash
git clone https://github.com/yourusername/snake-10-languages.git
cd snake-10-languages
```

### Запуск простейшей версии на Python

```bash
cd python/01_simple
python snake.py
```

### Запуск продвинутой версии на JavaScript

```bash
cd javascript/03_advanced
npm install
npm start
# Откройте http://localhost:3000
```

---

## 🤝 Как внести вклад

Мы приветствуем вклад в проект! Вот как вы можете помочь:

1. **🍴 Форкните репозиторий**
2. **🌱 Создайте ветку** (`git checkout -b feature/amazing-feature`)
3. **💻 Внесите изменения**
4. **✅ Добавьте тесты** (если применимо)
5. **📝 Обновите документацию**
6. **📤 Отправьте изменения** (`git push origin feature/amazing-feature`)
7. **🔄 Откройте Pull Request**

### Правила для контрибьюторов

- Следуйте стилю кода языка
- Добавляйте комментарии на английском или русском
- Обновляйте README при добавлении новых функций
- Тестируйте код перед отправкой

Подробнее в [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📅 Планы развития

- [ ] Добавить реализации на **Ruby**, **PHP**, **Perl**
- [ ] Создать **мобильные версии** (Flutter, React Native)
- [ ] Добавить **искусственный интеллект** для игры
- [ ] Реализовать **турнирную систему**
- [ ] Создать **видео-туториалы** по каждой реализации
- [ ] Добавить **web-демо** для всех версий

---

## 📖 Полезные ресурсы

- [Классическая игра Snake на Википедии](https://ru.wikipedia.org/wiki/Snake)
- [Учебник по созданию Snake на Python](https://docs.python.org/3/library/turtle.html#turtle-examples)
- [JavaScript Snake Tutorial](https://developer.mozilla.org/ru/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript)
- [C++ Snake с SFML](https://www.sfml-dev.org/tutorials/)

---

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2024 [Ваше имя]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## ⭐ Авторы

- **[Ваше имя](https://github.com/yourusername)** - Инициатор проекта
- **[Соавтор 1](https://github.com/coauthor1)** - Python и JavaScript версии
- **[Соавтор 2](https://github.com/coauthor2)** - C++ и Rust версии

---

## 📬 Контакты

- **Email**: your.email@example.com
- **Telegram**: [@yourusername](https://t.me/yourusername)
- **Twitter**: [@yourusername](https://twitter.com/yourusername)

---

## 🌟 Поддержка проекта

Если вам понравился проект, поставьте ⭐ на GitHub! Это поможет другим разработчикам найти этот учебный ресурс.

<p align="center">
  <a href="https://github.com/yourusername/snake-10-languages">
    <img src="https://img.shields.io/github/stars/yourusername/snake-10-languages?style=social" alt="Star on GitHub">
  </a>
</p>

---

<p align="center">
  Сделано с ❤️ для разработчиков по всему миру
</p>

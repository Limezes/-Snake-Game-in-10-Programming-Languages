using System;
using System.Collections.Generic;
using System.Threading;
using System.Runtime.InteropServices;

namespace SimpleSnake
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "🐍 Змейка - Консольная версия";
            SnakeGame game = new SnakeGame();
            game.Start();
        }
    }

    class SnakeGame
    {
        private const int Width = 40;
        private const int Height = 20;
        private const int InitialSpeed = 150;

        private LinkedList<Position> snake;
        private Position food;
        private Direction currentDirection;
        private Direction nextDirection;
        private int score;
        private bool gameOver;
        private bool running;

        private enum Direction { Up, Down, Left, Right }

        private struct Position
        {
            public int X { get; set; }
            public int Y { get; set; }

            public Position(int x, int y)
            {
                X = x;
                Y = y;
            }

            public override bool Equals(object obj)
            {
                if (obj is Position other)
                    return X == other.X && Y == other.Y;
                return false;
            }

            public override int GetHashCode()
            {
                return HashCode.Combine(X, Y);
            }
        }

        public SnakeGame()
        {
            Reset();
        }

        private void Reset()
        {
            snake = new LinkedList<Position>();
            snake.AddFirst(new Position(Width / 2, Height / 2));
            snake.AddFirst(new Position(Width / 2 - 1, Height / 2));
            snake.AddFirst(new Position(Width / 2 - 2, Height / 2));

            currentDirection = Direction.Right;
            nextDirection = Direction.Right;
            score = 0;
            gameOver = false;
            running = true;

            CreateFood();
        }

        private void CreateFood()
        {
            Random rand = new Random();
            do
            {
                food = new Position(rand.Next(1, Width - 1), rand.Next(1, Height - 1));
            } while (snake.Contains(food));
        }

        private void Move()
        {
            // Проверка направления
            if ((currentDirection == Direction.Up && nextDirection != Direction.Down) ||
                (currentDirection == Direction.Down && nextDirection != Direction.Up) ||
                (currentDirection == Direction.Left && nextDirection != Direction.Right) ||
                (currentDirection == Direction.Right && nextDirection != Direction.Left))
            {
                currentDirection = nextDirection;
            }

            // Новая голова
            Position head = snake.First.Value;

            switch (currentDirection)
            {
                case Direction.Up: head.Y--; break;
                case Direction.Down: head.Y++; break;
                case Direction.Left: head.X--; break;
                case Direction.Right: head.X++; break;
            }

            // Проверка столкновения со стенами
            if (head.X <= 0 || head.X >= Width - 1 || head.Y <= 0 || head.Y >= Height - 1)
            {
                gameOver = true;
                return;
            }

            // Добавление новой головы
            snake.AddFirst(head);

            // Проверка поедания еды
            if (head.Equals(food))
            {
                score += 10;
                CreateFood();
            }
            else
            {
                snake.RemoveLast();
            }

            // Проверка столкновения с собой
            var current = snake.First.Next;
            while (current != null)
            {
                if (current.Value.Equals(head))
                {
                    gameOver = true;
                    break;
                }
                current = current.Next;
            }
        }

        private void Render()
        {
            Console.Clear();

            // Верхняя граница
            Console.Write("┌");
            for (int i = 0; i < Width; i++) Console.Write("─");
            Console.WriteLine("┐");

            // Игровое поле
            for (int y = 0; y < Height; y++)
            {
                Console.Write("│");
                for (int x = 0; x < Width; x++)
                {
                    var currentPos = new Position(x, y);

                    if (snake.First.Value.Equals(currentPos))
                    {
                        Console.Write("●"); // Голова
                    }
                    else if (snake.Contains(currentPos))
                    {
                        Console.Write("○"); // Тело
                    }
                    else if (food.Equals(currentPos))
                    {
                        Console.Write("★"); // Еда
                    }
                    else
                    {
                        Console.Write(" ");
                    }
                }
                Console.WriteLine("│");
            }

            // Нижняя граница
            Console.Write("└");
            for (int i = 0; i < Width; i++) Console.Write("─");
            Console.WriteLine("┘");

            // Информация
            Console.WriteLine($"\n Счёт: {score}");
            Console.WriteLine(" Управление: WASD | Q - выход | R - рестарт");

            if (gameOver)
            {
                Console.WriteLine("\n 🎮 ИГРА ОКОНЧЕНА! Нажмите R для рестарта");
            }
        }

        private void HandleInput()
        {
            if (Console.KeyAvailable)
            {
                var key = Console.ReadKey(true).Key;

                if (key == ConsoleKey.Q)
                {
                    running = false;
                    return;
                }

                if (gameOver)
                {
                    if (key == ConsoleKey.R)
                    {
                        Reset();
                    }
                    return;
                }

                switch (key)
                {
                    case ConsoleKey.W:
                    case ConsoleKey.UpArrow:
                        nextDirection = Direction.Up;
                        break;
                    case ConsoleKey.S:
                    case ConsoleKey.DownArrow:
                        nextDirection = Direction.Down;
                        break;
                    case ConsoleKey.A:
                    case ConsoleKey.LeftArrow:
                        nextDirection = Direction.Left;
                        break;
                    case ConsoleKey.D:
                    case ConsoleKey.RightArrow:
                        nextDirection = Direction.Right;
                        break;
                }
            }
        }

        public void Start()
        {
            Console.CursorVisible = false;
            Console.WriteLine("=== КОНСОЛЬНАЯ ЗМЕЙКА НА C# ===\n");
            Console.WriteLine("Нажмите любую клавишу для начала...");
            Console.ReadKey(true);

            while (running)
            {
                if (!gameOver)
                {
                    Move();
                }
                Render();
                HandleInput();
                Thread.Sleep(InitialSpeed);
            }

            Console.CursorVisible = true;
            Console.Clear();
            Console.WriteLine("Игра завершена. Спасибо за игру!");
        }
    }
}

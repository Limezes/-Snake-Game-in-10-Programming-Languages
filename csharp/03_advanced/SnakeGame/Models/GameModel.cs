using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;

namespace SnakeGame.Models
{
    public enum Direction { Up, Down, Left, Right }
    public enum Difficulty { Easy, Medium, Hard, Expert }

    public class GameModel : INotifyPropertyChanged
    {
        private const int GridWidth = 20;
        private const int GridHeight = 20;

        private Snake snake;
        private ObservableCollection<Food> foods;
        private ObservableCollection<Wall> walls;
        private ObservableCollection<PowerUp> powerUps;
        private int score;
        private int level;
        private bool isGameOver;
        private Random random;

        public event PropertyChangedEventHandler? PropertyChanged;
        public event EventHandler<int>? ScoreChanged;
        public event EventHandler<int>? LevelChanged;
        public event EventHandler<bool>? GameStateChanged;

        public GameModel(Difficulty difficulty)
        {
            random = new Random();
            snake = new Snake();
            foods = new ObservableCollection<Food>();
            walls = new ObservableCollection<Wall>();
            powerUps = new ObservableCollection<PowerUp>();

            InitializeLevel(difficulty);
        }

        public Snake Snake => snake;
        public ObservableCollection<Food> Foods => foods;
        public ObservableCollection<Wall> Walls => walls;
        public ObservableCollection<PowerUp> PowerUps => powerUps;

        public int Score
        {
            get => score;
            private set
            {
                if (score != value)
                {
                    score = value;
                    OnPropertyChanged();
                    ScoreChanged?.Invoke(this, value);
                }
            }
        }

        public int Level
        {
            get => level;
            private set
            {
                if (level != value)
                {
                    level = value;
                    OnPropertyChanged();
                    LevelChanged?.Invoke(this, value);
                }
            }
        }

        public bool IsGameOver
        {
            get => isGameOver;
            private set
            {
                if (isGameOver != value)
                {
                    isGameOver = value;
                    OnPropertyChanged();
                    GameStateChanged?.Invoke(this, value);
                }
            }
        }

        private void InitializeLevel(Difficulty difficulty)
        {
            snake.Reset();

            // Очистка коллекций
            foods.Clear();
            walls.Clear();
            powerUps.Clear();

            // Создание начальной еды
            SpawnFood(FoodType.Normal);

            // Создание стен для сложных уровней
            if (difficulty == Difficulty.Hard || difficulty == Difficulty.Expert)
            {
                GenerateWalls();
            }

            Level = 1;
            Score = 0;
            IsGameOver = false;
        }

        private void GenerateWalls()
        {
            // Генерация стен по краям
            for (int x = 0; x < GridWidth; x++)
            {
                walls.Add(new Wall(x, 0));
                walls.Add(new Wall(x, GridHeight - 1));
            }
            for (int y = 1; y < GridHeight - 1; y++)
            {
                walls.Add(new Wall(0, y));
                walls.Add(new Wall(GridWidth - 1, y));
            }

            // Добавление случайных стен внутри
            for (int i = 0; i < Level * 5; i++)
            {
                int x = random.Next(2, GridWidth - 2);
                int y = random.Next(2, GridHeight - 2);

                if (!IsPositionOccupied(x, y))
                {
                    walls.Add(new Wall(x, y));
                }
            }
        }

        private bool IsPositionOccupied(int x, int y)
        {
            if (snake.GetBody().Any(p => p.X == x && p.Y == y))
                return true;

            if (walls.Any(w => w.X == x && w.Y == y))
                return true;

            return false;
        }

        private void SpawnFood(FoodType type)
        {
            int maxAttempts = 1000;
            int attempts = 0;

            while (attempts < maxAttempts)
            {
                int x = random.Next(GridWidth);
                int y = random.Next(GridHeight);

                if (!IsPositionOccupied(x, y))
                {
                    foods.Add(new Food(x, y, type));
                    return;
                }

                attempts++;
            }
        }

        private void SpawnPowerUp()
        {
            if (powerUps.Count < 3 && random.NextDouble() < 0.3)
            {
                int maxAttempts = 100;
                int attempts = 0;

                while (attempts < maxAttempts)
                {
                    int x = random.Next(GridWidth);
                    int y = random.Next(GridHeight);

                    if (!IsPositionOccupied(x, y))
                    {
                        powerUps.Add(new PowerUp(x, y, (PowerUpType)random.Next(5)));
                        return;
                    }

                    attempts++;
                }
            }
        }

        public void ChangeDirection(Direction newDirection)
        {
            snake.ChangeDirection(newDirection);
        }

        public void Update()
        {
            if (IsGameOver) return;

            snake.Move();

            // Проверка столкновений
            var head = snake.GetHead();

            // Столкновение со стенами
            if (head.X < 0 || head.X >= GridWidth || 
                head.Y < 0 || head.Y >= GridHeight ||
                walls.Any(w => w.X == head.X && w.Y == head.Y))
            {
                IsGameOver = true;
                return;
            }

            // Проверка еды
            var eatenFood = foods.FirstOrDefault(f => f.X == head.X && f.Y == head.Y);
            if (eatenFood != null)
            {
                Score += eatenFood.Points;
                snake.Grow();

                // Применение эффекта
                ApplyFoodEffect(eatenFood.Type);

                foods.Remove(eatenFood);
                SpawnFood(FoodType.Normal);
            }

            // Проверка power-ups
            var collectedPowerUp = powerUps.FirstOrDefault(p => p.X == head.X && p.Y == head.Y);
            if (collectedPowerUp != null)
            {
                ApplyPowerUp(collectedPowerUp.Type);
                powerUps.Remove(collectedPowerUp);
            }

            // Проверка столкновения с собой
            if (snake.CheckSelfCollision() && !snake.IsInvincible)
            {
                IsGameOver = true;
                return;
            }

            // Обновление эффектов
            snake.UpdateEffects();

            // Удаление просроченных power-ups
            for (int i = powerUps.Count - 1; i >= 0; i--)
            {
                if (powerUps[i].IsExpired)
                {
                    powerUps.RemoveAt(i);
                }
            }

            // Спавн новых объектов
            if (foods.Count < 3)
            {
                SpawnFood(FoodType.Normal);
            }

            if (random.NextDouble() < 0.02)
            {
                SpawnPowerUp();
            }

            // Проверка повышения уровня
            if (Score > Level * 100)
            {
                LevelUp();
            }
        }

        private void ApplyFoodEffect(FoodType type)
        {
            switch (type)
            {
                case FoodType.Speed:
                    snake.SetSpeedMultiplier(1.5, 300);
                    break;
                case FoodType.Slow:
                    snake.SetSpeedMultiplier(0.5, 300);
                    break;
                case FoodType.Golden:
                    snake.SetInvincible(true, 500);
                    break;
            }
        }

        private void ApplyPowerUp(PowerUpType type)
        {
            switch (type)
            {
                case PowerUpType.SpeedBoost:
                    snake.SetSpeedMultiplier(2.0, 500);
                    break;
                case PowerUpType.Invincibility:
                    snake.SetInvincible(true, 500);
                    break;
                case PowerUpType.ExtraLife:
                    // Дополнительная жизнь - сбрасываем game over при следующем столкновении
                    break;
                case PowerUpType.ScoreMultiplier:
                    Score *= 2;
                    break;
            }
        }

        private void LevelUp()
        {
            Level++;

            // Добавление новых стен
            if (Level % 2 == 0)
            {
                for (int i = 0; i < Level; i++)
                {
                    int x = random.Next(2, GridWidth - 2);
                    int y = random.Next(2, GridHeight - 2);

                    if (!IsPositionOccupied(x, y))
                    {
                        walls.Add(new Wall(x, y));
                    }
                }
            }

            // Увеличение скорости
            snake.IncreaseBaseSpeed();
        }

        protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}

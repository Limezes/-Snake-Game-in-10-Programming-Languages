using System;
using System.Collections.Generic;
using System.Drawing;

namespace SnakeGameWinForms
{
    public enum Direction { Up, Down, Left, Right }

    public class GameEngine
    {
        private const int GridSize = 20;
        private const int CellSize = 25;

        private Snake snake;
        private Food food;
        private int score;
        private int highScore;
        private bool isRunning;
        private bool isPaused;
        private bool gameOver;

        public event EventHandler<int>? ScoreChanged;
        public event EventHandler<int>? HighScoreChanged;
        public event EventHandler? GameOver;

        public int Score => score;
        public bool IsRunning => isRunning;
        public bool IsPaused => isPaused;

        public GameEngine()
        {
            LoadHighScore();
            Reset();
        }

        private void LoadHighScore()
        {
            try
            {
                if (System.IO.File.Exists("highscore.txt"))
                {
                    string hs = System.IO.File.ReadAllText("highscore.txt");
                    highScore = int.Parse(hs);
                }
            }
            catch { }
        }

        private void SaveHighScore()
        {
            try
            {
                System.IO.File.WriteAllText("highscore.txt", highScore.ToString());
            }
            catch { }
        }

        public void Reset()
        {
            snake = new Snake();
            food = new Food();
            food.Respawn(GetAllOccupiedPositions());
            score = 0;
            gameOver = false;
        }

        public void Start()
        {
            Reset();
            isRunning = true;
            isPaused = false;
        }

        public void TogglePause()
        {
            if (isRunning)
            {
                isPaused = !isPaused;
            }
        }

        public void ChangeDirection(Direction newDir)
        {
            snake.ChangeDirection(newDir);
        }

        public void Update()
        {
            if (!isRunning || isPaused || gameOver) return;

            snake.Move();

            // Проверка столкновения со стенами
            var head = snake.GetHead();
            if (head.X < 0 || head.X >= GridSize || head.Y < 0 || head.Y >= GridSize)
            {
                GameOverHandler();
                return;
            }

            // Проверка поедания еды
            if (head.Equals(food.Position))
            {
                snake.Grow();
                score += food.Points;
                ScoreChanged?.Invoke(this, score);

                if (score > highScore)
                {
                    highScore = score;
                    HighScoreChanged?.Invoke(this, highScore);
                    SaveHighScore();
                }

                food.Respawn(GetAllOccupiedPositions());
            }

            // Проверка столкновения с собой
            if (snake.CheckSelfCollision())
            {
                GameOverHandler();
            }
        }

        private void GameOverHandler()
        {
            gameOver = true;
            isRunning = false;
            GameOver?.Invoke(this, EventArgs.Empty);
        }

        private List<Point> GetAllOccupiedPositions()
        {
            var positions = new List<Point>(snake.GetBody());
            return positions;
        }

        public void Draw(Graphics g, Rectangle bounds)
        {
            g.Clear(Color.FromArgb(30, 30, 40));

            // Рисование сетки
            using (Pen gridPen = new Pen(Color.FromArgb(50, 50, 70)))
            {
                for (int i = 0; i <= GridSize; i++)
                {
                    g.DrawLine(gridPen, i * CellSize, 0, i * CellSize, GridSize * CellSize);
                    g.DrawLine(gridPen, 0, i * CellSize, GridSize * CellSize, i * CellSize);
                }
            }

            // Рисование змейки
            snake.Draw(g, CellSize);

            // Рисование еды
            food.Draw(g, CellSize);
        }
    }
}

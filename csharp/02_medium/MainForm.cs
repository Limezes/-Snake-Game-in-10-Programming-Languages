using System;
using System.Drawing;
using System.Windows.Forms;

namespace SnakeGameWinForms
{
    public partial class MainForm : Form
    {
        private GameEngine gameEngine;
        private Timer gameTimer;
        private Label scoreLabel;
        private Label highScoreLabel;
        private Button startButton;
        private Button pauseButton;
        private ComboBox difficultyCombo;

        public MainForm()
        {
            InitializeComponent();
            InitializeGame();
        }

        private void InitializeComponent()
        {
            this.Text = "🐍 Змейка на WinForms";
            this.Size = new Size(800, 600);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.DoubleBuffered = true;
            this.KeyPreview = true;
            this.BackColor = Color.FromArgb(40, 40, 40);

            // Создание элементов управления
            scoreLabel = new Label
            {
                Location = new Point(10, 10),
                Size = new Size(200, 30),
                Text = "Счёт: 0",
                ForeColor = Color.White,
                Font = new Font("Arial", 14, FontStyle.Bold)
            };

            highScoreLabel = new Label
            {
                Location = new Point(220, 10),
                Size = new Size(200, 30),
                Text = "Рекорд: 0",
                ForeColor = Color.Gold,
                Font = new Font("Arial", 14, FontStyle.Bold)
            };

            startButton = new Button
            {
                Location = new Point(600, 10),
                Size = new Size(80, 30),
                Text = "Старт",
                BackColor = Color.Green,
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            startButton.Click += StartButton_Click;

            pauseButton = new Button
            {
                Location = new Point(690, 10),
                Size = new Size(80, 30),
                Text = "Пауза",
                BackColor = Color.Orange,
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Enabled = false
            };
            pauseButton.Click += PauseButton_Click;

            difficultyCombo = new ComboBox
            {
                Location = new Point(500, 15),
                Size = new Size(90, 25),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            difficultyCombo.Items.AddRange(new[] { "Легко", "Средне", "Сложно" });
            difficultyCombo.SelectedIndex = 1;
            difficultyCombo.SelectedIndexChanged += DifficultyCombo_SelectedIndexChanged;

            Controls.AddRange(new Control[] { 
                scoreLabel, highScoreLabel, startButton, 
                pauseButton, difficultyCombo 
            });

            this.Paint += MainForm_Paint;
            this.KeyDown += MainForm_KeyDown;
        }

        private void InitializeGame()
        {
            gameEngine = new GameEngine();
            gameEngine.ScoreChanged += (s, score) => scoreLabel.Text = $"Счёт: {score}";
            gameEngine.HighScoreChanged += (s, score) => highScoreLabel.Text = $"Рекорд: {score}";
            gameEngine.GameOver += (s, e) =>
            {
                pauseButton.Enabled = false;
                startButton.Enabled = true;
                MessageBox.Show($"Игра окончена! Ваш счёт: {gameEngine.Score}", 
                    "Конец игры", MessageBoxButtons.OK, MessageBoxIcon.Information);
            };

            gameTimer = new Timer { Interval = 100 };
            gameTimer.Tick += (s, e) =>
            {
                gameEngine.Update();
                Invalidate();
            };
        }

        private void StartButton_Click(object? sender, EventArgs e)
        {
            gameEngine.Start();
            gameTimer.Start();
            startButton.Enabled = false;
            pauseButton.Enabled = true;
            Focus();
        }

        private void PauseButton_Click(object? sender, EventArgs e)
        {
            gameEngine.TogglePause();
            pauseButton.Text = gameEngine.IsPaused ? "Продолжить" : "Пауза";
        }

        private void DifficultyCombo_SelectedIndexChanged(object? sender, EventArgs e)
        {
            int speed = difficultyCombo.SelectedIndex switch
            {
                0 => 150,
                1 => 100,
                2 => 70,
                _ => 100
            };
            gameTimer.Interval = speed;
        }

        private void MainForm_KeyDown(object? sender, KeyEventArgs e)
        {
            if (gameEngine.IsRunning && !gameEngine.IsPaused)
            {
                switch (e.KeyCode)
                {
                    case Keys.Up:
                    case Keys.W:
                        gameEngine.ChangeDirection(Direction.Up);
                        break;
                    case Keys.Down:
                    case Keys.S:
                        gameEngine.ChangeDirection(Direction.Down);
                        break;
                    case Keys.Left:
                    case Keys.A:
                        gameEngine.ChangeDirection(Direction.Left);
                        break;
                    case Keys.Right:
                    case Keys.D:
                        gameEngine.ChangeDirection(Direction.Right);
                        break;
                }
            }

            if (e.KeyCode == Keys.Space)
            {
                PauseButton_Click(null, EventArgs.Empty);
            }
        }

        private void MainForm_Paint(object? sender, PaintEventArgs e)
        {
            if (gameEngine != null)
            {
                gameEngine.Draw(e.Graphics, ClientRectangle);
            }
        }
    }
}

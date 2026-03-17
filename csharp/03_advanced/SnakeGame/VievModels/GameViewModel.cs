using System;
using System.Windows.Input;
using System.Windows.Threading;
using SnakeGame.Models;
using SnakeGame.Services;
using SnakeGame.Helpers;

namespace SnakeGame.ViewModels
{
    public class GameViewModel : ViewModelBase
    {
        private readonly ISettingsService _settingsService;
        private readonly DispatcherTimer _gameTimer;
        private GameModel _gameModel;
        private int _score;
        private int _highScore;
        private int _level;
        private bool _isPaused;
        private bool _isGameOver;

        public GameViewModel(ISettingsService settingsService)
        {
            _settingsService = settingsService;
            _gameModel = new GameModel(settingsService.GetDifficulty());
            
            _gameTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(settingsService.GetGameSpeed())
            };
            _gameTimer.Tick += GameTimer_Tick;

            MoveCommand = new RelayCommand(ExecuteMove, CanExecuteMove);
            PauseCommand = new RelayCommand(ExecutePause);
            RestartCommand = new RelayCommand(ExecuteRestart);

            LoadHighScore();
            StartNewGame();
        }

        public int Score
        {
            get => _score;
            set => SetProperty(ref _score, value);
        }

        public int HighScore
        {
            get => _highScore;
            set => SetProperty(ref _highScore, value);
        }

        public int Level
        {
            get => _level;
            set => SetProperty(ref _level, value);
        }

        public bool IsPaused
        {
            get => _isPaused;
            set => SetProperty(ref _isPaused, value);
        }

        public bool IsGameOver
        {
            get => _isGameOver;
            set => SetProperty(ref _isGameOver, value);
        }

        public GameModel GameModel
        {
            get => _gameModel;
            set => SetProperty(ref _gameModel, value);
        }

        public ICommand MoveCommand { get; }
        public ICommand PauseCommand { get; }
        public ICommand RestartCommand { get; }

        private void LoadHighScore()
        {
            HighScore = _settingsService.GetHighScore();
        }

        private void StartNewGame()
        {
            _gameModel = new GameModel(_settingsService.GetDifficulty());
            _gameModel.GameStateChanged += OnGameStateChanged;
            _gameModel.ScoreChanged += OnScoreChanged;
            _gameModel.LevelChanged += OnLevelChanged;

            Score = 0;
            Level = 1;
            IsGameOver = false;
            IsPaused = false;

            _gameTimer.Start();

            OnPropertyChanged(nameof(GameModel));
        }

        private void OnGameStateChanged(object? sender, bool isGameOver)
        {
            IsGameOver = isGameOver;
            if (isGameOver)
            {
                _gameTimer.Stop();
                CheckHighScore();
            }
        }

        private void OnScoreChanged(object? sender, int newScore)
        {
            Score = newScore;
        }

        private void OnLevelChanged(object? sender, int newLevel)
        {
            Level = newLevel;
        }

        private void CheckHighScore()
        {
            if (Score > HighScore)
            {
                HighScore = Score;
                _settingsService.SetHighScore(HighScore);
            }
        }

        private void GameTimer_Tick(object? sender, EventArgs e)
        {
            if (!IsPaused && !IsGameOver)
            {
                _gameModel.Update();
            }
        }

        private bool CanExecuteMove(object? parameter)
        {
            return !IsPaused && !IsGameOver;
        }

        private void ExecuteMove(object? parameter)
        {
            if (parameter is string directionStr && 
                Enum.TryParse<Direction>(directionStr, out var direction))
            {
                _gameModel.ChangeDirection(direction);
            }
        }

        private void ExecutePause(object? parameter)
        {
            IsPaused = !IsPaused;
        }

        private void ExecuteRestart(object? parameter)
        {
            StartNewGame();
        }
    }
}

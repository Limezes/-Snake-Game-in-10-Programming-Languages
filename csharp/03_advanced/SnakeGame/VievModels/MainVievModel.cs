using System.Windows.Input;
using SnakeGame.Helpers;
using SnakeGame.Services;

namespace SnakeGame.ViewModels
{
    public class MainViewModel : ViewModelBase
    {
        private readonly ISettingsService _settingsService;
        private ViewModelBase _currentView;
        private string _playerName;

        public MainViewModel(ISettingsService settingsService)
        {
            _settingsService = settingsService;
            _playerName = settingsService.GetPlayerName();
            _currentView = new GameViewModel(settingsService);

            NavigateToGameCommand = new RelayCommand(ExecuteNavigateToGame);
            NavigateToSettingsCommand = new RelayCommand(ExecuteNavigateToSettings);
            ExitCommand = new RelayCommand(ExecuteExit);
        }

        public ViewModelBase CurrentView
        {
            get => _currentView;
            set => SetProperty(ref _currentView, value);
        }

        public string PlayerName
        {
            get => _playerName;
            set
            {
                if (SetProperty(ref _playerName, value))
                {
                    _settingsService.SetPlayerName(value);
                }
            }
        }

        public ICommand NavigateToGameCommand { get; }
        public ICommand NavigateToSettingsCommand { get; }
        public ICommand ExitCommand { get; }

        private void ExecuteNavigateToGame(object? parameter)
        {
            CurrentView = new GameViewModel(_settingsService);
        }

        private void ExecuteNavigateToSettings(object? parameter)
        {
            CurrentView = new SettingsViewModel(_settingsService);
        }

        private void ExecuteExit(object? parameter)
        {
            System.Windows.Application.Current.Shutdown();
        }
    }
}

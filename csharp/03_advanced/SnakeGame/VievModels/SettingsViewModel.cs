using System.Collections.ObjectModel;
using System.Windows.Input;
using SnakeGame.Helpers;
using SnakeGame.Models;
using SnakeGame.Services;

namespace SnakeGame.ViewModels
{
    public class SettingsViewModel : ViewModelBase
    {
        private readonly ISettingsService _settingsService;
        private Difficulty _selectedDifficulty;
        private string _playerName;
        private bool _soundEnabled;
        private int _soundVolume;
        private bool _gridVisible;

        public SettingsViewModel(ISettingsService settingsService)
        {
            _settingsService = settingsService;

            Difficulties = new ObservableCollection<Difficulty>(
                Enum.GetValues<Difficulty>()
            );

            LoadSettings();

            SaveCommand = new RelayCommand(ExecuteSave);
            ResetCommand = new RelayCommand(ExecuteReset);
        }

        public ObservableCollection<Difficulty> Difficulties { get; }

        public Difficulty SelectedDifficulty
        {
            get => _selectedDifficulty;
            set => SetProperty(ref _selectedDifficulty, value);
        }

        public string PlayerName
        {
            get => _playerName;
            set => SetProperty(ref _playerName, value);
        }

        public bool SoundEnabled
        {
            get => _soundEnabled;
            set => SetProperty(ref _soundEnabled, value);
        }

        public int SoundVolume
        {
            get => _soundVolume;
            set => SetProperty(ref _soundVolume, value);
        }

        public bool GridVisible
        {
            get => _gridVisible;
            set => SetProperty(ref _gridVisible, value);
        }

        public ICommand SaveCommand { get; }
        public ICommand ResetCommand { get; }

        private void LoadSettings()
        {
            SelectedDifficulty = _settingsService.GetDifficulty();
            PlayerName = _settingsService.GetPlayerName();
            SoundEnabled = _settingsService.IsSoundEnabled();
            SoundVolume = _settingsService.GetSoundVolume();
            GridVisible = _settingsService.IsGridVisible();
        }

        private void ExecuteSave(object? parameter)
        {
            _settingsService.SetDifficulty(SelectedDifficulty);
            _settingsService.SetPlayerName(PlayerName);
            _settingsService.SetSoundEnabled(SoundEnabled);
            _settingsService.SetSoundVolume(SoundVolume);
            _settingsService.SetGridVisible(GridVisible);
        }

        private void ExecuteReset(object? parameter)
        {
            _settingsService.ResetToDefaults();
            LoadSettings();
        }
    }
}

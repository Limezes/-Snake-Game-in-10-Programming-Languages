using SnakeGame.Models;

namespace SnakeGame.Services
{
    public interface ISettingsService
    {
        Difficulty GetDifficulty();
        void SetDifficulty(Difficulty difficulty);

        string GetPlayerName();
        void SetPlayerName(string name);

        bool IsSoundEnabled();
        void SetSoundEnabled(bool enabled);

        int GetSoundVolume();
        void SetSoundVolume(int volume);

        bool IsGridVisible();
        void SetGridVisible(bool visible);

        int GetHighScore();
        void SetHighScore(int score);

        int GetGameSpeed();
        
        void ResetToDefaults();
        void Save();
        void Load();
    }
}

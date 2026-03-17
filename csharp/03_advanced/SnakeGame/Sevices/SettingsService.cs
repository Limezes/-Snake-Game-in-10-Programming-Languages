using System;
using System.IO;
using System.Text.Json;
using SnakeGame.Models;

namespace SnakeGame.Services
{
    public class SettingsService : ISettingsService
    {
        private const string SettingsFile = "settings.json";
        private SettingsData data;

        public SettingsService()
        {
            Load();
        }

        public Difficulty GetDifficulty() => data.Difficulty;
        public void SetDifficulty(Difficulty difficulty)
        {
            data.Difficulty = difficulty;
            Save();
        }

        public string GetPlayerName() => data.PlayerName;
        public void SetPlayerName(string name)
        {
            data.PlayerName = name;
            Save();
        }

        public bool IsSoundEnabled() => data.SoundEnabled;
        public void SetSoundEnabled(bool enabled)
        {
            data.SoundEnabled = enabled;
            Save();
        }

        public int GetSoundVolume() => data.SoundVolume;
        public void SetSoundVolume(int volume)
        {
            data.SoundVolume = Math.Clamp(volume, 0, 100);
            Save();
        }

        public bool IsGridVisible() => data.GridVisible;
        public void SetGridVisible(bool visible)
        {
            data.GridVisible = visible;
            Save();
        }

        public int GetHighScore() => data.HighScore;
        public void SetHighScore(int score)
        {
            if (score > data.HighScore)
            {
                data.HighScore = score;
                Save();
            }
        }

        public int GetGameSpeed()
        {
            return data.Difficulty switch
            {
                Difficulty.Easy => 150,
                Difficulty.Medium => 100,
                Difficulty.Hard => 70,
                Difficulty.Expert => 50,
                _ => 100
            };
        }

        public void ResetToDefaults()
        {
            data = new SettingsData();
            Save();
        }

        public void Save()
        {
            try
            {
                string json = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
                File.WriteAllText(SettingsFile, json);
            }
            catch { }
        }

        public void Load()
        {
            try
            {
                if (File.Exists(SettingsFile))
                {
                    string json = File.ReadAllText(SettingsFile);
                    data = JsonSerializer.Deserialize<SettingsData>(json) ?? new SettingsData();
                }
                else
                {
                    data = new SettingsData();
                }
            }
            catch
            {
                data = new SettingsData();
            }
        }

        private class SettingsData
        {
            public Difficulty Difficulty { get; set; } = Difficulty.Medium;
            public string PlayerName { get; set; } = "Player";
            public bool SoundEnabled { get; set; } = true;
            public int SoundVolume { get; set; } = 50;
            public bool GridVisible { get; set; } = true;
            public int HighScore { get; set; } = 0;
        }
    }
}

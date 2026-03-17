using System;
using System.IO;
using System.Text.Json;

namespace SnakeGameWinForms
{
    public class ScoreManager
    {
        private const string ScoresFile = "scores.json";
        private int currentScore;
        private int highScore;

        public int CurrentScore => currentScore;
        public int HighScore => highScore;

        public ScoreManager()
        {
            LoadScores();
        }

        public void AddScore(int points)
        {
            currentScore += points;
            if (currentScore > highScore)
            {
                highScore = currentScore;
                SaveScores();
            }
        }

        public void ResetScore()
        {
            currentScore = 0;
        }

        private void LoadScores()
        {
            try
            {
                if (File.Exists(ScoresFile))
                {
                    string json = File.ReadAllText(ScoresFile);
                    var data = JsonSerializer.Deserialize<ScoreData>(json);
                    if (data != null)
                    {
                        highScore = data.HighScore;
                    }
                }
            }
            catch
            {
                highScore = 0;
            }
        }

        private void SaveScores()
        {
            try
            {
                var data = new ScoreData { HighScore = highScore };
                string json = JsonSerializer.Serialize(data);
                File.WriteAllText(ScoresFile, json);
            }
            catch { }
        }

        private class ScoreData
        {
            public int HighScore { get; set; }
        }
    }
}

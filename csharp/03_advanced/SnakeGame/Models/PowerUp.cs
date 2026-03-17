using System;

namespace SnakeGame.Models
{
    public enum PowerUpType
    {
        SpeedBoost,
        Invincibility,
        SlowTime,
        ExtraLife,
        ScoreMultiplier
    }

    public class PowerUp
    {
        public int X { get; set; }
        public int Y { get; set; }
        public PowerUpType Type { get; set; }
        public string Color { get; set; }
        public string Symbol { get; set; }
        public int Duration { get; set; }
        public int Lifetime { get; set; }
        public int Age { get; set; }
        public bool IsExpired => Age >= Lifetime;

        public PowerUp(int x, int y, PowerUpType type)
        {
            X = x;
            Y = y;
            Type = type;
            Age = 0;
            Lifetime = 300; // 5 секунд при 60 FPS

            switch (type)
            {
                case PowerUpType.SpeedBoost:
                    Color = "#00FFFF";
                    Symbol = "⚡";
                    Duration = 300;
                    break;
                case PowerUpType.Invincibility:
                    Color = "#FFFF00";
                    Symbol = "🛡️";
                    Duration = 300;
                    break;
                case PowerUpType.SlowTime:
                    Color = "#FF00FF";
                    Symbol = "⏱️";
                    Duration = 300;
                    break;
                case PowerUpType.ExtraLife:
                    Color = "#FF4444";
                    Symbol = "❤️";
                    Duration = 0;
                    break;
                case PowerUpType.ScoreMultiplier:
                    Color = "#FFAA00";
                    Symbol = "✖️";
                    Duration = 0;
                    break;
            }
        }

        public void Update()
        {
            Age++;
        }
    }
}

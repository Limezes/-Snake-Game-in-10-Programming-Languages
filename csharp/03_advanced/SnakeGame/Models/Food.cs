using System;

namespace SnakeGame.Models
{
    public enum FoodType
    {
        Normal,
        Bonus,
        Speed,
        Slow,
        Golden
    }

    public class Food
    {
        public int X { get; set; }
        public int Y { get; set; }
        public FoodType Type { get; set; }
        public int Points { get; set; }
        public string Color { get; set; }
        public int Lifetime { get; set; }
        public int Age { get; set; }
        public bool IsExpired => Lifetime > 0 && Age >= Lifetime;

        public Food(int x, int y, FoodType type)
        {
            X = x;
            Y = y;
            Type = type;
            Age = 0;

            switch (type)
            {
                case FoodType.Normal:
                    Points = 10;
                    Color = "#FF4444";
                    Lifetime = 0;
                    break;
                case FoodType.Bonus:
                    Points = 50;
                    Color = "#FFD700";
                    Lifetime = 300;
                    break;
                case FoodType.Speed:
                    Points = 20;
                    Color = "#44AAFF";
                    Lifetime = 0;
                    break;
                case FoodType.Slow:
                    Points = 20;
                    Color = "#AA44FF";
                    Lifetime = 0;
                    break;
                case FoodType.Golden:
                    Points = 100;
                    Color = "#FFAA00";
                    Lifetime = 0;
                    break;
            }
        }

        public void Update()
        {
            if (Lifetime > 0)
            {
                Age++;
            }
        }
    }
}

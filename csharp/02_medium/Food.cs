using System;
using System.Collections.Generic;
using System.Drawing;

namespace SnakeGameWinForms
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
        private static readonly Random random = new Random();
        private const int GridSize = 20;

        public Point Position { get; private set; }
        public FoodType Type { get; private set; }
        public int Points { get; private set; }
        public Color Color { get; private set; }

        public Food()
        {
            Type = FoodType.Normal;
            Points = 10;
            Color = Color.Red;
        }

        public void Respawn(List<Point> occupiedPositions)
        {
            int maxAttempts = 1000;
            bool validPosition = false;

            do
            {
                Position = new Point(random.Next(GridSize), random.Next(GridSize));
                maxAttempts--;

                if (!occupiedPositions.Contains(Position))
                {
                    validPosition = true;
                }
            } while (!validPosition && maxAttempts > 0);

            // Случайный тип еды
            int chance = random.Next(100);

            if (chance < 70)
            {
                Type = FoodType.Normal;
                Points = 10;
                Color = Color.Red;
            }
            else if (chance < 85)
            {
                Type = FoodType.Bonus;
                Points = 50;
                Color = Color.Gold;
            }
            else if (chance < 93)
            {
                Type = FoodType.Speed;
                Points = 20;
                Color = Color.Cyan;
            }
            else if (chance < 98)
            {
                Type = FoodType.Slow;
                Points = 20;
                Color = Color.Magenta;
            }
            else
            {
                Type = FoodType.Golden;
                Points = 100;
                Color = Color.Orange;
            }
        }

        public void Draw(Graphics g, int cellSize)
        {
            Rectangle rect = new Rectangle(
                Position.X * cellSize + 2,
                Position.Y * cellSize + 2,
                cellSize - 4,
                cellSize - 4
            );

            using (SolidBrush brush = new SolidBrush(Color))
            {
                g.FillEllipse(brush, rect);
            }

            // Символ для особой еды
            if (Type != FoodType.Normal)
            {
                string symbol = Type switch
                {
                    FoodType.Bonus => "★",
                    FoodType.Speed => "⚡",
                    FoodType.Slow => "🐢",
                    FoodType.Golden => "👑",
                    _ => ""
                };

                using (Font font = new Font("Arial", 12))
                using (SolidBrush textBrush = new SolidBrush(Color.White))
                {
                    g.DrawString(symbol, font, textBrush, 
                        Position.X * cellSize + 5, 
                        Position.Y * cellSize + 3);
                }
            }
        }
    }
}

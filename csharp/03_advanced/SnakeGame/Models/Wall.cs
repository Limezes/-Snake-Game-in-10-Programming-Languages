namespace SnakeGame.Models
{
    public class Wall
    {
        public int X { get; set; }
        public int Y { get; set; }
        public bool IsDestructible { get; set; }
        public string Color { get; set; }

        public Wall(int x, int y, bool destructible = false)
        {
            X = x;
            Y = y;
            IsDestructible = destructible;
            Color = destructible ? "#8B4513" : "#4A4A5A";
        }
    }
}

using System.Collections.ObjectModel;
using System.Linq;

namespace SnakeGame.Models
{
    public class Snake
    {
        private ObservableCollection<GridPosition> body;
        private Direction direction;
        private Direction nextDirection;
        private bool growFlag;
        private bool invincible;
        private float speedMultiplier;
        private int invincibleTimer;
        private int speedTimer;
        private int baseSpeed;

        public Snake()
        {
            body = new ObservableCollection<GridPosition>();
            Reset();
        }

        public ObservableCollection<GridPosition> Body => body;
        public bool IsInvincible => invincible;
        public float SpeedMultiplier => speedMultiplier;

        public void Reset()
        {
            body.Clear();
            body.Add(new GridPosition(10, 10));
            body.Add(new GridPosition(9, 10));
            body.Add(new GridPosition(8, 10));

            direction = Direction.Right;
            nextDirection = Direction.Right;
            growFlag = false;
            invincible = false;
            speedMultiplier = 1.0f;
            invincibleTimer = 0;
            speedTimer = 0;
            baseSpeed = 100;
        }

        public void Move()
        {
            // Проверка направления
            if ((direction == Direction.Up && nextDirection != Direction.Down) ||
                (direction == Direction.Down && nextDirection != Direction.Up) ||
                (direction == Direction.Left && nextDirection != Direction.Right) ||
                (direction == Direction.Right && nextDirection != Direction.Left))
            {
                direction = nextDirection;
            }

            // Новая голова
            var head = body.First().Clone();

            switch (direction)
            {
                case Direction.Up: head.Y--; break;
                case Direction.Down: head.Y++; break;
                case Direction.Left: head.X--; break;
                case Direction.Right: head.X++; break;
            }

            // Добавление новой головы
            body.Insert(0, head);

            // Удаление хвоста
            if (!growFlag)
            {
                body.RemoveAt(body.Count - 1);
            }
            else
            {
                growFlag = false;
            }
        }

        public void Grow()
        {
            growFlag = true;
        }

        public void ChangeDirection(Direction newDir)
        {
            nextDirection = newDir;
        }

        public void SetInvincible(bool inv, int duration)
        {
            invincible = inv;
            invincibleTimer = duration;
        }

        public void SetSpeedMultiplier(float mult, int duration)
        {
            speedMultiplier = mult;
            speedTimer = duration;
        }

        public void IncreaseBaseSpeed()
        {
            if (baseSpeed > 30)
            {
                baseSpeed -= 10;
            }
        }

        public void UpdateEffects()
        {
            if (invincibleTimer > 0)
            {
                invincibleTimer--;
                if (invincibleTimer <= 0)
                {
                    invincible = false;
                }
            }

            if (speedTimer > 0)
            {
                speedTimer--;
                if (speedTimer <= 0)
                {
                    speedMultiplier = 1.0f;
                }
            }
        }

        public GridPosition GetHead()
        {
            return body.First();
        }

        public ObservableCollection<GridPosition> GetBody()
        {
            return body;
        }

        public bool CheckSelfCollision()
        {
            if (invincible) return false;

            var head = body.First();
            return body.Skip(1).Any(p => p.X == head.X && p.Y == head.Y);
        }

        public int GetCurrentSpeed()
        {
            return (int)(baseSpeed / speedMultiplier);
        }
    }

    public class GridPosition
    {
        public int X { get; set; }
        public int Y { get; set; }

        public GridPosition(int x, int y)
        {
            X = x;
            Y = y;
        }

        public GridPosition Clone()
        {
            return new GridPosition(X, Y);
        }

        public override bool Equals(object? obj)
        {
            if (obj is GridPosition other)
                return X == other.X && Y == other.Y;
            return false;
        }

        public override int GetHashCode()
        {
            return System.HashCode.Combine(X, Y);
        }
    }
}

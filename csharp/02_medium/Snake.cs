using System;
using System.Collections.Generic;
using System.Drawing;

namespace SnakeGameWinForms
{
    public class Snake
    {
        private LinkedList<Point> body;
        private Direction direction;
        private Direction nextDirection;
        private bool growFlag;

        public Snake()
        {
            body = new LinkedList<Point>();
            Reset();
        }

        public void Reset()
        {
            body.Clear();
            body.AddFirst(new Point(10, 10));
            body.AddFirst(new Point(9, 10));
            body.AddFirst(new Point(8, 10));
            direction = Direction.Right;
            nextDirection = Direction.Right;
            growFlag = false;
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
            Point head = body.First.Value;

            switch (direction)
            {
                case Direction.Up: head.Y--; break;
                case Direction.Down: head.Y++; break;
                case Direction.Left: head.X--; break;
                case Direction.Right: head.X++; break;
            }

            // Добавление новой головы
            body.AddFirst(head);

            // Удаление хвоста
            if (!growFlag)
            {
                body.RemoveLast();
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

        public Point GetHead()
        {
            return body.First.Value;
        }

        public List<Point> GetBody()
        {
            return new List<Point>(body);
        }

        public bool CheckSelfCollision()
        {
            var head = body.First.Value;
            var current = body.First.Next;

            while (current != null)
            {
                if (current.Value == head)
                {
                    return true;
                }
                current = current.Next;
            }

            return false;
        }

        public void Draw(Graphics g, int cellSize)
        {
            int index = 0;
            foreach (var point in body)
            {
                Rectangle rect = new Rectangle(
                    point.X * cellSize + 1,
                    point.Y * cellSize + 1,
                    cellSize - 2,
                    cellSize - 2
                );

                if (index == 0)
                {
                    // Голова
                    using (SolidBrush brush = new SolidBrush(Color.FromArgb(50, 255, 50)))
                    {
                        g.FillRectangle(brush, rect);
                    }

                    // Глаза
                    using (SolidBrush eyeBrush = new SolidBrush(Color.White))
                    {
                        switch (direction)
                        {
                            case Direction.Right:
                                g.FillEllipse(eyeBrush, rect.X + cellSize - 8, rect.Y + 3, 4, 4);
                                g.FillEllipse(eyeBrush, rect.X + cellSize - 8, rect.Y + cellSize - 7, 4, 4);
                                break;
                            case Direction.Left:
                                g.FillEllipse(eyeBrush, rect.X + 4, rect.Y + 3, 4, 4);
                                g.FillEllipse(eyeBrush, rect.X + 4, rect.Y + cellSize - 7, 4, 4);
                                break;
                            case Direction.Up:
                                g.FillEllipse(eyeBrush, rect.X + 3, rect.Y + 4, 4, 4);
                                g.FillEllipse(eyeBrush, rect.X + cellSize - 7, rect.Y + 4, 4, 4);
                                break;
                            case Direction.Down:
                                g.FillEllipse(eyeBrush, rect.X + 3, rect.Y + cellSize - 8, 4, 4);
                                g.FillEllipse(eyeBrush, rect.X + cellSize - 7, rect.Y + cellSize - 8, 4, 4);
                                break;
                        }
                    }
                }
                else
                {
                    // Тело
                    int alpha = 255 - (index * 15);
                    if (alpha < 100) alpha = 100;
                    using (SolidBrush brush = new SolidBrush(Color.FromArgb(alpha, 0, 200, 0)))
                    {
                        g.FillRectangle(brush, rect);
                    }
                }
                index++;
            }
        }
    }
}

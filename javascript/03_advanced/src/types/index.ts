// Типы для игры

export type Position = {
  x: number;
  y: number;
};

export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';

export type FoodType = 'normal' | 'bonus' | 'speed' | 'slow' | 'golden';

export type Food = {
  position: Position;
  type: FoodType;
  points: number;
  color: string;
  lifetime?: number;
};

export type Difficulty = 'easy' | 'medium' | 'hard' | 'expert';

export type GameState = 'menu' | 'playing' | 'paused' | 'gameOver';

export type PowerUp = {
  type: string;
  duration: number;
  multiplier?: number;
};

export type Player = {
  id: string;
  name: string;
  score: number;
  color?: string;
};

export type HighScore = {
  playerName: string;
  score: number;
  difficulty: Difficulty;
  date: string;
  level: number;
  foodEaten: number;
};

export type Achievement = {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlockedAt?: Date;
};

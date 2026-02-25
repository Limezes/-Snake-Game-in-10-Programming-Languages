import { useState, useEffect, useCallback, useRef } from 'react';
import { Position, Direction, Food, FoodType, GameState, Difficulty, PowerUp } from '../types';

const GRID_SIZE = 20;
const INITIAL_SNAKE: Position[] = [
  { x: 10, y: 10 },
  { x: 9, y: 10 },
  { x: 8, y: 10 },
];

const FOOD_TYPES = {
  normal: { points: 10, color: '#ff4757', chance: 0.7, symbol: '●' },
  bonus: { points: 50, color: '#ffd32a', chance: 0.15, symbol: '★', lifetime: 200 },
  speed: { points: 20, color: '#70a1ff', chance: 0.05, symbol: '⚡', effect: 'speed' },
  slow: { points: 20, color: '#a55eea', chance: 0.05, symbol: '🐢', effect: 'slow' },
  golden: { points: 100, color: '#ffa502', chance: 0.05, symbol: '👑', effect: 'invincible' },
};

const DIFFICULTY_SETTINGS = {
  easy: { speed: 150, walls: false, bonusChance: 0.2 },
  medium: { speed: 100, walls: false, bonusChance: 0.15 },
  hard: { speed: 70, walls: true, bonusChance: 0.1 },
  expert: { speed: 50, walls: true, bonusChance: 0.05 },
};

export const useGame = (difficulty: Difficulty = 'medium') => {
  const [gameState, setGameState] = useState<GameState>('menu');
  const [snake, setSnake] = useState<Position[]>(INITIAL_SNAKE);
  const [direction, setDirection] = useState<Direction>('RIGHT');
  const [nextDirection, setNextDirection] = useState<Direction>('RIGHT');
  const [foods, setFoods] = useState<Food[]>([]);
  const [score, setScore] = useState(0);
  const [level, setLevel] = useState(1);
  const [powerUp, setPowerUp] = useState<PowerUp | null>(null);
  const [walls, setWalls] = useState<Position[]>([]);
  
  const gameLoopRef = useRef<NodeJS.Timeout>();
  const settings = DIFFICULTY_SETTINGS[difficulty];

  // Генерация стен для уровня
  const generateWalls = useCallback((currentLevel: number) => {
    const newWalls: Position[] = [];
    
    if (currentLevel >= 2) {
      // Добавляем стены по краям
      for (let x = 0; x < GRID_SIZE; x++) {
        newWalls.push({ x, y: 0 });
        newWalls.push({ x, y: GRID_SIZE - 1 });
      }
      for (let y = 0; y < GRID_SIZE; y++) {
        newWalls.push({ x: 0, y });
        newWalls.push({ x: GRID_SIZE - 1, y });
      }
    }
    
    if (currentLevel >= 3) {
      // Добавляем внутренние стены
      for (let i = 5; i < 15; i++) {
        newWalls.push({ x: i, y: 10 });
      }
    }
    
    if (currentLevel >= 4) {
      // Добавляем лабиринт
      for (let i = 3; i < 17; i++) {
        newWalls.push({ x: i, y: 5 });
        newWalls.push({ x: i, y: 15 });
      }
    }
    
    return newWalls;
  }, []);

  // Создание еды
  const createFood = useCallback(() => {
    const availablePositions: Position[] = [];
    
    for (let x = 0; x < GRID_SIZE; x++) {
      for (let y = 0; y < GRID_SIZE; y++) {
        const pos = { x, y };
        if (!snake.some(s => s.x === pos.x && s.y === pos.y) &&
            !walls.some(w => w.x === pos.x && w.y === pos.y) &&
            !foods.some(f => f.position.x === pos.x && f.position.y === pos.y)) {
          availablePositions.push(pos);
        }
      }
    }
    
    if (availablePositions.length === 0) return null;
    
    const randomIndex = Math.floor(Math.random() * availablePositions.length);
    const position = availablePositions[randomIndex];
    
    // Выбор типа еды
    const rand = Math.random();
    let foodType: FoodType = 'normal';
    
    if (rand > 1 - settings.bonusChance) {
      const types: FoodType[] = ['bonus', 'speed', 'slow', 'golden'];
      foodType = types[Math.floor(Math.random() * types.length)];
    }
    
    const foodConfig = FOOD_TYPES[foodType];
    
    return {
      position,
      type: foodType,
      points: foodConfig.points,
      color: foodConfig.color,
      lifetime: foodConfig.lifetime,
    };
  }, [snake, walls, foods, settings.bonusChance]);

  // Движение змейки
  const moveSnake = useCallback(() => {
    // Проверка направления
    const opposite = {
      'UP': 'DOWN',
      'DOWN': 'UP',
      'LEFT': 'RIGHT',
      'RIGHT': 'LEFT'
    };

    if (nextDirection !== opposite[direction]) {
      setDirection(nextDirection);
    }

    setSnake(prevSnake => {
      const head = { ...prevSnake[0] };
      
      switch (direction) {
        case 'UP': head.y--; break;
        case 'DOWN': head.y++; break;
        case 'LEFT': head.x--; break;
        case 'RIGHT': head.x++; break;
      }

      // Проверка столкновений
      const newSnake = [head, ...prevSnake];
      
      // Проверка стены
      if (settings.walls) {
        if (walls.some(w => w.x === head.x && w.y === head.y)) {
          setGameState('gameOver');
          return prevSnake;
        }
      } else {
        // Телепортация через стены
        if (head.x < 0) head.x = GRID_SIZE - 1;
        if (head.x >= GRID_SIZE) head.x = 0;
        if (head.y < 0) head.y = GRID_SIZE - 1;
        if (head.y >= GRID_SIZE) head.y = 0;
      }

      // Проверка еды
      const eatenFoodIndex = foods.findIndex(f => 
        f.position.x === head.x && f.position.y === head.y
      );

      if (eatenFoodIndex !== -1) {
        const eatenFood = foods[eatenFoodIndex];
        setScore(prev => prev + eatenFood.points);
        
        // Применение эффекта
        if (eatenFood.type !== 'normal') {
          handlePowerUp(eatenFood.type);
        }
        
        setFoods(prev => prev.filter((_, i) => i !== eatenFoodIndex));
        
        // Добавляем новую еду
        const newFood = createFood();
        if (newFood) {
          setFoods(prev => [...prev, newFood]);
        }
        
        return newSnake;
      }

      // Удаление хвоста
      newSnake.pop();
      
      // Проверка столкновения с собой
      const headCollision = newSnake.slice(1).some(s => 
        s.x === head.x && s.y === head.y
      );
      
      if (headCollision && !powerUp?.type.includes('invincible')) {
        setGameState('gameOver');
        return prevSnake;
      }

      return newSnake;
    });
  }, [direction, nextDirection, foods, walls, powerUp, settings.walls, createFood]);

  // Обработка power-up
  const handlePowerUp = (type: FoodType) => {
    switch (type) {
      case 'speed':
        setPowerUp({ type: 'speed', duration: 100, multiplier: 1.5 });
        break;
      case 'slow':
        setPowerUp({ type: 'slow', duration: 100, multiplier: 0.5 });
        break;
      case 'golden':
        setPowerUp({ type: 'invincible', duration: 150 });
        break;
    }
  };

  // Обновление power-up
  useEffect(() => {
    if (powerUp) {
      const timer = setTimeout(() => {
        setPowerUp(prev => {
          if (prev && prev.duration > 0) {
            return { ...prev, duration: prev.duration - 1 };
          }
          return null;
        });
      }, 100);
      
      return () => clearTimeout(timer);
    }
  }, [powerUp]);

  // Инициализация игры
  const initGame = useCallback(() => {
    setSnake(INITIAL_SNAKE);
    setDirection('RIGHT');
    setNextDirection('RIGHT');
    setFoods([]);
    setScore(0);
    setLevel(1);
    setPowerUp(null);
    setWalls(generateWalls(1));
    setGameState('playing');
    
    // Создание начальной еды
    const initialFood = createFood();
    if (initialFood) {
      setFoods([initialFood]);
    }
  }, [createFood, generateWalls]);

  // Основной игровой цикл
  useEffect(() => {
    if (gameState === 'playing') {
      gameLoopRef.current = setInterval(() => {
        moveSnake();
      }, settings.speed / (powerUp?.multiplier || 1));
      
      return () => {
        if (gameLoopRef.current) {
          clearInterval(gameLoopRef.current);
        }
      };
    }
  }, [gameState, settings.speed, powerUp, moveSnake]);

  // Управление
  const handleKeyPress = useCallback((e: KeyboardEvent) => {
    const key = e.key.toLowerCase();
    
    const keyMap: Record<string, Direction> = {
      'arrowup': 'UP', 'w': 'UP',
      'arrowdown': 'DOWN', 's': 'DOWN',
      'arrowleft': 'LEFT', 'a': 'LEFT',
      'arrowright': 'RIGHT', 'd': 'RIGHT'
    };
    
    if (keyMap[key]) {
      e.preventDefault();
      setNextDirection(keyMap[key]);
    }
    
    if (key === ' ') {
      e.preventDefault();
      setGameState(prev => prev === 'playing' ? 'paused' : 'playing');
    }
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  return {
    gameState,
    snake,
    foods,
    score,
    level,
    powerUp,
    walls,
    gridSize: GRID_SIZE,
    initGame,
    setGameState,
  };
};

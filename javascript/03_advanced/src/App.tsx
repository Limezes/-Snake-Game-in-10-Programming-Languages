import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
import styled from 'styled-components';
import { useGame } from './hooks/useGame';
import { useLocalStorage } from './hooks/useLocalStorage';
import { Snake } from './components/Snake';
import { Food } from './components/Food';
import { ScoreBoard } from './components/ScoreBoard';
import { GameOver } from './components/GameOver';
import { Difficulty } from './types';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
`;

const GameWrapper = styled.div`
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 30px;
  padding: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
`;

const GameBoard = styled.div`
  position: relative;
  width: 500px;
  height: 500px;
  background: #0f172a;
  border-radius: 20px;
  overflow: hidden;
  border: 2px solid #334155;
  box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
`;

const Grid = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(rgba(51, 65, 85, 0.2) 1px, transparent 1px),
    linear-gradient(90deg, rgba(51, 65, 85, 0.2) 1px, transparent 1px);
  background-size: 25px 25px;
  pointer-events: none;
`;

const Wall = styled.div<{ x: number; y: number }>`
  position: absolute;
  left: ${props => props.x * 25}px;
  top: ${props => props.y * 25}px;
  width: 25px;
  height: 25px;
  background: linear-gradient(135deg, #475569, #334155);
  border: 1px solid #64748b;
`;

const Menu = styled(motion.div)`
  text-align: center;
  padding: 40px;
`;

const Title = styled.h1`
  font-size: 48px;
  color: #fbbf24;
  margin-bottom: 40px;
  text-shadow: 0 0 30px #fbbf24;
`;

const DifficultyButton = styled(motion.button)<{ active: boolean }>`
  background: ${props => props.active ? 
    'linear-gradient(135deg, #fbbf24, #f59e0b)' : 
    'rgba(255,255,255,0.1)'
  };
  color: ${props => props.active ? '#000' : '#fff'};
  border: none;
  padding: 15px 30px;
  font-size: 18px;
  border-radius: 50px;
  margin: 10px;
  cursor: pointer;
  font-weight: bold;
  border: 1px solid rgba(255,255,255,0.1);
  
  &:hover {
    background: ${props => props.active ? 
      'linear-gradient(135deg, #fcd34d, #fbbf24)' : 
      'rgba(255,255,255,0.2)'
    };
  }
`;

const StartButton = styled(motion.button)`
  background: linear-gradient(135deg, #4ade80, #22c55e);
  color: white;
  border: none;
  padding: 20px 60px;
  font-size: 24px;
  border-radius: 50px;
  margin-top: 30px;
  cursor: pointer;
  font-weight: bold;
  box-shadow: 0 10px 30px #4ade80;
`;

function App() {
  const [difficulty, setDifficulty] = useState<Difficulty>('medium');
  const [highScore, setHighScore] = useLocalStorage('snakeHighScore', 0);
  const {
    gameState,
    snake,
    foods,
    score,
    level,
    powerUp,
    walls,
    gridSize,
    initGame,
    setGameState,
  } = useGame(difficulty);

  const handleGameOver = () => {
    if (score > highScore) {
      setHighScore(score);
    }
  };

  return (
    <AppContainer>
      <Toaster position="top-center" />
      
      <GameWrapper>
        {gameState === 'menu' ? (
          <Menu
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Title>🐍 SNAKE GAME</Title>
            
            <div style={{ marginBottom: 30 }}>
              <DifficultyButton
                active={difficulty === 'easy'}
                onClick={() => setDifficulty('easy')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🟢 Легко
              </DifficultyButton>
              
              <DifficultyButton
                active={difficulty === 'medium'}
                onClick={() => setDifficulty('medium')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🟡 Средне
              </DifficultyButton>
              
              <DifficultyButton
                active={difficulty === 'hard'}
                onClick={() => setDifficulty('hard')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                🔴 Сложно
              </DifficultyButton>
              
              <DifficultyButton
                active={difficulty === 'expert'}
                onClick={() => setDifficulty('expert')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                💀 Эксперт
              </DifficultyButton>
            </div>
            
            <StartButton
              onClick={initGame}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              Начать игру
            </StartButton>
          </Menu>
        ) : (
          <>
            <ScoreBoard
              score={score}
              level={level}
              difficulty={difficulty}
              highScore={highScore}
              powerUp={powerUp || undefined}
            />
            
            <GameBoard>
              <Grid />
              
              {walls.map(wall => (
                <Wall key={`${wall.x}-${wall.y}`} x={wall.x} y={wall.y} />
              ))}
              
              <Snake snake={snake} direction={direction} powerUp={powerUp || undefined} />
              <Food foods={foods} />
            </GameBoard>
          </>
        )}
        
        <AnimatePresence>
          {gameState === 'gameOver' && (
            <GameOver
              score={score}
              level={level}
              foodEaten={foods.length}
              onRestart={() => {
                handleGameOver();
                initGame();
              }}
              onMenu={() => {
                handleGameOver();
                setGameState('menu');
              }}
              onSave={() => {
                // Сохранение в Firebase или другую БД
                console.log('Сохраняем результат:', { score, level, difficulty });
              }}
            />
          )}
        </AnimatePresence>
        
        {gameState === 'paused' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'rgba(0,0,0,0.5)',
              backdropFilter: 'blur(5px)',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              zIndex: 100,
            }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring' }}
              style={{
                background: '#1e293b',
                padding: 40,
                borderRadius: 30,
                textAlign: 'center',
              }}
            >
              <h2 style={{ color: '#fbbf24', fontSize: 36, marginBottom: 20 }}>ПАУЗА</h2>
              <p style={{ color: '#94a3b8', marginBottom: 30 }}>Нажмите ПРОБЕЛ для продолжения</p>
            </motion.div>
          </motion.div>
        )}
      </GameWrapper>
    </AppContainer>
  );
}

export default App;

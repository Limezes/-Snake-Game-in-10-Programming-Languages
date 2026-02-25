import React from 'react';
import { motion } from 'framer-motion';
import { Difficulty, PowerUp } from '../types';
import styled from 'styled-components';

const ScoreContainer = styled.div`
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 15px;
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.1);
`;

const ScoreItem = styled.div`
  text-align: center;
`;

const ScoreLabel = styled.div`
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 5px;
`;

const ScoreValue = styled.div<{ color?: string }>`
  font-size: 28px;
  font-weight: bold;
  color: ${props => props.color || '#fbbf24'};
  text-shadow: 0 0 10px ${props => props.color || '#fbbf24'}80;
`;

const PowerUpIndicator = styled(motion.div)<{ type: string }>`
  padding: 5px 15px;
  border-radius: 20px;
  background: ${props => 
    props.type === 'speed' ? 'linear-gradient(135deg, #60a5fa, #3b82f6)' :
    props.type === 'slow' ? 'linear-gradient(135deg, #c084fc, #a855f7)' :
    'linear-gradient(135deg, #fbbf24, #f59e0b)'
  };
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
`;

interface ScoreBoardProps {
  score: number;
  level: number;
  difficulty: Difficulty;
  highScore: number;
  powerUp?: PowerUp;
}

export const ScoreBoard: React.FC<ScoreBoardProps> = ({
  score,
  level,
  difficulty,
  highScore,
  powerUp,
}) => {
  const difficultyColors = {
    easy: '#4ade80',
    medium: '#fbbf24',
    hard: '#f87171',
    expert: '#f43f5e',
  };

  return (
    <ScoreContainer>
      <ScoreItem>
        <ScoreLabel>Счёт</ScoreLabel>
        <ScoreValue>{score}</ScoreValue>
      </ScoreItem>
      
      <ScoreItem>
        <ScoreLabel>Рекорд</ScoreLabel>
        <ScoreValue color="#f87171">{highScore}</ScoreValue>
      </ScoreItem>
      
      <ScoreItem>
        <ScoreLabel>Уровень</ScoreLabel>
        <ScoreValue color="#4ade80">{level}</ScoreValue>
      </ScoreItem>
      
      <ScoreItem>
        <ScoreLabel>Сложность</ScoreLabel>
        <ScoreValue color={difficultyColors[difficulty]}>
          {difficulty === 'easy' && 'Легко'}
          {difficulty === 'medium' && 'Средне'}
          {difficulty === 'hard' && 'Сложно'}
          {difficulty === 'expert' && 'Эксперт'}
        </ScoreValue>
      </ScoreItem>
      
      {powerUp && powerUp.duration > 0 && (
        <PowerUpIndicator
          type={powerUp.type}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0 }}
        >
          {powerUp.type === 'speed' && '⚡ УСКОРЕНИЕ'}
          {powerUp.type === 'slow' && '🐢 ЗАМЕДЛЕНИЕ'}
          {powerUp.type === 'invincible' && '👑 НЕУЯЗВИМ'}
          <span style={{ fontSize: '14px', opacity: 0.8 }}>
            {Math.ceil(powerUp.duration / 10)}с
          </span>
        </PowerUpIndicator>
      )}
    </ScoreContainer>
  );
};

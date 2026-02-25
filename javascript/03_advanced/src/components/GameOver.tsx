import React from 'react';
import { motion } from 'framer-motion';
import styled from 'styled-components';
import toast from 'react-hot-toast';

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const Modal = styled(motion.div)`
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-radius: 30px;
  padding: 40px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  width: 90%;
`;

const Title = styled.h2`
  font-size: 48px;
  color: #f87171;
  margin-bottom: 20px;
  text-shadow: 0 0 20px #f87171;
`;

const ScoreText = styled.div`
  font-size: 64px;
  font-weight: bold;
  color: #fbbf24;
  margin-bottom: 10px;
  text-shadow: 0 0 30px #fbbf24;
`;

const InfoText = styled.div`
  color: #94a3b8;
  font-size: 18px;
  margin-bottom: 30px;
`;

const Button = styled(motion.button)`
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 15px 40px;
  font-size: 18px;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  margin: 10px;
  box-shadow: 0 10px 30px #3b82f6;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px #3b82f6;
  }
`;

const SecondaryButton = styled(Button)`
  background: transparent;
  border: 2px solid #475569;
  box-shadow: none;
  color: #94a3b8;
  
  &:hover {
    background: #1e293b;
    border-color: #64748b;
  }
`;

interface GameOverProps {
  score: number;
  level: number;
  foodEaten: number;
  onRestart: () => void;
  onMenu: () => void;
  onSave?: () => void;
}

export const GameOver: React.FC<GameOverProps> = ({
  score,
  level,
  foodEaten,
  onRestart,
  onMenu,
  onSave,
}) => {
  const handleSave = () => {
    if (onSave) {
      onSave();
      toast.success('Результат сохранен!', {
        icon: '🏆',
        style: {
          background: '#1e293b',
          color: '#fff',
          border: '1px solid #fbbf24',
        },
      });
    }
  };

  return (
    <Overlay
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <Modal
        initial={{ scale: 0.8, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        transition={{ type: 'spring', damping: 15 }}
      >
        <Title>GAME OVER</Title>
        
        <ScoreText>{score}</ScoreText>
        
        <InfoText>
          Достигнут уровень: {level}<br />
          Съедено еды: {foodEaten}
        </InfoText>
        
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center' }}>
          <Button
            onClick={onRestart}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Играть снова
          </Button>
          
          <SecondaryButton
            onClick={onMenu}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            В меню
          </SecondaryButton>
        </div>
        
        {onSave && (
          <motion.button
            onClick={handleSave}
            style={{
              marginTop: 20,
              background: 'none',
              border: 'none',
              color: '#fbbf24',
              cursor: 'pointer',
              fontSize: 16,
            }}
            whileHover={{ scale: 1.05 }}
          >
            💾 Сохранить результат
          </motion.button>
        )}
      </Modal>
    </Overlay>
  );
};

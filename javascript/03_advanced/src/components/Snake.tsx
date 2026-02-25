import React from 'react';
import { motion } from 'framer-motion';
import { Position, Direction } from '../types';

interface SnakeProps {
  snake: Position[];
  direction: Direction;
  powerUp?: { type: string; duration: number };
}

export const Snake: React.FC<SnakeProps> = ({ snake, direction, powerUp }) => {
  const getHeadColor = () => {
    if (powerUp?.type === 'invincible') {
      return 'rgba(255, 255, 0, 0.8)';
    }
    if (powerUp?.type === 'speed') {
      return 'rgba(0, 255, 255, 0.8)';
    }
    return '#4ade80';
  };

  const getBodyColor = (index: number) => {
    const opacity = 0.9 - index * 0.05;
    if (powerUp?.type === 'invincible') {
      return `rgba(255, 200, 0, ${opacity})`;
    }
    return `rgba(74, 222, 128, ${opacity})`;
  };

  return (
    <>
      {snake.map((segment, index) => (
        <motion.div
          key={`${segment.x}-${segment.y}-${index}`}
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.1 }}
          style={{
            position: 'absolute',
            left: segment.x * 25,
            top: segment.y * 25,
            width: 23,
            height: 23,
            backgroundColor: index === 0 ? getHeadColor() : getBodyColor(index),
            borderRadius: index === 0 ? '8px' : '5px',
            boxShadow: index === 0 
              ? '0 0 15px rgba(74, 222, 128, 0.5)' 
              : '0 2px 5px rgba(0,0,0,0.2)',
            zIndex: snake.length - index,
          }}
        >
          {index === 0 && (
            <>
              {/* Глаза */}
              <div
                style={{
                  position: 'absolute',
                  width: 5,
                  height: 5,
                  backgroundColor: 'white',
                  borderRadius: '50%',
                  ...(direction === 'RIGHT' && { right: 3, top: 3 }),
                  ...(direction === 'RIGHT' && { right: 3, bottom: 3 }),
                  ...(direction === 'LEFT' && { left: 3, top: 3 }),
                  ...(direction === 'LEFT' && { left: 3, bottom: 3 }),
                  ...(direction === 'UP' && { top: 3, left: 3 }),
                  ...(direction === 'UP' && { top: 3, right: 3 }),
                  ...(direction === 'DOWN' && { bottom: 3, left: 3 }),
                  ...(direction === 'DOWN' && { bottom: 3, right: 3 }),
                }}
              />
            </>
          )}
        </motion.div>
      ))}
    </>
  );
};

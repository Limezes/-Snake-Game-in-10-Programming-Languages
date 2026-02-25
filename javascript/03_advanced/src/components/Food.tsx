import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Food as FoodType } from '../types';

interface FoodProps {
  foods: FoodType[];
}

export const Food: React.FC<FoodProps> = ({ foods }) => {
  return (
    <AnimatePresence>
      {foods.map((food, index) => (
        <motion.div
          key={`${food.position.x}-${food.position.y}-${index}`}
          initial={{ scale: 0 }}
          animate={{ 
            scale: [1, 1.2, 1],
            rotate: food.type === 'golden' ? 360 : 0,
          }}
          transition={{ 
            duration: 1,
            repeat: Infinity,
            repeatType: 'reverse',
          }}
          exit={{ scale: 0, opacity: 0 }}
          style={{
            position: 'absolute',
            left: food.position.x * 25,
            top: food.position.y * 25,
            width: 23,
            height: 23,
            backgroundColor: food.color,
            borderRadius: '50%',
            boxShadow: `0 0 15px ${food.color}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: food.type === 'golden' ? '18px' : '16px',
            color: 'white',
            fontWeight: 'bold',
          }}
        >
          {food.type === 'bonus' && '★'}
          {food.type === 'speed' && '⚡'}
          {food.type === 'slow' && '🐢'}
          {food.type === 'golden' && '👑'}
        </motion.div>
      ))}
    </AnimatePresence>
  );
};

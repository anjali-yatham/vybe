import { useState, useEffect } from 'react';
import { motion, useAnimate } from 'motion/react';

// Simple floating ticket graphic
function FloatingTicket() {
  return (
    <motion.div
      className="relative"
      initial={{ x: -50, y: 0, scale: 0, rotate: -15 }}
      animate={{
        x: 0,
        y: [0, -8, 0], // Gentle floating motion
        scale: 1,
        rotate: 5,
      }}
      transition={{
        x: { duration: 0.4, delay: 1.5 },
        scale: { duration: 0.4, delay: 1.5, type: 'spring' },
        rotate: { duration: 0.4, delay: 1.5 },
        y: {
          duration: 2,
          delay: 2.2,
          repeat: Infinity,
          ease: 'easeInOut',
        },
      }}
    >
      {/* Ticket body with gradient */}
      <div className="relative w-32 h-16 bg-gradient-to-r from-[#FF8C42] to-[#F5B942] rounded-lg shadow-lg overflow-hidden">
        {/* Perforation line */}
        <div className="absolute left-10 top-0 bottom-0 w-px border-l-2 border-dashed border-white/40" />
        
        {/* Decorative elements */}
        <div className="absolute top-2 left-3 text-white text-xs font-bold">VYBE</div>
        <div className="absolute bottom-2 right-3 text-white text-xs">✦</div>
      </div>
    </motion.div>
  );
}

// Speech bubble with animated text
function SpeechBubble({ text }) {
  return (
    <motion.div
      key={text}
      initial={{ opacity: 0, scale: 0.8, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ duration: 0.3 }}
      className="absolute -top-16 left-1/2 -translate-x-1/2 bg-white px-4 py-2 rounded-2xl shadow-lg min-w-[140px] text-center"
    >
      <div className="text-[#3B2A24] font-semibold">{text}</div>
      {/* Speech bubble pointer */}
      <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-transparent border-t-white" />
    </motion.div>
  );
}

// Mascot character with animation sequence
function MascotCharacter() {
  const [scope, animate] = useAnimate();
  const [currentMessage, setCurrentMessage] = useState('');
  const [showTicket, setShowTicket] = useState(false);

  useEffect(() => {
    // Animation sequence
    const sequence = async () => {
      // Step 1: Slide in from right (0-0.6s)
      await animate(
        scope.current,
        { x: ['100%', '0%'] },
        { duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }
      );

      // Step 2: Wave and show first message (0.6-1.2s)
      setCurrentMessage('Hi there! 👋');
      
      // Waving animation
      const wavePromise = animate(
        '#mascot-image',
        { rotate: [0, -3, 3, -3, 3, 0] },
        { duration: 0.6, ease: 'easeInOut' }
      );
      
      await wavePromise;

      // Step 3: Change message and show ticket (1.5-2.2s)
      await new Promise(resolve => setTimeout(resolve, 300));
      setCurrentMessage('Want this?');
      
      await new Promise(resolve => setTimeout(resolve, 400));
      setShowTicket(true);

      // Step 4: Final message (after 2.2s)
      await new Promise(resolve => setTimeout(resolve, 700));
      setCurrentMessage('← Sign up now');
    };

    sequence();
  }, [animate, scope]);

  return (
    <motion.div
      ref={scope}
      className="relative"
      initial={{ x: '100%' }}
    >
      {/* Speech bubble */}
      {currentMessage && (
        <div className="relative mb-4">
          <SpeechBubble text={currentMessage} />
        </div>
      )}

      {/* Mascot image with gentle bounce */}
      <motion.div
        id="mascot-image"
        className="relative"
        animate={{
          y: [0, -8, 0],
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        <img 
          src="/images/mascot.png" 
          alt="Vybe Mascot" 
          className="w-64 h-auto drop-shadow-2xl"
        />
        
        {/* Ticket holder (appears when ticket shows) */}
        {showTicket && (
          <div className="absolute -right-24 top-20">
            <FloatingTicket />
          </div>
        )}
      </motion.div>
    </motion.div>
  );
}

// Main component with background
export default function MascotGreeting() {
  return (
    <div className="w-full h-full relative overflow-hidden flex items-center justify-center">
      {/* Warm gradient mesh background */}
      <div 
        className="absolute inset-0 bg-gradient-to-br from-[#FF8C42] via-[#FF6F91] to-[#9c27b0]"
        style={{
          filter: 'blur(60px)',
          opacity: 0.6,
        }}
      />
      
      {/* Additional soft overlay for depth */}
      <div className="absolute inset-0 bg-gradient-to-t from-[#9c27b0]/20 to-transparent" />

      {/* Mascot character */}
      <div className="relative z-10 flex items-center justify-center w-full h-full">
        <MascotCharacter />
      </div>

      {/* Decorative floating particles */}
      <motion.div
        className="absolute top-20 left-10 w-3 h-3 bg-[#F5B942] rounded-full opacity-60"
        animate={{
          y: [0, -20, 0],
          x: [0, 10, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />
      <motion.div
        className="absolute bottom-32 right-16 w-4 h-4 bg-[#FF6F91] rounded-full opacity-60"
        animate={{
          y: [0, 20, 0],
          x: [0, -10, 0],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 0.5,
        }}
      />
      <motion.div
        className="absolute top-1/2 left-20 w-2 h-2 bg-[#FF8C42] rounded-full opacity-60"
        animate={{
          y: [0, -15, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 2.5,
          repeat: Infinity,
          ease: 'easeInOut',
          delay: 1,
        }}
      />
    </div>
  );
}

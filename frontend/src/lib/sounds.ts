// Helper para sonidos de notificación usando Web Audio API

export const playNotificationSound = (type: 'success' | 'error' | 'warning' | 'victory' | 'battle' | 'info' | 'economic') => {
  if (typeof window === 'undefined') return;
  
  // Vibración para dispositivos móviles
  if ('vibrate' in navigator) {
    const vibrationPatterns = {
      success: [50, 50, 50],
      error: [100, 50, 100],
      warning: [75],
      victory: [100, 50, 100, 50, 200],
      battle: [50, 30, 50, 30, 50],
      info: [50],
      economic: [50, 50, 50]
    };
    navigator.vibrate(vibrationPatterns[type] || [50]);
  }
  
  try {
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    // Configurar frecuencias según el tipo
    const configs = {
      success: [523.25, 659.25, 783.99], // Do-Mi-Sol
      error: [392.00, 349.23, 293.66],   // Sol-Fa-Re (descendente)
      warning: [440.00, 493.88],         // La-Si
      victory: [523.25, 659.25, 783.99, 1046.50], // Do-Mi-Sol-Do (octava)
      battle: [293.66, 349.23, 293.66],   // Re-Fa-Re
      info: [440.00],                     // La
      economic: [523.25, 659.25]          // Do-Mi
    };
    
    const frequencies = configs[type] || configs.success;
    const noteDuration = 0.15;
    
    let currentTime = audioContext.currentTime;
    
    frequencies.forEach((freq, i) => {
      oscillator.frequency.setValueAtTime(freq, currentTime);
      gainNode.gain.setValueAtTime(0.1, currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, currentTime + noteDuration);
      currentTime += noteDuration;
    });
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(currentTime);
    
  } catch (error) {
    // Silenciar errores de audio si el navegador no soporta o bloquea
    console.debug('Audio notification not available');
  }
};

export const playAmbientSound = (mood: 'tense' | 'peaceful' | 'victory') => {
  // Placeholder para sonidos ambientales más complejos en el futuro
  console.debug(`Ambient sound: ${mood}`);
};

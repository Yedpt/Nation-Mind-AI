// Componente del botón para procesar turno
'use client';

interface TurnButtonProps {
  isProcessing: boolean;
  onProcessTurn: () => void;
  disabled?: boolean;
}

export default function TurnButton({ isProcessing, onProcessTurn, disabled = false }: TurnButtonProps) {
  return (
    <button
      onClick={onProcessTurn}
      disabled={isProcessing || disabled}
      className={`
        relative px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300
        ${isProcessing || disabled
          ? 'bg-gray-600 cursor-not-allowed opacity-50'
          : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 shadow-xl hover:shadow-2xl hover:scale-105 animate-pulse-glow'
        }
        text-white
      `}
    >
      {isProcessing ? (
        <span className="flex items-center gap-3">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
          Procesando turno...
        </span>
      ) : disabled ? (
        <span className="flex items-center gap-2">
          🏁 Juego Terminado
        </span>
      ) : (
        <span className="flex items-center gap-2">
          ⚡ Procesar Turno IA
          <span className="text-sm opacity-80 ml-2">🚀</span>
        </span>
      )}
      
      {!isProcessing && !disabled && (
        <div className="absolute inset-0 bg-white opacity-0 hover:opacity-20 rounded-xl transition-opacity duration-300"></div>
      )}
    </button>
  );
}

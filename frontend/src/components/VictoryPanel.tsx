'use client';

import { useEffect, useState } from 'react';

interface VictoryProgress {
  domination: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  elimination: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  economic: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  military: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  survival: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
}

interface VictoryPanelProps {
  progress: VictoryProgress | null;
  currentTurn: number;
}

export default function VictoryPanel({ progress, currentTurn }: VictoryPanelProps) {
  if (!progress) return null;

  const victoryTypes = [
    {
      key: 'domination',
      name: 'Dominación',
      icon: '👑',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-900/20',
      borderColor: 'border-purple-500'
    },
    {
      key: 'economic',
      name: 'Económica',
      icon: '💰',
      color: 'from-yellow-500 to-amber-500',
      bgColor: 'bg-yellow-900/20',
      borderColor: 'border-yellow-500'
    },
    {
      key: 'military',
      name: 'Militar',
      icon: '🪖',
      color: 'from-red-500 to-pink-500',
      bgColor: 'bg-red-900/20',
      borderColor: 'border-red-500'
    },
    {
      key: 'elimination',
      name: 'Eliminación',
      icon: '⚔️',
      color: 'from-gray-500 to-slate-500',
      bgColor: 'bg-slate-900/20',
      borderColor: 'border-slate-500'
    },
    {
      key: 'survival',
      name: 'Supervivencia',
      icon: '🛡️',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-900/20',
      borderColor: 'border-blue-500'
    }
  ];

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 shadow-2xl">
      <h3 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <span>🏆</span>
        Camino a la Victoria
      </h3>

      <div className="space-y-4">
        {victoryTypes.map((type) => {
          const data = progress[type.key as keyof VictoryProgress];
          const progressPercentage = Math.min(100, data.progress);
          
          return (
            <div 
              key={type.key}
              className={`${type.bgColor} border ${type.borderColor} rounded-lg p-4 transition-all duration-300 ${
                data.completed ? 'ring-2 ring-green-500 shadow-lg' : ''
              }`}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{type.icon}</span>
                  <div>
                    <h4 className="text-white font-bold">{type.name}</h4>
                    <p className="text-xs text-slate-400">{data.description}</p>
                  </div>
                </div>
                {data.completed && (
                  <span className="text-green-400 font-bold flex items-center gap-1">
                    <span>✓</span>
                    ¡Completado!
                  </span>
                )}
              </div>

              {/* Progress Bar */}
              <div className="relative w-full h-4 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r ${type.color} transition-all duration-500 ease-out ${
                    progressPercentage >= 80 ? 'animate-pulse-glow' : ''
                  }`}
                  style={{ width: `${progressPercentage}%` }}
                >
                  <div className="absolute inset-0 animate-pulse opacity-30 bg-white"></div>
                </div>
                
                {/* Indicador de milestone 50% */}
                {progressPercentage >= 50 && progressPercentage < 80 && (
                  <div className="absolute right-2 top-0 bottom-0 flex items-center">
                    <span className="text-xs text-white/80 font-bold bg-black/30 px-2 py-1 rounded">
                      ¡Avanzando! 🔥
                    </span>
                  </div>
                )}
                
                {/* Indicador de milestone 80% */}
                {progressPercentage >= 80 && !data.completed && (
                  <div className="absolute right-2 top-0 bottom-0 flex items-center">
                    <span className="text-xs text-yellow-300 font-bold bg-black/30 px-2 py-1 rounded animate-pulse">
                      ¡Casi! ⚡
                    </span>
                  </div>
                )}
              </div>

              {/* Stats */}
              <div className="flex justify-between mt-2 text-sm">
                <span className={`font-semibold ${
                  data.completed ? 'text-green-400' : 'text-slate-300'
                }`}>
                  {data.progress.toFixed(1)}%
                </span>
                <span className="text-slate-400">
                  Objetivo: {data.target}%
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Nota informativa */}
      <div className="mt-6 bg-slate-800/50 border border-slate-700 rounded-lg p-4 text-sm text-slate-300">
        <p className="mb-2">
          <strong className="text-white">💡 Condiciones de Victoria:</strong>
        </p>
        <ul className="space-y-1 text-xs">
          <li>👑 <strong>Dominación:</strong> Controla más del 50% de territorios</li>
          <li>💰 <strong>Económica:</strong> 10,000 oro + 90% poder económico</li>
          <li>🪖 <strong>Militar:</strong> 2,000 tropas + 90% poder militar</li>
          <li>⚔️ <strong>Eliminación:</strong> Sé la única nación superviviente</li>
          <li>🛡️ <strong>Supervivencia:</strong> Sobrevive 100 turnos con mejor puntuación</li>
        </ul>
      </div>

      {/* Turno actual */}
      <div className="mt-4 text-center text-slate-400 text-sm">
        Turno actual: <span className="text-white font-bold">{currentTurn}</span> / 100
      </div>
    </div>
  );
}

// Componente de tarjeta de nación
import Link from 'next/link';
import type { Nation } from '@/types';

interface NationCardProps {
  nation: Nation;
  isPlayer?: boolean;
}

export default function NationCard({ nation, isPlayer = false }: NationCardProps) {
  const getPersonalityColor = (personality: string) => {
    const colors: Record<string, string> = {
      aggressive: 'border-red-500',
      diplomatic: 'border-blue-500',
      economic: 'border-green-500',
      balanced: 'border-purple-500',
      defensive: 'border-gray-500',
    };
    return colors[personality] || 'border-slate-500';
  };

  const getPersonalityEmoji = (personality: string) => {
    const emojis: Record<string, string> = {
      aggressive: '⚔️',
      diplomatic: '🤝',
      economic: '💰',
      balanced: '⚖️',
      defensive: '🛡️',
    };
    return emojis[personality] || '🏛️';
  };

  const getPersonalityBgColor = (personality: string) => {
    const colors: Record<string, string> = {
      aggressive: 'from-red-500 to-orange-500',
      diplomatic: 'from-blue-500 to-cyan-500',
      economic: 'from-green-500 to-emerald-500',
      balanced: 'from-purple-500 to-pink-500',
      defensive: 'from-slate-500 to-gray-500',
    };
    return colors[personality] || 'from-gray-500 to-slate-500';
  };

  // Calcular ingreso estimado por turno
  const calculateEstimatedIncome = () => {
    const baseIncome = 100;
    const territoryIncome = nation.territories * 50;
    const powerIncome = (nation.economic_power / 100) * 300;
    const income = baseIncome + territoryIncome + powerIncome;
    
    const maintenance = Math.floor(nation.troops / 10) + 20;
    const netIncome = Math.floor(income - maintenance);
    
    return netIncome;
  };

  const estimatedIncome = calculateEstimatedIncome();

  return (
    <Link
      href={`/game/nations/${nation.id}`}
      className={`
        block bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2
        transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/30
        ${nation.is_eliminated ? 'border-red-600 opacity-70' : getPersonalityColor(nation.personality)}
        ${isPlayer ? 'ring-2 ring-purple-500 ring-offset-2 ring-offset-slate-900' : ''}
      `}
    >
      {/* Player Badge */}
      {isPlayer && (
        <div className="absolute -top-3 -right-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm px-4 py-1 rounded-full font-bold shadow-lg">
          TÚ
        </div>
      )}

      {/* Eliminated Badge */}
      {nation.is_eliminated && (
        <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-red-600 text-white text-sm px-4 py-1 rounded-full font-bold shadow-lg">
          ❌ ELIMINADA
        </div>
      )}

      {/* Header */}
      <div className="mb-4">
        <h3 className="text-2xl font-bold text-white mb-2">{nation.name}</h3>
        <div className={`inline-block bg-gradient-to-r ${getPersonalityBgColor(nation.personality)} text-white text-sm px-3 py-1 rounded-full`}>
          {getPersonalityEmoji(nation.personality)} {nation.personality}
        </div>
      </div>

      {/* Resources Grid */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="bg-slate-900/50 rounded-lg p-3 text-center">
          <div className="text-2xl mb-1">💰</div>
          <div className="text-yellow-400 font-bold text-lg">{nation.gold}</div>
          <div className="text-xs text-purple-300">Oro</div>
          {!nation.is_eliminated && (
            <div className={`text-xs mt-1 ${estimatedIncome >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {estimatedIncome >= 0 ? '+' : ''}{estimatedIncome}/turno
            </div>
          )}
        </div>
        <div className="bg-slate-900/50 rounded-lg p-3 text-center">
          <div className="text-2xl mb-1">🪖</div>
          <div className="text-red-400 font-bold text-lg">{nation.troops}</div>
          <div className="text-xs text-purple-300">Tropas</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-3 text-center">
          <div className="text-2xl mb-1">🏛️</div>
          <div className="text-blue-400 font-bold text-lg">{nation.territories}</div>
          <div className="text-xs text-purple-300">Territorios</div>
        </div>
      </div>

      {/* Power Bars */}
      <div className="space-y-2">
        <div>
          <div className="flex justify-between text-xs text-purple-300 mb-1">
            <span>⚔️ Militar</span>
            <span>{nation.military_power}</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-red-500 to-orange-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${nation.military_power}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs text-purple-300 mb-1">
            <span>💼 Económico</span>
            <span>{nation.economic_power}</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${nation.economic_power}%` }}
            />
          </div>
        </div>

        <div>
          <div className="flex justify-between text-xs text-purple-300 mb-1">
            <span>🤝 Diplomático</span>
            <span>{nation.diplomatic_power}</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${nation.diplomatic_power}%` }}
            />
          </div>
        </div>
      </div>
    </Link>
  );
}
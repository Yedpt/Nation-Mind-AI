'use client';

import { useEffect, useState } from 'react';

interface LeaderboardEntry {
  rank: number;
  nation_id: number;
  nation_name: string;
  total_score: number;
  gold: number;
  troops: number;
  territories: number;
  military_power: number;
  economic_power: number;
  diplomatic_influence: number;
}

export default function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/game/leaderboard');
      
      if (!response.ok) {
        throw new Error('Error al cargar el leaderboard');
      }

      const data = await response.json();
      setLeaderboard(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching leaderboard:', err);
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const getMedalIcon = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  const getScoreColor = (rank: number) => {
    switch (rank) {
      case 1: return 'text-yellow-400';
      case 2: return 'text-slate-300';
      case 3: return 'text-amber-600';
      default: return 'text-slate-400';
    }
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 shadow-2xl">
        <div className="text-center text-slate-400">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-2"></div>
          Cargando clasificación...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-red-700 shadow-2xl">
        <p className="text-red-400 text-center">❌ {error}</p>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>🏅</span>
          Clasificación Global
        </h3>
        <button
          onClick={fetchLeaderboard}
          className="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm text-white transition-colors"
        >
          🔄 Actualizar
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="text-left py-3 px-4 text-slate-400 font-semibold">Rank</th>
              <th className="text-left py-3 px-4 text-slate-400 font-semibold">Nación</th>
              <th className="text-center py-3 px-4 text-slate-400 font-semibold">Puntos</th>
              <th className="text-center py-3 px-4 text-slate-400 font-semibold">💰 Oro</th>
              <th className="text-center py-3 px-4 text-slate-400 font-semibold">⚔️ Tropas</th>
              <th className="text-center py-3 px-4 text-slate-400 font-semibold">🗺️ Terr.</th>
              <th className="text-center py-3 px-4 text-slate-400 font-semibold">Poderes</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry) => (
              <tr
                key={entry.nation_id}
                className={`border-b border-slate-800 transition-colors ${
                  entry.rank === 1 
                    ? 'bg-yellow-900/20 hover:bg-yellow-900/30' 
                    : entry.rank === 2
                    ? 'bg-slate-700/20 hover:bg-slate-700/30'
                    : entry.rank === 3
                    ? 'bg-amber-900/20 hover:bg-amber-900/30'
                    : 'hover:bg-slate-800/50'
                }`}
              >
                {/* Rank */}
                <td className="py-4 px-4">
                  <span className={`text-2xl font-bold ${getScoreColor(entry.rank)}`}>
                    {getMedalIcon(entry.rank)}
                  </span>
                </td>

                {/* Nation Name */}
                <td className="py-4 px-4">
                  <span className="text-white font-semibold">{entry.nation_name}</span>
                </td>

                {/* Total Score */}
                <td className="py-4 px-4 text-center">
                  <span className={`font-bold text-lg ${getScoreColor(entry.rank)}`}>
                    {entry.total_score.toLocaleString()}
                  </span>
                </td>

                {/* Gold */}
                <td className="py-4 px-4 text-center text-yellow-400">
                  {entry.gold.toLocaleString()}
                </td>

                {/* Troops */}
                <td className="py-4 px-4 text-center text-red-400">
                  {entry.troops.toLocaleString()}
                </td>

                {/* Territories */}
                <td className="py-4 px-4 text-center text-green-400">
                  {entry.territories}
                </td>

                {/* Powers */}
                <td className="py-4 px-4">
                  <div className="flex flex-col gap-1 text-xs">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-slate-400">🪖 Mil:</span>
                      <span className="text-red-400 font-semibold">
                        {entry.military_power.toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-slate-400">💰 Eco:</span>
                      <span className="text-yellow-400 font-semibold">
                        {entry.economic_power.toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-slate-400">🤝 Dip:</span>
                      <span className="text-blue-400 font-semibold">
                        {entry.diplomatic_influence.toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Footer with scoring formula */}
      <div className="mt-6 bg-slate-800/50 border border-slate-700 rounded-lg p-4 text-xs text-slate-400">
        <p className="mb-1">
          <strong className="text-white">📊 Fórmula de Puntuación:</strong>
        </p>
        <p className="font-mono">
          Puntos = (Oro ÷ 10) + Tropas + (Territorios × 200) + (Poderes × 10/10/5)
        </p>
      </div>
    </div>
  );
}

// Página de historial de batallas
'use client';

import { useState, useEffect } from 'react';
import { getBattleHistory, getAllNations, getActiveWars } from '@/lib/api';
import type { Battle, Nation, Relation } from '@/types';

interface ActiveWar {
  nation_a: string;
  nation_b: string;
  relationship_score: number;
  nation_a_id: number;
  nation_b_id: number;
}

export default function BattlesPage() {
  const [battles, setBattles] = useState<Battle[]>([]);
  const [nations, setNations] = useState<Nation[]>([]);
  const [activeWars, setActiveWars] = useState<ActiveWar[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [battlesData, nationsData, warsData] = await Promise.all([
          getBattleHistory(50),
          getAllNations(),
          getActiveWars()
        ]);
        setBattles(battlesData);
        setNations(nationsData);
        setActiveWars(warsData.active_wars);
      } catch (err) {
        console.error('Error loading battles:', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);

  const getNationName = (id: number) => {
    return nations.find(n => n.id === id)?.name || `Nación ${id}`;
  };

  const getBattleTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      skirmish: 'from-blue-500 to-cyan-500',
      battle: 'from-orange-500 to-red-500',
      total_war: 'from-red-600 to-pink-600',
    };
    return colors[type] || 'from-gray-500 to-slate-500';
  };

  const getBattleTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      skirmish: '⚔️ Escaramuza',
      battle: '🎯 Batalla',
      total_war: '💥 Guerra Total',
    };
    return labels[type] || type;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-slate-500 mx-auto mb-4"></div>
          <p className="text-slate-300 text-lg">Cargando batallas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">⚔️ Historial de Batallas</h1>
          <p className="text-slate-400">Todas las batallas registradas en la simulación</p>
        </div>

        {/* Active Wars Section */}
        {activeWars.length > 0 && (
          <div className="mb-8 bg-red-900/30 border border-red-500 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-red-400 mb-4">🔥 Guerras Activas ({activeWars.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {activeWars.map((war, index) => (
                <div key={index} className="bg-slate-800/50 rounded-lg p-4">
                  <div className="text-white font-bold text-center">
                    {war.nation_a} <span className="text-red-500 mx-2">⚔️</span> {war.nation_b}
                  </div>
                  <div className="text-center text-slate-400 text-sm mt-2">
                    Relación: {war.relationship_score}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Battles List */}
        <div className="space-y-4">
          {battles.length === 0 ? (
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border-2 border-slate-700 text-center">
              <p className="text-purple-300 text-lg">No hay batallas registradas aún</p>
              <p className="text-purple-400 text-sm mt-2">Las batallas aparecerán aquí cuando se declaren guerras</p>
            </div>
          ) : (
            battles.map((battle) => (
              <div
                key={battle.id}
                className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700 hover:border-purple-500 transition-all duration-300"
              >
                {/* Battle Header */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <div className={`inline-block bg-gradient-to-r ${getBattleTypeColor(battle.battle_type)} text-white px-3 py-1 rounded-full text-sm font-bold mb-2`}>
                      {getBattleTypeLabel(battle.battle_type)}
                    </div>
                    <h3 className="text-xl font-bold text-white">
                      {getNationName(battle.attacker_id)} vs {getNationName(battle.defender_id)}
                    </h3>
                  </div>
                  <div className="text-right">
                    <div className="text-purple-400 text-sm">Turno {battle.turn_number}</div>
                    {battle.is_decisive && (
                      <div className="bg-yellow-500 text-black text-xs px-2 py-1 rounded-full font-bold mt-1">
                        ⭐ Victoria Decisiva
                      </div>
                    )}
                  </div>
                </div>

                {/* Battle Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  {/* Attacker */}
                  <div className={`bg-slate-900/50 rounded-lg p-4 ${battle.winner_id === battle.attacker_id ? 'ring-2 ring-green-500' : 'opacity-75'}`}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-bold">{getNationName(battle.attacker_id)}</h4>
                      {battle.winner_id === battle.attacker_id && <span className="text-green-400 text-xl">👑</span>}
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Tropas:</span>
                        <span className="text-white">{battle.attacker_troops_initial}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Poder:</span>
                        <span className="text-white">{battle.attacker_power.toFixed(0)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Aliados:</span>
                        <span className="text-white">{battle.attacker_allies.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-red-400">Bajas:</span>
                        <span className="text-red-300">{battle.attacker_casualties}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Probabilidad:</span>
                        <span className="text-white">{(battle.attacker_win_chance * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>

                  {/* VS Divider */}
                  <div className="flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-4xl mb-2">⚔️</div>
                      <div className="text-purple-300 text-sm">vs</div>
                    </div>
                  </div>

                  {/* Defender */}
                  <div className={`bg-slate-900/50 rounded-lg p-4 ${battle.winner_id === battle.defender_id ? 'ring-2 ring-green-500' : 'opacity-75'}`}>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-bold">{getNationName(battle.defender_id)}</h4>
                      {battle.winner_id === battle.defender_id && <span className="text-green-400 text-xl">👑</span>}
                    </div>
                    <div className="space-y-1 text-sm">
                      <div className="flex justify-between">
                        <span className="text-purple-300">Tropas:</span>
                        <span className="text-white">{battle.defender_troops_initial}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Poder:</span>
                        <span className="text-white">{battle.defender_power.toFixed(0)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Aliados:</span>
                        <span className="text-white">{battle.defender_allies.length}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-red-400">Bajas:</span>
                        <span className="text-red-300">{battle.defender_casualties}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-purple-300">Probabilidad:</span>
                        <span className="text-white">{(battle.defender_win_chance * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Battle Results */}
                <div className="bg-slate-900/50 rounded-lg p-4">
                  <h4 className="text-white font-bold mb-2">📜 Resultado</h4>
                  <p className="text-purple-100 mb-3">{battle.description}</p>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-purple-300">🏛️ Territorios Conquistados:</span>
                      <span className="text-yellow-400 ml-2 font-bold">{battle.territories_conquered}</span>
                    </div>
                    <div>
                      <span className="text-purple-300">💰 Oro Saqueado:</span>
                      <span className="text-yellow-400 ml-2 font-bold">{battle.gold_looted}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

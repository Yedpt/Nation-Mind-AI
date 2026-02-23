// Página de diplomacia - Relaciones entre naciones
'use client';

import { useState, useEffect } from 'react';
import { getAllRelations, getAllNations, getPlayerNation, simulateBattle, executePlayerAction } from '@/lib/api';
import type { Relation, Nation, BattleSimulation } from '@/types';

export default function DiplomacyPage() {
  const [relations, setRelations] = useState<Relation[]>([]);
  const [nations, setNations] = useState<Nation[]>([]);
  const [playerNation, setPlayerNation] = useState<Nation | null>(null);
  const [selectedRelation, setSelectedRelation] = useState<Relation | null>(null);
  const [simulation, setSimulation] = useState<BattleSimulation | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [relationsData, nationsData, playerData] = await Promise.all([
        getAllRelations(),
        getAllNations(),
        getPlayerNation()
      ]);
      setRelations(relationsData);
      setNations(nationsData);
      setPlayerNation(playerData);
    } catch (err) {
      console.error('Error loading diplomacy:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const showMessage = (type: 'success' | 'error', text: string) => {
    setActionMessage({ type, text });
    setTimeout(() => setActionMessage(null), 5000);
  };

  const handleProposeAlliance = async (targetNationId: number) => {
    if (!playerNation) return;
    
    try {
      await executePlayerAction(playerNation.id, {
        action_type: 'alliance',
        target_nation_id: targetNationId
      });
      showMessage('success', `✅ Propuesta de alianza enviada a ${getNationName(targetNationId)}`);
      await loadData(); // Recargar datos
    } catch (err: any) {
      showMessage('error', `❌ Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleRequestPeace = async (targetNationId: number) => {
    if (!playerNation) return;
    
    try {
      await executePlayerAction(playerNation.id, {
        action_type: 'peace_treaty',
        target_nation_id: targetNationId
      });
      showMessage('success', `✅ Solicitud de paz enviada a ${getNationName(targetNationId)}`);
      await loadData();
    } catch (err: any) {
      showMessage('error', `❌ Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const handleDeclareWar = async (targetNationId: number) => {
    if (!playerNation) return;
    if (!confirm(`¿Seguro que quieres declarar la guerra a ${getNationName(targetNationId)}?`)) return;
    
    try {
      await executePlayerAction(playerNation.id, {
        action_type: 'attack',
        target_nation_id: targetNationId
      });
      showMessage('success', `⚔️ ¡Guerra declarada a ${getNationName(targetNationId)}!`);
      await loadData();
    } catch (err: any) {
      showMessage('error', `❌ Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  const getNationName = (id: number) => {
    return nations.find(n => n.id === id)?.name || `Nación ${id}`;
  };

  const getRelationColor = (status: string) => {
    const colors: Record<string, string> = {
      allied: 'from-green-500 to-emerald-500',
      neutral: 'from-gray-500 to-slate-500',
      war: 'from-red-600 to-pink-600',
      trade_agreement: 'from-yellow-500 to-amber-500',
    };
    return colors[status] || 'from-gray-500 to-slate-500';
  };

  const getRelationLabel = (status: string) => {
    const labels: Record<string, string> = {
      allied: '🤝 Aliados',
      neutral: '😐 Neutral',
      war: '⚔️ En Guerra',
      trade_agreement: '💰 Acuerdo Comercial',
    };
    return labels[status] || status;
  };

  const handleSimulateBattle = async (relation: Relation) => {
    if (!playerNation) return;
    
    try {
      const sim = await simulateBattle(playerNation.id, 
        relation.nation_a_id === playerNation.id ? relation.nation_b_id : relation.nation_a_id
      );
      setSimulation(sim);
      setSelectedRelation(relation);
    } catch (err) {
      console.error('Error simulating battle:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-slate-500 mx-auto mb-4"></div>
          <p className="text-slate-300 text-lg">Cargando relaciones...</p>
        </div>
      </div>
    );
  }

  const playerRelations = relations.filter(
    r => playerNation && (r.nation_a_id === playerNation.id || r.nation_b_id === playerNation.id)
  );

  const otherRelations = relations.filter(
    r => playerNation && r.nation_a_id !== playerNation.id && r.nation_b_id !== playerNation.id
  );

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="container mx-auto px-4">
        {/* Action Message */}
        {actionMessage && (
          <div className={`mb-4 p-4 rounded-lg border ${
            actionMessage.type === 'success' 
              ? 'bg-green-900/20 border-green-500 text-green-300' 
              : 'bg-red-900/20 border-red-500 text-red-300'
          }`}>
            {actionMessage.text}
          </div>
        )}

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🤝 Diplomacia</h1>
          <p className="text-slate-400">Relaciones diplomáticas entre naciones</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Tus Relaciones */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold text-white mb-4">
              Tus Relaciones ({playerNation?.name})
            </h2>
            <div className="space-y-4">
              {playerRelations.map((relation) => {
                const otherNationId = relation.nation_a_id === playerNation?.id 
                  ? relation.nation_b_id 
                  : relation.nation_a_id;
                const otherNation = nations.find(n => n.id === otherNationId);

                return (
                  <div
                    key={relation.id}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700 hover:border-slate-600 transition-all duration-300"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-white mb-2">
                          {otherNation?.name}
                        </h3>
                        <div className={`inline-block bg-gradient-to-r ${getRelationColor(relation.status)} text-white text-sm px-3 py-1 rounded-full font-bold`}>
                          {getRelationLabel(relation.status)}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-slate-400">Relación</div>
                        <div className={`text-2xl font-bold ${
                          relation.relationship_score > 50 ? 'text-green-400' :
                          relation.relationship_score > 0 ? 'text-blue-400' :
                          relation.relationship_score > -50 ? 'text-orange-400' :
                          'text-red-400'
                        }`}>
                          {relation.relationship_score}
                        </div>
                      </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="mb-4">
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-500 bg-gradient-to-r ${
                            relation.relationship_score > 0 
                              ? 'from-green-500 to-blue-500' 
                              : 'from-red-500 to-orange-500'
                          }`}
                          style={{ 
                            width: `${Math.abs(relation.relationship_score)}%`,
                            marginLeft: relation.relationship_score < 0 ? `${100 - Math.abs(relation.relationship_score)}%` : '0'
                          }}
                        />
                      </div>
                    </div>

                    {/* Nation Stats */}
                    {otherNation && (
                      <div className="grid grid-cols-3 gap-3 mb-4">
                        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
                          <div className="text-lg">💰</div>
                          <div className="text-yellow-400 font-bold">{otherNation.gold}</div>
                          <div className="text-xs text-slate-400">Oro</div>
                        </div>
                        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
                          <div className="text-lg">🪦</div>
                          <div className="text-red-400 font-bold">{otherNation.troops}</div>
                          <div className="text-xs text-slate-400">Tropas</div>
                        </div>
                        <div className="bg-slate-900/50 rounded-lg p-2 text-center">
                          <div className="text-lg">🏛️</div>
                          <div className="text-blue-400 font-bold">{otherNation.territories}</div>
                          <div className="text-xs text-slate-400">Territorios</div>
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex gap-2">
                      {relation.status !== 'war' && relation.status !== 'allied' && otherNation && (
                        <button 
                          onClick={() => handleProposeAlliance(otherNation.id)}
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          🤝 Proponer Alianza
                        </button>
                      )}
                      {relation.status === 'war' && otherNation && (
                        <button 
                          onClick={() => handleRequestPeace(otherNation.id)}
                          className="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-lg text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          🕊️ Pedir Paz
                        </button>
                      )}
                      {relation.status !== 'war' && relation.status !== 'allied' && otherNation && (
                        <button 
                          onClick={() => handleDeclareWar(otherNation.id)}
                          className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-lg text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          ⚔️ Declarar Guerra
                        </button>
                      )}
                      {relation.status !== 'war' && playerNation && otherNation && (
                        <button 
                          onClick={() => handleSimulateBattle(relation)}
                          className="flex-1 bg-orange-600 hover:bg-orange-700 text-white py-2 px-4 rounded-lg text-sm transition-colors"
                        >
                          🎯 Simular Batalla
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Otras Relaciones */}
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-white mb-4">
                Otras Relaciones Diplomáticas
              </h2>
              <div className="space-y-3">
                {otherRelations.map((relation) => (
                  <div
                    key={relation.id}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4 border border-slate-700"
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-3">
                        <span className="text-white font-bold">
                          {getNationName(relation.nation_a_id)}
                        </span>
                        <div className={`bg-gradient-to-r ${getRelationColor(relation.status)} text-white text-xs px-2 py-1 rounded-full`}>
                          {getRelationLabel(relation.status)}
                        </div>
                        <span className="text-white font-bold">
                          {getNationName(relation.nation_b_id)}
                        </span>
                      </div>
                      <span className={`font-bold ${
                        relation.relationship_score > 50 ? 'text-green-400' :
                        relation.relationship_score > 0 ? 'text-blue-400' :
                        relation.relationship_score > -50 ? 'text-orange-400' :
                        'text-red-400'
                      }`}>
                        {relation.relationship_score}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Simulador de Batalla */}
          <div className="lg:col-span-1">
            <div className="sticky top-8">
              <h2 className="text-2xl font-bold text-white mb-4">🎯 Simulador de Batalla</h2>
              
              {simulation && selectedRelation ? (
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-600">
                  <h3 className="text-lg font-bold text-white mb-4">
                    Resultado de Simulación
                  </h3>
                  
                  {/* Probabilidades */}
                  <div className="space-y-3 mb-4">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-400">Tus probabilidades</span>
                        <span className="text-white font-bold">{simulation.attacker_win_chance.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${simulation.attacker_win_chance}%` }}
                        />
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-400">Enemigo</span>
                        <span className="text-white font-bold">{simulation.defender_win_chance.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-red-500 to-orange-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${simulation.defender_win_chance}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Recomendación */}
                  <div className={`rounded-lg p-4 mb-4 ${
                    simulation.recommendation === 'attack' ? 'bg-green-900/30 border border-green-500' :
                    simulation.recommendation === 'risky' ? 'bg-yellow-900/30 border border-yellow-500' :
                    'bg-red-900/30 border border-red-500'
                  }`}>
                    <div className="font-bold mb-2 ${
                      simulation.recommendation === 'attack' ? 'text-green-400' :
                      simulation.recommendation === 'risky' ? 'text-yellow-400' :
                      'text-red-400'
                    }">
                      {simulation.recommendation === 'attack' && '✅ Recomendado Atacar'}
                      {simulation.recommendation === 'risky' && '⚠️ Arriesgado'}
                      {simulation.recommendation === 'avoid' && '❌ No Recomendado'}
                    </div>
                  </div>

                  {/* Estimaciones */}
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Bajas esperadas (tú)</span>
                      <span className="text-red-300">{simulation.attacker_expected_casualties}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Bajas esperadas (enemigo)</span>
                      <span className="text-red-300">{simulation.defender_expected_casualties}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Territorios esperados</span>
                      <span className="text-blue-400">{simulation.expected_territories}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Oro esperado</span>
                      <span className="text-yellow-400">{simulation.expected_gold}</span>
                    </div>
                  </div>

                  {/* Factores */}
                  <div className="mt-4 pt-4 border-t border-slate-700">
                    <div className="text-xs text-slate-400 space-y-1">
                      <div>Tus aliados: {simulation.factors.attacker_allies} ({simulation.factors.attacker_bonus})</div>
                      <div>Aliados enemigos: {simulation.factors.defender_allies} ({simulation.factors.defender_bonus})</div>
                      <div>Ratio de tropas: {simulation.factors.troop_ratio.toFixed(2)}</div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700 text-center">
                  <p className="text-slate-400">
                    Haz clic en "Simular Batalla" en cualquier relación para ver el análisis
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Página de detalle de nación
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useParams } from 'next/navigation';
import { getNationById, getNationRelations, getRecentEvents } from '@/lib/api';
import type { Nation, Relation, Event } from '@/types';
import Link from 'next/link';

export default function NationDetailPage() {
  const params = useParams();
  const nationId = Number(params.id);
  
  const [nation, setNation] = useState<Nation | null>(null);
  const [relations, setRelations] = useState<Relation[]>([]);
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const loadNationData = useCallback(async () => {
    try {
      const [nationData, relationsData, eventsData] = await Promise.all([
        getNationById(nationId),
        getNationRelations(nationId),
        getRecentEvents(50)
      ]);
      
      setNation(nationData);
      setRelations(relationsData);
      // Filter events related to this nation
      setEvents(eventsData.filter(e => 
        e.description.toLowerCase().includes(nationData.name.toLowerCase()) ||
        e.nation_id === nationId
      ));
    } catch (err) {
      console.error('Error loading nation data:', err);
    } finally {
      setIsLoading(false);
    }
  }, [nationId]);

  useEffect(() => {
    if (nationId) {
      loadNationData();
    }
  }, [nationId, loadNationData]);

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

  const getPersonalityColor = (personality: string) => {
    const colors: Record<string, string> = {
      aggressive: 'from-red-500 to-orange-500',
      diplomatic: 'from-blue-500 to-cyan-500',
      economic: 'from-green-500 to-emerald-500',
      balanced: 'from-purple-500 to-pink-500',
      defensive: 'from-slate-500 to-gray-500',
    };
    return colors[personality] || 'from-gray-500 to-slate-500';
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

  const getEventTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      military: '⚔️',
      economic: '💰',
      diplomatic: '🤝',
      battle: '🎯',
    };
    return icons[type] || '📝';
  };

  const getEventTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      military: 'border-red-500',
      economic: 'border-green-500',
      diplomatic: 'border-blue-500',
      battle: 'border-orange-500',
    };
    return colors[type] || 'border-slate-500';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-500 mx-auto mb-4"></div>
          <p className="text-purple-200 text-lg">Cargando información...</p>
        </div>
      </div>
    );
  }

  if (!nation) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="text-center">
          <p className="text-red-400 text-xl">❌ Nación no encontrada</p>
          <Link href="/game" className="text-purple-400 hover:text-purple-300 mt-4 inline-block">
            ← Volver al juego
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-8">
      <div className="container mx-auto px-4">
        {/* Back Button */}
        <Link 
          href="/game"
          className="inline-block mb-6 text-purple-400 hover:text-purple-300 transition-colors"
        >
          ← Volver al juego
        </Link>

        {/* Nation Header */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border-2 border-purple-500 mb-8">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2">{nation.name}</h1>
              <div className={`inline-block bg-gradient-to-r ${getPersonalityColor(nation.personality)} text-white px-4 py-2 rounded-full mb-4`}>
                {getPersonalityEmoji(nation.personality)} {nation.personality}
              </div>
              
              {nation.is_eliminated && (
                <div className="mt-2 inline-block bg-red-600 text-white px-4 py-2 rounded-full font-bold">
                  ❌ NACIÓN ELIMINADA
                </div>
              )}
            </div>

            <div className="text-right">
              <div className="text-purple-300 text-sm mb-1">Poder Total</div>
              <div className="text-5xl font-bold text-white">
                {Math.round((nation.military_power + nation.economic_power + nation.diplomatic_power) / 3)}
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Stats & Powers */}
          <div className="space-y-8">
            {/* Resources */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700">
              <h2 className="text-2xl font-bold text-white mb-4">📊 Recursos</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-purple-300">💰 Oro</span>
                  <span className="text-yellow-400 font-bold text-2xl">{nation.gold}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-300">🪖 Tropas</span>
                  <span className="text-red-400 font-bold text-2xl">{nation.troops}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-purple-300">🏛️ Territorios</span>
                  <span className="text-blue-400 font-bold text-2xl">{nation.territories}</span>
                </div>
              </div>
            </div>

            {/* Power Levels */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700">
              <h2 className="text-2xl font-bold text-white mb-4">⚡ Poderes</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm text-purple-300 mb-2">
                    <span>⚔️ Poder Militar</span>
                    <span className="font-bold">{nation.military_power}</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-4">
                    <div 
                      className="bg-gradient-to-r from-red-500 to-orange-500 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${nation.military_power}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm text-purple-300 mb-2">
                    <span>💼 Poder Económico</span>
                    <span className="font-bold">{nation.economic_power}</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-4">
                    <div 
                      className="bg-gradient-to-r from-green-500 to-emerald-500 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${nation.economic_power}%` }}
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm text-purple-300 mb-2">
                    <span>🤝 Poder Diplomático</span>
                    <span className="font-bold">{nation.diplomatic_power}</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-4">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-cyan-500 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${nation.diplomatic_power}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Middle Column - Relations */}
          <div className="space-y-8">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700">
              <h2 className="text-2xl font-bold text-white mb-4">🌐 Relaciones</h2>
              <div className="space-y-3">
                {relations.length === 0 ? (
                  <p className="text-purple-300 text-center py-4">No hay relaciones registradas</p>
                ) : (
                  relations.map((relation) => {
                    const otherNationId = relation.nation_a_id === nationId 
                      ? relation.nation_b_id 
                      : relation.nation_a_id;
                    
                    return (
                      <div
                        key={relation.id}
                        className="bg-slate-900/50 rounded-lg p-4 border border-slate-700"
                      >
                        <div className="flex justify-between items-center mb-2">
                          <Link 
                            href={`/game/nations/${otherNationId}`}
                            className="text-white font-bold hover:text-purple-400 transition-colors"
                          >
                            Nación #{otherNationId}
                          </Link>
                          <div className={`bg-gradient-to-r ${getRelationColor(relation.status)} text-white text-xs px-2 py-1 rounded-full`}>
                            {getRelationLabel(relation.status)}
                          </div>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-purple-300 text-sm">Nivel de relación:</span>
                          <span className={`font-bold ${
                            relation.relationship_score > 50 ? 'text-green-400' :
                            relation.relationship_score > 0 ? 'text-blue-400' :
                            relation.relationship_score > -50 ? 'text-orange-400' :
                            'text-red-400'
                          }`}>
                            {relation.relationship_score}
                          </span>
                        </div>
                        <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
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
                    );
                  })
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Events */}
          <div className="space-y-8">
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700">
              <h2 className="text-2xl font-bold text-white mb-4">📜 Eventos Recientes</h2>
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
                {events.length === 0 ? (
                  <p className="text-purple-300 text-center py-4">No hay eventos recientes</p>
                ) : (
                  events.slice(0, 20).map((event) => (
                    <div
                      key={event.id}
                      className={`bg-slate-900/50 rounded-lg p-4 border-l-4 ${getEventTypeColor(event.event_type)}`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{getEventTypeIcon(event.event_type)}</span>
                        <div className="flex-1">
                          <div className="flex justify-between items-start mb-2">
                            <span className="text-xs text-purple-400">Turno {event.turn_number}</span>
                            {event.importance >= 9 && (
                              <span className="text-xs bg-red-600 text-white px-2 py-1 rounded">🔥 CRÍTICO</span>
                            )}
                          </div>
                          <p className="text-white text-sm">{event.description}</p>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(51, 51, 51, 0.3);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: linear-gradient(180deg, #9333ea 0%, #ec4899 100%);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: linear-gradient(180deg, #a855f7 0%, #f472b6 100%);
        }
      `}</style>
    </div>
  );
}

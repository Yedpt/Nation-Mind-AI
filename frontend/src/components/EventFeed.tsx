// Componente para mostrar eventos recientes
'use client';

import type { Event } from '@/types';

interface CasualtiesData {
  attacker?: number;
  defender?: number;
}

interface EventFeedProps {
  events: Event[];
}

export default function EventFeed({ events }: EventFeedProps) {
  const getEventIcon = (eventType: string) => {
    const icons: Record<string, string> = {
      MILITARY: '⚔️',
      ECONOMIC: '💰',
      DIPLOMATIC: '🤝',
      battle: '🎯',
      default: '📌',
    };
    return icons[eventType] || icons.default;
  };

  const getEventColor = (eventType: string) => {
    const colors: Record<string, string> = {
      MILITARY: 'border-red-500/50 bg-red-900/20',
      ECONOMIC: 'border-green-500/50 bg-green-900/20',
      DIPLOMATIC: 'border-blue-500/50 bg-blue-900/20',
      battle: 'border-orange-500/50 bg-orange-900/20',
      default: 'border-purple-500/50 bg-purple-900/20',
    };
    return colors[eventType] || colors.default;
  };

  const getImportanceLabel = (importance: number) => {
    if (importance >= 9) return { label: '🔥 CRÍTICO', color: 'text-red-400' };
    if (importance >= 7) return { label: '⚠️ Importante', color: 'text-orange-400' };
    if (importance >= 5) return { label: 'ℹ️ Notable', color: 'text-yellow-400' };
    return { label: '📝 Normal', color: 'text-purple-300' };
  };

  if (!events || events.length === 0) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border-2 border-slate-700">
        <p className="text-purple-300 text-center">No hay eventos recientes</p>
      </div>
    );
  }

  return (
    <div className="space-y-3 max-h-200 overflow-y-auto pr-2 custom-scrollbar">
      {events.map((event) => {
        const importance = getImportanceLabel(event.importance);
        
        return (
          <div
            key={event.id}
            className={`
              border-l-4 rounded-r-xl p-4 backdrop-blur-sm transition-all duration-300 hover:scale-[1.02]
              ${getEventColor(event.event_type)}
            `}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{getEventIcon(event.event_type)}</span>
                <div>
                  {event.title && (
                    <h4 className="text-white font-bold text-sm">{event.title}</h4>
                  )}
                  <span className={`text-xs ${importance.color}`}>
                    {importance.label}
                  </span>
                </div>
              </div>
              
              <span className="text-xs text-purple-400">
                Turno {event.turn_id}
              </span>
            </div>

            {/* Description */}
            <p className="text-purple-100 text-sm leading-relaxed">
              {event.description}
            </p>

            {/* Additional Data */}
            {event.data && Object.keys(event.data).length > 0 && (
              <div className="mt-3 pt-3 border-t border-slate-700/50">
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {typeof event.data === 'object' && event.data !== null && 'target_nation' in event.data && (
                    <div>
                      <span className="text-purple-400">Objetivo:</span>
                      <span className="text-white ml-1">Nación {String(event.data.target_nation)}</span>
                    </div>
                  )}
                  {typeof event.data === 'object' && event.data !== null && 'action' in event.data && (
                    <div>
                      <span className="text-purple-400">Acción:</span>
                      <span className="text-white ml-1">{String(event.data.action)}</span>
                    </div>
                  )}
                  {typeof event.data === 'object' && event.data !== null && 'casualties' in event.data && (
                    <div className="col-span-2">
                      <span className="text-purple-400">Bajas:</span>
                      <span className="text-red-300 ml-1">
                        Atacante: {String((event.data.casualties as CasualtiesData)?.attacker || 0)}, 
                        Defensor: {String((event.data.casualties as CasualtiesData)?.defender || 0)}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        );
      })}

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(100, 116, 139, 0.2);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(147, 51, 234, 0.5);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(147, 51, 234, 0.8);
        }
      `}</style>
    </div>
  );
}

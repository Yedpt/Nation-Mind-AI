// Página principal del juego - Dashboard
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getGameState, getPlayerNation, processAgentTurn } from '@/lib/api';
import type { GameState, Nation } from '@/types';
import NationCard from '@/components/NationCard';
import EventFeed from '@/components/EventFeed';
import TurnButton from '@/components/TurnButton';
import PlayerActions from '@/components/PlayerActions';
import VictoryPanel from '@/components/VictoryPanel';
import Leaderboard from '@/components/Leaderboard';
import ToastNotification, { useToast } from '@/components/ToastNotification';
import Confetti from '@/components/Confetti';

type TabType = 'overview' | 'actions' | 'leaderboard' | 'events';

export default function GamePage() {
  const router = useRouter();
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [playerNation, setPlayerNation] = useState<Nation | null>(null);
  const [isProcessingTurn, setIsProcessingTurn] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('overview');
  const [previousGold, setPreviousGold] = useState<number>(0);
  const [previousTurn, setPreviousTurn] = useState<number>(0);
  const [showConfetti, setShowConfetti] = useState(false);
  const { toasts, showToast, removeToast } = useToast();

  const getVictoryTypeName = (type: string): string => {
    const victoryNames: { [key: string]: string } = {
      'domination': 'Dominación 👑',
      'elimination': 'Eliminación ⚔️',
      'economic': 'Económica 💰',
      'military': 'Militar 🪖',
      'survival': 'Supervivencia 🛡️'
    };
    return victoryNames[type] || type;
  };

  const loadGameData = async () => {
    try {
      const [state, player] = await Promise.all([
        getGameState(),
        getPlayerNation()
      ]);
      
      // Detectar cambios importantes y mostrar notificaciones
      if (playerNation && player) {
        const goldDiff = player.gold - previousGold;
        
        // Notificación de cambio de oro significativo
        if (Math.abs(goldDiff) >= 100 && previousGold > 0) {
          if (goldDiff > 0) {
            showToast(
              'economic',
              '💰 Ingreso de Oro',
              `+${goldDiff} oro generado este turno`,
              4000
            );
          } else {
            showToast(
              'warning',
              '💸 Gasto de Oro',
              `${goldDiff} oro gastado`,
              4000
            );
          }
        }
        
        // Detectar cambio de turno
        if (state.current_turn > previousTurn && previousTurn > 0) {
          showToast(
            'info',
            '📅 Nuevo Turno',
            `Turno ${state.current_turn} iniciado`,
            3000
          );
        }
        
        // Detectar eventos de batalla recientes
        const battleEvents = state.recent_events.filter(
          e => e.event_type === 'battle_result' && e.turn_number === state.current_turn
        );
        if (battleEvents.length > 0) {
          battleEvents.forEach(event => {
            showToast(
              'battle',
              '⚔️ Batalla Resuelta',
              event.description,
              5000
            );
          });
        }
        
        setPreviousGold(player.gold);
      }
      
      if (state && state.current_turn > previousTurn) {
        setPreviousTurn(state.current_turn);
      }
      
      setGameState(state);
      setPlayerNation(player);
      setError(null);
    } catch (err: unknown) {
      console.error('Error loading game:', err);
      if (err && typeof err === 'object' && 'response' in err) {
        const response = err as { response?: { status?: number } };
        if (response.response?.status === 404) {
          router.push('/');
          return;
        }
      }
      showToast('error', '❌ Error', 'Error cargando datos del juego', 4000);
      setError('Error cargando datos del juego');
    }
  };

  useEffect(() => {
    loadGameData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Detectar victoria próxima
  useEffect(() => {
    if (gameState?.victory_progress) {
      const conditions = Object.entries(gameState.victory_progress);
      
      conditions.forEach(([key, data]) => {
        const conditionData = data as { progress: number; completed: boolean; description: string };
        
        // Celebrar cuando se completa una condición
        if (conditionData.completed) {
          setShowConfetti(true);
          setTimeout(() => setShowConfetti(false), 3000);
        }
        
        // Notificar cuando se alcanza 75% en alguna condición
        if (conditionData.progress >= 75 && conditionData.progress < 100 && !conditionData.completed) {
          const victoryNames: { [key: string]: string } = {
            'domination': 'Dominación 👑',
            'economic': 'Económica 💰',
            'military': 'Militar 🪖',
            'elimination': 'Eliminación ⚔️',
            'survival': 'Supervivencia 🛡️'
          };
          
          showToast(
            'victory',
            '🏆 Victoria Próxima',
            `¡Estás al ${conditionData.progress.toFixed(0)}% de la victoria por ${victoryNames[key] || key}!`,
            6000
          );
        }
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gameState?.victory_progress?.domination?.progress]); // Trigger cuando cambia el progreso

  const handleProcessTurn = async () => {
    setIsProcessingTurn(true);
    showToast('info', '⚙️ Procesando Turno', 'Ejecutando acciones de las IA...', 3000);
    
    try {
      await processAgentTurn();
      await loadGameData();
      
      showToast(
        'success',
        '✅ Turno Completado',
        'Todas las naciones han actuado. Revisa los eventos.',
        5000
      );
    } catch (err) {
      console.error('Error processing turn:', err);
      showToast(
        'error',
        '❌ Error al Procesar Turno',
        'Hubo un problema procesando el turno',
        4000
      );
      setError('Error procesando turno');
    } finally {
      setIsProcessingTurn(false);
    }
  };

  if (!gameState || !playerNation) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-slate-500 mx-auto mb-4"></div>
          <p className="text-slate-300 text-lg">Cargando juego...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 py-4">
      {/* Sistema de notificaciones */}
      <ToastNotification toasts={toasts} onRemove={removeToast} />
      
      {/* Confetti de celebración */}
      <Confetti show={showConfetti} />
      
      <div className="container mx-auto px-4">
        {/* Compact Header con info clave */}
        <div className="bg-gradient-to-r from-slate-800 to-slate-900 rounded-xl p-6 mb-6 border border-slate-700 shadow-2xl">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            {/* Info del jugador */}
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-1">
                {playerNation.name}
              </h1>
              <div className="flex items-center gap-4 text-sm flex-wrap">
                <span className="text-slate-400">Turno {gameState.current_turn}</span>
                <span className={`flex items-center gap-1 font-bold transition-all duration-300 ${
                  playerNation.gold >= 1000 ? 'text-yellow-400 scale-110' : 'text-yellow-400'
                }`}>
                  💰 {playerNation.gold} oro
                  {playerNation.gold >= 5000 && <span className="text-xs ml-1">🔥</span>}
                </span>
                <span className={`flex items-center gap-1 font-bold transition-all duration-300 ${
                  playerNation.troops >= 1000 ? 'text-red-400 scale-110' : 'text-red-400'
                }`}>
                  ⚔️ {playerNation.troops} tropas
                  {playerNation.troops >= 1500 && <span className="text-xs ml-1">💪</span>}
                </span>
                <span className={`flex items-center gap-1 font-bold transition-all duration-300 ${
                  playerNation.territories >= 10 ? 'text-blue-400 scale-110' : 'text-blue-400'
                }`}>
                  🏛️ {playerNation.territories} territorios
                  {playerNation.territories >= 15 && <span className="text-xs ml-1">🌟</span>}
                </span>
              </div>
            </div>
            
            {/* Botón de procesar turno destacado */}
            <TurnButton 
              isProcessing={isProcessingTurn}
              onProcessTurn={handleProcessTurn}
              disabled={gameState.is_game_over}
            />
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-900/30 border border-red-500 rounded-lg p-4">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Game Over */}
        {gameState.is_game_over && (
          <div className="mb-6 bg-gradient-to-r from-yellow-900/50 to-amber-900/50 border-2 border-yellow-500 rounded-xl p-6 text-center shadow-2xl animate-pulse">
            <h2 className="text-3xl font-bold text-yellow-400 mb-3 flex items-center justify-center gap-3">
              <span>🏆</span>
              ¡Juego Terminado!
              <span>🏆</span>
            </h2>
            {gameState.winner && (
              <p className="text-xl text-yellow-200 mb-2">
                <strong className="text-white">{gameState.winner}</strong> ha ganado
              </p>
            )}
            {gameState.victory_type && (
              <p className="text-lg text-yellow-300">
                Victoria por <strong>{getVictoryTypeName(gameState.victory_type)}</strong>
              </p>
            )}
          </div>
        )}

        {/* Sistema de Tabs */}
        <div className="mb-6">
          <div className="flex gap-2 border-b border-slate-700 pb-2 overflow-x-auto">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-6 py-3 rounded-t-lg font-bold transition-all duration-200 whitespace-nowrap ${
                activeTab === 'overview'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              🌍 Tablero General
            </button>
            <button
              onClick={() => setActiveTab('actions')}
              className={`relative px-6 py-3 rounded-t-lg font-bold transition-all duration-200 whitespace-nowrap ${
                activeTab === 'actions'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              🎮 Tus Acciones
              {playerNation.gold >= 800 && (
                <span className="absolute -top-1 -right-1 bg-green-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
                  !
                </span>
              )}
            </button>
            <button
              onClick={() => setActiveTab('leaderboard')}
              className={`px-6 py-3 rounded-t-lg font-bold transition-all duration-200 whitespace-nowrap ${
                activeTab === 'leaderboard'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              🏅 Clasificación
            </button>
            <button
              onClick={() => setActiveTab('events')}
              className={`relative px-6 py-3 rounded-t-lg font-bold transition-all duration-200 whitespace-nowrap ${
                activeTab === 'events'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
              }`}
            >
              📰 Eventos
              {gameState.recent_events.length > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {gameState.recent_events.length > 9 ? '9+' : gameState.recent_events.length}
                </span>
              )}
            </button>
          </div>
        </div>

        {/* Contenido de Tabs */}
        <div className="animate-fadeIn">
          {/* TAB: Tablero General */}
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Naciones (2 columnas) */}
              <div className="lg:col-span-2">
                <h2 className="text-2xl font-bold text-white mb-4">Naciones del Mundo</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {gameState.nations.map((nation) => (
                    <NationCard 
                      key={nation.id}
                      nation={nation}
                      isPlayer={nation.id === playerNation.id}
                    />
                  ))}
                </div>
              </div>

              {/* Panel de Victoria (1 columna) */}
              <div>
                {gameState.victory_progress && (
                  <VictoryPanel 
                    progress={gameState.victory_progress}
                    currentTurn={gameState.current_turn}
                  />
                )}
              </div>
            </div>
          )}

          {/* TAB: Tus Acciones */}
          {activeTab === 'actions' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div>
                <PlayerActions 
                  playerNation={playerNation}
                  onActionComplete={loadGameData}
                  onShowNotification={(type, title, message) => 
                    showToast(type, title, message, 4000)
                  }
                />
              </div>
              <div>
                {gameState.victory_progress && (
                  <VictoryPanel 
                    progress={gameState.victory_progress}
                    currentTurn={gameState.current_turn}
                  />
                )}
              </div>
            </div>
          )}

          {/* TAB: Clasificación */}
          {activeTab === 'leaderboard' && (
            <div className="max-w-4xl mx-auto">
              <Leaderboard />
            </div>
          )}

          {/* TAB: Eventos */}
          {activeTab === 'events' && (
            <div className="max-w-4xl mx-auto">
              <h2 className="text-2xl font-bold text-white mb-4">📰 Eventos Recientes</h2>
              <EventFeed events={gameState.recent_events} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

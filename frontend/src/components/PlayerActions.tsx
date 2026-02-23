'use client';

import { useState } from 'react';
import { executePlayerAction } from '@/lib/api';
import type { Nation } from '@/types';

interface PlayerActionsProps {
  playerNation: Nation;
  onActionComplete: () => void;
  onShowNotification?: (type: 'success' | 'error' | 'warning', title: string, message: string) => void;
}

export default function PlayerActions({ playerNation, onActionComplete, onShowNotification }: PlayerActionsProps) {
  const [isProcessing, setIsProcessing] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const showMessage = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 4000);
  };

  const handleInvestEconomy = async () => {
    if (playerNation.gold < 800) {
      showMessage('error', '❌ Necesitas al menos 800 de oro');
      if (onShowNotification) {
        onShowNotification('error', '💰 Oro Insuficiente', 'Necesitas 800 oro para invertir en economía');
      }
      return;
    }

    setIsProcessing(true);
    try {
      await executePlayerAction(playerNation.id, {
        action_type: 'build',
        data: { type: 'economy', amount: 800 }
      });
      showMessage('success', '✅ Inversión económica realizada (+20-40% poder económico)');
      if (onShowNotification) {
        onShowNotification('success', '💼 Inversión Exitosa', 'Tu economía ha mejorado significativamente');
      }
      onActionComplete();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      const errorMsg = error.response?.data?.detail || error.message || 'Error desconocido';
      showMessage('error', `❌ Error: ${errorMsg}`);
      if (onShowNotification) {
        onShowNotification('error', '❌ Error', errorMsg);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRecruitTroops = async () => {
    if (playerNation.gold < 800) {
      showMessage('error', '❌ Necesitas al menos 800 de oro');
      if (onShowNotification) {
        onShowNotification('error', '💰 Oro Insuficiente', 'Necesitas 800 oro para reclutar tropas');
      }
      return;
    }

    setIsProcessing(true);
    try {
      await executePlayerAction(playerNation.id, {
        action_type: 'recruit',
        data: { amount: 400 }
      });
      showMessage('success', '✅ Tropas reclutadas (+400 tropas, -800 oro)');
      if (onShowNotification) {
        onShowNotification('success', '🪖 Tropas Reclutadas', '¡400 nuevas tropas listas para la batalla!');
      }
      onActionComplete();
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } }; message?: string };
      const errorMsg = error.response?.data?.detail || error.message || 'Error desconocido';
      showMessage('error', `❌ Error: ${errorMsg}`);
      if (onShowNotification) {
        onShowNotification('error', '❌ Error', errorMsg);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const canAfford = playerNation.gold >= 800;

  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 border border-slate-700 shadow-2xl">
      <h3 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
        <span>🎮</span>
        Tus Acciones
      </h3>

      {/* Mensaje de notificación */}
      {message && (
        <div className={`mb-4 p-3 rounded-lg border text-sm ${
          message.type === 'success' 
            ? 'bg-green-900/20 border-green-500 text-green-300' 
            : 'bg-red-900/20 border-red-500 text-red-300'
        }`}>
          {message.text}
        </div>
      )}

      {/* Recursos actuales */}
      <div className="bg-slate-800/50 rounded-lg p-4 mb-6">
        <h4 className="text-sm font-semibold text-slate-400 mb-3">Tus Recursos</h4>
        <div className="grid grid-cols-3 gap-3">
          <div className="text-center">
            <div className="text-2xl mb-1">💰</div>
            <div className="text-xl font-bold text-yellow-400">{playerNation.gold}</div>
            <div className="text-xs text-slate-400">Oro</div>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-1">⚔️</div>
            <div className="text-xl font-bold text-red-400">{playerNation.troops}</div>
            <div className="text-xs text-slate-400">Tropas</div>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-1">🏛️</div>
            <div className="text-xl font-bold text-blue-400">{playerNation.territories}</div>
            <div className="text-xs text-slate-400">Territorios</div>
          </div>
        </div>
      </div>

      {/* Advertencia de oro insuficiente */}
      {!canAfford && (
        <div className="mb-4 bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-3 text-sm text-yellow-300">
          ⚠️ Necesitas al menos 800 de oro para realizar acciones
        </div>
      )}

      {/* Botones de acción */}
      <div className="space-y-3">
        <button
          onClick={handleInvestEconomy}
          disabled={isProcessing || !canAfford}
          className={`
            w-full py-4 rounded-lg font-bold text-lg transition-all duration-300
            ${canAfford && !isProcessing
              ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
              : 'bg-slate-700 text-slate-500 cursor-not-allowed opacity-50'
            }
          `}
        >
          {isProcessing ? (
            <span className="flex items-center justify-center gap-2">
              <span className="animate-spin">⏳</span>
              Procesando...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <span>💼</span>
              Invertir en Economía
              <span className="text-sm opacity-80">(800 oro)</span>
            </span>
          )}
        </button>

        <button
          onClick={handleRecruitTroops}
          disabled={isProcessing || !canAfford}
          className={`
            w-full py-4 rounded-lg font-bold text-lg transition-all duration-300
            ${canAfford && !isProcessing
              ? 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
              : 'bg-slate-700 text-slate-500 cursor-not-allowed opacity-50'
            }
          `}
        >
          {isProcessing ? (
            <span className="flex items-center justify-center gap-2">
              <span className="animate-spin">⏳</span>
              Procesando...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <span>🪖</span>
              Reclutar Tropas
              <span className="text-sm opacity-80">(+400 tropas, 800 oro)</span>
            </span>
          )}
        </button>
      </div>

      {/* Información adicional */}
      <div className="mt-6 text-xs text-slate-400 space-y-1">
        <p>💡 <strong>Tip:</strong> Invierte en economía para generar más oro cada turno</p>
        <p>💡 <strong>Tip:</strong> Recluta tropas para defenderte o atacar a otras naciones</p>
        <p>💡 Ve a la página de <a href="/game/diplomacy" className="text-blue-400 hover:text-blue-300 underline">Diplomacia</a> para alianzas y guerras</p>
      </div>
    </div>
  );
}

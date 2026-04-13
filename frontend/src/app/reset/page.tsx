'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { initializeGame } from '@/lib/api';

export default function ResetPage() {
  const router = useRouter();
  const [isResetting, setIsResetting] = useState(false);
  const [message, setMessage] = useState('');

  const handleReset = async () => {
    if (!confirm('⚠️ ¿Estás seguro? Esto eliminará el juego actual y todos los datos.')) {
      return;
    }

    setIsResetting(true);
    setMessage('');

    try {
      await initializeGame('ESP', true);
      setMessage('✅ Juego reseteado exitosamente');
      setTimeout(() => router.push('/'), 1500);
    } catch (err) {
      setMessage('❌ Error al resetear el juego');
      console.error(err);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-8 shadow-2xl">
          <div className="text-center mb-8">
            <div className="mb-4 text-6xl">🔄</div>
            <h1 className="text-4xl font-bold text-white mb-2">Resetear Juego</h1>
            <p className="text-slate-400">
              Esto eliminará el juego actual y todas las partidas guardadas
            </p>
          </div>

          <div className="bg-yellow-900/30 border border-yellow-500/50 rounded-lg p-6 mb-8">
            <h3 className="text-yellow-400 font-bold mb-2">⚠️ Advertencia:</h3>
            <ul className="text-yellow-200 space-y-1 text-sm">
              <li>• Se eliminarán todas las naciones</li>
              <li>• Se perderán todos los turnos y eventos</li>
              <li>• Se borrarán todas las relaciones diplomáticas</li>
              <li>• Esta acción NO se puede deshacer</li>
            </ul>
          </div>

          {message && (
            <div className={`mb-6 p-4 rounded-lg ${
              message.includes('✅') 
                ? 'bg-green-900/30 border border-green-500 text-green-200'
                : 'bg-red-900/30 border border-red-500 text-red-200'
            }`}>
              {message}
            </div>
          )}

          <div className="flex gap-4">
            <button
              onClick={() => router.push('/')}
              className="flex-1 bg-slate-700 hover:bg-slate-600 text-white py-4 rounded-xl font-semibold transition-all"
              disabled={isResetting}
            >
              ← Cancelar
            </button>
            <button
              onClick={handleReset}
              disabled={isResetting}
              className={`flex-1 py-4 rounded-xl font-semibold transition-all ${
                isResetting
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-red-600 hover:bg-red-700 text-white shadow-lg hover:shadow-xl'
              }`}
            >
              {isResetting ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Reseteando...
                </span>
              ) : (
                '🗑️ Resetear Juego'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

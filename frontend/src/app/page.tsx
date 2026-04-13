// Pagina de inicio - Selección de nación
'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { getAvailableNations, initializeGame, healthCheck } from '@/lib/api';
import type { AvailableNation } from '@/types';
import ToastNotification, { useToast } from '@/components/ToastNotification';

export default function Home() {
  const router = useRouter();
  const [nations, setNations] = useState<AvailableNation[]>([]);
  const [selectedNation, setSelectedNation] = useState<string>('');
  const [isInitializing, setIsInitializing] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'ok' | 'error'>('checking');
  const [error, setError] = useState<string | null>(null);
  const { toasts, showToast, removeToast } = useToast();
  const backendStatusToastShown = useRef(false);

  // Mapeo de países a códigos, regiones y stats simulados (solo naciones disponibles en el backend)
  const countryData: Record<string, { code: string; region: string; population: string; gdp: string }> = {
    'estados unidos': { code: 'USA', region: 'América del Norte', population: '331M', gdp: '$21000B' },
    'china': { code: 'CHN', region: 'Asia', population: '1400M', gdp: '$14000B' },
    'rusia': { code: 'RUS', region: 'Europa/Asia', population: '144M', gdp: '$1700B' },
    'alemania': { code: 'DEU', region: 'Europa', population: '83M', gdp: '$3800B' },
    'reino unido': { code: 'GBR', region: 'Europa', population: '67M', gdp: '$2800B' },
    'francia': { code: 'FRA', region: 'Europa', population: '65M', gdp: '$2700B' },
    'japón': { code: 'JPN', region: 'Asia', population: '126M', gdp: '$5000B' },
    'españa': { code: 'ESP', region: 'Europa', population: '47M', gdp: '$1400B' },
  };

  const checkBackendAndLoadNations = async () => {
    try {
      await healthCheck();
      setBackendStatus('ok');
      const nationsData = await getAvailableNations();
      setNations(nationsData.available_nations);
      if (!backendStatusToastShown.current) {
        showToast('success', 'Backend conectado', 'Sistema listo para iniciar la partida', 3500);
        backendStatusToastShown.current = true;
      }
    } catch (error) {
      setBackendStatus('error');
      setError('No se pudo conectar con el backend. Asegúrate de que esté corriendo en http://localhost:8000');
      if (!backendStatusToastShown.current) {
        showToast('error', 'Backend no disponible', 'Revisa que la API esté activa antes de comenzar', 4500);
        backendStatusToastShown.current = true;
      }
    }
  };

  useEffect(() => {
    checkBackendAndLoadNations();
  }, []);

  const handleInitializeGame = async () => {
    if (!selectedNation || isInitializing) return;

    setIsInitializing(true);
    setError(null);

    try {
      // Convertir nombre a código de 3 letras que el backend espera
      const nationCode = countryData[selectedNation]?.code;
      
      console.log('==========================================');
      console.log('🎮 INICIANDO JUEGO');
      console.log('Selected Nation (estado):', selectedNation);
      console.log('Country Data:', countryData[selectedNation]);
      console.log('Nation Code:', nationCode);
      console.log('Tipo de nationCode:', typeof nationCode);
      console.log('Length de nationCode:', nationCode?.length);
      console.log('==========================================');
      
      if (!nationCode) {
        throw new Error('Código de nación no válido');
      }
      
      await initializeGame(nationCode);
      console.log('✅ Juego inicializado, redirigiendo...');
      router.push('/game');
    } catch (err) {
      console.error('❌ Error al inicializar juego:', err);
      setError(err instanceof Error ? err.message : 'Error al inicializar el juego');
      setIsInitializing(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 py-8">
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(circle at 8% 0%, rgba(168, 85, 247, 0.2), transparent 30%), radial-gradient(circle at 88% 12%, rgba(56, 189, 248, 0.14), transparent 28%), linear-gradient(to bottom, rgba(15, 23, 42, 1), rgba(2, 6, 23, 1))',
        }}
      />

      <ToastNotification toasts={toasts} onRemove={removeToast} />

      <div className="relative container mx-auto px-4">
        {/* Hero Section */}
        <div className="text-center mb-8 rounded-3xl border border-slate-800/80 bg-slate-900/55 px-6 py-8 shadow-2xl shadow-black/20 backdrop-blur-sm">
          <div className="inline-block mb-5">
            <span className="rounded-full border border-slate-700 bg-slate-950/80 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.22em] text-slate-300">
              ⚙️ Simulador de Estrategia Global
            </span>
          </div>
          <h1 className="mb-3 bg-linear-to-r from-white via-purple-200 to-sky-200 bg-clip-text text-4xl font-bold text-transparent md:text-6xl">
            Gobierna el Mundo
          </h1>
          <p className="mb-2 text-lg text-slate-200 md:text-xl">Selecciona una nación y lidera tu país hacia la gloria en un mundo simulado</p>
          <p className="mx-auto max-w-3xl text-sm text-slate-400 md:text-base">
            Gestiona diplomacia, economía, ejército y tecnología mientras agentes de IA controlan el resto del mundo
          </p>
          <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
            <span className="rounded-full border border-purple-500/20 bg-purple-500/10 px-3 py-1 text-xs text-purple-200">
              8 naciones
            </span>
            <span className="rounded-full border border-sky-500/20 bg-sky-500/10 px-3 py-1 text-xs text-sky-200">
              IA multiagente
            </span>
            <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-200">
              RAG + memoria
            </span>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mx-auto mb-6 max-w-4xl rounded-xl border-2 border-red-500/70 bg-red-900/20 p-4 backdrop-blur-sm">
            <p className="text-red-200 text-center font-bold">{error}</p>
          </div>
        )}

        {/* Nations Grid */}
        {backendStatus === 'ok' && nations.length > 0 && (
          <>
            <div className="grid grid-cols-1 gap-4 pb-8 md:grid-cols-2 xl:grid-cols-4">
              {nations.map((nation) => {
                const countryInfo = countryData[nation.name.toLowerCase()] || { 
                  code: nation.name.substring(0, 2).toUpperCase(), 
                  region: 'Desconocida',
                  population: '0M',
                  gdp: '$0B'
                };
                const isSelected = selectedNation === nation.name.toLowerCase();
                
                return (
                  <div
                    key={nation.name}
                    onClick={() => setSelectedNation(nation.name.toLowerCase())}
                    className={`
                      relative cursor-pointer rounded-2xl border-2 bg-slate-900/60 p-4 backdrop-blur-sm
                      transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/30
                      ${isSelected 
                        ? 'border-purple-400 shadow-lg shadow-purple-500/25 bg-slate-800/75' 
                        : 'border-slate-700/60 hover:border-slate-500'}
                    `}
                  >
                    {/* Selected Indicator */}
                    {isSelected && (
                      <div className="absolute -top-2 -right-2 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 shadow-lg shadow-purple-500/40">
                        <span className="text-white text-base">✓</span>
                      </div>
                    )}

                    {/* Country Code */}
                    <div className="mb-1 text-4xl font-bold text-slate-200 xl:text-[2.5rem]">
                      {countryInfo.code}
                    </div>

                    {/* Country Name */}
                    <h3 className="mb-1 text-lg font-bold text-white xl:text-xl">
                      {nation.name}
                    </h3>

                    {/* Region */}
                    <p className="mb-4 text-xs text-slate-500 xl:text-sm">
                      {countryInfo.region}
                    </p>

                    {/* Stats */}
                    <div className="mb-4 space-y-2">
                      <div className="flex items-center justify-between text-xs xl:text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-sm">👥</span>
                          <span>Población</span>
                        </div>
                        <span className="font-semibold text-white">{countryInfo.population}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-xs xl:text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-sm">🏛️</span>
                          <span>PIB</span>
                        </div>
                        <span className="font-semibold text-white">{countryInfo.gdp}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-xs xl:text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-sm">🛡️</span>
                          <span>Militar</span>
                        </div>
                        <span className="font-semibold text-white">{nation.military_power}/100</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-xs xl:text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-sm">💡</span>
                          <span>Tecnología</span>
                        </div>
                        <span className="font-semibold text-white">{nation.diplomatic_power}/100</span>
                      </div>
                    </div>

                    {/* Action Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedNation(nation.name.toLowerCase());
                      }}
                      className={`
                        w-full rounded-lg py-2.5 text-sm font-semibold transition-all duration-300 xl:text-base
                        ${isSelected 
                          ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50' 
                          : 'bg-slate-700 text-slate-300 hover:bg-slate-600 hover:text-white'}
                      `}
                    >
                      Gobernar {nation.name}
                    </button>
                  </div>
                );
              })}
            </div>

            {/* Initialize Button */}
            <div className="text-center">
              <button
                onClick={handleInitializeGame}
                disabled={isInitializing || !selectedNation}
                className={`
                  bg-linear-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white text-lg font-bold
                  px-12 py-3.5 rounded-xl transition-all duration-300
                  shadow-lg shadow-purple-500/30
                  ${isInitializing || !selectedNation
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:scale-105 hover:shadow-xl hover:shadow-purple-500/40'
                  }
                `}
              >
                {isInitializing ? (
                  <span className="flex items-center gap-3">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                    Inicializando mundo...
                  </span>
                ) : (
                  <span>🌍 Comenzar Simulación</span>
                )}
              </button>
              {selectedNation && !isInitializing && (
                <p className="mt-3 text-sm text-slate-400">
                  Liderarás: <span className="font-bold text-white">{selectedNation.charAt(0).toUpperCase() + selectedNation.slice(1)}</span>
                </p>
              )}
            </div>
          </>
        )}

        {/* Loading State */}
        {backendStatus === 'checking' && (
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-500 mx-auto mb-4"></div>
            <p className="text-purple-200 text-lg">Cargando naciones disponibles...</p>
          </div>
        )}
      </div>
    </div>
  );
}
// Pagina de inicio - Selección de nación
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getAvailableNations, initializeGame, healthCheck } from '@/lib/api';
import type { AvailableNation } from '@/types';

export default function Home() {
  const router = useRouter();
  const [nations, setNations] = useState<AvailableNation[]>([]);
  const [selectedNation, setSelectedNation] = useState<string>('');
  const [isInitializing, setIsInitializing] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'ok' | 'error'>('checking');
  const [error, setError] = useState<string | null>(null);

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
    } catch (error) {
      setBackendStatus('error');
      setError('No se pudo conectar con el backend. Asegúrate de que esté corriendo en http://localhost:8000');
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
    <div className="min-h-screen bg-slate-900 py-12">
      <div className="container mx-auto px-4">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-block mb-6">
            <span className="bg-slate-800 text-slate-300 px-4 py-2 rounded-lg text-sm border border-slate-700">
              ⚙️ Simulador de Estrategia Global
            </span>
          </div>
          <h1 className="text-7xl font-bold mb-4 text-white">
            Gobierna el Mundo
          </h1>
          <p className="text-xl text-slate-300 mb-2">Selecciona una nación y lidera tu país hacia la gloria en un mundo simulado</p>
          <p className="text-base text-slate-400">Gestiona diplomacia, economía, ejército y tecnología mientras agentes de IA controlan el resto del mundo</p>
          
          {/* Backend Status */}
          <div className="mt-6 inline-block">
            {backendStatus === 'checking' && (
              <div className="bg-yellow-900/30 border border-yellow-500 text-yellow-200 px-4 py-2 rounded-lg">
                ⏳ Conectando con el backend...
              </div>
            )}
            {backendStatus === 'ok' && (
              <div className="bg-green-900/30 border border-green-500 text-green-200 px-4 py-2 rounded-lg">
                ✅ Backend conectado correctamente
              </div>
            )}
            {backendStatus === 'error' && (
              <div className="bg-red-900/30 border border-red-500 text-red-200 px-4 py-2 rounded-lg">
                ❌ Error de conexión con el backend
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8 bg-red-900/30 border-2 border-red-500 rounded-xl p-4">
            <p className="text-red-200 text-center font-bold">{error}</p>
          </div>
        )}

        {/* Nations Grid */}
        {backendStatus === 'ok' && nations.length > 0 && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
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
                      relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border-2 cursor-pointer
                      transition-all duration-300 hover:scale-105 hover:shadow-2xl
                      ${isSelected 
                        ? 'border-blue-500 shadow-lg shadow-blue-500/30 bg-slate-700/70' 
                        : 'border-slate-700/50 hover:border-slate-600'}
                    `}
                  >
                    {/* Selected Indicator */}
                    {isSelected && (
                      <div className="absolute -top-2 -right-2 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center shadow-lg">
                        <span className="text-white text-base">✓</span>
                      </div>
                    )}

                    {/* Country Code */}
                    <div className="text-5xl font-bold text-slate-300 mb-2">
                      {countryInfo.code}
                    </div>

                    {/* Country Name */}
                    <h3 className="text-2xl font-bold text-white mb-1">
                      {nation.name}
                    </h3>

                    {/* Region */}
                    <p className="text-sm text-slate-500 mb-6">
                      {countryInfo.region}
                    </p>

                    {/* Stats */}
                    <div className="space-y-3 mb-6">
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-base">👥</span>
                          <span>Población</span>
                        </div>
                        <span className="text-white font-semibold">{countryInfo.population}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-base">🏛️</span>
                          <span>PIB</span>
                        </div>
                        <span className="text-white font-semibold">{countryInfo.gdp}</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-base">🛡️</span>
                          <span>Militar</span>
                        </div>
                        <span className="text-white font-semibold">{nation.military_power}/100</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-base">💡</span>
                          <span>Tecnología</span>
                        </div>
                        <span className="text-white font-semibold">{nation.diplomatic_power}/100</span>
                      </div>
                    </div>

                    {/* Action Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedNation(nation.name.toLowerCase());
                      }}
                      className={`
                        w-full py-3 rounded-lg font-semibold transition-all duration-300
                        ${isSelected 
                          ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/50' 
                          : 'bg-slate-700 text-slate-300 hover:bg-slate-600 hover:text-white'}
                      `}
                    >
                      Governar {nation.name}
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
                  bg-blue-600 hover:bg-blue-700 text-white text-xl font-bold
                  px-16 py-4 rounded-xl transition-all duration-300
                  shadow-lg shadow-blue-500/30
                  ${isInitializing || !selectedNation
                    ? 'opacity-50 cursor-not-allowed'
                    : 'hover:scale-105 hover:shadow-xl hover:shadow-blue-500/50'
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
                <p className="text-slate-400 mt-4">
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
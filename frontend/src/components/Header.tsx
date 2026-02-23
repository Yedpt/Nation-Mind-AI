'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();
  
  const isActive = (path: string) => pathname === path;
  
  return (
    <header className="bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900 border-b border-purple-500/30 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo y Título */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="relative">
              <div className="absolute inset-0 bg-purple-500 blur-xl opacity-50 rounded-full"></div>
              <div className="relative bg-gradient-to-br from-purple-400 to-pink-600 p-3 rounded-xl shadow-lg">
                <svg
                  className="w-8 h-8 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">
                Nation-Mind AI
              </h1>
              <p className="text-xs text-purple-300">Simulador Geopolítico</p>
            </div>
          </Link>

          {/* Navegación */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              href="/"
              className={`px-4 py-2 rounded-lg transition-all ${
                isActive('/')
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'text-purple-200 hover:text-white hover:bg-white/10'
              }`}
            >
              Inicio
            </Link>
            <Link
              href="/game"
              className={`px-4 py-2 rounded-lg transition-all ${
                isActive('/game')
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'text-purple-200 hover:text-white hover:bg-white/10'
              }`}
            >
              🎮 Juego
            </Link>
            <Link
              href="/game/battles"
              className={`px-4 py-2 rounded-lg transition-all ${
                pathname?.startsWith('/game/battles')
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'text-purple-200 hover:text-white hover:bg-white/10'
              }`}
            >
              ⚔️ Batallas
            </Link>
            <Link
              href="/game/diplomacy"
              className={`px-4 py-2 rounded-lg transition-all ${
                pathname?.startsWith('/game/diplomacy')
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'text-purple-200 hover:text-white hover:bg-white/10'
              }`}
            >
              🤝 Diplomacia
            </Link>
            <Link
              href="/reset"
              className={`px-4 py-2 rounded-lg transition-all ${
                pathname?.startsWith('/reset')
                  ? 'bg-red-600 text-white shadow-lg shadow-red-500/50'
                  : 'text-red-400 hover:text-white hover:bg-red-900/20'
              }`}
            >
              🔄 Reset
            </Link>
          </nav>

          {/* Mobile Menu Button */}
          <button className="md:hidden p-2 text-purple-200 hover:text-white">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}

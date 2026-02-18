// src/app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { healthCheck } from '@/lib/api';

export default function Home() {
  const [backendStatus, setBackendStatus] = useState('checking...');

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await healthCheck();
        setBackendStatus(`✅ Backend conectado: ${data.status}`);
      } catch (error) {
        setBackendStatus('❌ Backend no disponible' + (error instanceof Error ? `: ${error.message}` : ''));
      }
    };
    checkBackend();
  }, []);

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-4">Nation Mind AI</h1>
      <p className="text-lg mb-8">Simulador Geopolítico con IA</p>
      
      <div className="bg-gray-100 p-4 rounded">
        <p>Estado del Backend: {backendStatus}</p>
      </div>
    </main>
  );
}
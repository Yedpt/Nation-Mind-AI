import { NextRequest, NextResponse } from 'next/server';

const normalizeBackendBaseUrl = (value: string): string =>
  value.replace(/\/+$/, '').replace(/\/api$/i, '');

const BACKEND_BASE_URL = normalizeBackendBaseUrl(
  process.env.BACKEND_INTERNAL_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    (process.env.NODE_ENV === 'production'
      ? 'https://nation-mind-ai.onrender.com'
      : 'http://localhost:8000')
);
const BACKEND_API_KEY = process.env.BACKEND_API_KEY || '';
const NODE_ENV = process.env.NODE_ENV || 'development';

export async function POST(request: NextRequest) {
  const requireApiKey = NODE_ENV === 'production';
  if (requireApiKey && !BACKEND_API_KEY) {
    return NextResponse.json(
      { detail: 'Backend API key not configured' },
      { status: 503 }
    );
  }

  try {
    const body = await request.json();
    const playerNation = (body?.playerNation || 'ESP') as string;
    const forceReset = Boolean(body?.forceReset);

    const params = new URLSearchParams({
      player_nation: playerNation,
      force_reset: String(forceReset),
    });

    const backendResponse = await fetch(
      `${BACKEND_BASE_URL}/api/game/initialize?${params.toString()}`,
      {
        method: 'POST',
        headers: BACKEND_API_KEY ? { 'x-api-key': BACKEND_API_KEY } : {},
        cache: 'no-store',
      }
    );

    const data = await backendResponse.json();

    return NextResponse.json(data, { status: backendResponse.status });
  } catch {
    return NextResponse.json(
      { detail: 'Error forwarding initialize request' },
      { status: 500 }
    );
  }
}

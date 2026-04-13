import type { NextConfig } from "next";

const isVercel = process.env.VERCEL === "1";

const nextConfig: NextConfig = {
  // Habilitar standalone solo fuera de Vercel (docker/self-hosted)
  ...(isVercel ? {} : { output: 'standalone' }),
  
  // Configuración de API externa (backend FastAPI)
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL 
          ? `${process.env.NEXT_PUBLIC_API_URL}/:path*` 
          : 'http://localhost:8000/:path*',
      },
    ];
  },
};

export default nextConfig;

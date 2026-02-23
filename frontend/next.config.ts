import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Habilitar standalone output para Docker (producción)
  output: 'standalone',
  
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

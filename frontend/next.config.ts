import type { NextConfig } from "next";

const isVercel = process.env.VERCEL === "1";

const nextConfig: NextConfig = {
  // Habilitar standalone solo fuera de Vercel (docker/self-hosted)
  ...(isVercel ? {} : { output: 'standalone' }),
};

export default nextConfig;

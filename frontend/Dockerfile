# Frontend Dockerfile - Next.js 15 + React 19
# Multi-stage build para optimizar tamaño final

# ===========================
# STAGE 1: Dependencies
# ===========================
FROM node:20-alpine AS deps

WORKDIR /app

# Copiar package files
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm ci --legacy-peer-deps

# ===========================
# STAGE 2: Builder
# ===========================
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar dependencias instaladas
COPY --from=deps /app/node_modules ./node_modules

# Copiar código fuente
COPY . .

# Variables de entorno para build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build de Next.js
RUN npm run build

# ===========================
# STAGE 3: Runner (Producción)
# ===========================
FROM node:20-alpine AS runner

WORKDIR /app

# Variables de entorno
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Crear usuario no-root para seguridad
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copiar archivos necesarios para producción
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Cambiar al usuario no-root
USER nextjs

# Exponer puerto
EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Comando para ejecutar
CMD ["node", "server.js"]

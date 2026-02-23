# 🌍 Nation-Mind AI - Simulador Geopolítico con Inteligencia Artificial

> **Un juego de estrategia donde gobiernas una nación en un mundo donde las otras 7 naciones son controladas por agentes de IA autónomos con memoria, personalidad y objetivos propios.**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6A00?style=for-the-badge)](https://www.trychroma.com/)

---

## 📖 Tabla de Contenidos

1. [¿Qué es Nation-Mind AI?](#-qué-es-nation-mind-ai)
2. [🚀 Inicio Rápido](#-inicio-rápido)
3. [🧠 Tecnologías IA Explicadas con Manzanas](#-tecnologías-ia-explicadas-con-manzanas)
4. [🏗️ Arquitectura del Proyecto](#️-arquitectura-del-proyecto)
5. [🎮 Cómo Funciona el Juego](#-cómo-funciona-el-juego)
6. [💻 Stack Tecnológico Completo](#-stack-tecnológico-completo)
7. [📁 Estructura de Carpetas](#-estructura-de-carpetas)
8. [🔧 Configuración y Deploy](#-configuración-y-deploy)

---

## 🎯 ¿Qué es Nation-Mind AI?

Imagina un juego de Risk o Civilization, pero donde **los oponentes NO son tontos**. Cada nación rival:

- 🧠 **Piensa por sí misma** usando LLMs (Modelos de Lenguaje tipo ChatGPT)
- 📚 **Recuerda todo lo que ha pasado** (sistema de memoria vectorial)
- 🎭 **Tiene personalidad única** (agresiva, diplomática, económica...)
- 🎯 **Persigue objetivos a largo plazo** (conquistar el mundo, acumular oro, formar alianzas)
- 📰 **Genera narrativas believables** (cada decisión viene con una explicación)

**No es un juego donde la IA sigue patrones predecibles**. Es un simulador donde las naciones toman decisiones autónomas basadas en el contexto histórico de la partida.

### ✨ Características Principales

✅ **8 Naciones Jugables**: España, Francia, Alemania, Rusia, China, Japón, India, Estados Unidos  
✅ **Agentes Autónomos**: Cada nación IA es un agente independiente con memoria  
✅ **Sistema de Turnos**: Procesas tu decisión → Las 7 IA deciden → Se resuelven conflictos  
✅ **Diplomacia Real**: Alianzas, guerras, propuestas de paz con razonamiento  
✅ **Batallas Automáticas**: Sistema probabilístico con aliados, terreno y poderes  
✅ **Economía Dinámica**: Generación automática de oro cada turno  
✅ **5 Formas de Ganar**: Dominación, Eliminación, Económica, Militar, Supervivencia  
✅ **Narrativa Emergente**: Cada partida es única y genera su propia historia  

---

## 🚀 Inicio Rápido

### 🐳 **Método Recomendado: Docker (Todo en uno)**

Levanta **frontend + backend + PostgreSQL + ChromaDB** con un solo comando:

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu GROQ_API_KEY (gratis en https://console.groq.com/keys)

# 2. Levantar todo
docker-compose up --build

# 3. Abre tu navegador
# http://localhost:3000 → Frontend (juego)
# http://localhost:8000/docs → Backend API docs
```

✅ **Eso es todo.** Todo funciona automáticamente.

📚 **Documentación completa de Docker:** [DOCKER.md](./DOCKER.md)

---

### 🔧 Alternativa: Desarrollo Local (Sin Docker)

Si prefieres correr todo manualmente:

#### 1️⃣ Base de Datos (PostgreSQL + ChromaDB)

```bash
# Solo PostgreSQL y ChromaDB con Docker
docker-compose up postgres chromadb -d
```

#### 2️⃣ Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Asegúrate de tener: USE_CHROMADB_HTTP=False para local

# Ejecutar
uvicorn main:app --reload
```

✅ Backend corriendo en: http://localhost:8000

#### 3️⃣ Frontend (Next.js)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

✅ Frontend corriendo en: http://localhost:3000

---

### 📋 Requisitos Previos

| Software | Versión Mínima | Docker | Local |
|----------|----------------|--------|-------|
| **Docker** | ≥ 20.0 | ✅ Requerido | ❌ Opcional |
| **Docker Compose** | ≥ 2.0 | ✅ Requerido | ❌ Opcional |
| **Python** | ≥ 3.11 | ❌ No | ✅ Requerido |
| **Node.js** | ≥ 18 | ❌ No | ✅ Requerido |
| **PostgreSQL** | ≥ 15 | ❌ No | ✅ Requerido |

**API Keys:**
- **Groq API Key** (gratis): https://console.groq.com/keys
  - Tier gratuito: 14,400 requests/día, 100k tokens/día
  - Suficiente para jugar ~30 turnos al día

---

**3. Servicios externos:**
- Instala PostgreSQL (puerto 5432)
- Instala ChromaDB (puerto 8001)

**4. Variables de entorno:**
```bash
# backend/.env
GROQ_API_KEY=tu_clave_aqui  # Gratis en https://console.groq.com
DATABASE_URL=postgresql://user:pass@localhost:5432/geopol
CHROMADB_HOST=localhost
CHROMADB_PORT=8001
```

---

## 🧠 Tecnologías IA Explicadas con Manzanas

### 🤖 ¿Qué es un LLM? (Large Language Model)

**Con manzanas 🍎:**  
Imagina que tienes un amigo que ha leído TODOS los libros del mundo. Si le preguntas "¿Qué haría un rey agresivo si su vecino tiene mucho oro?", te dará una respuesta razonada basada en todo lo que ha leído sobre historia, estrategia y psicología.

**En Nation-Mind AI:**  
El LLM es **LLaMA 3** (creado por Meta, gratis via Groq). Cada vez que una nación IA debe decidir qué hacer, le preguntamos al LLM:

```
Prompt enviado a LLaMA 3:
"Eres España, una nación con personalidad AGRESIVA.
Tu objetivo es conquistar Europa.
Francia tiene 15 territorios y 5000 tropas.
Tú tienes 10 territorios y 4000 tropas.
¿Qué haces?"

Respuesta de LLaMA 3:
"Declaro guerra a Francia. Aunque tiene más tropas,
su posición me bloquea la expansión y mi personalidad
agresiva me impulsa a actuar ahora antes de que se fortalezca."
```

**Por qué usamos Groq:**  
Groq es una empresa que ejecuta LLaMA 3 **SUPER RÁPIDO y GRATIS** (con límites generosos). Normalmente ejecutar un LLM en tu PC sería lento. Groq tiene chips especiales que lo hacen en milisegundos.

---

### 🎭 ¿Qué son los Agentes de IA?

**Con manzanas 🍎:**  
Un agente es como un robot mayordomo al que le das un objetivo ("limpia la casa") y él decide qué herramientas usar (escoba, aspiradora, trapo). No le dices paso a paso qué hacer, él piensa y actúa solo.

**En Nation-Mind AI:**  
Cada nación es un **agente autónomo**:
- 🎯 **Objetivo**: España quiere conquistar Europa
- 🧰 **Herramientas**: Puede declarar guerra, pedir alianzas, invertir en economía
- 🧠 **Decisión**: El LLM decide qué herramienta usar según el contexto
- 📚 **Memoria**: Recuerda todo lo que ha pasado en la partida

**Ejemplo de ciclo de un agente:**
```
1. España despierta en su turno
2. Consulta su memoria: "¿Qué ha pasado hasta ahora?"
   → Francia me atacó hace 3 turnos
   → Alemania es mi aliado
   → Tengo poco oro pero muchas tropas
3. Piensa con LLaMA 3: "¿Qué hago?"
4. Decide: "Voy a atacar a Francia para vengarme"
5. Ejecuta la acción automáticamente
6. Guarda en memoria: "Ataqué a Francia en turno 12"
```

---

### 🤝 ¿Qué es un Sistema Multiagente?

**Con manzanas 🍎:**  
Imagina 8 chefs en una cocina. Cada uno tiene su receta y objetivos, pero todos comparten el mismo horno y nevera. Tienen que coordinarse, competir por recursos y a veces colaborar.

**En Nation-Mind AI:**  
Las 8 naciones son **agentes independientes** que:
- 🔄 **Actúan en paralelo**: Todas deciden al mismo tiempo cada turno
- 🌍 **Comparten el mundo**: Compiten por territorios, oro y alianzas
- 🤝 **Interactúan entre sí**: Pueden formar alianzas o declararse la guerra
- 🧠 **Cada una piensa diferente**: España es agresiva, Francia es diplomática

**El desafío técnico:**  
No podemos dejar que un agente decida primero y otro después, porque el segundo tendría ventaja. Todos deben decidir "a ciegas" con la información del principio del turno.

---

### 🕸️ ¿Qué es LangGraph?

**Con manzanas 🍎:**  
Imagina que tienes una receta de cocina complicada con decisiones: "Si la masa está blanda → amasar más, si está dura → añadir agua". LangGraph es como un diagrama de flujo que controla qué hacer en cada situación.

**En Nation-Mind AI:**  
LangGraph orquesta el flujo de decisiones de los agentes:

```
┌─────────────┐
│ TURNO INICIA│
└──────┬──────┘
       │
   ┌───▼────────────────────┐
   │ Para cada nación IA    │
   ├────────────────────────┤
   │ 1. Consultar memoria   │ ← RAG
   │ 2. Preguntar a LLM     │ ← Groq/LLaMA
   │ 3. Ejecutar acción     │ ← Game Service
   │ 4. Guardar en memoria  │ ← ChromaDB
   └───┬────────────────────┘
       │
   ┌───▼────────────┐
   │ Resolver       │
   │ Batallas       │
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │ Verificar      │
   │ Victoria       │
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │ TURNO TERMINA  │
   └────────────────┘
```

**Por qué NO usamos solo código normal:**  
LangGraph permite:
- ✅ **Reintentar** si un agente falla (el LLM puede dar respuestas inválidas)
- ✅ **Ejecutar en paralelo** las decisiones de 7 agentes
- ✅ **Detectar bucles infinitos** (si un agente entra en conflicto consigo mismo)
- ✅ **Debuggar visualmente** el flujo de decisiones

---

### 📚 ¿Qué es RAG? (Retrieval-Augmented Generation)

**Con manzanas 🍎:**  
Imagina que te preguntan "¿Quién ganó el Mundial 2022?". Si no lo sabes, puedes:
1. **Generación pura**: Adivinar (puede estar mal)
2. **RAG**: Buscar en Google primero, leer la respuesta, y luego contestar con certeza

**En Nation-Mind AI:**  
El RAG da **memoria a largo plazo** a los agentes:

**Sin RAG (problema):**
```
Turno 50: España decide qué hacer
LLaMA 3 solo recuerda los últimos 4000 tokens (~3 páginas)
No sabe que Francia la atacó en turno 5
Toma decisiones sin contexto histórico
```

**Con RAG (solución):**
```
Turno 50: España necesita decidir
1. Sistema busca en ChromaDB: "¿Qué ha hecho Francia?"
2. Recupera: "Francia atacó a España en turno 5"
            "Francia formó alianza con Alemania en turno 20"
3. Incluye esto en el prompt a LLaMA 3
4. España decide con contexto completo: "Vengarme de Francia"
```

**¿Cómo funciona técnicamente?**
```
Evento: "España atacó a Francia en turno 5"
    ↓
[sentence-transformers] convierte texto a vector numérico
    ↓
Vector: [0.15, -0.84, 0.23, 0.67, ...] (384 números)
    ↓
[ChromaDB] guarda este vector con el texto original
    
─────────────────────────────────────────
    
Turno 50: España consulta "¿Qué sé de Francia?"
    ↓
[sentence-transformers] convierte pregunta a vector
    ↓
[ChromaDB] busca vectores similares (similarity search)
    ↓
Recupera eventos relevantes: "España atacó a Francia en turno 5"
```

**Por qué vectores:**  
Los vectores capturan el **significado semántico**:
- "España atacó Francia" tiene vector similar a "Guerra España-Francia"
- Aunque las palabras sean diferentes, el significado es parecido
- Permite buscar por concepto, no solo por palabras exactas

---

### 🗄️ ¿Qué es ChromaDB?

**Con manzanas 🍎:**  
ChromaDB es como una biblioteca donde los libros NO están ordenados alfabéticamente, sino por **tema**. Si buscas "gatos", te trae libros sobre "felinos", "mascotas" y "animales" aunque no digan exactamente "gato".

**En Nation-Mind AI:**  
ChromaDB almacena todos los eventos del juego como **vectores numéricos**:

```
Tabla de eventos en ChromaDB:
┌──────────────────────────────┬──────────────────┬──────────┐
│ Texto del evento             │ Vector (384D)    │ Metadata │
├──────────────────────────────┼──────────────────┼──────────┤
│ "España atacó Francia T5"    │ [0.15, -0.84...] │ turn=5   │
│ "Francia pidió paz T8"       │ [0.12, -0.80...] │ turn=8   │
│ "Alemania invirtió oro T10"  │ [-0.50, 0.92...] │ turn=10  │
└──────────────────────────────┴──────────────────┴──────────┘
```

**Ventajas sobre base de datos normal:**
- ❌ SQL: SELECT * WHERE text LIKE '%guerra%' (solo palabras exactas)
- ✅ ChromaDB: Busca eventos "similares a guerra" → encuentra "conflicto", "batalla", "ataque"

**Por qué NO usamos solo PostgreSQL:**  
PostgreSQL guarda datos estructurados (tablas, filas). ChromaDB guarda **significados** (vectores). Son complementarios:
- **PostgreSQL**: Estado actual (oro, tropas, territorios) → consultas exactas
- **ChromaDB**: Historia narrativa (eventos, decisiones) → búsqueda semántica

---

### 🐘 PostgreSQL en el Proyecto

**Con manzanas 🍎:**  
PostgreSQL es como una hoja de Excel gigante donde guardas los números importantes: cuánto oro tiene cada nación, cuántas tropas, quién es aliado de quién.

**En Nation-Mind AI:**  
PostgreSQL guarda el **estado actual del juego**:

```
Tabla: nations
┌────┬─────────┬──────┬────────┬──────────────┬────────────┐
│ id │ name    │ gold │ troops │ territories  │ is_active  │
├────┼─────────┼──────┼────────┼──────────────┼────────────┤
│ 1  │ España  │ 3500 │ 800    │ 12           │ true       │
│ 2  │ Francia │ 5000 │ 1200   │ 15           │ true       │
│ 3  │ Italia  │ 0    │ 0      │ 0            │ false      │ ← Eliminada
└────┴─────────┴──────┴────────┴──────────────┴────────────┘

Tabla: relations
┌────┬────────────┬────────────┬─────────┬───────────────────┐
│ id │ nation_a_id│ nation_b_id│ status  │ relationship_score│
├────┼────────────┼────────────┼─────────┼───────────────────┤
│ 1  │ 1 (España) │ 2 (Francia)│ war     │ -80               │
│ 2  │ 1 (España) │ 4 (Alemania)│ allied  │ 90                │
└────┴────────────┴────────────┴─────────┴───────────────────┘
```

**Por qué PostgreSQL y no SQLite:**
- ✅ **Concurrencia**: 7 agentes escriben al mismo tiempo
- ✅ **Integridad**: Transacciones ACID (si falla algo, se deshace todo)
- ✅ **Escalabilidad**: Soporta millones de turnos sin problemas
- ✅ **Deploy**: Fácil de hostear en servicios gratuitos (Railway, Render)

---

### ⚡ ¿Qué es Groq y por qué LLaMA?

**Con manzanas 🍎:**  
Groq es como tener un Ferrari que corre súper rápido. LLaMA 3 es el motor del Ferrari.

**Groq:**
- 🏢 Empresa que hace chips especializados en IA
- ⚡ **10-100x más rápido** que GPT-4 en generar texto
- 💰 **Gratis** hasta 100,000 tokens/día (suficiente para 500+ turnos)
- 🆓 No requiere tarjeta de crédito para empezar

**LLaMA 3:**
- 🧠 Modelo de lenguaje creado por Meta (como ChatGPT pero open source)
- 📊 **70B parámetros** (70 mil millones de números que determinan su inteligencia)
- 🎯 Especializado en razonamiento y seguir instrucciones
- 🔓 **Open source** (puedes revisar cómo funciona)

**Alternativas que evaluamos:**
- ❌ **GPT-4**: $0.03 por 1000 tokens → caro para 7 agentes por turno
- ❌ **Claude**: Similar a GPT-4, también de pago
- ❌ **Gemini**: Gratis pero lento y límites muy bajos
- ✅ **Groq + LLaMA 3**: Gratis, rápido y suficientemente inteligente

**Velocidad comparada:**
```
Generar 500 tokens (1 decisión de agente):
- GPT-4:         ~10 segundos
- Groq/LLaMA 3:  ~1 segundo   👈 10x más rápido
```

---

## ⚛️ De React a Next.js - Guía para Desarrolladores React

### ¿Por qué Next.js si ya sabes React?

**Analogía 🍎:**  
React es como tener un coche. Next.js es como tener un coche con GPS, control crucero, y piloto automático incluidos. Sigues conduciendo (React) pero con super-poderes.

---

### Cambio 1: File-Based Routing (Rutas automáticas)

**Antes en React:**
```jsx
// App.js con react-router
import { BrowserRouter, Route } from 'react-router-dom';

<BrowserRouter>
  <Route path="/" component={Home} />
  <Route path="/game" component={Game} />
  <Route path="/game/battles" component={Battles} />
</BrowserRouter>
```

**Ahora en Next.js:**
```
src/app/
├─ page.tsx           → /
├─ game/
│  ├─ page.tsx        → /game
│  └─ battles/
│     └─ page.tsx     → /game/battles
```

¡**Creas carpeta = creas ruta!** Sin react-router, sin configuración. El nombre de la carpeta ES la URL.

**Rutas dinámicas:**
```
src/app/nations/[id]/page.tsx  → /nations/1, /nations/2, etc.
```

```tsx
// En el componente:
export default function NationDetail({ params }: { params: { id: string } }) {
  const nationId = params.id; // "1", "2", etc.
  return <div>Nación {nationId}</div>;
}
```

---

### Cambio 2: Server Components vs Client Components

**Analogía 🍎:**  
Imagina una tienda online:
- **Server Component** = Preparar paquete en almacén (servidor)
- **Client Component** = Cliente abre paquete en casa (navegador)

**En React tradicional:** TODO es Client Component (corre en navegador del usuario)
**En Next.js:** Por defecto TODO es Server Component (corre en servidor)

**Server Components (por defecto):**
```tsx
// Este componente corre en el SERVIDOR
export default function Dashboard() {
  // Puedes llamar DB directamente, sin API!
  const nations = await db.query("SELECT * FROM nations");
  
  return (
    <div>
      {nations.map(n => <NationCard key={n.id} nation={n} />)}
    </div>
  );
}
```

**Ventajas:**
- 📦 **Menos JavaScript al navegador** (más rápido)
- 🔒 **Código sensible seguro** (API keys nunca llegan al cliente)
- 🚀 **Carga inicial rápida** (HTML pre-renderizado)

**Client Components (cuando necesites interactividad):**
```tsx
'use client'; // ← Esto lo convierte en Client Component

import { useState } from 'react';

export default function TurnButton() {
  const [loading, setLoading] = useState(false);
  
  const handleClick = () => {
    setLoading(true);
    // Lógica...
  };
  
  return <button onClick={handleClick}>Procesar Turno</button>;
}
```

**Cuándo usar Client Component:**
- ✅ Necesitas **useState, useEffect, eventos (onClick, onChange)**
- ✅ Necesitas **Web APIs del navegador** (localStorage, window, navigator)
- ✅ Necesitas **librerías que usan navegador** (react-confetti, sonidos)

**Regla de oro:**  
Por defecto deja Server Component. Solo agrega `'use client'` si React te da error de "useState is not a function" o similar.

---

### Cambio 3: App Router - Estructura de carpetas

**Pages Router (viejo, NO usamos):**
```
pages/
├─ index.tsx
├─ game.tsx
└─ _app.tsx
```

**App Router (nuevo, USAMOS ESTE):**
```
app/
├─ layout.tsx      ← Layout global (Header, Footer)
├─ page.tsx        ← Página raíz "/"
├─ globals.css     ← Estilos globales
├─ game/
│  ├─ layout.tsx   ← Layout solo para /game/*
│  └─ page.tsx     ← /game
```

**Archivos especiales:**
- `layout.tsx`: Layout compartido (se mantiene al navegar)
- `page.tsx`: Contenido de la ruta
- `loading.tsx`: UI de carga automática
- `error.tsx`: UI de error automática

**Ejemplo layout compartido:**
```tsx
// app/layout.tsx (SIEMPRE se muestra)
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Header /> {/* ← Siempre visible */}
        {children} {/* ← Contenido cambia */}
        <Footer /> {/* ← Siempre visible */}
      </body>
    </html>
  );
}
```

**Layouts anidados:**
```tsx
// app/game/layout.tsx (solo para /game/*)
export default function GameLayout({ children }) {
  return (
    <div className="game-container">
      <GameSidebar />
      {children}
    </div>
  );
}
```

Cuando navegas de `/game` a `/game/battles`, el `layout.tsx` NO se re-renderiza (más rápido).

---

### Cambio 4: Cómo hacer fetching de datos

**Antes en React:**
```tsx
function Dashboard() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetch('/api/game/state')
      .then(res => res.json())
      .then(setData);
  }, []);
  
  if (!data) return <div>Cargando...</div>;
  return <div>{data.nations.map(...)}</div>;
}
```

**Ahora en Next.js (Server Component):**
```tsx
async function Dashboard() {
  // Fetch directo, sin useEffect!
  const res = await fetch('http://localhost:8000/api/game/state');
  const data = await res.json();
  
  return <div>{data.nations.map(...)}</div>;
}
```

**O con axios (Client Component):**
```tsx
'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';

function Dashboard() {
  const [gameState, setGameState] = useState(null);
  
  useEffect(() => {
    api.getGameState().then(setGameState);
  }, []);
  
  if (!gameState) return <div>Cargando...</div>;
  return <div>...</div>;
}
```

---

### Cambio 5: TypeScript por Todas Partes

**Por qué TypeScript y no JavaScript puro:**

```javascript
// JavaScript (sin tipos):
function calcularDaño(tropas) {
  return tropas * 0.25;  // ¿tropas es número o string? 🤷
}
calcularDaño("500");  // ❌ Funciona pero resultado malo: "5000.250.250.25"
```

```typescript
// TypeScript (con tipos):
function calcularDaño(tropas: number): number {
  return tropas * 0.25;
}
calcularDaño("500");  // ❌ ERROR en COMPILACIÓN antes de ejecutar
calcularDaño(500);    // ✅ OK
```

**Ventajas:**
- 🐛 **Menos bugs** (errores se detectan antes de ejecutar)
- 💡 **Autocompletado inteligente** en VS Code
- 📖 **Código auto-documentado** (los tipos explican qué hace cada función)
- 🔄 **Refactoring seguro** (cambias algo y TypeScript te dice qué se rompe)

**Ejemplo en el proyecto:**
```typescript
// types/index.ts
export type Nation = {
  id: number;
  name: string;
  gold: number;
  troops: number;
  territories: number;
  is_active: boolean;
};

// Componente:
interface NationCardProps {
  nation: Nation; // ← Autocompletado perfecto!
}

export default function NationCard({ nation }: NationCardProps) {
  return <div>{nation.gold}</div>; // ← VS Code sabe que gold es number
}
```

---

### Resumen: React → Next.js

| Característica | React (CRA) | Next.js (App Router) |
|---------------|-------------|----------------------|
| **Routing** | react-router manual | Automático (carpetas) |
| **Renderizado** | CSR (Client-Side) | SSR + CSR híbrido |
| **Fetching** | useEffect + fetch | async/await directo |
| **SEO** | Malo (JS necesario) | Excelente (HTML pre-renderizado) |
| **Performance** | Buena | Excelente (optimizado) |
| **Curva aprendizaje** | Baja | Media |
| **Deploy** | Cualquier CDN | Vercel (optimizado), otros |

**En 1 línea:** Next.js es React con superpoderes de performance, SEO y developer experience.

---

## 🏗️ Arquitectura del Proyecto

### Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────┐
│                        JUGADOR                               │
│                    (Tu navegador)                            │
└────────────────────┬───────────────────────────────────────┘
                     │ HTTP Requests
                     │ (POST /api/game/process-turn)
┌────────────────────▼───────────────────────────────────────┐
│                      FRONTEND                               │
│                    Next.js 15 + React 19                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Components: Dashboard, NationCard, EventFeed, etc    │  │
│  │ State Management: React Hooks                         │  │
│  │ Styling: Tailwind CSS 4 + Framer Motion             │  │
│  │ API Client: Axios (typesafe con TypeScript)          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────────┐
│                      BACKEND                                │
│                      FastAPI (Python)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Controllers: Endpoints REST (MVC Pattern)            │  │
│  │ ├─ game_controller.py                                │  │
│  │ ├─ agent_controller.py                               │  │
│  │ ├─ battle_controller.py                              │  │
│  │ └─ memory_controller.py                              │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                  │                                          │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ Services: Lógica de Negocio                          │  │
│  │ ├─ agent_service.py      ← Sistema multiagente      │  │
│  │ ├─ battle_service.py     ← Combate probabilístico   │  │
│  │ ├─ economy_service.py    ← Generación de oro        │  │
│  │ ├─ victory_service.py    ← Condiciones de victoria  │  │
│  │ └─ rag_service.py        ← Memoria vectorial        │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                  │                                          │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ Agent Tools: Acciones disponibles para agentes       │  │
│  │ ├─ declare_war(target_id)                            │  │
│  │ ├─ propose_alliance(target_id)                       │  │
│  │ ├─ invest_in_economy()                               │  │
│  │ ├─ recruit_troops(amount)                            │  │
│  │ └─ ... 5 herramientas más                            │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────┬──────────────────┬─────────────────────────────┘
            │                  │
┌───────────▼──────────┐  ┌───▼──────────────────────────────┐
│    PostgreSQL         │  │         ChromaDB                 │
│  (Base de Datos)      │  │    (Memoria Vectorial)          │
│                       │  │                                  │
│ • nations             │  │ • Embeddings de eventos         │
│ • relations           │  │ • Búsqueda semántica            │
│ • battles             │  │ • Historial de decisiones       │
│ • events              │  │ • Contexto para agentes         │
│ • turns               │  │                                  │
└───────────────────────┘  └──────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────┐
│                     GROQ API                                  │
│                   (Servicio Externo)                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ LLaMA 3 - 70B                                          │  │
│  │ Input: Prompt con personalidad + memoria + estado     │  │
│  │ Output: Decisión razonada del agente                  │  │
│  │ Velocidad: ~500 tokens/segundo                        │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### Flujo de un Turno Completo

```
┌──────────────────────────────────────────────────────────────┐
│ 1. JUGADOR PRESIONA "⚡ PROCESAR TURNO IA"                   │
└────────────┬─────────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│ 2. FRONTEND → Backend: POST /api/agent/process-turn        │
└────────────┬───────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────┐
│ 3. BACKEND INICIA PROCESO DE 5 FASES                       │
└────────────┬───────────────────────────────────────────────┘
             │
             ├─── FASE 1: ECONOMÍA ────────────────────────┐
             │                                              │
             │    Para cada nación activa:                 │
             │    ├─ Calcular ingresos:                    │
             │    │  Base 100 + Territorios*50 +           │
             │    │  (Poder Económico/100)*300              │
             │    ├─ Calcular gastos:                       │
             │    │  (Tropas/10) + 20                       │
             │    └─ Actualizar oro en PostgreSQL           │
             │                                              │
             ├─── FASE 2: AGENTES IA ──────────────────────┤
             │                                              │
             │    Para cada nación IA (7 naciones):        │
             │                                              │
             │    ┌──────────────────────────────┐          │
             │    │ 1. Consultar RAG             │          │
             │    │    ├─ Query ChromaDB:        │          │
             │    │    │  "¿Qué he hecho?"       │          │
             │    │    │  "¿Qué ha pasado?"      │          │
             │    │    └─ Recupera top 5 eventos │          │
             │    └──────────┬───────────────────┘          │
             │               │                              │
             │    ┌──────────▼───────────────────┐          │
             │    │ 2. Preparar Prompt          │          │
             │    │    Personalidad: "Agresiva"  │          │
             │    │    Objetivo: "Conquista"     │          │
             │    │    Memoria: [eventos RAG]    │          │
             │    │    Estado actual: {stats}    │          │
             │    │    Herramientas: [5 tools]   │          │
             │    └──────────┬───────────────────┘          │
             │               │                              │
             │    ┌──────────▼───────────────────┐          │
             │    │ 3. LLM Decision (Groq)      │          │
             │    │    Groq API → LLaMA 3       │          │
             │    │    Tiempo: ~1 segundo       │          │
             │    │    Output: JSON con acción  │          │
             │    └──────────┬───────────────────┘          │
             │               │                              │
             │    ┌──────────▼───────────────────┐          │
             │    │ 4. Ejecutar Acción          │          │
             │    │    declare_war(target=2)    │          │
             │    │    invest_in_economy()      │          │
             │    │    recruit_troops(400)      │          │
             │    └──────────┬───────────────────┘          │
             │               │                              │
             │    ┌──────────▼───────────────────┐          │
             │    │ 5. Guardar en Memoria       │          │
             │    │    Evento → Embedding       │          │
             │    │    Embedding → ChromaDB     │          │
             │    └──────────────────────────────┘          │
             │                                              │
             ├─── FASE 3: BATALLAS ────────────────────────┤
             │                                              │
             │    Para cada guerra activa:                 │
             │    ├─ Calcular probabilidad victoria        │
             │    │  (tropas, aliados, poderes)            │
             │    ├─ Simular batalla (random roll)         │
             │    ├─ Calcular bajas (10-30%)               │
             │    ├─ Transferir territorios (1-3)          │
             │    ├─ Saquear oro (~25%)                    │
             │    └─ Si territories ≤ 0: eliminar nación   │
             │                                              │
             ├─── FASE 4: VICTORIA ────────────────────────┤
             │                                              │
             │    Verificar 5 condiciones:                 │
             │    ├─ Dominación: >50% territorios          │
             │    ├─ Eliminación: última nación activa     │
             │    ├─ Económica: 10,000 oro + 90% poder     │
             │    ├─ Militar: 2,000 tropas + 90% poder     │
             │    └─ Supervivencia: 100 turnos (puntos)    │
             │                                              │
             │    Si victoria detectada:                   │
             │    └─ Marcar juego como terminado           │
             │                                              │
             └─── FASE 5: SIGUIENTE TURNO ─────────────────┤
                                                            │
                  ├─ Incrementar turn_number               │
                  ├─ Generar summary del turno             │
                  └─ Guardar estado completo en PostgreSQL │
                                                            │
┌───────────────────────────────────────────────────────────┐│
│ 4. BACKEND → Frontend: JSON con nuevo estado             ││
└────────────┬──────────────────────────────────────────────┘│
             │                                               │
             ▼                                               │
┌────────────────────────────────────────────────────────────▼┐
│ 5. FRONTEND ACTUALIZA UI                                    │
│    ├─ Dashboard: nuevos stats de naciones                   │
│    ├─ EventFeed: eventos del turno                          │
│    ├─ Notificaciones Toast: cambios importantes             │
│    └─ VictoryPanel: progreso hacia victoria                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎮 Cómo Funciona el Juego

### 1. Inicio de Partida

1. **Selección de Nación**: Eliges una de 8 naciones (España recomendada)
2. **Inicialización**: Backend crea estado inicial en PostgreSQL
   - Cada nación empieza con: 3000 oro, 500 tropas, 7-9 territorios
   - Relaciones iniciales: todas neutral (score = 0)
3. **Primer Turno**: El jugador puede empezar a actuar

### 2. Acciones del Jugador

**Económicas:**
- 💼 Invertir en Economía (800 oro) → +20-40% poder económico
- 🪖 Reclutar Tropas (800 oro) → +400 tropas

**Diplomáticas:**
- 🤝 Proponer Alianza → Si aceptan, +50 relación
- ⚔️ Declarar Guerra → Status pasa a "war"
- 🕊️ Pedir Paz → Status vuelve a "neutral"

**Militares:**
- 🎯 Simular Batalla → Ver probabilidades antes de atacar
- ⚔️ Las guerras se resuelven automáticamente cada turno

### 3. Turno de las IA

Cuando presionas "⚡ Procesar Turno IA":

**Cada nación IA:**
1. Consulta su memoria en ChromaDB
2. Analiza su situación (oro, tropas, enemigos, aliados)
3. Pregunta a LLaMA 3 qué hacer
4. Ejecuta la acción automáticamente
5. La acción se guarda en memoria

**Personalidades implementadas:**
- 🔥 **Agresiva** (Alemania): Prioriza conquista militar
- 🤝 **Diplomática** (Francia): Busca alianzas y evita guerras
- 💰 **Económica** (China): Acumula oro e invierte
- ⚖️ **Balanceada** (España): Mix de todo
- 🛡️ **Defensiva** (Rusia): Protege sus territorios

### 4. Resolución de Batallas

**Sistema probabilístico:**
```javascript
// Ejemplo de cálculo
España (atacante):
  - 800 tropas base
  - +200 tropas de aliados (Alemania ayuda)
  - +10% bonus por Poder Militar alto
  - Total efectivo: 1100 tropas

Francia (defensor):
  - 1000 tropas base
  - +0 aliados (nadie la ayuda)
  - +5% bonus por Poder Militar medio
  - Total efectivo: 1050 tropas

Probabilidad victoria España: 51%
Probabilidad victoria Francia: 49%

Roll dado: 0.45 → España gana
Bajas España: 160 tropas (20%)
Bajas Francia: 250 tropas (25%)
Territorios capturados: 2
Oro saqueado: 1250 (25% del oro de Francia)
```

**Consecuencias:**
- Perdedor sin territorios → Eliminado del juego permanentemente
- Ganador saquea oro y captura territorios
- Relación automaticamente se degrada a -80

### 5. Economía del Juego

**Ingresos por turno:**
```
Oro generado = 100 (base)
             + Territorios × 50
             + (Poder Económico / 100) × 300
             ± 10% variabilidad aleatoria

Ejemplo España (12 territorios, 80% poder eco):
Ingresos = 100 + 600 + 240 ± 94 = ~940 oro/turno
```

**Gastos por turno:**
```
Mantenimiento = (Tropas / 10) + 20

Ejemplo con 500 tropas:
Gastos = 50 + 20 = 70 oro/turno
```

**Balance neto:**
```
Neto = Ingresos - Gastos
España: 940 - 70 = +870 oro/turno ¡Muy rentable!
```

### 6. Condiciones de Victoria

#### 👑 Dominación (más común)
- Controlar >50% de los territorios del mundo
- Ejemplo: 29+ de 56 territorios totales

#### ⚔️ Eliminación (más épica)
- Ser la única nación que queda activa
- Todas las demás han sido destruidas

#### 💰 Económica (para estrategas)
- Acumular 10,000 oro
- Tener 90%+ de poder económico mundial

#### 🪖 Militar (para agresivos)
- Tener 2,000+ tropas
- Tener 90%+ de poder militar mundial

#### 🛡️ Supervivencia (a los 100 turnos)
- Llegar al turno 100 sin que nadie gane
- Ganador: nación con más puntos totales
- Puntos = oro/10 + tropas + territorios×200 + poderes×25

---

## 💻 Stack Tecnológico Completo

### Backend (Python)

#### FastAPI
**¿Qué es?** Framework web moderno para crear APIs REST.

**Ventajas:**
- ⚡ Rápido como Node.js
- 📝 Generación automática de documentación (Swagger)
- ✅ Validación automática con Pydantic
- 🔄 Hot reload en desarrollo

**Alternativas evaluadas:**
- ❌ Flask: Más simple pero menos features
- ❌ Django: Muy pesado para una API
- ✅ FastAPI: Moderno, rápido, con tipado

#### LangGraph
**¿Qué es?** Framework para crear workflows de agentes IA.

**Ventajas:**
- 🕸️ Define flujos complejos con grafos
- 🔄 Manejo automático de reintentos
- 🎭 Orquestación de múltiples agentes
- 🐛 Herramientas de debugging

**Código ejemplo:**
```python
from langgraph.graph import StateGraph

# Define estados del workflow
class AgentState(TypedDict):
    nation_id: int
    memory: List[str]
    decision: str

# Crea grafo
workflow = StateGraph(AgentState)

# Define nodos
workflow.add_node("consultar_memoria", consultar_rag)
workflow.add_node("tomar_decision", llamar_llm)
workflow.add_node("ejecutar_accion", ejecutar)

# Define flujo
workflow.add_edge("consultar_memoria", "tomar_decision")
workflow.add_edge("tomar_decision", "ejecutar_accion")

# Compila y ejecuta
app = workflow.compile()
result = app.invoke({"nation_id": 1})
```

#### SQLAlchemy
**¿Qué es?** ORM (Object-Relational Mapper) para Python.

**Con manzanas:** En vez de escribir SQL manual:
```sql
SELECT * FROM nations WHERE gold > 5000;
```

Escribes código Python más legible:
```python
nations = db.query(Nation).filter(Nation.gold > 5000).all()
```

**Ventajas:**
- 🛡️ Previene inyecciones SQL
- 🔄 Migraciones automáticas
- 💻 Código más mantenible

#### Pydantic
**¿Qué es?** Librería de validación de datos.

**Ejemplo:**
```python
class NationCreate(BaseModel):
    name: str  # Obligatorio, debe ser string
    gold: int = 3000  # Opcional, default 3000
    
    @validator('name')
    def name_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Nombre muy corto')
        return v

# Si envías datos inválidos → error automático
nation = NationCreate(name="Es", gold="abc")  # ❌ Error
```

### Frontend (TypeScript)

#### Tailwind CSS 4
**¿Qué es?** Framework CSS con clases utilitarias.

**Comparación:**

```css
/* CSS tradicional: */
.card {
  background: linear-gradient(to right, #9333ea, #ec4899);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

/* Tailwind: */
<div className="bg-gradient-to-r from-purple-600 to-pink-600 
                rounded-xl p-6 shadow-2xl">
```

**Ventajas:**
- ⚡ No salir del HTML para estilar
- 🎨 Diseño consistente (espaciados, colores predefinidos)
- 📦 Bundle final más pequeño (solo CSS usado)

### Infraestructura

#### Docker & Docker Compose
**¿Qué es Docker?** Empaqueta tu aplicación con TODO lo que necesita.

**Con manzanas:**  
Imagina que tu código es una receta de cocina. Docker es como empaquetar:
- La receta
- Los ingredientes
- La olla
- La estufa

Y enviarla en una caja. Quien la abra puede cocinar EXACTAMENTE lo mismo que tú.

**docker-compose.yml:**
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/geopol
    depends_on:
      - postgres
      - chromadb
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
  
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
```

Un solo comando: `docker-compose up` → todo funciona.

---

## 📁 Estructura de Carpetas

```
Nation-Mind-AI/
├── backend/                          # Backend FastAPI (Python)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Punto de entrada, rutas principales
│   │   ├── config/
│   │   │   └── settings.py           # Variables de entorno (Groq API Key, DB URLs)
│   │   ├── controllers/              # 🎮 Capa de Presentación (MVC)
│   │   │   ├── game_controller.py    # GET /api/game/state, POST /api/game/process-turn
│   │   │   ├── agent_controller.py   # POST /api/agent/process-turn
│   │   │   ├── battle_controller.py  # GET /api/battles, POST /api/battles/simulate
│   │   │   └── memory_controller.py  # GET /api/memory/query
│   │   ├── services/                 # 🧠 Capa de Lógica de Negocio (MVC)
│   │   │   ├── game_service.py       # Lógica general del juego
│   │   │   ├── agent_service.py      # 🤖 Sistema multiagente con LangGraph
│   │   │   ├── agent_tools.py        # 🔧 5 herramientas para agentes (declare_war, etc)
│   │   │   ├── battle_service.py     # Simulación de batallas
│   │   │   ├── economy_service.py    # Generación de ingresos/gastos
│   │   │   ├── victory_service.py    # 5 condiciones de victoria
│   │   │   ├── rag_service.py        # 📚 RAG con ChromaDB
│   │   │   ├── nation_service.py     # CRUD de naciones
│   │   │   ├── relation_service.py   # Diplomacia entre naciones
│   │   │   ├── event_service.py      # Timeline de eventos
│   │   │   └── turn_service.py       # Manejo de turnos
│   │   ├── models/                   # 🗄️ Capa de Datos (MVC)
│   │   │   ├── nation.py             # SQLAlchemy: Tabla nations
│   │   │   ├── relation.py           # SQLAlchemy: Tabla relations
│   │   │   ├── battle.py             # SQLAlchemy: Tabla battles
│   │   │   ├── event.py              # SQLAlchemy: Tabla events
│   │   │   └── turn.py               # SQLAlchemy: Tabla turns
│   │   └── schemas/                  # ✅ Validación Pydantic
│   │       ├── nation_schema.py      # NationCreate, NationResponse
│   │       ├── game_schema.py        # GameStateResponse, VictoryProgress
│   │       └── battle_schema.py      # BattleSimulation, BattleResult
│   ├── requirements.txt              # Dependencias Python
│   ├── .env                          # Variables secretas (NO subir a Git)
│   └── reset_game.py                 # Script para reiniciar partida
│
├── frontend/                         # Frontend Next.js (TypeScript)
│   ├── src/
│   │   ├── app/                      # 🗂️ App Router (Next.js 15)
│   │   │   ├── layout.tsx            # Layout global (Header + Footer)
│   │   │   ├── page.tsx              # Home: Selección de nación
│   │   │   ├── globals.css           # Estilos globales + animaciones
│   │   │   ├── game/
│   │   │   │   ├── page.tsx          # Dashboard principal con tabs
│   │   │   │   ├── battles/page.tsx  # Historial de batallas
│   │   │   │   ├── diplomacy/page.tsx# Panel diplomático
│   │   │   │   └── nations/[id]/page.tsx # Detalle de nación (ruta dinámica)
│   │   │   └── reset/page.tsx        # Página para reiniciar juego
│   │   ├── components/               # 🧩 Componentes React reutilizables
│   │   │   ├── Header.tsx            # Navegación superior
│   │   │   ├── Footer.tsx            # Pie de página
│   │   │   ├── NationCard.tsx        # Tarjeta de nación (oro, tropas, etc)
│   │   │   ├── EventFeed.tsx         # Timeline de eventos
│   │   │   ├── TurnButton.tsx        # Botón "Procesar Turno IA" mejorado
│   │   │   ├── PlayerActions.tsx     # Panel de acciones del jugador
│   │   │   ├── VictoryPanel.tsx      # 📊 Progreso hacia victoria (5 barras)
│   │   │   ├── Leaderboard.tsx       # 🏅 Ranking global de naciones
│   │   │   ├── ToastNotification.tsx # 🔔 Sistema de notificaciones toast
│   │   │   └── Confetti.tsx          # 🎊 Efecto celebración victoria
│   │   ├── lib/
│   │   │   ├── api.ts                # Cliente HTTP (Axios) para backend
│   │   │   └── sounds.ts             # 🔊 Sonidos de notificación (Web Audio API)
│   │   └── types/
│   │       └── index.ts              # 📝 Tipos TypeScript (Nation, Battle, etc)
│   ├── package.json                  # Dependencias Node.js
│   ├── .env.local                    # Variables de entorno frontend
│   ├── next.config.js                # Configuración Next.js
│   ├── tailwind.config.js            # Configuración Tailwind CSS
│   └── tsconfig.json                 # Configuración TypeScript
│
├── docker-compose.yml                # 🐳 Orquestación de servicios
├── .gitignore                        # Archivos ignorados por Git
└── README.md                         # 📖 Este archivo
```

### Archivos Clave Explicados

#### `backend/app/main.py`
Punto de entrada del backend. Define:
- Configuración CORS (permite que frontend acceda)
- Importación de routers (controllers)
- Inicialización de FastAPI

#### `backend/app/services/agent_service.py`
**Archivo más importante del proyecto**. Implementa:
- `process_ai_turn()`: Método principal que ejecuta los 5 fases del turno
- Sistema multiagente con LangGraph
- Integración con Groq/LLaMA 3
- Llamadas a RAG para memoria

#### `backend/app/services/agent_tools.py`
Tools que los agentes pueden ejecutar:
```python
def declare_war(db, nation_id: int, target_id: int):
    # Valida que target sea válido
    # Cambia relation status a "war"
    # Genera evento en timeline
    # Guarda en memoria RAG
```

#### `frontend/src/app/game/page.tsx`
Dashboard principal del juego. Incluye:
- Sistema de tabs (Tablero, Acciones, Leaderboard, Eventos)
- Estado global con React hooks
- Integración de notificaciones toast
- Detección de cambios (oro modificado, batallas, victoria)

#### `frontend/src/components/ToastNotification.tsx`
Sistema de notificaciones visuales:
- 7 tipos: success, error, warning, info, victory, battle, economic
- Animaciones CSS personalizadas
- Sonidos con Web Audio API
- Vibración en móviles

#### `frontend/src/lib/api.ts`
Cliente HTTP tipado:
```typescript
export async function getGameState(): Promise<GameState> {
  const response = await axios.get('/api/game/state');
  return response.data;
}

export async function processAgentTurn(): Promise<void> {
  await axios.post('/api/agent/process-turn');
}
```

---

## 🔧 Configuración y Deploy

### Variables de Entorno

#### Backend (`.env`)
```env
# API Keys
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx  # Consíguelo gratis en console.groq.com
GROQ_MODEL=llama-3.1-70b-versatile      # Modelo a usar

# Base de Datos
DATABASE_URL=postgresql://user:password@localhost:5432/geopol
DB_USER=postgres
DB_PASSWORD=secret123
DB_NAME=geopol

# ChromaDB
CHROMADB_HOST=localhost
CHROMADB_PORT=8001

# Configuración
DEBUG=True
LOG_LEVEL=INFO
```

#### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Deploy a Producción

#### Opción 1: Vercel (Frontend) + Railway (Backend)

**Frontend en Vercel:**
```bash
cd frontend
npm install -g vercel
vercel login
vercel deploy --prod
```

Configurar en Vercel:
- Build Command: `npm run build`
- Output Directory: `.next`
- Environment Variable: `NEXT_PUBLIC_API_URL=https://tu-backend.railway.app`

**Backend en Railway:**
1. Conecta GitHub en railway.app
2. Selecciona repositorio Nation-Mind-AI
3. Railway detecta `Dockerfile` automáticamente
4. Agrega PostgreSQL addon
5. Configura variables de entorno (Groq API Key, etc)

#### Opción 2: Docker en VPS

```bash
# En tu servidor (DigitalOcean, AWS, etc)
git clone https://github.com/tu-usuario/Nation-Mind-AI.git
cd Nation-Mind-AI
docker-compose up -d
```

### Costos Mensuales Estimados

**Tier Gratuito:**
- Groq: Gratis (100,000 tokens/día)
- Vercel: Gratis (hobby plan)
- Railway: $5/mes (500 horas) o gratis con GitHub Student
- PostgreSQL: Railway incluido
- ChromaDB: Auto-host gratis

**Total: $0-5/mes** 🎉

---

## 🐛 Troubleshooting

### Backend no inicia

**Error:** `ModuleNotFoundError: No module named 'chromadb'`
```bash
cd backend
pip install -r requirements.txt
```

**Error:** `GROQ_API_KEY not found`
```bash
# Crea archivo .env en backend/
echo "GROQ_API_KEY=tu_clave_aqui" > .env
```

**Error:** `could not connect to server: Connection refused (PostgreSQL)`
```bash
# Asegúrate que PostgreSQL esté corriendo
docker-compose up -d postgres
```

### Frontend no conecta con backend

**Error:** `Network Error` en consola del navegador

**Solución:**
1. Verifica que backend esté corriendo: http://localhost:8000/docs
2. Verifica CORS está habilitado en `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```
3. Verifica `.env.local` tenga URL correcta:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🤝 Contribuir

¡Contribuciones bienvenidas! 🎉

### Áreas donde puedes ayudar:

**Backend:**
- [ ] Mejorar prompts de agentes
- [ ] Nuevas herramientas para agentes (espionaje, comercio)
- [ ] Tests unitarios

**Frontend:**
- [ ] Mapa interactivo del mundo
- [ ] Gráficos de evolución (Chart.js)
- [ ] Animaciones de batallas
- [ ] Modo oscuro/claro

**Documentación:**
- [ ] Tutoriales en video
- [ ] Guía de contribución
- [ ] Traducir a inglés

### Cómo contribuir:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/mi-feature`
3. Haz commits: `git commit -m 'Add: nueva feature'`
4. Push: `git push origin feature/mi-feature`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto usa la licencia **MIT**.

```
MIT License

Copyright (c) 2024 Nation-Mind AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...
```

**En cristiano:** Puedes usar este código para lo que quieras (incluso comercialmente), solo menciona al autor original.

---

## 👨‍💻 Autor

**Desarrollado en el F5 Bootcamp de IA**

- 🌐 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- 📧 Email: tu@email.com

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias a:

- **[F5 Bootcamp de IA](https://www.fundacionf5.org/)** - Por la formación en IA y la oportunidad
- **[LangChain Team](https://www.langchain.com/)** - Por LangGraph y excelente documentación
- **[Groq](https://groq.com/)** - Por API gratuita ultra-rápida
- **[Meta AI](https://ai.meta.com/)** - Por LLaMA 3 open source
- **[Vercel](https://vercel.com/)** - Por hosting gratuito del frontend
- **Comunidad open source** 💚 - Por todas las librerías increíbles

---

## 🗺️ Roadmap

### ✅ v1.0 - MVP (Actual)
- [x] 8 naciones jugables
- [x] Sistema de agentes con LangGraph
- [x] RAG con ChromaDB
- [x] 5 condiciones de victoria
- [x] Batallas automáticas
- [x] Economía dinámica
- [x] Frontend completo con Next.js
- [x] Sistema de notificaciones
- [x] Leaderboard y progreso

### 🚧 v1.1 - Polish (2 semanas)
- [ ] Tests unitarios (backend)
- [ ] Tests E2E (frontend)
- [ ] Optimización de prompts
- [ ] Fix bugs reportados

### 🎯 v2.0 - Expansión (1 mes)
- [ ] Mapa interactivo del mundo
- [ ] Sistema de espionaje
- [ ] Economía avanzada (comercio, inflación)
- [ ] Eventos aleatorios

### 🌟 v3.0 - Mult ijugador (2 meses)
- [ ] Matchmaking
- [ ] Modo 2-4 jugadores humanos + IA
- [ ] Chat en tiempo real
- [ ] Sistema de rankings global

---

## 🎉 ¡Gracias por llegar hasta aquí!

Si este proyecto te ayudó a aprender algo nuevo:

- ⭐ **Dale una estrella** al repo
- 🐛 **Reporta bugs** si encuentras alguno
- 💡 **Sugiere features** que te gustaría ver
- 🤝 **Contribuye** código o documentación
- 📢 **Comparte** con otros developers

**Happy coding! 🚀**

---

<div align="center">

### Construido con ❤️ en el Bootcamp F5 de IA

**Nation-Mind AI** © 2024

</div>

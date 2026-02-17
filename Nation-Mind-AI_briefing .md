# Nation-Mind AI — Civilization Survival con Agentes Geopolíticos
### Proyecto Individual · Bootcamp de IA · Fase 1 — Briefing Técnico + MVP

---

## 1. Problema que queremos resolver

### ¿Qué problema existe?

Los simuladores de estrategia geopolítica existentes (Civilization, Victoria 3, Risk) utilizan una IA basada en reglas fijas y árboles de decisión predefinidos. Las naciones enemigas siguen patrones mecánicos, no tienen objetivos propios coherentes, no negocian de forma convincente y no recuerdan el contexto histórico de la partida.

El resultado es una experiencia que pierde profundidad rápidamente: el jugador aprende las rutinas de la IA y las explota, rompiendo la inmersión y la tensión dramática que debería generar gobernar una nación real.

### ¿Para quién?

- Jugadores de estrategia que buscan una experiencia más dinámica y narrativa
- Estudiantes y entusiastas de geopolítica y ciencias políticas
- Desarrolladores e investigadores interesados en sistemas multiagente aplicados a simulación

### ¿Por qué es relevante?

Con la llegada de los LLMs y los sistemas de agentes, por primera vez es posible crear naciones virtuales con **personalidades, memorias y objetivos propios**, capaces de negociar, aliarse, mentir y declarar guerras de forma coherente y contextual. Este proyecto explora ese potencial de forma concreta y demostrable.

### ¿Cómo se resuelve actualmente?

| Solución actual | Limitación |
|---|---|
| Juegos AAA (Civilization, Victoria 3) | IA basada en reglas fijas. Predecible y sin memoria real. |
| Juegos de rol por texto (AI Dungeon) | Narrativa generativa pero sin mecánicas de simulación estratégica. |
| Ningún producto existente | Combina simulación geopolítica real con agentes LLM autónomos. |

---

## 2. Propuesta de solución

**Nation-Mind AI** es un simulador geopolítico por turnos donde el jugador gobierna una nación en un mundo compartido con **3-5 naciones controladas por agentes de inteligencia artificial**. Cada agente tiene:

- Una **personalidad propia** (agresiva, diplomática, aislacionista, expansionista…)
- **Objetivos a largo plazo** (dominar el continente, acumular riqueza, vengarse de una nación…)
- **Memoria persistente** del historial de la partida via RAG
- Capacidad de tomar **decisiones autónomas entre turnos**

La propuesta central es que las naciones-IA **no reaccionan solo al jugador: actúan, planifican y ejecutan su propia agenda**. Si ignoras a un vecino durante 10 turnos, puede haberse aliado con tu enemigo, comprado recursos que tú necesitas o fomentado una rebelión en tu territorio.

### ¿Qué aporta la IA en este proyecto?

La IA no es decorativa. Cada nación es un **agente LLM con memoria persistente** y objetivos propios. El sistema **RAG** permite que los agentes recuerden eventos históricos de la partida para tomar decisiones coherentes. La lógica de simulación (recursos, guerras, diplomacia) está separada del LLM, garantizando consistencia mecánica.

### ¿Por qué esta solución es interesante?

- Combina **simulación estratégica** con **narrativa emergente** generada por LLMs
- Cada partida es única: los agentes evolucionan según las decisiones del jugador
- Permite demostrar **sistemas multiagente complejos** en un contexto intuitivo y visual
- Es un *portfolio piece* que muestra dominio de IA aplicada, full stack y arquitectura de sistemas

---

## 3. Definición del MVP

> El MVP debe ser: **realista, alcanzable, funcional y demostrable.**

### ✅ Funcionalidades mínimas del MVP

- Mapa del mundo simplificado con **4-5 naciones** (regiones SVG o celdas simples)
- **Sistema de turnos**: el jugador decide, luego los agentes ejecutan sus acciones
- **3 tipos de interacción diplomática**: Proponer alianza · Declarar guerra · Negociar comercio
- **3 recursos básicos por nación**: Oro · Tropas · Territorios
- Cada nación-IA tiene: nombre, personalidad definida, objetivos visibles y memoria de eventos
- **Feed de noticias** del mundo generado por LLM (lo que ocurre cada turno narrado)
- **Panel de estado** del jugador: recursos, relaciones diplomáticas, historial
- **Chat diplomático**: el jugador escribe mensajes a otras naciones y el agente responde en personaje

### ❌ Fuera del MVP (future scope)

- Mapa geográfico complejo con renderizado avanzado
- Sistema de combate táctico detallado
- Más de 5 naciones simultáneas
- Multijugador (otros humanos como gobernantes)
- Economía avanzada (inflación, mercados, cadenas de suministro)
- Sistema de espionaje y acciones encubiertas

### 🧪 ¿Qué se puede testear en la demo?

- Iniciar una partida y ver el mundo con las naciones y sus personalidades generadas
- Enviar un mensaje diplomático a una nación y recibir respuesta coherente con su perfil
- Declarar guerra y observar cómo el resto de naciones reacciona según sus propios intereses
- Avanzar 5-10 turnos y ver cómo el mundo evoluciona de forma no lineal
- Leer el feed de noticias que narra los eventos del turno de forma inmersiva

---

## 4. Arquitectura técnica (alto nivel)

### Flujo de datos por turno

```
[Jugador] → acción (ej: "Proponer alianza a Nación B")
    │
    ▼
[FastAPI] → valida acción → actualiza estado en PostgreSQL
    │
    ▼
[LangGraph] → orquesta agentes
    │   ├─ Agente Nación A → consulta RAG (ChromaDB) → decide acción
    │   ├─ Agente Nación B → consulta RAG (ChromaDB) → decide acción
    │   └─ Agente Nación C → consulta RAG (ChromaDB) → decide acción
    │
    ▼
[FastAPI] → genera feed de noticias del turno (Groq/LLaMA3)
    │       → vectoriza nuevos eventos → guarda en ChromaDB
    │       → persiste nuevo estado en PostgreSQL
    ▼
[Next.js] → actualiza UI con el nuevo estado del mundo
```

### Diagrama de arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                         │
│                   Next.js 14                        │
│  Mapa SVG · Panel recursos · Chat · Feed noticias   │
└─────────────────┬───────────────────────────────────┘
                  │  REST API (HTTP/JSON)
┌─────────────────▼───────────────────────────────────┐
│                    BACKEND                          │
│               FastAPI (Python)                      │
│                                                     │
│   ┌─────────────────────────────────────────────┐   │
│   │           LangGraph (Agentes)               │   │
│   │  Nación A · Nación B · Nación C · Nación D  │   │
│   │       (cada una: LLaMA3 via Groq)           │   │
│   └─────────────────────────────────────────────┘   │
└──────────┬──────────────────────────┬───────────────┘
           │                          │
┌──────────▼──────────┐   ┌───────────▼───────────────┐
│    PostgreSQL        │   │       ChromaDB            │
│  Estado del mundo   │   │   Memoria RAG             │
│  Recursos · Turns   │   │   Eventos vectorizados    │
│  Relaciones dipl.   │   │   Contexto por agente     │
└─────────────────────┘   └───────────────────────────┘
```

---

## 5. Stack tecnológico

### Lenguajes y Frameworks

| Capa | Tecnología | Justificación | Coste |
|---|---|---|---|
| Frontend | **Next.js 14** | Routing nativo, SSR, deploy en Vercel con un clic. Mejor que React puro para producción. | Gratis |
| Backend | **FastAPI (Python)** | Async nativo (ideal para agentes en paralelo), ecosistema Python insuperable para IA. | Gratis |
| Agentes | **LangGraph** | Modela el flujo entre agentes como grafo dirigido. Perfecto para turnos y estados. | Gratis |
| LLM | **Groq + LLaMA 3** | Inferencia gratuita, velocidad muy superior a OpenAI en tier básico. Crítico para buena UX. | Gratis |
| BD Relacional | **PostgreSQL** | Estado del mundo, historial de turnos, relaciones diplomáticas. | Gratis |
| BD Vectorial | **ChromaDB** | RAG local sin cuenta externa. Migración a Pinecone en producción transparente. | Gratis |
| Embeddings | **HuggingFace sentence-transformers** | Vectorización de eventos para RAG. Sin coste y corre en local. | Gratis |
| Deploy Frontend | **Vercel** | Tier gratuito generoso, integración directa con Next.js. | Gratis |
| Deploy Backend | **Railway / Render** | Tier gratuito suficiente para el MVP. | Gratis |
| Contenedores | **Docker** | Entorno reproducible en local. Recomendado pero no bloqueante. | Gratis |

### Justificación de decisiones técnicas clave

**LangGraph sobre CrewAI:** LangGraph permite modelar el flujo de agentes como un grafo dirigido de estados, lo cual se adapta perfectamente a la lógica de turnos. CrewAI está más orientado a pipelines lineales de tareas.

**Groq sobre OpenAI:** Groq ofrece inferencia de LLaMA 3 completamente gratuita con velocidades de respuesta muy superiores. Crítico para que la UX en tiempo real sea fluida durante la demo.

**ChromaDB sobre Pinecone:** ChromaDB corre completamente en local sin necesidad de cuenta externa, perfecto para desarrollo. La migración a Pinecone en producción es transparente sin cambiar código.

**PostgreSQL sobre MongoDB:** El estado del mundo (recursos, relaciones, turnos) es inherentemente relacional. Las queries analíticas (¿cuántas guerras ha tenido la Nación A?) son más limpias en SQL.

---

## 6. Dataset y datos

### ¿De dónde salen los datos?

No se usan datasets externos. Los datos del mundo son **generados proceduralmente** al inicio de cada partida por el propio sistema.

| Dato | Origen | Cómo se procesa |
|---|---|---|
| Perfil de naciones | Generado por LLM al iniciar partida | Guardado como JSON en PostgreSQL |
| Estado del mundo (recursos, territorios) | Generado proceduralmente (seed aleatorio) | Persistido en PostgreSQL por turno |
| Eventos históricos | Generados en cada turno por los agentes | Vectorizados con sentence-transformers → ChromaDB |
| Respuestas diplomáticas | Generadas por LLM en tiempo real | No persistidas permanentemente (stateless) |

### Pipeline RAG — el componente clave

```
Evento del turno (texto)
        │
        ▼
sentence-transformers (embedding)
        │
        ▼
ChromaDB (almacenamiento vectorial)
        │
        ▼ (en el siguiente turno, para cada agente)
Query semántica: "eventos relevantes para Nación B"
        │
        ▼
Top-N eventos recuperados → inyectados en el prompt del agente
        │
        ▼
LLaMA 3 via Groq → decisión coherente con la historia de la partida
```

El RAG es lo que distingue este proyecto de un simple wrapper de LLM. Sin él, los agentes olvidan eventos anteriores al llenarse el contexto. Con él, un agente puede recordar que "hace 12 turnos el jugador rompió un acuerdo comercial" y actuar en consecuencia.

---

## 7. Plan de desarrollo

### Fases de trabajo

| Fase | Tareas | Tiempo estimado |
|---|---|---|
| **Setup + BD** | Repos, Docker, FastAPI, modelos de datos PostgreSQL (Nación, Turno, Evento, Relación), seed de partida | 2 días |
| **Agentes LLM** | LangGraph, integración Groq, prompts de personalidad, ChromaDB, pipeline RAG completo | 4 días |
| **Frontend MVP** | Next.js: mapa SVG, panel recursos, chat diplomático, feed de noticias, integración API | 3 días |
| **Pulido + Demo** | Testing flujo completo, ajuste de prompts, deploy Vercel + Railway, preparación demo | 2 días |

### Riesgos técnicos y planes alternativos

| Riesgo | Probabilidad | Impacto | Plan alternativo |
|---|---|---|---|
| Rate limit de Groq en demos en vivo | Media | Medio | Cachear respuestas frecuentes o usar Ollama en local (Mistral 7B) |
| LangGraph: curva de aprendizaje alta | Media | Alto | Simplificar a llamadas secuenciales con LangChain básico |
| Incoherencia narrativa entre turnos | Baja | Medio | Ajuste de prompts con contexto forzado y restricciones de formato JSON |
| Deploy con errores de configuración | Baja | Bajo | Demo en local con vídeo grabado como backup |

---

## Resumen ejecutivo

**Nation-Mind AI** es un simulador geopolítico donde cada nación enemiga es un agente de IA autónomo con personalidad, objetivos y memoria. El jugador gobierna una nación y toma decisiones diplomáticas, militares y económicas que afectan a un mundo que evoluciona de forma no lineal.

El proyecto demuestra aplicación real de **sistemas multiagente**, **RAG**, **LLMs en tiempo real** y **arquitectura full stack moderna**, usando exclusivamente tecnologías gratuitas y open source.

```
Next.js  ·  FastAPI  ·  LangGraph  ·  Groq LLaMA 3  ·  PostgreSQL  ·  ChromaDB
                    100% gratuito  ·  Escalable  ·  Demostrable
```
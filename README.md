# 🌍 Nation-Mind AI

**Simulador Geopolítico con Agentes de Inteligencia Artificial**

Un juego de estrategia por turnos donde cada nación enemiga es un agente autónomo con personalidad, objetivos y memoria. Combina simulación geopolítica con narrativa emergente generada por LLMs.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

---

## 🎯 ¿Qué es Nation-Mind AI?

Nation-Mind AI es un simulador donde gobiernas una nación en un mundo compartido con **3-5 naciones controladas por agentes de IA**. A diferencia de juegos tradicionales con IA predecible:

- ✅ Cada nación tiene **personalidad propia** (agresiva, diplomática, aislacionista...)
- ✅ **Objetivos a largo plazo** (dominar el continente, acumular riqueza, venganza...)
- ✅ **Memoria persistente** vía RAG - recuerdan todo lo que ha pasado
- ✅ Toman **decisiones autónomas** entre turnos
- ✅ **Narrativa emergente** - cada partida es única

### Ejemplo de Partida

```
Turno 1:  Declaras alianza con Francia
Turno 3:  España (IA) ataca a Italia
Turno 5:  Francia, recordando tu alianza, te ayuda contra España
Turno 8:  Italia se venga de España formando coalición contigo
Turno 10: Francia traiciona la alianza porque necesita tus recursos
```

Los agentes NO reaccionan solo al jugador: **actúan, planifican y ejecutan su propia agenda**.

---

## 🚀 Características

### MVP (Versión 1.0)
- 🗺️ Mapa interactivo con 4-5 naciones
- 🤖 Sistema de agentes con LangGraph
- 🧠 Memoria persistente con RAG (ChromaDB)
- ⚔️ 3 tipos de interacción: Alianza, Guerra, Comercio
- 📰 Feed de noticias generado por IA
- 💬 Chat diplomático con agentes

### Post-MVP
- 🎮 Sistema de combate táctico
- 🕵️ Espionaje y acciones encubiertas
- 💰 Economía avanzada
- 👥 Multijugador
- 📊 Estadísticas y replay

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - API REST con Python
- **LangGraph** - Orquestación de agentes multiagente
- **Groq** - Inferencia de LLaMA 3 (gratis y rápido)
- **PostgreSQL** - Base de datos relacional
- **ChromaDB** - Base de datos vectorial para RAG
- **SQLAlchemy** - ORM para Python

### Frontend
- **Next.js 14** - Framework React con App Router
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos utilitarios
- **Shadcn UI** - Componentes UI
- **Framer Motion** - Animaciones

### DevOps & Deploy
- **Docker** - Contenedores
- **Vercel** - Deploy frontend
- **Railway** - Deploy backend
- **GitHub Actions** - CI/CD

---

## 📁 Estructura del Proyecto

```
Nation-Mind-AI/
├── backend/                # FastAPI (Python)
│   ├── app/
│   │   ├── controllers/    # Endpoints API (MVC)
│   │   ├── services/       # Lógica de negocio
│   │   ├── models/         # Modelos de BD (SQLAlchemy)
│   │   ├── schemas/        # Validación (Pydantic)
│   │   └── agents/         # Sistema de agentes (LangGraph)
│   └── requirements.txt
│
├── frontend/               # Next.js (TypeScript)
│   ├── src/
│   │   ├── app/            # App Router
│   │   ├── components/     # Componentes React
│   │   └── lib/            # Utils y API client
│   └── package.json
│
├── docs/                   # Documentación completa
│   ├── GUIA_DESARROLLO.md
│   ├── TECH_STACK_EXPLICADO.md
│   ├── MVC_ARQUITECTURA.md
│   ├── TECNOLOGIAS_GRATUITAS.md
│   └── QUICK_START.md
│
└── docker-compose.yml      # Orquestación de servicios
```

---

## 🎓 Para Junior Developers

Este proyecto incluye **documentación educativa completa**:

📖 **[GUIA_DESARROLLO.md](./GUIA_DESARROLLO.md)** - Desarrollo paso a paso del MVP  
📖 **[TECH_STACK_EXPLICADO.md](./TECH_STACK_EXPLICADO.md)** - Conceptos clave de cada tecnología  
📖 **[MVC_ARQUITECTURA.md](./MVC_ARQUITECTURA.md)** - Patrón MVC en FastAPI explicado  
📖 **[QUICK_START.md](./QUICK_START.md)** - Setup inicial en 10 minutos  
📖 **[TECNOLOGIAS_GRATUITAS.md](./TECNOLOGIAS_GRATUITAS.md)** - Stack gratuito completo  

Cada concepto está explicado desde cero: qué es, por qué se usa, cómo se implementa.

---

## ⚡ Quick Start

### Prerrequisitos

```bash
python --version  # ≥ 3.10
node --version    # ≥ 18
docker --version  # opcional pero recomendado
```

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Nation-Mind-AI.git
cd Nation-Mind-AI
```

### 2. Setup Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu GROQ_API_KEY
```

### 3. Levantar PostgreSQL

```bash
cd ..
docker-compose up -d
```

### 4. Ejecutar Backend

```bash
cd backend
uvicorn app.main:app --reload

# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 5. Setup Frontend

```bash
cd ../frontend
npm install
npm run dev

# App: http://localhost:3000
```

Ver **[QUICK_START.md](./QUICK_START.md)** para más detalles.

---

## 🏗️ Arquitectura

### Flujo de un Turno

```
1. JUGADOR toma decisión
   POST /api/diplomacy/declare-war
   
2. BACKEND valida acción
   Controller → Service → Model → PostgreSQL
   
3. SISTEMA DE AGENTES (LangGraph)
   ├─ Agente España consulta RAG
   ├─ Agente Francia consulta RAG
   └─ Agente Italia consulta RAG
   
4. CADA AGENTE decide con LLM (Groq)
   Personalidad + Memoria + Estado → LLaMA 3 → Decisión
   
5. PROCESAMIENTO
   ├─ Resolver combates
   ├─ Actualizar recursos
   ├─ Generar feed de noticias (LLM)
   ├─ Vectorizar eventos → ChromaDB
   └─ Guardar estado → PostgreSQL
   
6. FRONTEND actualiza
   Polling → Estado actualizado → UI refresh
```

### Sistema RAG (Memoria de Agentes)

```
Evento: "España atacó a Francia en turno 5"
    ↓ [sentence-transformers]
Vector: [0.15, -0.84, 0.23, ...]
    ↓ [ChromaDB]
Almacenado en memoria vectorial

Turno 15: Francia necesita decidir
    ↓ Query: "¿Qué ha hecho España?"
    ↓ [ChromaDB similarity search]
Recupera: "España atacó a Francia en turno 5"
    ↓ [Prompt con contexto]
LLaMA 3 decide: "Declarar guerra a España"
```

---

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## 📦 Deploy

### Frontend (Vercel)

```bash
cd frontend
vercel deploy
```

### Backend (Railway)

```bash
cd backend
railway up
```

Ver documentación completa en [GUIA_DESARROLLO.md](./GUIA_DESARROLLO.md).

---

## 🗺️ Roadmap

### ✅ Fase 1: Fundamentos (Semana 1-2)
- [x] Setup proyecto
- [x] Backend FastAPI con MVC
- [x] PostgreSQL con modelos básicos
- [x] Frontend Next.js básico

### 🚧 Fase 2: Sistema de Agentes (Semana 3)
- [ ] Integración ChromaDB + RAG
- [ ] Sistema de agentes con LangGraph
- [ ] Integración Groq (LLaMA 3)
- [ ] Prompts de personalidad

### 📋 Fase 3: Lógica del Juego (Semana 4)
- [ ] Sistema de turnos
- [ ] Lógica de combate
- [ ] Diplomacia (alianzas, guerra, comercio)
- [ ] Feed de noticias

### 🎨 Fase 4: UI/UX (Semana 5)
- [ ] Mapa interactivo
- [ ] Panel de recursos
- [ ] Chat diplomático
- [ ] Animaciones

### 🚀 Fase 5: MVP Deploy (Semana 6)
- [ ] Testing completo
- [ ] Deploy a producción
- [ ] Video demo
- [ ] Documentación final

### 🌟 Post-MVP
- [ ] Sistema de espionaje
- [ ] Economía avanzada
- [ ] Multijugador
- [ ] IA mejorada con fine-tuning

---

## 🤝 Contribuir

¡Contribuciones bienvenidas! 

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**Tu Nombre**
- Portfolio: [tu-portfolio.com](https://tu-portfolio.com)
- LinkedIn: [linkedin.com/in/tu-perfil](https://linkedin.com/in/tu-perfil)
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

---

## 🙏 Agradecimientos

- [F5 Bootcamp de IA](https://www.fundacionf5.org/) - Por el programa de formación
- [LangChain](https://www.langchain.com/) - Por LangGraph
- [Groq](https://groq.com/) - Por inferencia gratuita de LLMs
- Comunidad open source 💚

---

## 📚 Recursos Adicionales

- [Blog Post: Cómo construí Nation-Mind AI](#)
- [Video Tutorial: Sistema de Agentes desde Cero](#)
- [Showcase: Mejores partidas](#)

---

<div align="center">

**Si te gusta el proyecto, ⭐ dale una estrella!**

[Ver Demo](#) | [Reportar Bug](https://github.com/tu-usuario/Nation-Mind-AI/issues) | [Solicitar Feature](https://github.com/tu-usuario/Nation-Mind-AI/issues)

</div>

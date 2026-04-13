'use client';

import { useMemo, useState } from 'react';

type FooterModalKey = 'how-to-play' | 'strategy' | 'nations' | 'updates' | 'feedback' | null;

export default function Footer() {
  const currentYear = new Date().getFullYear();
  const [activeModal, setActiveModal] = useState<FooterModalKey>(null);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [feedbackForm, setFeedbackForm] = useState({
    name: '',
    email: '',
    topic: 'General',
    message: '',
  });

  const modalContent = useMemo(() => {
    switch (activeModal) {
      case 'how-to-play':
        return {
          icon: '🎮',
          title: 'Cómo Jugar',
          subtitle: 'Los fundamentos para arrancar una partida sólida.',
          body: [
            'Selecciona una nación al inicio y gobierna tu país turno a turno.',
            'Gestiona diplomacia, economía y ejército mientras las otras naciones actúan por IA.',
            'Tu objetivo es crecer, sobrevivir y buscar una condición de victoria antes que el resto.',
          ],
        };
      case 'strategy':
        return {
          icon: '🧠',
          title: 'Estrategias',
          subtitle: 'Ideas prácticas para jugar con más ventaja.',
          body: [
            'No gastes todo al principio: reserva recursos para responder a guerras y alianzas.',
            'Si tu economía crece, tus decisiones futuras tienen mucho más margen.',
            'Usa la diplomacia para ganar tiempo y la guerra solo cuando tengas ventaja real.',
          ],
        };
      case 'nations':
        return {
          icon: '🌍',
          title: 'Guía de Naciones',
          subtitle: 'Cómo leer las personalidades y fortalezas del tablero.',
          body: [
            'Cada nación tiene personalidad, poder militar, económico y diplomático distintos.',
            'Las personalidades influyen en su estilo: agresivas, diplomáticas, defensivas o expansionistas.',
            'Explora la ficha de cada nación en la partida para detectar fortalezas y debilidades.',
          ],
        };
      case 'updates':
        return {
          icon: '🚀',
          title: 'Actualizaciones',
          subtitle: 'Sección en construcción para roadmap y changelog.',
          body: [
            'Pronto tendrás aquí un changelog visual con las mejoras más recientes.',
            'También se pueden mostrar notas de balance, nuevas naciones y cambios en IA.',
          ],
        };
      case 'feedback':
        return {
          icon: '📝',
          title: 'Feedback',
          subtitle: 'Cuéntanos qué mejorarías en la experiencia.',
          body: [
            'De momento este formulario es decorativo: todavía no envía datos a ningún servicio.',
            'Úsalo para validar el diseño antes de conectar almacenamiento o email.',
          ],
        };
      default:
        return null;
    }
  }, [activeModal]);

  const closeModal = () => setActiveModal(null);

  const handleFeedbackChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = event.target;
    setFeedbackForm((current) => ({ ...current, [name]: value }));
  };

  const handleFeedbackSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFeedbackSubmitted(true);
  };
  
  return (
    <footer className="relative mt-auto overflow-hidden border-t border-slate-800 bg-slate-950">
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(circle at top left, rgba(168, 85, 247, 0.16), transparent 32%), radial-gradient(circle at top right, rgba(59, 130, 246, 0.12), transparent 28%), linear-gradient(to bottom, rgba(15, 23, 42, 0.92), rgba(2, 6, 23, 1))',
        }}
      />
      <div className="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-purple-500/60 to-transparent" />

      <div className="relative container mx-auto px-4 py-14">
        <div className="mb-10 flex flex-col gap-4 rounded-3xl border border-slate-800/80 bg-slate-900/60 px-6 py-5 shadow-2xl shadow-black/20 backdrop-blur-sm lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-purple-300/80">
              Nation-Mind AI
            </p>
            <h3 className="mt-1 text-2xl font-bold text-white">
              Un simulador geopolítico con IA, memoria y decisiones emergentes.
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="rounded-full border border-slate-700 bg-slate-950/70 px-3 py-1 text-xs font-medium text-slate-300">
              8 naciones
            </span>
            <span className="rounded-full border border-slate-700 bg-slate-950/70 px-3 py-1 text-xs font-medium text-slate-300">
              Memoria RAG
            </span>
            <span className="rounded-full border border-slate-700 bg-slate-950/70 px-3 py-1 text-xs font-medium text-slate-300">
              Agentes autónomos
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1.3fr_1fr_1fr]">
          {/* GeoPolitik Info */}
          <div className="rounded-3xl border border-slate-800/70 bg-slate-900/55 p-6 shadow-xl shadow-black/15 backdrop-blur-sm">
            <div className="flex items-center gap-3 mb-5">
              <div className="relative rounded-2xl bg-slate-800/90 p-3 ring-1 ring-white/5">
                <div className="absolute inset-0 rounded-2xl bg-purple-500/10 blur-xl" />
                <svg
                  className="relative w-6 h-6 text-slate-300"
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
              <div>
                <h3 className="text-xl font-bold text-white">Nation-Mind AI</h3>
                <p className="text-xs uppercase tracking-[0.18em] text-purple-300/80">Simulador Geopolítico por Turnos</p>
              </div>
            </div>
            <p className="max-w-xl text-sm leading-7 text-slate-300">
              Gobierna una nación en un mundo simulado donde agentes de IA controlan el resto del planeta. 
              Toma decisiones estratégicas en diplomacia, economía y defensa.
            </p>
            <div className="mt-5 flex flex-wrap gap-2">
              <span className="rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs text-blue-200">
                Diplomacia dinámica
              </span>
              <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-200">
                Economía viva
              </span>
              <span className="rounded-full border border-rose-500/20 bg-rose-500/10 px-3 py-1 text-xs text-rose-200">
                Combate táctico
              </span>
            </div>
          </div>

          {/* Enlaces Rápidos */}
          <div className="rounded-3xl border border-slate-800/70 bg-slate-900/55 p-6 shadow-xl shadow-black/15 backdrop-blur-sm">
            <h3 className="mb-4 text-lg font-bold text-white">Enlaces Rápidos</h3>
            <ul className="space-y-2.5">
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('how-to-play')}
                  className="group flex items-center gap-2 text-sm text-slate-300 transition-colors hover:text-white"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-purple-400/80 transition-transform group-hover:scale-125" />
                  Cómo Jugar
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('strategy')}
                  className="group flex items-center gap-2 text-sm text-slate-300 transition-colors hover:text-white"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-sky-400/80 transition-transform group-hover:scale-125" />
                  Estrategias
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('nations')}
                  className="group flex items-center gap-2 text-sm text-slate-300 transition-colors hover:text-white"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400/80 transition-transform group-hover:scale-125" />
                  Guía de Naciones
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('updates')}
                  className="group flex items-center gap-2 text-sm text-slate-300 transition-colors hover:text-white"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-amber-300/90 transition-transform group-hover:scale-125" />
                  Actualizaciones <span className="text-xs text-slate-500">· pronto...</span>
                </button>
              </li>
            </ul>
          </div>

          {/* Comunidad */}
          <div className="rounded-3xl border border-slate-800/70 bg-slate-900/55 p-6 shadow-xl shadow-black/15 backdrop-blur-sm">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-lg font-bold text-white">Comunidad</h3>
              <span className="rounded-full border border-slate-700 bg-slate-950/70 px-2.5 py-1 text-[11px] uppercase tracking-[0.2em] text-slate-400">
                Beta
              </span>
            </div>
            <ul className="space-y-2.5 mb-5">
              <li>
                <a href="https://discord.gg" target="_blank" rel="noopener noreferrer" className="text-sm text-slate-300 transition-colors hover:text-white">
                  Discord
                </a>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('nations')}
                  className="text-sm text-slate-300 transition-colors hover:text-white"
                >
                  Foro
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('how-to-play')}
                  className="text-sm text-slate-300 transition-colors hover:text-white"
                >
                  Soporte
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => setActiveModal('feedback')}
                  className="text-sm text-slate-300 transition-colors hover:text-white"
                >
                  Feedback
                </button>
              </li>
            </ul>
            <button
              type="button"
              onClick={() => setActiveModal('feedback')}
              className="w-full rounded-2xl border border-purple-500/30 bg-linear-to-r from-purple-500/15 to-blue-500/15 px-4 py-3 text-left text-sm text-white transition hover:border-purple-400/60 hover:from-purple-500/20 hover:to-blue-500/20"
            >
              <span className="block font-semibold">Enviar feedback</span>
              <span className="block text-xs text-slate-300/80">Comparte ideas visuales o mejoras para la experiencia</span>
            </button>
          </div>
        </div>

        {/* Divider */}
        <div className="mt-8 border-t border-slate-800/80 pt-6">
          <div className="flex flex-col items-center justify-between gap-5 md:flex-row">
            {/* Copyright */}
            <p className="text-center text-sm text-slate-500 md:text-left">
              © {currentYear} Nation-Mind AI. Todos los derechos reservados.
            </p>

            {/* Social Icons */}
            <div className="flex items-center gap-3">
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-xl border border-slate-800 bg-slate-900/80 p-2.5 text-slate-400 transition-all hover:border-slate-600 hover:text-white hover:shadow-lg hover:shadow-black/20"
                aria-label="Twitter"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
              <a
                href="https://github.com/Yedpt/Nation-Mind-AI"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-xl border border-slate-800 bg-slate-900/80 p-2.5 text-slate-400 transition-all hover:border-slate-600 hover:text-white hover:shadow-lg hover:shadow-black/20"
                aria-label="GitHub"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" clipRule="evenodd" />
                </svg>
              </a>
              <a
                href="mailto:contact@nationmind.ai"
                className="rounded-xl border border-slate-800 bg-slate-900/80 p-2.5 text-slate-400 transition-all hover:border-slate-600 hover:text-white hover:shadow-lg hover:shadow-black/20"
                aria-label="Email"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </a>
            </div>
          </div>
          <p className="mt-4 text-center text-xs text-slate-500">
            Hecho con ❤️ para jugadores de estrategia
          </p>
        </div>
      </div>

      {activeModal && modalContent && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/85 backdrop-blur-md px-4">
          <div className="relative w-full max-w-2xl overflow-hidden rounded-3xl border border-slate-700/90 bg-slate-900 shadow-2xl shadow-black/50">
            <div className="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-purple-400/70 to-transparent" />
            <div className="absolute -top-16 right-0 h-44 w-44 rounded-full bg-purple-500/10 blur-3xl" />

            <div className="relative flex items-start justify-between gap-4 border-b border-slate-800/90 px-6 py-5">
              <div className="flex items-start gap-3">
                <div className="mt-0.5 rounded-xl border border-slate-700 bg-slate-950/80 px-2.5 py-1.5 text-sm text-slate-200">
                  {modalContent.icon}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">{modalContent.title}</h3>
                  <p className="mt-1 text-sm text-slate-400">{modalContent.subtitle}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={closeModal}
                className="rounded-xl border border-slate-700 bg-slate-800/80 px-3 py-1.5 text-slate-200 hover:border-slate-500 hover:bg-slate-700"
                aria-label="Cerrar modal"
              >
                Cerrar
              </button>
            </div>

            <div className="relative px-6 py-6">
              {activeModal === 'feedback' ? (
                <form onSubmit={handleFeedbackSubmit} className="space-y-5">
                  <p className="rounded-2xl border border-slate-700/80 bg-slate-950/70 px-4 py-3 text-sm text-slate-300">
                    Este formulario es solo visual por ahora. Sirve para dejar listo el diseño antes de conectar el backend.
                  </p>
                  {feedbackSubmitted && (
                    <div className="rounded-xl border border-emerald-500/40 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
                      Feedback preparado. Cuando conectemos el backend, aquí se enviará de verdad.
                    </div>
                  )}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <label className="space-y-2">
                      <span className="text-sm text-slate-300">Nombre</span>
                      <input
                        name="name"
                        value={feedbackForm.name}
                        onChange={handleFeedbackChange}
                        className="w-full rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                        placeholder="Tu nombre"
                      />
                    </label>
                    <label className="space-y-2">
                      <span className="text-sm text-slate-300">Email</span>
                      <input
                        name="email"
                        type="email"
                        value={feedbackForm.email}
                        onChange={handleFeedbackChange}
                        className="w-full rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                        placeholder="tu@email.com"
                      />
                    </label>
                  </div>
                  <label className="block space-y-2">
                    <span className="text-sm text-slate-300">Tema</span>
                    <select
                      name="topic"
                      value={feedbackForm.topic}
                      onChange={handleFeedbackChange}
                      className="w-full rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                    >
                      <option>General</option>
                      <option>UI / UX</option>
                      <option>Balance</option>
                      <option>Bug visual</option>
                    </select>
                  </label>
                  <label className="block space-y-2">
                    <span className="text-sm text-slate-300">Mensaje</span>
                    <textarea
                      name="message"
                      rows={5}
                      value={feedbackForm.message}
                      onChange={handleFeedbackChange}
                      className="w-full rounded-xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-white outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                      placeholder="Cuéntanos qué mejorarías..."
                    />
                  </label>
                  <div className="flex justify-end gap-3">
                    <button
                      type="button"
                      onClick={closeModal}
                      className="rounded-xl border border-slate-700 px-4 py-2 text-slate-300 hover:border-slate-500 hover:text-white"
                    >
                      Cancelar
                    </button>
                    <button
                      type="submit"
                      className="rounded-xl bg-purple-600 px-4 py-2 font-semibold text-white hover:bg-purple-500"
                    >
                      Enviar feedback
                    </button>
                  </div>
                </form>
              ) : (
                <div className="space-y-3">
                  {modalContent.body.map((item, index) => (
                    <div
                      key={item}
                      className="rounded-2xl border border-slate-700/70 bg-slate-950/60 px-4 py-3 text-slate-200"
                    >
                      <p className="text-xs uppercase tracking-[0.18em] text-slate-500">Punto {index + 1}</p>
                      <p className="mt-1 leading-7">{item}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </footer>
  );
}

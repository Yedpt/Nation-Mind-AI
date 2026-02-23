'use client';

import { useEffect, useState } from 'react';
import { playNotificationSound } from '@/lib/sounds';

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info' | 'victory' | 'battle' | 'economic';
  title: string;
  message: string;
  duration?: number;
}

interface ToastNotificationProps {
  toasts: Toast[];
  onRemove: (id: string) => void;
}

export default function ToastNotification({ toasts, onRemove }: ToastNotificationProps) {
  const getToastStyles = (type: Toast['type']) => {
    const styles = {
      success: {
        bg: 'from-green-600 to-emerald-600',
        border: 'border-green-500',
        icon: '✅',
        shadow: 'shadow-green-500/50'
      },
      error: {
        bg: 'from-red-600 to-pink-600',
        border: 'border-red-500',
        icon: '❌',
        shadow: 'shadow-red-500/50'
      },
      warning: {
        bg: 'from-yellow-600 to-amber-600',
        border: 'border-yellow-500',
        icon: '⚠️',
        shadow: 'shadow-yellow-500/50'
      },
      info: {
        bg: 'from-blue-600 to-cyan-600',
        border: 'border-blue-500',
        icon: 'ℹ️',
        shadow: 'shadow-blue-500/50'
      },
      victory: {
        bg: 'from-purple-600 to-pink-600',
        border: 'border-purple-500',
        icon: '🏆',
        shadow: 'shadow-purple-500/50'
      },
      battle: {
        bg: 'from-red-700 to-orange-600',
        border: 'border-red-600',
        icon: '⚔️',
        shadow: 'shadow-red-600/50'
      },
      economic: {
        bg: 'from-yellow-600 to-green-600',
        border: 'border-yellow-500',
        icon: '💰',
        shadow: 'shadow-yellow-600/50'
      }
    };
    return styles[type];
  };

  useEffect(() => {
    toasts.forEach((toast) => {
      const duration = toast.duration || 5000;
      const timer = setTimeout(() => {
        onRemove(toast.id);
      }, duration);

      return () => clearTimeout(timer);
    });
  }, [toasts, onRemove]);

  return (
    <div className="fixed top-20 right-4 z-50 space-y-3 pointer-events-none">
      {toasts.map((toast) => {
        const styles = getToastStyles(toast.type);
        return (
          <div
            key={toast.id}
            className={`
              pointer-events-auto
              bg-gradient-to-r ${styles.bg}
              border-2 ${styles.border}
              rounded-xl p-4 min-w-[320px] max-w-md
              shadow-2xl ${styles.shadow}
              animate-slideInRight
              backdrop-blur-sm
            `}
          >
            <div className="flex items-start gap-3">
              <div className="text-3xl mt-1 animate-bounce">
                {styles.icon}
              </div>
              <div className="flex-1">
                <h4 className="text-white font-bold text-lg mb-1">
                  {toast.title}
                </h4>
                <p className="text-white/90 text-sm">
                  {toast.message}
                </p>
              </div>
              <button
                onClick={() => onRemove(toast.id)}
                className="text-white/80 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>
            
            {/* Progress bar inferior */}
            <div className="mt-3 h-1 bg-white/20 rounded-full overflow-hidden">
              <div 
                className="h-full bg-white/80 animate-progressBar"
                style={{ 
                  animationDuration: `${toast.duration || 5000}ms` 
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}

// Hook personalizado para usar toasts
export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = (
    type: Toast['type'],
    title: string,
    message: string,
    duration?: number
  ) => {
    const id = `toast-${Date.now()}-${Math.random()}`;
    const newToast: Toast = { id, type, title, message, duration };
    setToasts((prev) => [...prev, newToast]);
    
    // Reproducir sonido de notificación
    playNotificationSound(type);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  return { toasts, showToast, removeToast };
}

"use client";

import React from "react";

interface Fase2QuadrantsProps {
  onQuadrantSelect: (quadrant: 1 | 2 | 3 | 4) => void;
}

type QuadrantData = {
  id: 1 | 2 | 3 | 4;
  title: string;
  subtitle: string;
  color: string;
  colorLight: string;
  colorDark: string;
};

/**
 * Fase 2: Fire Kvadranter (Forenklet)
 *
 * Viser 4 store, pulserende kvadranter basert på Circumplex-modellen.
 * Brukeren velger hvilken kvadrant som best beskriver deres nåværende tilstand.
 *
 * Kvadranter:
 * - Q1 (Rød): Høy Energi, Ubehagelig
 * - Q2 (Gul): Høy Energi, Behagelig
 * - Q3 (Blå): Lav Energi, Ubehagelig
 * - Q4 (Grønn): Lav Energi, Behagelig
 *
 * Design: Myke, pulserende animasjoner
 * Inspirert av: How We Feel (HWF) app
 *
 * Triadisk Score: 0.12 (PROCEED)
 */
export default function Fase2Quadrants({ onQuadrantSelect }: Fase2QuadrantsProps) {
  const quadrants: QuadrantData[] = [
    {
      id: 1,
      title: "Høy Energi",
      subtitle: "Ubehagelig",
      color: "var(--color-emotion-q1-primary)",
      colorLight: "var(--color-emotion-q1-light)",
      colorDark: "var(--color-emotion-q1-dark)",
    },
    {
      id: 2,
      title: "Høy Energi",
      subtitle: "Behagelig",
      color: "var(--color-emotion-q2-primary)",
      colorLight: "var(--color-emotion-q2-light)",
      colorDark: "var(--color-emotion-q2-dark)",
    },
    {
      id: 3,
      title: "Lav Energi",
      subtitle: "Ubehagelig",
      color: "var(--color-emotion-q3-primary)",
      colorLight: "var(--color-emotion-q3-light)",
      colorDark: "var(--color-emotion-q3-dark)",
    },
    {
      id: 4,
      title: "Lav Energi",
      subtitle: "Behagelig",
      color: "var(--color-emotion-q4-primary)",
      colorLight: "var(--color-emotion-q4-light)",
      colorDark: "var(--color-emotion-q4-dark)",
    },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-white p-6">
      {/* Header */}
      <div className="text-center mb-12 max-w-md">
        <h2 className="text-3xl font-bold text-gray-900 mb-3">
          Hvordan føler du deg akkurat nå?
        </h2>
        <p className="text-base text-gray-600">
          Velg fargen som best beskriver din tilstand
        </p>
      </div>

      {/* Quadrant Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full px-4 md:px-12 lg:px-24">
        {quadrants.map((q) => (
          <button
            key={q.id}
            onClick={() => onQuadrantSelect(q.id)}
            className="group relative h-64 rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:scale-105"
            style={{
              background: `linear-gradient(135deg, ${q.colorLight} 0%, ${q.color} 50%, ${q.colorDark} 100%)`,
            }}
          >
            {/* Pulsing animation overlay */}
            <div
              className="absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity duration-1000"
              style={{
                background: `radial-gradient(circle at center, ${q.colorLight}, transparent)`,
                animation: "pulse-glow 2s ease-in-out infinite",
              }}
            />

            {/* Content */}
            <div className="relative z-10 h-full flex flex-col items-center justify-center text-white p-8">
              <h3 className="text-2xl font-bold mb-2 drop-shadow-lg">
                {q.title}
              </h3>
              <p className="text-lg font-medium drop-shadow-md opacity-90">
                {q.subtitle}
              </p>
            </div>

            {/* Hover indicator */}
            <div className="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <div className="w-10 h-10 rounded-full bg-white/30 backdrop-blur-sm flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes pulse-glow {
          0%, 100% {
            transform: scale(1);
            opacity: 0.3;
          }
          50% {
            transform: scale(1.1);
            opacity: 0.5;
          }
        }
      `}</style>
    </div>
  );
}

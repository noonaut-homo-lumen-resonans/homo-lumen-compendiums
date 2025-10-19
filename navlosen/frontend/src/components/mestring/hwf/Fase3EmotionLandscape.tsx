"use client";

import React, { useState, useEffect } from "react";
import { ALL_EMOTIONS, type EmotionWord } from "./emotionData";

interface Fase3EmotionLandscapeProps {
  quadrant: 1 | 2 | 3 | 4 | null;
  onEmotionSelect: (emotion: EmotionWord) => void;
}

/**
 * Fase 3: Følelseslandskap (Redesigned)
 *
 * Viser ALLE 100 følelsesord i en stor 2x2 grid (4 kvadranter).
 * Hver kvadrant har sin egen bakgrunnsfarge.
 * Ordene flyter med continuous floating animation.
 *
 * Design: 4-kvadrant grid layout
 * Inspirert av: Marc Brackett's Mood Meter
 *
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function Fase3EmotionLandscape({
  quadrant,
  onEmotionSelect,
}: Fase3EmotionLandscapeProps) {
  const [time, setTime] = useState(0);
  const [clickedEmotionId, setClickedEmotionId] = useState<string | null>(null);

  // Continuous floating animation
  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 0.01);
    }, 16); // ~60fps
    return () => clearInterval(interval);
  }, []);

  const getFloatingOffset = (index: number) => {
    return Math.sin(time + index * 0.5) * 10; // Vertical offset in px
  };

  // Quadrant background colors (20-30% darker for better contrast)
  const getQuadrantBg = (q: 1 | 2 | 3 | 4) => {
    const colors = {
      1: "linear-gradient(135deg, #D65A50 0%, #CC4D3E 50%, #B82020 100%)", // Rød (mørkere)
      2: "linear-gradient(135deg, #E6C300 0%, #CCAA00 50%, #B39000 100%)", // Gul (mørkere)
      3: "linear-gradient(135deg, #6080D0 0%, #4A66CC 50%, #3A4FA8 100%)", // Blå (mørkere)
      4: "linear-gradient(135deg, #78C8A0 0%, #60B088 50%, #4A9966 100%)", // Grønn (mørkere)
    };
    return colors[q];
  };

  // Get quadrant emotions
  const getQuadrantEmotions = (q: 1 | 2 | 3 | 4) => {
    return ALL_EMOTIONS.filter((e) => e.quadrant === q);
  };

  // Handle emotion click with morph animation
  const handleEmotionClick = (emotion: EmotionWord) => {
    setClickedEmotionId(emotion.id);
    // Wait for morph animation to complete before showing definition
    setTimeout(() => {
      onEmotionSelect(emotion);
    }, 300);
  };

  // Render quadrant
  const renderQuadrant = (q: 1 | 2 | 3 | 4) => {
    const emotions = getQuadrantEmotions(q);

    return (
      <div
        key={q}
        className="relative overflow-auto p-4"
        style={{ background: getQuadrantBg(q) }}
      >
        {/* Quadrant Label */}
        <div className="absolute top-4 left-4 z-10 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-full shadow-lg">
          <span className="text-sm font-semibold text-gray-800">
            {q === 1 && "Høy Energi, Ubehagelig"}
            {q === 2 && "Høy Energi, Behagelig"}
            {q === 3 && "Lav Energi, Ubehagelig"}
            {q === 4 && "Lav Energi, Behagelig"}
          </span>
        </div>

        {/* Emotions Grid */}
        <div className="pt-16 grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3 place-items-center min-h-full">
          {emotions.map((emotion, index) => {
            const floatOffset = getFloatingOffset(index);
            const isClicked = clickedEmotionId === emotion.id;
            const hasUniqueSvg = !!emotion.svgPath;

            return (
              <button
                key={emotion.id}
                onClick={() => handleEmotionClick(emotion)}
                className="relative flex items-center justify-center overflow-visible transition-all duration-300 hover:scale-110 hover:shadow-2xl"
                style={{
                  width: "100px",
                  height: "100px",
                  transform: `translateY(${floatOffset}px)`,
                }}
              >
                {/* Square (default state) or SVG (clicked state) */}
                {!isClicked || !hasUniqueSvg ? (
                  // Square shape (before click)
                  <div
                    className="absolute inset-0 flex items-center justify-center rounded-lg animate-breathe"
                    style={{
                      backgroundColor: emotion.color,
                      transition: "all 0.3s ease-out",
                    }}
                  >
                    <span className="relative z-10 drop-shadow-lg text-center px-2 text-white font-semibold text-xs">
                      {emotion.word}
                    </span>
                  </div>
                ) : (
                  // Unique SVG shape (after click)
                  <svg
                    viewBox="0 0 100 100"
                    className="absolute inset-0 w-full h-full animate-morph animate-breathe"
                    style={{
                      transition: "all 0.3s ease-out",
                    }}
                  >
                    <path
                      d={emotion.svgPath}
                      fill={emotion.color}
                      className="drop-shadow-lg"
                    />
                    <text
                      x="50"
                      y="50"
                      textAnchor="middle"
                      dominantBaseline="middle"
                      fill="white"
                      fontSize="8"
                      fontWeight="600"
                      className="drop-shadow-lg"
                    >
                      {emotion.word}
                    </text>
                  </svg>
                )}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <div className="text-center py-6 px-6 bg-white shadow-sm">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Hvilket ord passer best?
        </h2>
        <p className="text-sm text-gray-600">
          Velg det ordet som best beskriver hvordan du føler deg akkurat nå
        </p>
      </div>

      {/* 2x2 Quadrant Grid */}
      <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-0">
        {/* Top row */}
        {renderQuadrant(1)}
        {renderQuadrant(2)}

        {/* Bottom row */}
        {renderQuadrant(3)}
        {renderQuadrant(4)}
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes breathe {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.02);
          }
        }

        @keyframes morph {
          0% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.15);
          }
          100% {
            transform: scale(1);
          }
        }

        .animate-breathe {
          animation: breathe 4s ease-in-out infinite;
        }

        .animate-morph {
          animation: morph 0.3s ease-out;
        }
      `}</style>
    </div>
  );
}

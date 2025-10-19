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

  // Quadrant background colors
  const getQuadrantBg = (q: 1 | 2 | 3 | 4) => {
    const colors = {
      1: "linear-gradient(135deg, #FF8A80 0%, #FF6F61 50%, #E63946 100%)", // Rød
      2: "linear-gradient(135deg, #FFE44D 0%, #FFD700 50%, #F4A300 100%)", // Gul
      3: "linear-gradient(135deg, #8BA3F0 0%, #6A88E3 50%, #4A5FBF 100%)", // Blå
      4: "linear-gradient(135deg, #A8E8C8 0%, #88D8B0 50%, #5FBE8D 100%)", // Grønn
    };
    return colors[q];
  };

  // Get quadrant emotions
  const getQuadrantEmotions = (q: 1 | 2 | 3 | 4) => {
    return ALL_EMOTIONS.filter((e) => e.quadrant === q);
  };

  // Shape styling with CSS clip-path
  const getShapeStyle = (emotion: EmotionWord) => {
    const baseSize = 100; // Smaller for grid layout
    switch (emotion.shape) {
      case "circle":
        return {
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          borderRadius: "50%",
        };
      case "diamond":
        return {
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          borderRadius: "10%",
          transform: "rotate(45deg)",
        };
      case "rounded-square":
        return {
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          borderRadius: "25%",
        };
      case "hexagon":
        return {
          width: `${baseSize}px`,
          height: `${baseSize * 1.15}px`,
          clipPath: "polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)",
        };
      case "star-6":
        return {
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          clipPath: "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
        };
      case "star-8":
        return {
          width: `${baseSize}px`,
          height: `${baseSize}px`,
          clipPath: "polygon(50% 0%, 65% 35%, 100% 50%, 65% 65%, 50% 100%, 35% 65%, 0% 50%, 35% 35%)",
        };
    }
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
            const shapeStyle = getShapeStyle(emotion);

            return (
              <button
                key={emotion.id}
                onClick={() => onEmotionSelect(emotion)}
                className="flex items-center justify-center text-white font-semibold text-xs transition-all duration-300 hover:scale-110 hover:shadow-2xl relative"
                style={{
                  ...shapeStyle,
                  backgroundColor: emotion.color,
                  transform: `translateY(${floatOffset}px) ${emotion.shape === 'diamond' ? 'rotate(45deg)' : ''}`,
                  transition: "transform 0.3s ease-out, box-shadow 0.3s ease-out",
                }}
              >
                {/* Word */}
                <span
                  className="relative z-10 drop-shadow-lg text-center px-2"
                  style={{ transform: emotion.shape === 'diamond' ? 'rotate(-45deg)' : 'none' }}
                >
                  {emotion.word}
                </span>
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
    </div>
  );
}

"use client";

import React, { useRef, useState, useEffect } from "react";
import { getEmotionsByQuadrant, type EmotionWord } from "./emotionData";

interface Fase3EmotionLandscapeProps {
  quadrant: 1 | 2 | 3 | 4;
  onEmotionSelect: (emotion: EmotionWord) => void;
}

/**
 * Fase 3: Følelseslandskapet
 *
 * Et stort, draggbart canvas med 36 følelsesord for den valgte kvadranten.
 * Hvert ord har sin egen farge (gradient i kvadrantens farge) og organisk form.
 *
 * Features:
 * - Horizontal dragging/scrolling for å utforske ord
 * - Kontinuerlig, rolig bevegelse (flyter som i vann)
 * - Smooth parallax-effekt når bruker drar
 * - Click/tap på ord for å velge
 *
 * Design: Organisk, rolig, meditativ atmosfære
 * Inspirert av: How We Feel (HWF) app
 *
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function Fase3EmotionLandscape({
  quadrant,
  onEmotionSelect,
}: Fase3EmotionLandscapeProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);
  const [time, setTime] = useState(0);

  const emotions = getEmotionsByQuadrant(quadrant);

  // Get quadrant color
  const getQuadrantColor = () => {
    const colors = {
      1: {
        primary: "var(--color-emotion-q1-primary)",
        light: "var(--color-emotion-q1-light)",
        dark: "var(--color-emotion-q1-dark)",
      },
      2: {
        primary: "var(--color-emotion-q2-primary)",
        light: "var(--color-emotion-q2-light)",
        dark: "var(--color-emotion-q2-dark)",
      },
      3: {
        primary: "var(--color-emotion-q3-primary)",
        light: "var(--color-emotion-q3-light)",
        dark: "var(--color-emotion-q3-dark)",
      },
      4: {
        primary: "var(--color-emotion-q4-primary)",
        light: "var(--color-emotion-q4-light)",
        dark: "var(--color-emotion-q4-dark)",
      },
    };
    return colors[quadrant];
  };

  const colors = getQuadrantColor();

  // Continuous floating animation
  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 0.01);
    }, 16); // ~60fps

    return () => clearInterval(interval);
  }, []);

  // Mouse/touch drag handlers
  const handleDragStart = (e: React.MouseEvent | React.TouchEvent) => {
    setIsDragging(true);
    const pageX = "touches" in e ? e.touches[0].pageX : e.pageX;
    setStartX(pageX - (containerRef.current?.offsetLeft || 0));
    setScrollLeft(containerRef.current?.scrollLeft || 0);
  };

  const handleDragMove = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDragging) return;
    e.preventDefault();
    const pageX = "touches" in e ? e.touches[0].pageX : e.pageX;
    const x = pageX - (containerRef.current?.offsetLeft || 0);
    const walk = (x - startX) * 2; // Scroll speed multiplier
    if (containerRef.current) {
      containerRef.current.scrollLeft = scrollLeft - walk;
    }
  };

  const handleDragEnd = () => {
    setIsDragging(false);
  };

  // Get color for specific emotion - now using direct HEX from Mood Meter
  const getEmotionColor = (emotion: EmotionWord) => {
    return emotion.color; // Direct HEX color from emotionData
  };

  // Get floating animation offset
  const getFloatingOffset = (index: number) => {
    return Math.sin(time + index * 0.5) * 10; // Vertical offset in px
  };

  // Get shape style based on emotion shape
  const getShapeStyle = (emotion: EmotionWord) => {
    const baseSize = 140;
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

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <div className="text-center py-8 px-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-3">
          Hvilket ord passer best?
        </h2>
        <p className="text-base text-gray-600">
          Dra fingeren sidelengs for å utforske, trykk for å velge
        </p>
      </div>

      {/* Scrollable Emotion Landscape */}
      <div
        ref={containerRef}
        className="flex-1 overflow-x-auto overflow-y-hidden cursor-grab active:cursor-grabbing"
        onMouseDown={handleDragStart}
        onMouseMove={handleDragMove}
        onMouseUp={handleDragEnd}
        onMouseLeave={handleDragEnd}
        onTouchStart={handleDragStart}
        onTouchMove={handleDragMove}
        onTouchEnd={handleDragEnd}
        style={{
          scrollbarWidth: "none", // Firefox
          msOverflowStyle: "none", // IE/Edge
        }}
      >
        <div className="flex items-center gap-8 px-12 py-24 min-w-max">
          {emotions.map((emotion, index) => {
            const floatOffset = getFloatingOffset(index);
            const shapeStyle = getShapeStyle(emotion);
            const bgColor = getEmotionColor(emotion);

            return (
              <button
                key={emotion.id}
                onClick={() => onEmotionSelect(emotion)}
                className="flex-shrink-0 flex items-center justify-center text-white font-semibold text-lg transition-all duration-300 hover:scale-110 hover:shadow-2xl relative"
                style={{
                  ...shapeStyle,
                  backgroundColor: bgColor,
                  transform: `translateY(${floatOffset}px)`,
                  transition: "transform 0.3s ease-out, box-shadow 0.3s ease-out",
                }}
              >
                {/* Glow effect on hover */}
                <div
                  className="absolute inset-0 rounded-full opacity-0 hover:opacity-40 transition-opacity duration-500"
                  style={{
                    background: `radial-gradient(circle, ${colors.light}, transparent)`,
                    filter: "blur(20px)",
                  }}
                />

                {/* Word */}
                <span className="relative z-10 drop-shadow-lg px-4 text-center">
                  {emotion.word}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Hide scrollbar */}
      <style jsx>{`
        div::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </div>
  );
}

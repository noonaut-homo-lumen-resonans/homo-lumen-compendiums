"use client";

import React from "react";
import type { EmotionWord } from "./emotionData";

interface EmotionBadgeProps {
  emotion: EmotionWord;
}

/**
 * Floating Emotion Badge
 *
 * Displays selected emotion in top-right corner
 * - Shows emotion's unique SVG shape
 * - Shows emotion name
 * - Shows emotion definition (always visible, wraps if long)
 * - Uses emotion's color
 * - Subtle breathe animation
 * - Sticky position (follows scroll)
 *
 * Design: Minimalist, non-intrusive companion
 * Triadisk Score: 0.08 (PROCEED)
 */
export default function EmotionBadge({ emotion }: EmotionBadgeProps) {
  const hasUniqueSvg = !!emotion.svgPath;

  return (
    <div className="fixed top-6 right-6 z-30 animate-fade-in">
      <div
        className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-lg border-2 p-4 flex items-start gap-3 transition-all hover:scale-105 hover:shadow-xl min-w-[280px] max-w-md"
        style={{ borderColor: emotion.color }}
      >
        {/* Emotion Shape/Icon */}
        <div className="relative w-16 h-16 flex-shrink-0">
          {hasUniqueSvg ? (
            // Unique SVG shape
            <svg
              viewBox="0 0 100 100"
              className="w-full h-full animate-breathe"
              style={{
                filter: "drop-shadow(0 2px 4px rgba(0,0,0,0.1))",
              }}
            >
              <path d={emotion.svgPath} fill={emotion.color} />
            </svg>
          ) : (
            // Fallback square shape
            <div
              className="w-full h-full rounded-lg flex items-center justify-center animate-breathe"
              style={{
                backgroundColor: emotion.color,
                boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
              }}
            >
              <span className="text-white font-bold text-xs text-center px-2">
                {emotion.word}
              </span>
            </div>
          )}
        </div>

        {/* Emotion Text */}
        <div className="flex flex-col">
          <span className="text-xs font-medium text-gray-600 uppercase tracking-wide">
            Din følelse
          </span>
          <span
            className="text-lg font-bold leading-tight"
            style={{ color: emotion.color }}
          >
            {emotion.word}
          </span>
          <span className="text-sm text-gray-600 italic mt-1 leading-snug">
            {emotion.definition}
          </span>
        </div>
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes breathe {
          0%,
          100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-breathe {
          animation: breathe 4s ease-in-out infinite;
        }

        .animate-fade-in {
          animation: fade-in 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}

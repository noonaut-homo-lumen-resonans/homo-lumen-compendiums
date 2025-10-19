"use client";

import React, { useState, useEffect } from "react";
import { ArrowRight, ArrowLeft } from "lucide-react";
import type { EmotionWord } from "./emotionData";
import { getKairosWindowFromBigFive, getKairosAdjustedDefinition, type KairosWindow } from "@/utils/kairosMapping";
import { affectBus } from "@/utils/affectBus";
import { loadBigFive } from "@/utils/bigfive/mergeProfiles";

interface Fase4DefinitionProps {
  emotion: EmotionWord;
  onContinue: () => void;
  onBack?: () => void; // Optional callback to go back and choose different emotion
}

/**
 * Fase 4: Ordets Betydning
 *
 * En liten pop-up boks nederst på skjermen som viser:
 * - Det valgte følelsesorder
 * - En kort, nøytral definisjon
 * - En pil-knapp for å fortsette
 *
 * Design: Minimalistisk, rolig, kunnskapsbyggende
 * Inspirert av: How We Feel (HWF) app
 *
 * Triadisk Score: 0.10 (PROCEED)
 */
export default function Fase4Definition({
  emotion,
  onContinue,
  onBack,
}: Fase4DefinitionProps) {
  const [kairosWindow, setKairosWindow] = useState<KairosWindow | null>(null);
  const [adjustedDefinition, setAdjustedDefinition] = useState<string>(emotion.definition);
  const [showExtendedInfo, setShowExtendedInfo] = useState<boolean>(false);

  // Compute Kairos Window on mount
  useEffect(() => {
    const bigFive = loadBigFive();
    if (bigFive) {
      const latestAffect = affectBus.getLatest();
      const window = getKairosWindowFromBigFive(bigFive, {
        valence: latestAffect?.valence ?? 0,
        arousal: latestAffect?.arousal ?? 0.5,
        hrvRmssd: latestAffect?.hrvRmssd ?? 50,
      });
      setKairosWindow(window);

      // Adjust definition based on complexity
      const adjusted = getKairosAdjustedDefinition(emotion.definition, window);
      setAdjustedDefinition(adjusted.definition);
      setShowExtendedInfo(adjusted.showExtendedInfo);
    }
  }, [emotion.definition]);

  // Get quadrant color
  const getQuadrantColor = () => {
    const colors = {
      1: "var(--color-emotion-q1-primary)",
      2: "var(--color-emotion-q2-primary)",
      3: "var(--color-emotion-q3-primary)",
      4: "var(--color-emotion-q4-primary)",
    };
    return colors[emotion.quadrant];
  };

  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-end justify-center z-50 p-0">
      {/* Pop-up Box */}
      <div
        className="w-full bg-white rounded-t-3xl shadow-2xl transform transition-all duration-500 ease-out animate-slide-up"
      >
        {/* Color accent bar */}
        <div
          className="h-2 rounded-t-3xl"
          style={{ backgroundColor: getQuadrantColor() }}
        />

        {/* Content */}
        <div className="p-8 pb-10">
          <div className="mb-6">
            <h3
              className="text-3xl font-bold mb-4"
              style={{ color: getQuadrantColor() }}
            >
              {emotion.word}
            </h3>
            <p className="text-lg text-gray-700 leading-relaxed">
              {adjustedDefinition}
            </p>

            {/* Extended info for high complexity users */}
            {showExtendedInfo && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 italic">
                  💡 <strong>Dypere forståelse:</strong> Denne følelsen oppstår ofte i{" "}
                  {emotion.quadrant === 1 || emotion.quadrant === 4 ? "trygge" : "utfordrende"} situasjoner
                  og kan påvirke både kroppens spenningsnivå og tankemønstre.
                </p>
              </div>
            )}
          </div>

          {/* Buttons */}
          <div className="flex gap-3">
            {/* Back Button - optional */}
            {onBack && (
              <button
                onClick={onBack}
                className="flex items-center justify-center gap-2 px-6 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 hover:shadow-lg border-2"
                style={{
                  borderColor: getQuadrantColor(),
                  color: getQuadrantColor(),
                  backgroundColor: "white",
                }}
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Velg annen</span>
              </button>
            )}

            {/* Continue Button */}
            <button
              onClick={onContinue}
              className="flex-1 flex items-center justify-between px-6 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 hover:shadow-lg group"
              style={{
                backgroundColor: getQuadrantColor(),
                color: "white",
              }}
            >
              <span>Fortsett</span>
              <ArrowRight className="w-6 h-6 transition-transform duration-300 group-hover:translate-x-2" />
            </button>
          </div>
        </div>
      </div>

      {/* CSS Animation */}
      <style jsx>{`
        @keyframes slide-up {
          from {
            transform: translateY(100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        .animate-slide-up {
          animation: slide-up 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}

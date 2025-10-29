"use client";

import React from "react";
import EmotionQuadrant from "@/components/mestring/EmotionQuadrant";
import Button from "@/components/ui/Button";
import { ArrowRight } from "lucide-react";

interface Stage1EmotionsProps {
  selectedEmotions: { word: string; quadrant: number | null }[];
  onChange: (emotions: { word: string; quadrant: number | null }[]) => void;
  onNext: () => void;
}

/**
 * Stage 1: Emotion Check-in
 *
 * First step in the multi-stage flow.
 * User selects emotions from 100 Norwegian words organized in 4 quadrants.
 *
 * Triadisk Score: 0.1 (PROCEED)
 */
export default function Stage1Emotions({
  selectedEmotions,
  onChange,
  onNext,
}: Stage1EmotionsProps) {
  const canProceed = selectedEmotions.length > 0;

  return (
    <div className="w-full max-w-6xl mx-auto fade-in">
      {/* Progress indicator - Path lighting up */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full fill-path"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <p className="text-sm text-gray-600">Steg 1 av 4: Følelser</p>
      </div>

      {/* Intro text - NVC: Validering før spørsmål */}
      <div className="mb-8 text-left">
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-4 rounded">
          <p className="text-sm text-blue-800">
            💙 Det du opplever akkurat nå er helt naturlig. Alle følelser er velkomne her.
          </p>
        </div>
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Hvordan kjennes det akkurat nå?
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)] mb-3">
          Velg ord som beskriver dine følelser. Du kan velge så mange du vil.
          Jo mer presist du beskriver følelsene dine, desto bedre kan vi hjelpe deg.
        </p>
        <p className="text-sm text-gray-600 italic">
          💡 Tips: Det er ingen «riktige» eller «gale» følelser. Dette er din opplevelse, og den er gyldig.
        </p>
      </div>

      {/* Emotion Quadrant */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <EmotionQuadrant
          selectedEmotions={selectedEmotions}
          onChange={onChange}
        />
      </div>

      {/* Navigation - Triadisk Port 1: Bruker-suverenitet */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <div className="text-sm">
            {selectedEmotions.length === 0 ? (
              <p className="text-gray-500">Velg minst én følelse for å fortsette</p>
            ) : (
              <div className="flex items-center gap-2">
                <span className="sprout-animation text-xl">🌱</span>
                <p className="text-gray-700 font-medium">
                  {selectedEmotions.length} {selectedEmotions.length === 1 ? "følelse" : "følelser"} valgt
                </p>
              </div>
            )}
          </div>
          {/* Hopp over knapp - Port 1: Kognitiv suverenitet */}
          <Button
            variant="text"
            size="medium"
            onClick={onNext}
            className="text-gray-500 hover:text-gray-700"
          >
            Hopp over dette steget →
          </Button>
        </div>
        <Button
          variant="primary"
          size="large"
          onClick={onNext}
          disabled={!canProceed}
          rightIcon={<ArrowRight className="h-5 w-5" />}
          className={canProceed ? "calm-hover" : ""}
        >
          Neste: Trykk & Signaler
        </Button>
      </div>
    </div>
  );
}

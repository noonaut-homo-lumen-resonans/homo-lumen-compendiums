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
    <div className="w-full max-w-6xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <p className="text-sm text-gray-600">Steg 1 av 4: Følelser</p>
      </div>

      {/* Intro text */}
      <div className="mb-8 text-left">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Hvordan kjennes det akkurat nå?
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)]">
          Velg ord som beskriver dine følelser. Du kan velge så mange du vil.
          Jo mer presist du beskriver følelsene dine, desto bedre kan vi hjelpe deg.
        </p>
      </div>

      {/* Emotion Quadrant */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <EmotionQuadrant
          selectedEmotions={selectedEmotions}
          onChange={onChange}
        />
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <p className="text-sm text-gray-600">
          {selectedEmotions.length === 0 ? (
            "Velg minst én følelse for å fortsette"
          ) : (
            `${selectedEmotions.length} ${selectedEmotions.length === 1 ? "følelse" : "følelser"} valgt`
          )}
        </p>
        <Button
          variant="primary"
          size="large"
          onClick={onNext}
          disabled={!canProceed}
          rightIcon={<ArrowRight className="h-5 w-5" />}
        >
          Neste: Trykk & Signaler
        </Button>
      </div>
    </div>
  );
}

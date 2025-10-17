"use client";

import React from "react";
import StressSlider from "@/components/mestring/StressSlider";
import SomaticSignals from "@/components/mestring/SomaticSignals";
import Button from "@/components/ui/Button";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { SomaticSignal } from "@/types";

interface Stage2SignalsProps {
  stressLevel: number;
  onStressChange: (level: number) => void;
  somaticSignals: SomaticSignal[];
  onSignalsChange: (signals: SomaticSignal[]) => void;
  onBack: () => void;
  onNext: () => void;
}

/**
 * Stage 2: Trykk & Signaler
 *
 * Second step: User indicates stress level (1-10) and somatic awareness.
 * This determines polyvagal state and informs Lira's questions.
 *
 * Triadisk Score: 0.15 (PROCEED)
 */
export default function Stage2Signals({
  stressLevel,
  onStressChange,
  somaticSignals,
  onSignalsChange,
  onBack,
  onNext,
}: Stage2SignalsProps) {
  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <p className="text-sm text-gray-600">Steg 2 av 4: Trykk & Signaler</p>
      </div>

      {/* Intro text */}
      <div className="mb-8 text-left">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Hvor høyt er trykket nå?
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)]">
          Hjelp oss å forstå ditt stressnivå og hva kroppen din forteller deg.
        </p>
      </div>

      <div className="space-y-8">
        {/* Stress Slider */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <StressSlider value={stressLevel} onChange={onStressChange} />
        </div>

        {/* Somatic Signals */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <SomaticSignals
            signals={somaticSignals}
            onChange={onSignalsChange}
          />
        </div>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center mt-8">
        <Button
          variant="secondary"
          size="large"
          onClick={onBack}
          leftIcon={<ArrowLeft className="h-5 w-5" />}
        >
          Tilbake
        </Button>
        <Button
          variant="primary"
          size="large"
          onClick={onNext}
          rightIcon={<ArrowRight className="h-5 w-5" />}
        >
          Neste: Chat med Lira
        </Button>
      </div>
    </div>
  );
}

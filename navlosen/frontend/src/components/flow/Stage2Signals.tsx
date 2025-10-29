"use client";

import React from "react";
import StressSlider from "@/components/mestring/StressSlider";
import SomaticSignals from "@/components/mestring/SomaticSignals";
import CrisisBanner from "@/components/safety/CrisisBanner";
import Button from "@/components/ui/Button";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { SomaticSignal } from "@/types";

interface Stage2SignalsProps {
  stressLevel: number;
  onStressChange: (level: number) => void;
  somaticSignals: SomaticSignal[];
  onSignalsChange: (signals: SomaticSignal[]) => void;
  selectedEmotions?: string[]; // For crisis detection
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
  selectedEmotions = [],
  onBack,
  onNext,
}: Stage2SignalsProps) {
  // Crisis detection
  const showCrisisBanner = stressLevel >= 9;
  return (
    <div className="w-full max-w-6xl mx-auto fade-in">
      {/* Progress indicator - Path continues */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full fill-path"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <p className="text-sm text-gray-600">Steg 2 av 4: Trykk & Signaler</p>
      </div>

      {/* Intro text - NVC: Validering og normalisering */}
      <div className="mb-8 text-left">
        <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4 rounded">
          <p className="text-sm text-green-800">
            🌿 Kroppen din kommuniserer med deg hele tiden. La oss lytte sammen.
          </p>
        </div>
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Hvor høyt er trykket nå?
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)] mb-3">
          Hjelp oss å forstå ditt stressnivå og hva kroppen din forteller deg.
        </p>
        <p className="text-sm text-gray-600 italic">
          💡 Tips: Det er normalt at kroppen reagerer på stress. Dette er informasjon, ikke noe du trenger å fikse.
        </p>
      </div>

      <div className="space-y-8">
        {/* Stress Slider */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <StressSlider value={stressLevel} onChange={onStressChange} />
        </div>

        {/* Crisis Banner - Show if stress 9-10 */}
        {showCrisisBanner && (
          <CrisisBanner visible={true} variant="full" />
        )}

        {/* Somatic Signals */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <SomaticSignals
            signals={somaticSignals}
            onChange={onSignalsChange}
          />
        </div>
      </div>

      {/* Navigation - Triadisk Port 1: Bruker-suverenitet */}
      <div className="flex justify-between items-center mt-8">
        <div className="flex items-center gap-4">
          <Button
            variant="secondary"
            size="large"
            onClick={onBack}
            leftIcon={<ArrowLeft className="h-5 w-5" />}
            className="calm-hover"
          >
            Tilbake
          </Button>
          {/* Hopp over knapp */}
          <Button
            variant="text"
            size="medium"
            onClick={onNext}
            className="text-gray-500 hover:text-gray-700"
          >
            Hopp over →
          </Button>
        </div>
        <Button
          variant="primary"
          size="large"
          onClick={onNext}
          rightIcon={<ArrowRight className="h-5 w-5" />}
          className="calm-hover"
        >
          Neste: Chat med Lira
        </Button>
      </div>
    </div>
  );
}

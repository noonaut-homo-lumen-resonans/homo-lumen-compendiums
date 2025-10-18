"use client";

import React, { useState } from "react";
import { BigFive } from "@/types";
import Button from "@/components/ui/Button";
import { X, CheckCircle, AlertCircle } from "lucide-react";

interface BigFiveSurveyProps {
  onComplete: (bigFive: BigFive) => void;
  onCancel: () => void;
  polyvagalState?: "ventral" | "sympathetic" | "dorsal";
}

interface SurveyItem {
  id: string;
  text: string;
  trait: "O" | "C" | "E" | "A" | "N";
  reverse?: boolean; // Reverse-coded items
}

/**
 * BigFiveSurvey Component
 *
 * Voluntary Big Five personality questionnaire using Mini-IPIP (20 items, 4 per trait).
 * Polyvagal-safe design:
 * - Dorsal: Survey blocked with empathetic message
 * - Sympathetic: Quick 2-3 item version offered
 * - Ventral: Full 20-item survey available
 *
 * Based on Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006).
 * The Mini-IPIP Scales: Tiny-yet-effective measures of the Big Five.
 *
 * Triadisk Score: 0.16 (PROCEED)
 */
export default function BigFiveSurvey({
  onComplete,
  onCancel,
  polyvagalState = "ventral",
}: BigFiveSurveyProps) {
  const [responses, setResponses] = useState<Record<string, number>>({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const [useQuickMode, setUseQuickMode] = useState(false);

  // Mini-IPIP items (Norwegian translation)
  const fullItems: SurveyItem[] = [
    // Extraversion (E)
    { id: "E1", text: "Jeg er sjeleglad på fester", trait: "E" },
    { id: "E2", text: "Jeg holder meg i bakgrunnen", trait: "E", reverse: true },
    { id: "E3", text: "Jeg snakker med mange forskjellige mennesker på fester", trait: "E" },
    { id: "E4", text: "Jeg liker ikke å trekke oppmerksomhet til meg selv", trait: "E", reverse: true },

    // Agreeableness (A)
    { id: "A1", text: "Jeg sympatiserer med andres følelser", trait: "A" },
    { id: "A2", text: "Jeg er ikke interessert i andres problemer", trait: "A", reverse: true },
    { id: "A3", text: "Jeg føler andres emosjoner", trait: "A" },
    { id: "A4", text: "Jeg er ikke virkelig interessert i andre", trait: "A", reverse: true },

    // Conscientiousness (C)
    { id: "C1", text: "Jeg får ting gjort med en gang", trait: "C" },
    { id: "C2", text: "Jeg glemmer ofte å legge ting tilbake der de hører hjemme", trait: "C", reverse: true },
    { id: "C3", text: "Jeg liker orden", trait: "C" },
    { id: "C4", text: "Jeg gjør rot i tingene mine", trait: "C", reverse: true },

    // Neuroticism (N)
    { id: "N1", text: "Jeg har hyppige humørsvingninger", trait: "N" },
    { id: "N2", text: "Jeg er avslappet mesteparten av tiden", trait: "N", reverse: true },
    { id: "N3", text: "Jeg blir lett opprørt", trait: "N" },
    { id: "N4", text: "Jeg er sjelden bekymret", trait: "N", reverse: true },

    // Openness (O)
    { id: "O1", text: "Jeg har en livlig fantasi", trait: "O" },
    { id: "O2", text: "Jeg har ikke tid for andres drømmerier", trait: "O", reverse: true },
    { id: "O3", text: "Jeg er full av ideer", trait: "O" },
    { id: "O4", text: "Jeg liker ikke abstrakte ideer", trait: "O", reverse: true },
  ];

  // Quick mode: 2 items per trait (10 total)
  const quickItems = fullItems.filter((_, idx) => idx % 2 === 0);

  const items = useQuickMode ? quickItems : fullItems;
  const currentItem = items[currentIndex];

  // Polyvagal-safe blocking
  if (polyvagalState === "dorsal") {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div className="flex items-center gap-3 mb-4">
            <AlertCircle className="w-8 h-8 text-blue-500" />
            <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
              Ta det med ro nå
            </h3>
          </div>
          <p className="text-[var(--color-text-secondary)] mb-4">
            Jeg ser at du er i en overveldet tilstand akkurat nå. Personlighetsspørreskjemaet kan vente.
            Kom tilbake når du føler deg mer rolig og trygg. ❤️
          </p>
          <Button onClick={onCancel} variant="primary" size="large" fullWidth>
            Greit, jeg kommer tilbake senere
          </Button>
        </div>
      </div>
    );
  }

  const calculateBigFive = (): BigFive => {
    const traits = ["O", "C", "E", "A", "N"] as const;
    const scores: Partial<BigFive> = {};

    traits.forEach((trait) => {
      const traitItems = items.filter((item) => item.trait === trait);
      let sum = 0;

      traitItems.forEach((item) => {
        const response = responses[item.id];
        if (response !== undefined) {
          // Reverse-coded items
          const value = item.reverse ? 6 - response : response;
          sum += value;
        }
      });

      // Normalize to 0..1
      const maxScore = traitItems.length * 5; // 5-point scale
      scores[trait] = sum / maxScore;
    });

    return {
      ...scores,
      updatedAt: new Date().toISOString(),
      source: "self_report",
      uncertainty: {
        O: 0.2,
        C: 0.2,
        E: 0.2,
        A: 0.2,
        N: 0.2,
      },
    } as BigFive;
  };

  const handleResponse = (value: number) => {
    setResponses({ ...responses, [currentItem.id]: value });

    if (currentIndex < items.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Survey complete
      const bigFive = calculateBigFive();
      onComplete(bigFive);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const progress = ((currentIndex + 1) / items.length) * 100;

  // Offer quick mode in sympathetic state
  if (polyvagalState === "sympathetic" && !useQuickMode && currentIndex === 0) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
              Lås opp mer presise forslag?
            </h3>
            <button onClick={onCancel} className="text-gray-500 hover:text-gray-700">
              <X className="w-5 h-5" />
            </button>
          </div>

          <p className="text-[var(--color-text-secondary)] mb-4">
            Du kan svare på noen korte spørsmål om hvordan du vanligvis er (ikke bare nå), slik at Lira kan gi deg bedre tilpassede anbefalinger.
          </p>

          <div className="space-y-3">
            <Button
              onClick={() => setUseQuickMode(true)}
              variant="primary"
              size="large"
              fullWidth
            >
              Ja, kjapp versjon (10 spørsmål)
            </Button>
            <Button
              onClick={() => setUseQuickMode(false)}
              variant="secondary"
              size="large"
              fullWidth
            >
              Full versjon (20 spørsmål)
            </Button>
            <Button onClick={onCancel} variant="text" size="large" fullWidth>
              Ikke nå, takk
            </Button>
          </div>

          <p className="text-xs text-gray-500 mt-4 italic">
            💡 Du kan når som helst endre eller slette denne dataen.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
            Personlighetsprofil ({useQuickMode ? "Kjapp" : "Full"})
          </h3>
          <button onClick={onCancel} className="text-gray-500 hover:text-gray-700">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Progress bar */}
        <div className="mb-6">
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-500 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Spørsmål {currentIndex + 1} av {items.length}
          </p>
        </div>

        {/* Question */}
        <div className="mb-8">
          <p className="text-xl font-semibold text-[var(--color-text-primary)] mb-6">
            {currentItem.text}
          </p>

          {/* 5-point Likert scale */}
          <div className="space-y-2">
            {[
              { value: 1, label: "Helt uenig" },
              { value: 2, label: "Uenig" },
              { value: 3, label: "Nøytral" },
              { value: 4, label: "Enig" },
              { value: 5, label: "Helt enig" },
            ].map((option) => (
              <button
                key={option.value}
                onClick={() => handleResponse(option.value)}
                className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
                  responses[currentItem.id] === option.value
                    ? "border-purple-500 bg-purple-50"
                    : "border-gray-200 hover:border-purple-300 hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-[var(--color-text-primary)]">
                    {option.label}
                  </span>
                  {responses[currentItem.id] === option.value && (
                    <CheckCircle className="w-5 h-5 text-purple-500" />
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <Button
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            variant="text"
            size="medium"
          >
            ← Forrige
          </Button>

          <Button onClick={onCancel} variant="text" size="medium">
            Avbryt
          </Button>
        </div>

        {/* Info */}
        <div className="mt-6 p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-900">
          <p>
            <strong>💡 Hvorfor spør vi om dette?</strong> Personlighet påvirker ikke hva du føler nå (det måler vi allerede), men kan hjelpe oss å velge riktig språk og tempo i anbefalingene.
          </p>
        </div>
      </div>
    </div>
  );
}

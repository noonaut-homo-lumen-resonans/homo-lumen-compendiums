"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { Emotion } from "@/types";

interface EmotionWheelProps {
  selectedEmotions: string[];
  onChange: (emotions: string[]) => void;
  className?: string;
}

/**
 * EmotionWheel Component
 *
 * Emotion check-in with 8 core emotions
 * Based on circumplex model (valence × energy)
 *
 * Emotions mapped on two dimensions:
 * - Valence: Positive (green) vs Negative (red)
 * - Energy: High (bright) vs Low (muted)
 *
 * @example
 * <EmotionWheel
 *   selectedEmotions={emotions}
 *   onChange={setEmotions}
 * />
 */
export default function EmotionWheel({
  selectedEmotions,
  onChange,
  className,
}: EmotionWheelProps) {
  const emotions: Emotion[] = [
    // High energy, positive (8 emotions)
    { id: "gledelig", label: "Gledelig", valence: "positive", energy: "high" },
    { id: "entusiastisk", label: "Entusiastisk", valence: "positive", energy: "high" },
    { id: "inspirert", label: "Inspirert", valence: "positive", energy: "high" },
    { id: "optimistisk", label: "Optimistisk", valence: "positive", energy: "high" },
    { id: "spent-positivt", label: "Spent (positivt)", valence: "positive", energy: "high" },
    { id: "energisk", label: "Energisk", valence: "positive", energy: "high" },
    { id: "leken", label: "Leken", valence: "positive", energy: "high" },
    { id: "stolt", label: "Stolt", valence: "positive", energy: "high" },

    // Low energy, positive (8 emotions)
    { id: "rolig", label: "Rolig", valence: "positive", energy: "low" },
    { id: "takknemlig", label: "Takknemlig", valence: "positive", energy: "low" },
    { id: "trygg", label: "Trygg", valence: "positive", energy: "low" },
    { id: "tilfreds", label: "Tilfreds", valence: "positive", energy: "low" },
    { id: "fokusert", label: "Fokusert", valence: "positive", energy: "low" },
    { id: "fredelig", label: "Fredelig", valence: "positive", energy: "low" },
    { id: "håpefull", label: "Håpefull", valence: "positive", energy: "low" },
    { id: "avslappet", label: "Avslappet", valence: "positive", energy: "low" },

    // High energy, negative (8 emotions)
    { id: "frustrert", label: "Frustrert", valence: "negative", energy: "high" },
    { id: "sint", label: "Sint", valence: "negative", energy: "high" },
    { id: "irritert", label: "Irritert", valence: "negative", energy: "high" },
    { id: "engstelig", label: "Engstelig", valence: "negative", energy: "high" },
    { id: "nervøs", label: "Nervøs", valence: "negative", energy: "high" },
    { id: "urolig", label: "Urolig", valence: "negative", energy: "high" },
    { id: "overveldet", label: "Overveldet", valence: "negative", energy: "high" },
    { id: "stresset", label: "Stresset", valence: "negative", energy: "high" },

    // Low energy, negative (8 emotions)
    { id: "trist", label: "Trist", valence: "negative", energy: "low" },
    { id: "nedfor", label: "Nedfor", valence: "negative", energy: "low" },
    { id: "utmattet", label: "Utmattet", valence: "negative", energy: "low" },
    { id: "sårbar", label: "Sårbar", valence: "negative", energy: "low" },
    { id: "ensom", label: "Ensom", valence: "negative", energy: "low" },
    { id: "fortvilet", label: "Fortvilet", valence: "negative", energy: "low" },
    { id: "nummen", label: "Nummen", valence: "negative", energy: "low" },
    { id: "håpløs", label: "Håpløs", valence: "negative", energy: "low" },
  ];

  const getEmotionColor = (emotion: Emotion): string => {
    if (emotion.valence === "positive" && emotion.energy === "high") {
      return "bg-green-100 text-green-700 border-green-300 hover:bg-green-200";
    }
    if (emotion.valence === "positive" && emotion.energy === "low") {
      return "bg-blue-100 text-blue-700 border-blue-300 hover:bg-blue-200";
    }
    if (emotion.valence === "negative" && emotion.energy === "high") {
      return "bg-orange-100 text-orange-700 border-orange-300 hover:bg-orange-200";
    }
    // negative + low
    return "bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200";
  };

  const toggleEmotion = (emotionId: string) => {
    if (selectedEmotions.includes(emotionId)) {
      onChange(selectedEmotions.filter((id) => id !== emotionId));
    } else {
      onChange([...selectedEmotions, emotionId]);
    }
  };

  return (
    <div className={cn("w-full text-left", className)}>
      <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-4 text-left">
        Hvordan kjennes det akkurat nå?
      </h3>

      <p className="text-sm text-[var(--color-text-secondary)] mb-4 text-left">
        Velg en eller flere emosjoner som beskriver hvordan du har det. Jo mer
        presist du kan navngi følelsene dine, desto lettere blir det å regulere dem.
      </p>

      {/* Emotion grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-2">
        {emotions.map((emotion) => {
          const isSelected = selectedEmotions.includes(emotion.id);
          const colorClasses = getEmotionColor(emotion);

          return (
            <button
              key={emotion.id}
              onClick={() => toggleEmotion(emotion.id)}
              className={cn(
                "px-4 py-3 rounded-lg border-2 font-medium text-sm",
                "transition-all duration-200",
                "focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-primary)]",
                colorClasses,
                {
                  "ring-2 ring-offset-2 ring-[var(--color-primary)] scale-105":
                    isSelected,
                }
              )}
              aria-pressed={isSelected}
              aria-label={`Velg emosjon: ${emotion.label}`}
            >
              {emotion.label}
            </button>
          );
        })}
      </div>

      {/* Selected emotions summary */}
      {selectedEmotions.length > 0 && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>Du har valgt:</strong>{" "}
            {selectedEmotions
              .map(
                (id) => emotions.find((e) => e.id === id)?.label || id
              )
              .join(", ")}
          </p>
        </div>
      )}

      {/* Legend & Educational Info */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="text-sm font-semibold text-blue-900 mb-3">
          💡 Følelseshjulet - Lær å kjenne dine følelser
        </h4>
        <p className="text-xs text-blue-800 mb-3">
          Følelser kan beskrives langs to dimensjoner: <strong>valens</strong> (positiv/negativ)
          og <strong>energi</strong> (høy/lav). Dette hjelper deg å finne mer presise ord for
          hvordan du har det.
        </p>
        <div className="grid grid-cols-2 gap-3 text-xs text-blue-900">
          <div className="flex items-start gap-2">
            <span className="inline-block w-4 h-4 bg-green-100 border border-green-400 rounded flex-shrink-0 mt-0.5" />
            <div>
              <strong>Positiv + Energisk:</strong> Du føler deg bra og har mye krefter
              (f.eks. gledelig, entusiastisk)
            </div>
          </div>
          <div className="flex items-start gap-2">
            <span className="inline-block w-4 h-4 bg-blue-100 border border-blue-400 rounded flex-shrink-0 mt-0.5" />
            <div>
              <strong>Positiv + Rolig:</strong> Du føler deg bra og avslappet
              (f.eks. rolig, takknemlig)
            </div>
          </div>
          <div className="flex items-start gap-2">
            <span className="inline-block w-4 h-4 bg-orange-100 border border-orange-400 rounded flex-shrink-0 mt-0.5" />
            <div>
              <strong>Negativ + Energisk:</strong> Du sliter, men har mye aktivering
              (f.eks. sint, engstelig)
            </div>
          </div>
          <div className="flex items-start gap-2">
            <span className="inline-block w-4 h-4 bg-gray-200 border border-gray-400 rounded flex-shrink-0 mt-0.5" />
            <div>
              <strong>Negativ + Lav energi:</strong> Du sliter og føler deg utmattet
              (f.eks. trist, nummen)
            </div>
          </div>
        </div>
        <p className="text-xs text-blue-700 mt-3 italic">
          Forskning viser at personer som kan navngi følelsene sine mer presist
          (høy emosjonell granularitet) har bedre mental helse og reguleringsevne.
        </p>
      </div>
    </div>
  );
}

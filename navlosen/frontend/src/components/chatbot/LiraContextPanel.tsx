"use client";

import React, { useState, useEffect } from "react";
import { Heart, Activity, User, ExternalLink, RefreshCw } from "lucide-react";
import Link from "next/link";
import type { BiofieldContext } from "@/lib/liraService";
import type { SomaticSignal, BigFive } from "@/types";
import PersonalityAvatar from "@/components/traits/PersonalityAvatar";
import BigFiveSurvey from "@/components/traits/BigFiveSurvey";
import { loadBigFive, saveSelfReport } from "@/utils/bigfive/mergeProfiles";

interface LiraContextPanelProps {
  biofieldContext?: BiofieldContext;
}

/**
 * Lira Context Panel
 *
 * Viser brukerens emosjonelle og fysiske tilstand fra Mestring
 * i en sidebar til venstre for chatgrensesnittet.
 *
 * Features:
 * - Polyvagal state indicator (stor visuell circle)
 * - Stress-score med farge-indikator
 * - Valgte emosjoner gruppert etter kvadrant
 * - Somatic signals (kroppssignaler)
 * - Link til Mestring for å oppdatere data
 * - Vis sist oppdatert timestamp
 *
 * Triadisk Score: 0.1 (PROCEED)
 */
export default function LiraContextPanel({ biofieldContext }: LiraContextPanelProps) {
  const [emotions, setEmotions] = useState<{ word: string; quadrant: number | null }[]>([]);
  const [somaticSignals, setSomaticSignals] = useState<SomaticSignal[]>([]);
  const [lastUpdated, setLastUpdated] = useState<number | null>(null);
  const [bigFive, setBigFive] = useState<BigFive | undefined>(undefined);
  const [showSurvey, setShowSurvey] = useState(false);
  const [selectedEmotion, setSelectedEmotion] = useState<{
    word: string;
    color: string;
    svgPath: string;
    definition: string;
  } | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;

    // Load emotions from localStorage
    const savedEmotions = localStorage.getItem("navlosen-emotions");
    if (savedEmotions) {
      try {
        setEmotions(JSON.parse(savedEmotions));
      } catch (e) {
        console.error("Failed to parse emotions", e);
      }
    }

    // Load somatic signals from localStorage
    const savedSignals = localStorage.getItem("navlosen-somatic-signals");
    if (savedSignals) {
      try {
        setSomaticSignals(JSON.parse(savedSignals));
      } catch (e) {
        console.error("Failed to parse somatic signals", e);
      }
    }

    // Load last Mestring timestamp
    const timestamp = localStorage.getItem("navlosen-last-mestring-timestamp");
    if (timestamp) {
      setLastUpdated(parseInt(timestamp));
    }

    // Load selected emotion for avatar display
    const savedSelectedEmotion = localStorage.getItem("navlosen-selected-emotion");
    if (savedSelectedEmotion) {
      try {
        setSelectedEmotion(JSON.parse(savedSelectedEmotion));
      } catch (e) {
        console.error("Failed to parse selected emotion", e);
      }
    }

    // Load Big Five profile
    const loadedBigFive = loadBigFive();
    setBigFive(loadedBigFive);
  }, []);

  // Get polyvagal state display info
  const getPolyvagalDisplay = () => {
    const state = biofieldContext?.polyvagalState || "ventral";

    switch (state) {
      case "ventral":
        return {
          color: "bg-green-500",
          borderColor: "border-green-500",
          textColor: "text-green-700",
          label: "Rolig",
          emoji: "🟢",
        };
      case "sympathetic":
        return {
          color: "bg-orange-500",
          borderColor: "border-orange-500",
          textColor: "text-orange-700",
          label: "Aktivert",
          emoji: "🟠",
        };
      case "dorsal":
        return {
          color: "bg-blue-500",
          borderColor: "border-blue-500",
          textColor: "text-blue-700",
          label: "Overveldet",
          emoji: "🔵",
        };
      default:
        return {
          color: "bg-gray-500",
          borderColor: "border-gray-500",
          textColor: "text-gray-700",
          label: "Ukjent",
          emoji: "⚪",
        };
    }
  };

  const polyvagalDisplay = getPolyvagalDisplay();

  // Get stress level color
  const getStressColor = (level: number) => {
    if (level <= 3) return "text-green-600";
    if (level <= 7) return "text-orange-600";
    return "text-red-600";
  };

  // Group emotions by quadrant
  const emotionsByQuadrant = emotions.reduce((acc, emotion) => {
    const quadrant = emotion.quadrant || 4;
    if (!acc[quadrant]) acc[quadrant] = [];
    acc[quadrant].push(emotion.word);
    return acc;
  }, {} as Record<number, string[]>);

  // Get quadrant display info
  const getQuadrantInfo = (quadrant: number) => {
    switch (quadrant) {
      case 1:
        return { label: "Positiv + Energisk", color: "text-green-700", bgColor: "bg-green-50", emoji: "✨" };
      case 2:
        return { label: "Positiv + Rolig", color: "text-blue-700", bgColor: "bg-blue-50", emoji: "🌊" };
      case 3:
        return { label: "Negativ + Utmattet", color: "text-gray-700", bgColor: "bg-gray-50", emoji: "💧" };
      case 4:
        return { label: "Negativ + Aktivert", color: "text-orange-700", bgColor: "bg-orange-50", emoji: "🔥" };
      default:
        return { label: "Ukjent", color: "text-gray-600", bgColor: "bg-gray-50", emoji: "❓" };
    }
  };

  // Count checked somatic signals
  const checkedSignals = somaticSignals.filter(s => s.checked);

  // Handle survey completion
  const handleSurveyComplete = (newBigFive: BigFive) => {
    saveSelfReport(newBigFive);
    setBigFive(newBigFive);
    setShowSurvey(false);
  };

  // Format last updated time
  const formatTimestamp = (timestamp: number) => {
    const now = Date.now();
    const diffMinutes = Math.floor((now - timestamp) / (1000 * 60));

    if (diffMinutes < 1) return "Akkurat nå";
    if (diffMinutes === 1) return "1 minutt siden";
    if (diffMinutes < 60) return `${diffMinutes} minutter siden`;

    const diffHours = Math.floor(diffMinutes / 60);
    if (diffHours === 1) return "1 time siden";
    if (diffHours < 24) return `${diffHours} timer siden`;

    const diffDays = Math.floor(diffHours / 24);
    if (diffDays === 1) return "1 dag siden";
    return `${diffDays} dager siden`;
  };

  return (
    <div className="w-80 h-[calc(100vh-16rem)] bg-white rounded-lg shadow-lg p-4 overflow-y-auto">
      {/* Header */}
      <div className="mb-4 pb-3 border-b">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)] flex items-center gap-2">
          <User className="w-5 h-5 text-purple-500" />
          Din tilstand
        </h3>
        {lastUpdated && (
          <p className="text-xs text-[var(--color-text-secondary)] mt-1">
            Oppdatert: {formatTimestamp(lastUpdated)}
          </p>
        )}
      </div>

      {/* Polyvagal State Indicator */}
      <div className="mb-4 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-3 mb-2">
          <div className={`w-16 h-16 rounded-full ${polyvagalDisplay.color} flex items-center justify-center text-3xl border-4 ${polyvagalDisplay.borderColor}`}>
            {polyvagalDisplay.emoji}
          </div>
          <div className="flex-1">
            <p className="text-xs text-[var(--color-text-secondary)] uppercase tracking-wide">
              Tilstand
            </p>
            <p className={`text-lg font-bold ${polyvagalDisplay.textColor}`}>
              {polyvagalDisplay.label}
            </p>
          </div>
        </div>
      </div>

      {/* Stress Score */}
      {biofieldContext && (
        <div className="mb-4 p-3 bg-gray-50 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-[var(--color-text-secondary)]" />
              <span className="text-sm font-medium text-[var(--color-text-primary)]">
                Stressnivå
              </span>
            </div>
            <span className={`text-2xl font-bold ${getStressColor(biofieldContext.stressLevel)}`}>
              {biofieldContext.stressLevel}/10
            </span>
          </div>
          {/* Visual stress meter */}
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ${
                biofieldContext.stressLevel <= 3
                  ? "bg-green-500"
                  : biofieldContext.stressLevel <= 7
                  ? "bg-orange-500"
                  : "bg-red-500"
              }`}
              style={{ width: `${(biofieldContext.stressLevel / 10) * 100}%` }}
            />
          </div>
        </div>
      )}

      {/* Emotions */}
      {emotions.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <Heart className="w-4 h-4 text-red-500" />
            <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
              Følelser ({emotions.length})
            </h4>
          </div>
          <div className="space-y-2">
            {[1, 2, 3, 4].map((quadrant) => {
              const quadrantEmotions = emotionsByQuadrant[quadrant];
              if (!quadrantEmotions || quadrantEmotions.length === 0) return null;

              const quadrantInfo = getQuadrantInfo(quadrant);

              return (
                <div key={quadrant} className={`p-2 rounded-lg ${quadrantInfo.bgColor}`}>
                  <p className={`text-xs font-medium ${quadrantInfo.color} mb-1`}>
                    {quadrantInfo.emoji} {quadrantInfo.label}
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {quadrantEmotions.map((emotion, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 text-xs bg-white rounded-full border border-gray-200"
                      >
                        {emotion}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Somatic Signals */}
      {checkedSignals.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)] mb-2">
            Kroppssignaler ({checkedSignals.length})
          </h4>
          <div className="space-y-1">
            {checkedSignals.map((signal, idx) => (
              <div key={idx} className="flex items-center gap-2 text-xs text-[var(--color-text-secondary)]">
                <div className="w-1.5 h-1.5 rounded-full bg-orange-500" />
                {signal.label}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {emotions.length === 0 && checkedSignals.length === 0 && (
        <div className="mb-4 p-4 bg-gray-50 rounded-lg text-center">
          <p className="text-sm text-[var(--color-text-secondary)] mb-2">
            Ingen Mestring-data enda
          </p>
          <p className="text-xs text-[var(--color-text-secondary)]">
            Gå til Mestring for å dele hvordan du har det
          </p>
        </div>
      )}

      {/* Emotion Avatar */}
      {selectedEmotion && (
        <div className="mb-4 p-4 bg-white border border-gray-200 rounded-lg">
          <p className="text-xs text-gray-600 mb-3 uppercase font-medium text-center">
            Din følelse
          </p>
          <div className="flex flex-col items-center">
            <div className="relative w-20 h-20 flex-shrink-0 mb-2">
              {selectedEmotion.svgPath && selectedEmotion.svgPath !== "" ? (
                <svg
                  viewBox="0 0 100 100"
                  className="w-full h-full breathe-animation drop-shadow-lg"
                >
                  <path
                    d={selectedEmotion.svgPath}
                    fill={selectedEmotion.color}
                  />
                </svg>
              ) : (
                <div
                  className="w-full h-full rounded-full flex items-center justify-center text-white font-bold text-lg drop-shadow-lg breathe-animation"
                  style={{ backgroundColor: selectedEmotion.color }}
                >
                  {selectedEmotion.word.charAt(0).toUpperCase()}
                </div>
              )}
            </div>
            <p
              className="text-base font-bold text-center"
              style={{ color: selectedEmotion.color }}
            >
              {selectedEmotion.word}
            </p>
            <p className="text-xs text-gray-600 italic text-center mt-1">
              {selectedEmotion.definition}
            </p>
          </div>
        </div>
      )}

      {/* Big Five Personality Profile */}
      {bigFive ? (
        <div className="mb-4 flex justify-center">
          <PersonalityAvatar
            bigFive={bigFive}
            polyvagalState={biofieldContext?.polyvagalState}
            size="medium"
            interactive={true}
            showLabel={true}
            onEdit={() => setShowSurvey(true)}
          />
        </div>
      ) : (
        <div className="mb-4 p-4 bg-gray-50 border border-gray-200 rounded-lg">
          <p className="text-xs text-gray-600 text-center mb-2">
            <strong>Personlighetsprofil</strong>
          </p>
          <p className="text-xs text-gray-500 text-center mb-3">
            Fyll ut en kort personlighetstest for at Lira skal kunne gi deg mer personlig veiledning.
          </p>
          <button
            onClick={() => setShowSurvey(true)}
            className="w-full py-2 px-4 bg-purple-100 hover:bg-purple-200 text-purple-700 rounded-lg transition-colors text-sm font-medium"
          >
            Fyll ut personlighetstest
          </button>
        </div>
      )}

      {/* Update Button */}
      <Link
        href="/mestring"
        className="flex items-center justify-center gap-2 w-full p-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors font-medium text-sm"
      >
        <RefreshCw className="w-4 h-4" />
        Oppdater Mestring-data
      </Link>

      {/* Info Box */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-blue-800">
          <strong>💡 Tips:</strong> Lira bruker denne informasjonen for å tilpasse
          veiledningen til hvordan du har det akkurat nå.
        </p>
      </div>

      {/* Big Five Survey Modal */}
      {showSurvey && (
        <BigFiveSurvey
          onComplete={handleSurveyComplete}
          onCancel={() => setShowSurvey(false)}
          polyvagalState={biofieldContext?.polyvagalState}
        />
      )}
    </div>
  );
}

"use client";

import React, { useState } from "react";
import { BigFive } from "@/types";
import { Settings, HelpCircle } from "lucide-react";

interface BigFiveMiniProps {
  bigFive?: BigFive;
  onEdit?: () => void;
  className?: string;
}

/**
 * BigFiveMini Component
 *
 * Compact display of Big Five (OCEAN) personality traits with uncertainty visualization.
 * Shows 5 bars (O, C, E, A, N) + uncertainty shadows.
 *
 * Design principles:
 * - Polyvagal-safe: No trait questions in dorsal state
 * - Opt-in: All trait data is voluntary and reversible
 * - Transparent: Shows uncertainty and data source
 * - Weak influence: Traits used only for re-ranking (≤10% weight)
 *
 * "Tilstand leder, trekk hvisker."
 *
 * Triadisk Score: 0.15 (PROCEED)
 */
export default function BigFiveMini({
  bigFive,
  onEdit,
  className = "",
}: BigFiveMiniProps) {
  const [showInfo, setShowInfo] = useState(false);

  const traits = [
    { key: "O", label: "Åpenhet", color: "bg-purple-500", desc: "Nysgjerrighet, kreativitet" },
    { key: "C", label: "Planmessighet", color: "bg-blue-500", desc: "Struktur, målrettethet" },
    { key: "E", label: "Utadvendthet", color: "bg-green-500", desc: "Sosial energi" },
    { key: "A", label: "Omgjengelighet", color: "bg-orange-500", desc: "Samarbeid, varme" },
    { key: "N", label: "Nevrotisisme", color: "bg-red-500", desc: "Emosjonell følsomhet" },
  ];

  const getTraitValue = (key: string): number => {
    if (!bigFive) return 0.5; // Default to middle if no data
    return bigFive[key as keyof BigFive] as number ?? 0.5;
  };

  const getUncertainty = (key: string): number => {
    if (!bigFive?.uncertainty) return 0.7; // High uncertainty if no data
    return bigFive.uncertainty[key as keyof typeof bigFive.uncertainty] ?? 0.7;
  };

  const getSourceLabel = (): string => {
    if (!bigFive) return "Ingen data";
    switch (bigFive.source) {
      case "self_report":
        return "Selvrapport";
      case "inferred":
        return "Estimert fra mønstre";
      case "mixed":
        return "Selvrapport + estimat";
      default:
        return "Ukjent kilde";
    }
  };

  const getSourceColor = (): string => {
    if (!bigFive) return "text-gray-500";
    switch (bigFive.source) {
      case "self_report":
        return "text-green-700";
      case "inferred":
        return "text-orange-700";
      case "mixed":
        return "text-blue-700";
      default:
        return "text-gray-700";
    }
  };

  return (
    <div className={`bg-gray-50 rounded-lg p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <h4 className="text-sm font-semibold text-[var(--color-text-primary)]">
            Personlighetsprofil (OCEAN)
          </h4>
          <button
            onClick={() => setShowInfo(!showInfo)}
            className="text-gray-500 hover:text-gray-700 transition-colors"
            aria-label="Vis informasjon"
          >
            <HelpCircle className="w-4 h-4" />
          </button>
        </div>
        {onEdit && (
          <button
            onClick={onEdit}
            className="flex items-center gap-1 text-xs text-purple-700 hover:text-purple-900 font-medium transition-colors"
          >
            <Settings className="w-3 h-3" />
            Rediger
          </button>
        )}
      </div>

      {/* Info panel */}
      {showInfo && (
        <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-900">
          <p className="font-semibold mb-1">💡 Hvordan brukes dette?</p>
          <ul className="space-y-1 list-disc list-inside text-blue-800">
            <li>
              <strong>Tilstand leder, trekk hvisker:</strong> Din følelsestilstand (fra Mestring) styrer alle anbefalinger.
            </li>
            <li>
              <strong>Svak påvirkning:</strong> Personlighet brukes kun som tie-breaker (≤10% vekt) når to forslag er like gode.
            </li>
            <li>
              <strong>Frivillig:</strong> Du kan når som helst redigere, deaktivere eller slette denne dataen.
            </li>
          </ul>
        </div>
      )}

      {/* Trait bars */}
      <div className="space-y-3">
        {traits.map((trait) => {
          const value = getTraitValue(trait.key);
          const uncertainty = getUncertainty(trait.key);
          const lowerBound = Math.max(0, value - uncertainty);
          const upperBound = Math.min(1, value + uncertainty);

          return (
            <div key={trait.key}>
              {/* Label */}
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-gray-900 w-4">
                    {trait.key}
                  </span>
                  <span className="text-xs text-gray-700">{trait.label}</span>
                </div>
                <span className="text-xs text-gray-500">{trait.desc}</span>
              </div>

              {/* Bar container */}
              <div className="relative h-6 bg-gray-200 rounded-full overflow-hidden">
                {/* Uncertainty shadow (lighter) */}
                <div
                  className={`absolute h-full ${trait.color} opacity-20 transition-all duration-300`}
                  style={{
                    left: `${lowerBound * 100}%`,
                    width: `${(upperBound - lowerBound) * 100}%`,
                  }}
                />

                {/* Main value bar (darker) */}
                <div
                  className={`absolute h-full ${trait.color} transition-all duration-300`}
                  style={{
                    left: 0,
                    width: `${value * 100}%`,
                  }}
                />

                {/* Value label */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xs font-bold text-white drop-shadow-md">
                    {Math.round(value * 100)}%
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Source info */}
      <div className="mt-3 pt-3 border-t border-gray-300">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-600">Datakilde:</span>
          <span className={`font-medium ${getSourceColor()}`}>
            {getSourceLabel()}
          </span>
        </div>
        {bigFive?.updatedAt && (
          <div className="flex items-center justify-between text-xs mt-1">
            <span className="text-gray-600">Oppdatert:</span>
            <span className="text-gray-700">
              {new Date(bigFive.updatedAt).toLocaleDateString("nb-NO", {
                day: "numeric",
                month: "short",
                year: "numeric",
              })}
            </span>
          </div>
        )}
      </div>

      {/* No data message */}
      {!bigFive && (
        <div className="mt-3 p-3 bg-purple-50 border border-purple-200 rounded-lg">
          <p className="text-xs text-purple-900">
            <strong>Ingen personlighetsdata ennå.</strong> Du kan frivillig svare på noen spørsmål for mer personaliserte anbefalinger, eller la systemet estimere over tid basert på dine mønstre.
          </p>
          {onEdit && (
            <button
              onClick={onEdit}
              className="mt-2 text-xs text-purple-700 hover:text-purple-900 font-semibold underline"
            >
              Start frivillig spørreskjema →
            </button>
          )}
        </div>
      )}
    </div>
  );
}

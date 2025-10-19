"use client";

import React, { useState } from "react";
import Button from "@/components/ui/Button";
import { Activity, Heart, Moon, TrendingUp, Smile, Zap, Wind, Sun } from "lucide-react";
import type { SomaticSignal } from "@/types";

interface Fase4aPressureSignalsProps {
  onContinue: (data: {
    pressure: number;
    signals: string[];
  }) => void;
  healthData?: {
    sleep?: number; // hours
    steps?: number;
    hrv?: number;
  };
}

// Grouped somatic signals with color coding
const SOMATIC_SIGNALS = [
  // POSITIVE SIGNALS (Grønn gruppe)
  {
    id: "lett-kropp",
    label: "Lett i kroppen",
    icon: Wind,
    category: "positive",
    color: "green"
  },
  {
    id: "avslapte-muskler",
    label: "Avslappete muskler",
    icon: Smile,
    category: "positive",
    color: "green"
  },
  {
    id: "rolig-pust",
    label: "Rolig pust",
    icon: Wind,
    category: "positive",
    color: "green"
  },
  {
    id: "varm-fyldig",
    label: "Varm og fyldig følelse",
    icon: Sun,
    category: "positive",
    color: "green"
  },
  {
    id: "energisk",
    label: "Energisk",
    icon: Zap,
    category: "positive",
    color: "green"
  },
  {
    id: "rolig-hjerterytme",
    label: "Rolig hjerterytme",
    icon: Heart,
    category: "positive",
    color: "green"
  },
  {
    id: "harene-reiser-seg",
    label: "Hårene reiser seg",
    icon: Zap,
    category: "positive",
    color: "green"
  },

  // NEUTRAL/AKTIVERING (Blå/Gul gruppe)
  {
    id: "varm-bryst",
    label: "Varm i brystet",
    icon: Heart,
    category: "neutral",
    color: "yellow"
  },
  {
    id: "hjertebank",
    label: "Hjertebank",
    icon: Heart,
    category: "neutral",
    color: "yellow"
  },
  {
    id: "rask-pust",
    label: "Rask pust",
    icon: Activity,
    category: "neutral",
    color: "yellow"
  },
  {
    id: "sommerfugler-mage",
    label: "Sommerfugler i magen",
    icon: Activity,
    category: "neutral",
    color: "yellow"
  },

  // NEGATIVE/UBEHAG (Rød gruppe)
  {
    id: "tung-pust",
    label: "Tung pust",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "knyttneve",
    label: "Knyttnever",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "kald-svette",
    label: "Kald svette",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "knute-mage",
    label: "Knute i magen",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "tung-kropp",
    label: "Tung kropp",
    icon: TrendingUp,
    category: "negative",
    color: "red"
  },
  {
    id: "anspent",
    label: "Anspente muskler",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "skjelving",
    label: "Skjelving",
    icon: Activity,
    category: "negative",
    color: "red"
  },
  {
    id: "hodepine",
    label: "Hodepine/press i hodet",
    icon: Activity,
    category: "negative",
    color: "red"
  },
];

/**
 * Fase 4a: Trykk & Kroppslige Signaler
 *
 * Bruker velger:
 * 1. Hvor høyt trykket/intensiteten er (0-10 slider)
 * 2. Hvilke kroppslige signaler de kjenner på (klikkbare tags)
 *
 * Viser også Health Connect data hvis tilgjengelig (søvn, skritt, HRV)
 *
 * Design: Rolig, somatisk, polyvagal-informert
 * Inspirert av: How We Feel (HWF) app
 *
 * Triadisk Score: 0.15 (PROCEED)
 */
export default function Fase4aPressureSignals({
  onContinue,
  healthData,
}: Fase4aPressureSignalsProps) {
  const [pressure, setPressure] = useState(5);
  const [selectedSignals, setSelectedSignals] = useState<string[]>([]);

  const toggleSignal = (signalId: string) => {
    setSelectedSignals((prev) =>
      prev.includes(signalId)
        ? prev.filter((id) => id !== signalId)
        : [...prev, signalId]
    );
  };

  const handleContinue = () => {
    onContinue({
      pressure,
      signals: selectedSignals,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-purple-50 to-pink-50 p-6">
      <div className="w-full space-y-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-3">
            Hva kjenner du i kroppen?
          </h2>
          <p className="text-base text-gray-600">
            La oss sjekke inn på kroppslige signaler
          </p>
        </div>

        {/* Health Connect Data (if available) */}
        {healthData && (
          <div className="bg-white rounded-2xl p-6 shadow-sm border-2 border-blue-200">
            <div className="flex items-start gap-3 mb-4">
              <Activity className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  Helseinformasjon fra i dag
                </h3>
                <p className="text-sm text-gray-700">
                  Jeg ser at du har{" "}
                  {healthData.sleep !== undefined && (
                    <>
                      <strong>sovet {healthData.sleep} timer</strong>
                      {healthData.steps !== undefined && " og "}
                    </>
                  )}
                  {healthData.steps !== undefined && (
                    <strong>gått {healthData.steps.toLocaleString()} skritt</strong>
                  )}
                  . Dette kan påvirke energinivået ditt.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Section 1: Pressure/Intensity */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-6">
            Hvor høyt er trykket nå?
          </h3>

          {/* Slider */}
          <div className="space-y-4">
            <input
              type="range"
              min="0"
              max="10"
              step="1"
              value={pressure}
              onChange={(e) => setPressure(Number(e.target.value))}
              className="w-full h-3 bg-gradient-to-r from-green-300 via-yellow-300 to-red-500 rounded-full appearance-none cursor-pointer accent-purple-600"
              style={{
                background: `linear-gradient(to right,
                  #88D8B0 0%,
                  #FFD700 50%,
                  #FF6F61 100%)`,
              }}
            />

            {/* Value display */}
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Lavt</span>
              <div className="text-center">
                <div className="text-5xl font-bold text-purple-600 mb-1">
                  {pressure}
                </div>
                <div className="text-sm text-gray-600">av 10</div>
              </div>
              <span className="text-sm text-gray-600">Høyt</span>
            </div>
          </div>
        </div>

        {/* Section 2: Somatic Signals */}
        <div className="bg-white rounded-2xl p-8 shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Kjenner du på noen av disse kroppslige signalene?
          </h3>
          <p className="text-sm text-gray-600 mb-6">
            Velg alle som passer (valgfritt)
          </p>

          {/* Signal tags */}
          <div className="flex flex-wrap gap-3">
            {SOMATIC_SIGNALS.map((signal) => {
              const Icon = signal.icon;
              const isSelected = selectedSignals.includes(signal.id);

              // Color mapping for unselected state
              const getUnselectedStyle = () => {
                switch (signal.color) {
                  case "green":
                    return "border-green-300 text-green-700 hover:border-green-400 hover:bg-green-50";
                  case "yellow":
                    return "border-yellow-300 text-yellow-700 hover:border-yellow-400 hover:bg-yellow-50";
                  case "red":
                    return "border-red-300 text-red-700 hover:border-red-400 hover:bg-red-50";
                  default:
                    return "border-gray-300 text-gray-700 hover:border-gray-400 hover:bg-gray-50";
                }
              };

              // Color mapping for selected state
              const getSelectedStyle = () => {
                switch (signal.color) {
                  case "green":
                    return "bg-green-500 border-green-500 text-white shadow-lg";
                  case "yellow":
                    return "bg-yellow-500 border-yellow-500 text-white shadow-lg";
                  case "red":
                    return "bg-red-500 border-red-500 text-white shadow-lg";
                  default:
                    return "bg-purple-500 border-purple-500 text-white shadow-lg";
                }
              };

              return (
                <button
                  key={signal.id}
                  onClick={() => toggleSignal(signal.id)}
                  className={`flex items-center gap-2 px-4 py-3 rounded-full border-2 transition-all duration-300 ${
                    isSelected ? getSelectedStyle() : `bg-white ${getUnselectedStyle()}`
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{signal.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Continue Button */}
        <Button
          onClick={handleContinue}
          variant="primary"
          size="large"
          fullWidth
          className="text-lg py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg hover:shadow-xl"
        >
          Fortsett til Lira
        </Button>
      </div>
    </div>
  );
}

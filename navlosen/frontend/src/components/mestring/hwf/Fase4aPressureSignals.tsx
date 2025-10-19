"use client";

import React, { useState } from "react";
import Button from "@/components/ui/Button";
import { Activity, Heart, Moon, TrendingUp } from "lucide-react";
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

const SOMATIC_SIGNALS = [
  { id: "hjertebank", label: "Hjertebank", icon: Heart },
  { id: "tung-pust", label: "Tung pust", icon: Activity },
  { id: "knyttneve", label: "Knyttnever", icon: Activity },
  { id: "varm-bryst", label: "Varm i brystet", icon: Heart },
  { id: "kald-svette", label: "Kald svette", icon: Activity },
  { id: "knute-mage", label: "Knute i magen", icon: Activity },
  { id: "tung-kropp", label: "Tung kropp", icon: TrendingUp },
  { id: "anspent", label: "Anspente muskler", icon: Activity },
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

              return (
                <button
                  key={signal.id}
                  onClick={() => toggleSignal(signal.id)}
                  className={`flex items-center gap-2 px-4 py-3 rounded-full border-2 transition-all duration-300 ${
                    isSelected
                      ? "bg-purple-500 border-purple-500 text-white shadow-lg"
                      : "bg-white border-gray-300 text-gray-700 hover:border-purple-300 hover:bg-purple-50"
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

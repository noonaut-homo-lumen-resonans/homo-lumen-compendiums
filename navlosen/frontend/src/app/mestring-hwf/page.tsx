"use client";

import React, { useState } from "react";
import { ArrowLeft } from "lucide-react";
import Fase1Welcome from "@/components/mestring/hwf/Fase1Welcome";
import Fase2Quadrants from "@/components/mestring/hwf/Fase2Quadrants";
import Fase3EmotionLandscape from "@/components/mestring/hwf/Fase3EmotionLandscape";
import Fase4Definition from "@/components/mestring/hwf/Fase4Definition";
import Fase4aPressureSignals from "@/components/mestring/hwf/Fase4aPressureSignals";
import Stage3LiraChat from "@/components/mestring/Stage3LiraChat";
import type { EmotionWord } from "@/components/mestring/hwf/emotionData";
import type { LiraAnswer } from "@/lib/compositeStressScore";

type HWFFase =
  | "welcome"
  | "quadrants"
  | "landscape"
  | "definition"
  | "pressure-signals"
  | "lira-chat"
  | "results";

/**
 * Mestring HWF - How We Feel Inspired Flow
 *
 * 6-fase guidet brukeropplevelse basert på "How We Feel" app design:
 *
 * **Fase 1:** Velkomsthilsen - Introduksjon til verktøyet
 * **Fase 2:** 4 Kvadranter - Høy/Lav energi × Behagelig/Ubehagelig
 * **Fase 3:** Følelseslandskap - 36 ord i valgt kvadrant (draggbar)
 * **Fase 4:** Definisjon - Popup med ordets betydning
 * **Fase 4a:** Trykk & Kroppslige Signaler - Slider + tags + Health Connect
 * **Fase 5-6:** Lira Dialog - 4 spørsmål + anbefaling
 *
 * Design Philosophy:
 * - Minimalistisk, rolig, trygg atmosfære
 * - HWF fargepalett (Rød, Gul, Blå, Grønn)
 * - Smooth animasjoner (ease-in-out)
 * - Triadisk Ethics i hver fase
 *
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function MestringHWFPage() {
  const [currentFase, setCurrentFase] = useState<HWFFase>("welcome");
  const [selectedQuadrant, setSelectedQuadrant] = useState<1 | 2 | 3 | 4 | null>(null);
  const [selectedEmotion, setSelectedEmotion] = useState<EmotionWord | null>(null);
  const [showDefinition, setShowDefinition] = useState(false);
  const [pressureData, setPressureData] = useState<{
    pressure: number;
    signals: string[];
  } | null>(null);
  const [liraAnswers, setLiraAnswers] = useState<LiraAnswer[]>([]);

  // Mock Health Connect data (replace with real API later)
  const healthData = {
    sleep: 5,
    steps: 2300,
    hrv: undefined,
  };

  // Phase handlers
  const handleWelcomeContinue = () => {
    setCurrentFase("quadrants");
  };

  const handleQuadrantSelect = (quadrant: 1 | 2 | 3 | 4) => {
    setSelectedQuadrant(quadrant);
    setCurrentFase("landscape");
  };

  const handleEmotionSelect = (emotion: EmotionWord) => {
    setSelectedEmotion(emotion);
    setShowDefinition(true);
  };

  const handleDefinitionContinue = () => {
    setShowDefinition(false);
    setCurrentFase("pressure-signals");
  };

  const handlePressureSignalsContinue = (data: {
    pressure: number;
    signals: string[];
  }) => {
    setPressureData(data);
    setCurrentFase("lira-chat");
  };

  const handleLiraComplete = (answers: LiraAnswer[]) => {
    setLiraAnswers(answers);
    setCurrentFase("results");
  };

  // Render current phase
  const renderCurrentFase = () => {
    switch (currentFase) {
      case "welcome":
        return <Fase1Welcome onContinue={handleWelcomeContinue} />;

      case "quadrants":
        return <Fase2Quadrants onQuadrantSelect={handleQuadrantSelect} />;

      case "landscape":
        if (!selectedQuadrant) return null;
        return (
          <Fase3EmotionLandscape
            quadrant={selectedQuadrant}
            onEmotionSelect={handleEmotionSelect}
          />
        );

      case "pressure-signals":
        return (
          <Fase4aPressureSignals
            onContinue={handlePressureSignalsContinue}
            healthData={healthData}
          />
        );

      case "lira-chat":
        if (!selectedEmotion || !pressureData) return null;

        // Determine stress state from pressure
        const getStressState = () => {
          if (pressureData.pressure <= 3) return "ventral";
          if (pressureData.pressure <= 7) return "sympathetic";
          return "dorsal";
        };

        return (
          <div className="min-h-screen">
            <Stage3LiraChat
              stressState={getStressState()}
              liraAnswers={liraAnswers}
              onAnswersChange={setLiraAnswers}
              onBack={() => setCurrentFase("pressure-signals")}
              onNext={() => setCurrentFase("results")}
              polyvagalState={getStressState()}
              stressLevel={pressureData.pressure}
            />
          </div>
        );

      case "results":
        return (
          <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-green-50 to-blue-50 p-6">
            <div className="max-w-2xl w-full text-center space-y-6">
              <h1 className="text-4xl font-bold text-gray-900">
                Takk for at du delte!
              </h1>
              <p className="text-lg text-gray-600">
                Lira vil gi deg personaliserte anbefalinger basert på dialogen.
              </p>
              <button
                onClick={() => window.location.href = "/"}
                className="px-8 py-4 bg-purple-600 text-white rounded-full text-lg font-semibold hover:bg-purple-700 transition-all"
              >
                Tilbake til Dashboard
              </button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="relative">
      {/* Back to Dashboard Button */}
      {currentFase !== "welcome" && (
        <button
          onClick={() => window.location.href = "/"}
          className="fixed top-6 left-6 z-40 flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm text-gray-700 rounded-full shadow-md hover:bg-white hover:shadow-lg transition-all"
        >
          <ArrowLeft className="w-5 h-5" />
          <span className="text-sm font-medium">Tilbake</span>
        </button>
      )}

      {renderCurrentFase()}

      {/* Definition Modal Overlay */}
      {showDefinition && selectedEmotion && (
        <Fase4Definition
          emotion={selectedEmotion}
          onContinue={handleDefinitionContinue}
        />
      )}
    </div>
  );
}

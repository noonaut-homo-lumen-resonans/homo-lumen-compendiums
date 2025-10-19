"use client";

import React, { useState } from "react";
import { ArrowLeft } from "lucide-react";
import Fase1Welcome from "@/components/mestring/hwf/Fase1Welcome";
import Fase2Quadrants from "@/components/mestring/hwf/Fase2Quadrants";
import Fase3EmotionLandscape from "@/components/mestring/hwf/Fase3EmotionLandscape";
import Fase4Definition from "@/components/mestring/hwf/Fase4Definition";
import Fase4aPressureSignals from "@/components/mestring/hwf/Fase4aPressureSignals";
import Fase6Results from "@/components/mestring/hwf/Fase6Results";
import EmotionBadge from "@/components/mestring/hwf/EmotionBadge";
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
 * Mestring - How We Feel Inspired Flow
 *
 * 6-fase guidet brukeropplevelse basert på "How We Feel" app design:
 *
 * **Fase 1:** Velkomsthilsen - Introduksjon til verktøyet
 * **Fase 2:** 4 Kvadranter - Høy/Lav energi × Behagelig/Ubehagelig
 * **Fase 3:** Følelseslandskap - 100 norske emosjoner i 4-kvadrant grid
 * **Fase 4:** Definisjon - Popup med ordets betydning
 * **Fase 4a:** Trykk & Kroppslige Signaler - Slider + tags + Health Connect
 * **Fase 5-6:** Lira Dialog - 4 spørsmål + anbefaling
 *
 * Design Philosophy:
 * - Minimalistisk, rolig, trygg atmosfære
 * - HWF fargepalett (Rød, Gul, Blå, Grønn)
 * - Smooth animasjoner (ease-in-out)
 * - Triadisk Ethics i hver fase
 * - 100 unike SVG-former for hver emosjon
 *
 * Living Compendium V1.7.14
 * HWF Emotion Wheel: 100% Complete
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function MestringPage() {
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
    setCurrentFase("landscape"); // Skip quadrants, go directly to landscape
  };

  const handleQuadrantSelect = (quadrant: 1 | 2 | 3 | 4) => {
    setSelectedQuadrant(quadrant);
    setCurrentFase("landscape");
  };

  const handleEmotionSelect = (emotion: EmotionWord) => {
    setSelectedEmotion(emotion);
    setShowDefinition(true);

    // Save selected emotion to localStorage for Dashboard display
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-selected-emotion", JSON.stringify({
        word: emotion.word,
        color: emotion.color,
        svgPath: emotion.svgPath || "",
        definition: emotion.definition
      }));
    }
  };

  const handleDefinitionContinue = () => {
    setShowDefinition(false);
    setCurrentFase("pressure-signals");
  };

  const handleDefinitionBack = () => {
    // Close definition popup to let user choose a different emotion
    setShowDefinition(false);
    // Stay on landscape phase so user can see all emotions
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

  const handleRestart = () => {
    setCurrentFase("welcome");
    setSelectedQuadrant(null);
    setSelectedEmotion(null);
    setShowDefinition(false);
    setPressureData(null);
    setLiraAnswers([]);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleGoHome = () => {
    window.location.href = "/";
  };

  // Render current phase
  const renderCurrentFase = () => {
    switch (currentFase) {
      case "welcome":
        return <Fase1Welcome onContinue={handleWelcomeContinue} />;

      case "quadrants":
        return <Fase2Quadrants onQuadrantSelect={handleQuadrantSelect} />;

      case "landscape":
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
        if (!selectedEmotion || !pressureData) return null;

        return (
          <Fase6Results
            selectedEmotion={selectedEmotion}
            pressureLevel={pressureData.pressure}
            selectedSignals={pressureData.signals}
            onRestart={handleRestart}
            onGoHome={handleGoHome}
          />
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

      {/* Floating Emotion Badge - shows after emotion is selected */}
      {selectedEmotion && currentFase !== "landscape" && !showDefinition && (
        <EmotionBadge emotion={selectedEmotion} />
      )}

      {/* Always render landscape if emotion is selected but definition is showing */}
      {showDefinition && currentFase === "landscape" ? (
        <>
          {/* Show landscape in background */}
          <Fase3EmotionLandscape
            quadrant={selectedQuadrant}
            onEmotionSelect={handleEmotionSelect}
          />

          {/* Definition Modal Overlay on top */}
          {selectedEmotion && (
            <Fase4Definition
              emotion={selectedEmotion}
              onContinue={handleDefinitionContinue}
              onBack={handleDefinitionBack}
            />
          )}
        </>
      ) : (
        renderCurrentFase()
      )}
    </div>
  );
}

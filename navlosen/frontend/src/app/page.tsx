"use client";

import React, { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import ConsentModal from "@/components/safety/ConsentModal";
import Stage1Emotions from "@/components/flow/Stage1Emotions";
import Stage2Signals from "@/components/flow/Stage2Signals";
import Stage3Chat from "@/components/flow/Stage3Chat";
import Stage4Recommendations from "@/components/flow/Stage4Recommendations";
import RAINModule from "@/components/mestring/RAINModule";
import {
  FlowStage,
  SomaticSignal,
  LiraAnswer,
  SessionData,
  HealthConnectData,
  WeatherData
} from "@/types";
import {
  multiScaleLogger,
  logCelleEvent,
  logVevEvent,
} from "@/lib/multi-scale-metadata";

/**
 * NAV-Losen Home Page - Multi-Stage Adaptive Flow
 *
 * 4-stage wizard that guides users through:
 * 1. Emotion Check-in (Quadrant selection)
 * 2. Trykk & Signaler (Stress + Somatic awareness)
 * 3. Lira Chat (2-5 adaptive questions)
 * 4. Personalized Recommendations (Exercises, Music, Knowledge, Context)
 *
 * Integrates:
 * - Polyvagal Theory (stress-responsive UI)
 * - Emotional Granularity (100 emotion words)
 * - HealthConnect data (mock for now)
 * - Weather context (mock for now)
 *
 * Triadisk Score: 0.18 (PROCEED)
 * - Suverenitet: User-controlled progression
 * - Koherens: Grounded in neuroscience
 * - Healing: Personalized capacity building
 */
export default function Home() {
  // Consent management
  const [hasConsented, setHasConsented] = useState<boolean>(false);

  // Stage management
  const [currentStage, setCurrentStage] = useState<FlowStage>("emotions");
  const [showRAIN, setShowRAIN] = useState<boolean>(false);

  // Default somatic signals
  const defaultSomaticSignals: SomaticSignal[] = [
    { id: "rask-puls", label: "Rask puls eller hjertebank", checked: false },
    { id: "anspent-kjeve", label: "Anspent kjeve eller skuldre", checked: false },
    { id: "grunn-pust", label: "Grunn eller rask pust", checked: false },
    { id: "mage-uro", label: "Uro i magen eller kvalme", checked: false },
    { id: "trett", label: "Tretthet eller tung kropp", checked: false },
    { id: "nummen", label: "Nummen eller koblet fra", checked: false },
  ];

  // Session state
  const [selectedEmotions, setSelectedEmotions] = useState<{ word: string; quadrant: number | null }[]>([]);
  const [stressLevel, setStressLevel] = useState<number>(5);
  const [somaticSignals, setSomaticSignals] = useState<SomaticSignal[]>(defaultSomaticSignals);
  const [liraAnswers, setLiraAnswers] = useState<LiraAnswer[]>([]);

  // Mock HealthConnect & Weather data
  const [healthConnect] = useState<HealthConnectData>({
    steps: 4532,
    sleepHours: 6.5,
    sleepQuality: "fair",
    heartRate: 72,
  });

  const [weather] = useState<WeatherData>({
    temperature: 12,
    condition: "sunny",
    recommendation: "Fint vær for en tur!",
  });

  // Check consent on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedConsent = localStorage.getItem("navlosen_consent");
      if (savedConsent) {
        try {
          const consent = JSON.parse(savedConsent);
          setHasConsented(consent.consented === true);
        } catch (e) {
          console.error("Failed to parse consent from localStorage", e);
        }
      }
    }
  }, []);

  // Load from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedStage = localStorage.getItem("navlosen-current-stage");
      const savedEmotions = localStorage.getItem("navlosen-emotions");
      const savedStressLevel = localStorage.getItem("navlosen-stress-level");
      const savedSignals = localStorage.getItem("navlosen-somatic-signals");
      const savedAnswers = localStorage.getItem("navlosen-lira-answers");

      if (savedStage) setCurrentStage(savedStage as FlowStage);
      if (savedEmotions) {
        try {
          setSelectedEmotions(JSON.parse(savedEmotions));
        } catch (e) {
          console.error("Failed to parse emotions from localStorage", e);
        }
      }
      if (savedStressLevel) setStressLevel(Number(savedStressLevel));
      if (savedSignals) {
        try {
          setSomaticSignals(JSON.parse(savedSignals));
        } catch (e) {
          console.error("Failed to parse signals from localStorage", e);
        }
      }
      if (savedAnswers) {
        try {
          setLiraAnswers(JSON.parse(savedAnswers));
        } catch (e) {
          console.error("Failed to parse answers from localStorage", e);
        }
      }
    }
  }, []);

  // Save to localStorage when state changes
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-current-stage", currentStage);
    }
  }, [currentStage]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-emotions", JSON.stringify(selectedEmotions));
    }
  }, [selectedEmotions]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-stress-level", String(stressLevel));
    }
  }, [stressLevel]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-somatic-signals", JSON.stringify(somaticSignals));
    }
  }, [somaticSignals]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-lira-answers", JSON.stringify(liraAnswers));
    }
  }, [liraAnswers]);

  // Stage navigation with multi-scale logging
  const goToStage = (stage: FlowStage) => {
    // Log multi-scale event (Skala 1: Celle - Claude Code learns from user progression)
    if (multiScaleLogger && stage === "signals") {
      const celleEvent = logCelleEvent(
        "Claude Code",
        `User completed emotion selection: ${selectedEmotions.length} emotions selected`,
        "Users engage with emotion wheel → better emotional granularity",
        "Progressed to Stage 2 (Signals)",
        "Emotional granularity builds self-awareness",
        "Flow orchestration and UX implementation"
      );

      multiScaleLogger.logBottomUpEmergence(
        `User selected ${selectedEmotions.length} emotions`,
        celleEvent
      );
    }

    if (multiScaleLogger && stage === "chat") {
      const celleEvent = logCelleEvent(
        "Claude Code",
        `User stress level: ${stressLevel}/10, somatic signals: ${somaticSignals.filter(s => s.checked).length}`,
        "Stress + somatic patterns correlate → polyvagal state detection",
        "Progressed to Stage 3 (Chat) via RAIN module",
        "Self-regulation practice enhances emotional capacity",
        "RAIN module integration and polyvagal routing"
      );

      multiScaleLogger.logBottomUpEmergence(
        `User stress ${stressLevel}/10`,
        celleEvent
      );
    }

    setCurrentStage(stage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleRestart = () => {
    setCurrentStage("emotions");
    setSelectedEmotions([]);
    setStressLevel(5);
    setSomaticSignals(defaultSomaticSignals);
    setLiraAnswers([]);
    localStorage.removeItem("navlosen-current-stage");
    localStorage.removeItem("navlosen-emotions");
    localStorage.removeItem("navlosen-stress-level");
    localStorage.removeItem("navlosen-somatic-signals");
    localStorage.removeItem("navlosen-lira-answers");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  // Build session data for recommendations
  const sessionData: SessionData = {
    emotions: selectedEmotions,
    stressLevel,
    somaticSignals,
    liraAnswers,
    healthConnect,
    weather,
    timestamp: new Date().toISOString(),
  };

  // Get background color based on stress level (subtle, not overwhelming)
  const getBackgroundColor = (): string => {
    if (stressLevel <= 3) return "bg-green-50/50";
    if (stressLevel <= 7) return "bg-orange-50/50";
    return "bg-blue-50/50";
  };

  return (
    <Layout>
      {/* Consent Modal - Shown before any content */}
      {!hasConsented && (
        <ConsentModal onConsent={() => setHasConsented(true)} />
      )}

      <div className={`min-h-screen transition-all duration-700 ${getBackgroundColor()} -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8`}>
        {/* Render current stage */}
        {currentStage === "emotions" && (
          <Stage1Emotions
            selectedEmotions={selectedEmotions}
            onChange={setSelectedEmotions}
            onNext={() => goToStage("signals")}
          />
        )}

        {currentStage === "signals" && !showRAIN && (
          <Stage2Signals
            stressLevel={stressLevel}
            onStressChange={setStressLevel}
            somaticSignals={somaticSignals}
            onSignalsChange={setSomaticSignals}
            selectedEmotions={selectedEmotions.map(e => e.word)}
            onBack={() => goToStage("emotions")}
            onNext={() => setShowRAIN(true)}
          />
        )}

        {/* RAIN Mini-Module - Optional between Stage 2 and 3 */}
        {currentStage === "signals" && showRAIN && (
          <RAINModule
            onComplete={() => {
              setShowRAIN(false);
              goToStage("chat");
            }}
            onSkip={() => {
              setShowRAIN(false);
              goToStage("chat");
            }}
            showSkipButton={true}
          />
        )}

        {currentStage === "chat" && (
          <Stage3Chat
            stressLevel={stressLevel}
            onAnswersChange={setLiraAnswers}
            onBack={() => goToStage("signals")}
            onNext={() => goToStage("recommendations")}
          />
        )}

        {currentStage === "recommendations" && (
          <Stage4Recommendations
            sessionData={sessionData}
            onBack={() => goToStage("chat")}
            onRestart={handleRestart}
          />
        )}
      </div>
    </Layout>
  );
}

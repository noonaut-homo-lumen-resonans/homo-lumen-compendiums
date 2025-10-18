"use client";

import React, { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import Stage1Emotions from "@/components/mestring/Stage1Emotions";
import Stage2Signals from "@/components/mestring/Stage2Signals";
import Stage3LiraChat from "@/components/mestring/Stage3LiraChat";
import Stage4Results from "@/components/mestring/Stage4Results";
import { SomaticSignal } from "@/types";
import { Heart } from "lucide-react";
import {
  calculateCompositeStressScore,
  type CompositeStressInput,
  type LiraAnswer,
} from "@/lib/compositeStressScore";

type FlowStage = "emotions" | "signals" | "chat" | "results";

/**
 * Mestring Page - Multi-Stage Adaptive Flow
 *
 * NAV-Losen's stress regulation and self-awareness page
 * Based on Polyvagal Theory by Stephen Porges
 *
 * 4-stage wizard that guides users through:
 * 1. Emotion Check-in (100 words in 4 quadrants)
 * 2. Trykk & Signaler (Stress slider + Somatic awareness)
 * 3. Lira Chat (2-5 adaptive questions based on stress state)
 * 4. Results (Composite stress score + Recommended strategies + Min Reise link)
 *
 * Features:
 * - Composite Stress Score (weighted combination of all inputs)
 * - Polyvagal state indicator throughout flow
 * - Personalized regulation strategies
 *
 * Triadisk Score: 0.2 (PROCEED)
 * - Suverenitet: User-controlled regulation and progression
 * - Koherens: Grounded in neuroscience
 * - Healing: Direct capacity building
 */
export default function MestringPage() {
  // Stage management
  const [currentStage, setCurrentStage] = useState<FlowStage>("emotions");

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

  // Load from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedStage = localStorage.getItem("navlosen-mestring-stage");
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

  // Save to localStorage when stage changes
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-mestring-stage", currentStage);
    }
  }, [currentStage]);

  // Save to localStorage when state changes
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

  // Calculate Composite Stress Score
  const compositeInput: CompositeStressInput = {
    stressSlider: stressLevel,
    selectedEmotions: selectedEmotions.map((e) => ({
      word: e.word,
      quadrant: e.quadrant || 1,
    })),
    somaticSignals,
    liraAnswers,
  };

  const compositeResult = calculateCompositeStressScore(compositeInput);
  const currentState = compositeResult.polyvagalState;

  // Background color based on stress state
  const getBackgroundColor = (): string => {
    switch (currentState) {
      case "ventral":
        return "bg-green-50";
      case "sympathetic":
        return "bg-orange-50";
      case "dorsal":
        return "bg-blue-50";
    }
  };

  // Navigation handlers
  const handleNext = (nextStage: FlowStage) => {
    setCurrentStage(nextStage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleBack = (prevStage: FlowStage) => {
    setCurrentStage(prevStage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleRestart = () => {
    setCurrentStage("emotions");
    setSelectedEmotions([]);
    setStressLevel(5);
    setSomaticSignals(defaultSomaticSignals);
    setLiraAnswers([]);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <Layout>
      <div
        className={`min-h-screen transition-all duration-700 ease-in-out ${getBackgroundColor()} -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8`}
        style={{
          transform: `scale(${currentState === "dorsal" ? 0.98 : 1})`,
        }}
      >
        {/* Page header (only show on first stage) */}
        {currentStage === "emotions" && (
          <div className="w-full mb-8 text-left">
            {/* Breadcrumb */}
            <div className="mb-4 text-sm text-[var(--color-text-secondary)]">
              <span>NAV-Losen</span>
              <span className="mx-2">/</span>
              <span className="text-[var(--color-text-primary)] font-medium">Mestring</span>
            </div>

            <div className="flex items-center gap-3 mb-2">
              <Heart className="h-8 w-8 text-red-500" />
              <h1 className="text-3xl font-bold text-[var(--color-text-primary)] text-left">
                Mestring og Indre Ro
              </h1>
            </div>
            <p className="text-lg text-[var(--color-text-secondary)] text-left">
              Et trygt rom for å sjekke inn med deg selv og finne verktøy for
              regulering.
            </p>
          </div>
        )}

        {/* Main content */}
        <div className="w-full">
          {currentStage === "emotions" && (
            <Stage1Emotions
              selectedEmotions={selectedEmotions}
              onChange={setSelectedEmotions}
              onNext={() => handleNext("signals")}
              polyvagalState={currentState}
            />
          )}

          {currentStage === "signals" && (
            <Stage2Signals
              stressLevel={stressLevel}
              onStressChange={setStressLevel}
              somaticSignals={somaticSignals}
              onSignalsChange={setSomaticSignals}
              onBack={() => handleBack("emotions")}
              onNext={() => handleNext("chat")}
              polyvagalState={currentState}
            />
          )}

          {currentStage === "chat" && (
            <Stage3LiraChat
              stressState={currentState}
              liraAnswers={liraAnswers}
              onAnswersChange={setLiraAnswers}
              onBack={() => handleBack("signals")}
              onNext={() => handleNext("results")}
              polyvagalState={currentState}
            />
          )}

          {currentStage === "results" && (
            <Stage4Results
              compositeResult={compositeResult}
              selectedEmotions={selectedEmotions}
              stressLevel={stressLevel}
              somaticSignals={somaticSignals}
              onBack={() => handleBack("chat")}
              onRestart={handleRestart}
              polyvagalState={currentState}
            />
          )}
        </div>
      </div>
    </Layout>
  );
}

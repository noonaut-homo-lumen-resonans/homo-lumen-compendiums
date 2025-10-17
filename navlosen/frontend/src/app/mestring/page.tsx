"use client";

import React, { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import EmotionQuadrant from "@/components/mestring/EmotionQuadrant";
import StressSlider from "@/components/mestring/StressSlider";
import SomaticSignals from "@/components/mestring/SomaticSignals";
import StrategyCard from "@/components/mestring/StrategyCard";
import { SomaticSignal, Strategy, StressState } from "@/types";
import { Heart } from "lucide-react";

/**
 * Mestring Page (Crown Jewel!)
 *
 * NAV-Losen's stress regulation and self-awareness page
 * Based on Polyvagal Theory by Stephen Porges
 *
 * Features:
 * - Emotion check-in (circumplex model)
 * - Stress level tracking (1-10 polyvagal scale)
 * - Somatic awareness (body signals)
 * - Personalized regulation strategies
 *
 * Triadisk Score: 0.2 (PROCEED)
 * - Suverenitet: User-controlled regulation
 * - Koherens: Grounded in neuroscience
 * - Healing: Direct capacity building
 */
export default function MestringPage() {
  // Default somatic signals
  const defaultSomaticSignals: SomaticSignal[] = [
    { id: "rask-puls", label: "Rask puls eller hjertebank", checked: false },
    { id: "anspent-kjeve", label: "Anspent kjeve eller skuldre", checked: false },
    { id: "grunn-pust", label: "Grunn eller rask pust", checked: false },
    { id: "mage-uro", label: "Uro i magen eller kvalme", checked: false },
    { id: "trett", label: "Tretthet eller tung kropp", checked: false },
    { id: "nummen", label: "Nummen eller koblet fra", checked: false },
  ];

  // State management with localStorage
  const [selectedEmotions, setSelectedEmotions] = useState<{ word: string; quadrant: number | null }[]>([]);
  const [stressLevel, setStressLevel] = useState<number>(5);
  const [somaticSignals, setSomaticSignals] = useState<SomaticSignal[]>(defaultSomaticSignals);

  // Load from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedEmotions = localStorage.getItem("navlosen-emotions");
      const savedStressLevel = localStorage.getItem("navlosen-stress-level");
      const savedSignals = localStorage.getItem("navlosen-somatic-signals");

      if (savedEmotions) {
        setSelectedEmotions(JSON.parse(savedEmotions));
      }
      if (savedStressLevel) {
        setStressLevel(Number(savedStressLevel));
      }
      if (savedSignals) {
        setSomaticSignals(JSON.parse(savedSignals));
      }
    }
  }, []);

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

  // Determine current stress state
  const getStressState = (): StressState => {
    if (stressLevel <= 3) return "ventral";
    if (stressLevel <= 7) return "sympathetic";
    return "dorsal";
  };

  const currentState = getStressState();

  // Strategies (4 core strategies from Design System)
  const allStrategies: Strategy[] = [
    {
      id: "breathing-468",
      title: "Pust: 4-6-8 metoden",
      description:
        "Pust inn gjennom nesen i 4 sekunder. Hold pusten i 6 sekunder. Pust ut gjennom munnen i 8 sekunder. Gjenta 3-5 ganger. Denne teknikken aktiverer parasympatiske nervesystemet og fremmer ro. Lang utpust signaliserer til kroppen at du er trygg.",
      duration: "1-3 min",
      stressState: "sympathetic",
    },
    {
      id: "grounding-54321",
      title: "Jording: 5-4-3-2-1 teknikken",
      description:
        "Navngi 5 ting du ser, 4 ting du hører, 3 ting du kan berøre, 2 ting du lukter, og 1 ting du smaker. Denne teknikken bringer deg tilbake til nåtiden og ut av tankespiraler. Den gir nervesystemet sansebaserte ankerpunkt.",
      duration: "2-5 min",
      stressState: "dorsal",
    },
    {
      id: "small-action",
      title: "Handling: Ett lite steg",
      description:
        "Velg én liten, håndterbar oppgave du kan fullføre akkurat nå (f.eks. drikke et glass vann, sende én e-post, rydde ett lite område). Fullføring av små oppgaver gir mestringsfølelse og aktiverer belønningssystemet i hjernen.",
      duration: "3 min",
      stressState: "sympathetic",
    },
    {
      id: "progressive-relaxation",
      title: "Progressiv muskelavslapning",
      description:
        "Stram alle musklene i kroppen i 5 sekunder, deretter slipp. Start med føttene, arbeid deg oppover. Merk forskjellen mellom anspent og avslappet. Denne teknikken reduserer fysisk spenning og øker kroppsbevissthet.",
      duration: "5-10 min",
      stressState: "ventral",
    },
  ];

  // Filter strategies based on stress state
  const getRecommendedStrategies = (): Strategy[] => {
    // Always show breathing
    const breathing = allStrategies.find((s) => s.id === "breathing-468")!;

    if (currentState === "ventral") {
      // Low stress: show preventative strategies
      return [
        breathing,
        allStrategies.find((s) => s.id === "progressive-relaxation")!,
      ].filter(Boolean);
    }

    if (currentState === "sympathetic") {
      // Medium stress: show active regulation
      return [
        breathing,
        allStrategies.find((s) => s.id === "small-action")!,
        allStrategies.find((s) => s.id === "grounding-54321")!,
      ].filter(Boolean);
    }

    // High stress (dorsal): show grounding
    return [
      allStrategies.find((s) => s.id === "grounding-54321")!,
      breathing,
    ].filter(Boolean);
  };

  const recommendedStrategies = getRecommendedStrategies();

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

  return (
    <Layout>
      <div
        className={`min-h-screen transition-all duration-700 ease-in-out ${getBackgroundColor()} -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8`}
        style={{
          transform: `scale(${currentState === "dorsal" ? 0.98 : 1})`,
        }}
      >
        {/* Page header */}
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

        {/* Main content */}
        <div className="w-full space-y-8">
          {/* 1. Emotion Check-in */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <EmotionQuadrant
              selectedEmotions={selectedEmotions}
              onChange={setSelectedEmotions}
            />
          </div>

          {/* 2. Stress Level */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <StressSlider value={stressLevel} onChange={setStressLevel} />
          </div>

          {/* 3. Somatic Signals */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <SomaticSignals
              signals={somaticSignals}
              onChange={setSomaticSignals}
            />
          </div>

          {/* 4. Recommended Strategies */}
          <div className="text-left">
            <h2 className="text-2xl font-semibold text-[var(--color-text-primary)] mb-4 text-left">
              Anbefalte strategier for deg
            </h2>
            <p className="text-sm text-[var(--color-text-secondary)] mb-6 text-left">
              Basert på ditt stressnivå ({stressLevel}/10) foreslår vi disse
              teknikkene:
            </p>

            <div className="grid md:grid-cols-2 gap-4">
              {recommendedStrategies.map((strategy) => (
                <StrategyCard key={strategy.id} strategy={strategy} />
              ))}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>ℹ️ Viktig:</strong> Disse teknikkene er verktøy for
              selvregulering, ikke medisinsk behandling. Hvis du opplever alvorlig
              angst, depresjon eller selvmordstanker, kontakt fastlegen din eller
              ring Mental Helse på{" "}
              <a
                href="tel:116123"
                className="underline font-semibold hover:text-blue-900"
              >
                116 123
              </a>
              .
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

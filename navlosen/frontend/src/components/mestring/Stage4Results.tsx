"use client";

import React from "react";
import Button from "@/components/ui/Button";
import StrategyCard from "@/components/mestring/StrategyCard";
import { ArrowLeft, RefreshCw, Brain, MapPin } from "lucide-react";
import { Strategy, SomaticSignal } from "@/types";
import Link from "next/link";
import {
  type CompositeStressResult,
} from "@/lib/compositeStressScore";

interface Stage4ResultsProps {
  compositeResult: CompositeStressResult;
  selectedEmotions: { word: string; quadrant: number | null }[];
  stressLevel: number;
  somaticSignals: SomaticSignal[];
  onBack: () => void;
  onRestart: () => void;
  polyvagalState: string;
}

/**
 * Stage 4: Results & Recommendations
 *
 * Final step: Shows composite stress score, recommended strategies,
 * and link to Min Reise for long-term journey tracking.
 *
 * Triadisk Score: 0.22 (PROCEED)
 */
export default function Stage4Results({
  compositeResult,
  selectedEmotions,
  stressLevel,
  somaticSignals,
  onBack,
  onRestart,
  polyvagalState,
}: Stage4ResultsProps) {
  const currentState = compositeResult.polyvagalState;

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
    const breathing = allStrategies.find((s) => s.id === "breathing-468")!;

    if (currentState === "ventral") {
      return [
        breathing,
        allStrategies.find((s) => s.id === "progressive-relaxation")!,
      ].filter(Boolean);
    }

    if (currentState === "sympathetic") {
      return [
        breathing,
        allStrategies.find((s) => s.id === "small-action")!,
        allStrategies.find((s) => s.id === "grounding-54321")!,
      ].filter(Boolean);
    }

    // Dorsal: show grounding first
    return [
      allStrategies.find((s) => s.id === "grounding-54321")!,
      breathing,
    ].filter(Boolean);
  };

  const recommendedStrategies = getRecommendedStrategies();

  const getStateLabel = () => {
    switch (currentState) {
      case "ventral":
        return "Rolig";
      case "sympathetic":
        return "Aktivert";
      case "dorsal":
        return "Overveldet";
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
        </div>
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600">Steg 4 av 4: Dine resultater</p>
          <div className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-700">
            Tilstand: {polyvagalState === "ventral" ? "Rolig" : polyvagalState === "sympathetic" ? "Aktivert" : "Overveldet"}
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="mb-8 text-left">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Din tilstand akkurat nå
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)]">
          Her er en oppsummering av din tilstand og anbefalte strategier.
        </p>
      </div>

      {/* Composite Stress Score Card */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="h-6 w-6 text-purple-500" />
          <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
            Samlet Stress-Analyse
          </h3>
        </div>

        <div className="space-y-4">
          {/* Composite Score */}
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Kompositt Score (1-10):
            </span>
            <span
              className="text-2xl font-bold"
              style={{
                color:
                  currentState === "ventral"
                    ? "#4CAF50"
                    : currentState === "sympathetic"
                    ? "#FF9800"
                    : "#2196F3",
              }}
            >
              {compositeResult.compositeScore.toFixed(1)}
            </span>
          </div>

          {/* Polyvagal State */}
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Din tilstand:
            </span>
            <span
              className="px-3 py-1 rounded-full text-sm font-semibold"
              style={{
                backgroundColor:
                  currentState === "ventral"
                    ? "#4CAF5020"
                    : currentState === "sympathetic"
                    ? "#FF980020"
                    : "#2196F320",
                color:
                  currentState === "ventral"
                    ? "#4CAF50"
                    : currentState === "sympathetic"
                    ? "#FF9800"
                    : "#2196F3",
              }}
            >
              {getStateLabel()}
            </span>
          </div>

          {/* Confidence */}
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              Analysetillit:
            </span>
            <div className="flex items-center gap-2">
              <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-purple-500 rounded-full transition-all"
                  style={{ width: `${compositeResult.confidence * 100}%` }}
                />
              </div>
              <span className="text-xs text-gray-600">
                {Math.round(compositeResult.confidence * 100)}%
              </span>
            </div>
          </div>

          {/* Breakdown */}
          <details className="mt-4">
            <summary className="text-sm font-medium text-gray-700 cursor-pointer hover:text-purple-600">
              Vis detaljert analyse
            </summary>
            <div className="mt-3 space-y-2 text-xs text-gray-600">
              <div className="flex justify-between">
                <span>Stress Slider (40%):</span>
                <span className="font-medium">
                  {compositeResult.breakdown.sliderContribution.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Følelser (30%):</span>
                <span className="font-medium">
                  {compositeResult.breakdown.emotionContribution.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Kropps-signaler (20%):</span>
                <span className="font-medium">
                  {compositeResult.breakdown.somaticContribution.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Lira Spørsmål (10%):</span>
                <span className="font-medium">
                  {compositeResult.breakdown.liraContribution.toFixed(2)}
                </span>
              </div>
            </div>
          </details>
        </div>

        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-xs text-blue-800">
            <strong>💡 Om Kompositt Score:</strong> Dette tallet kombinerer
            alle dine input (følelser, kropps-signaler, stress-slider, Lira-spørsmål) for å
            gi et mer nøyaktig bilde av din tilstand. Jo flere data du
            oppgir, desto høyere blir analysetilliten.
          </p>
        </div>
      </div>

      {/* Recommended Strategies */}
      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-[var(--color-text-primary)] mb-4">
          Anbefalte strategier for deg
        </h2>
        <p className="text-sm text-[var(--color-text-secondary)] mb-6">
          Basert på din tilstand ({getStateLabel()} - {compositeResult.compositeScore.toFixed(1)}/10)
          foreslår vi disse teknikkene:
        </p>

        <div className="grid md:grid-cols-2 gap-4">
          {recommendedStrategies.map((strategy) => (
            <StrategyCard key={strategy.id} strategy={strategy} />
          ))}
        </div>
      </div>

      {/* Min Reise Link */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg p-6 mb-8 border-2 border-purple-200">
        <div className="flex items-start gap-4">
          <MapPin className="h-8 w-8 text-purple-600 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="font-bold text-lg mb-2">Spor din reise over tid</h3>
            <p className="text-sm text-gray-700 mb-4">
              Denne sjekk-inn er et øyeblikksbilde. Vil du se hvordan tilstanden din
              utvikler seg over tid? Gå til <strong>Min Reise</strong> for å spore
              fremgang og mønstre.
            </p>
            <Link href="/min-reise">
              <Button variant="primary" size="medium">
                Gå til Min Reise
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
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

      {/* Navigation */}
      <div className="flex justify-between items-center">
        <Button
          variant="secondary"
          size="large"
          onClick={onBack}
          leftIcon={<ArrowLeft className="h-5 w-5" />}
        >
          Tilbake
        </Button>
        <Button
          variant="text"
          size="large"
          onClick={onRestart}
          leftIcon={<RefreshCw className="h-5 w-5" />}
        >
          Start ny sesjon
        </Button>
      </div>
    </div>
  );
}

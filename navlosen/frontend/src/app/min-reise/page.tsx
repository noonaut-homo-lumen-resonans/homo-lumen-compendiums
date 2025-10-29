"use client";

import { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import MasteryLog from "@/components/mestring/MasteryLog";
import BiofeltCheckpoint from "@/components/mestring/BiofeltCheckpoint";
import JourneySuccess from "@/components/mestring/JourneySuccess";
import PersonalityAvatar from "@/components/traits/PersonalityAvatar";
import PersonalityModal from "@/components/traits/PersonalityModal";
import BigFiveSurvey from "@/components/traits/BigFiveSurvey";
import { BookOpen, Heart, Compass, Sparkles, User, TrendingUp } from "lucide-react";
import { BigFive } from "@/types";
import { loadBigFive, saveSelfReport, deleteBigFiveData } from "@/utils/bigfive/mergeProfiles";
import {
  calculateCompositeStressScore,
  type CompositeStressInput,
  type LiraAnswer,
} from "@/lib/compositeStressScore";
import { SomaticSignal } from "@/types";
import AffectTimeline from "@/components/timeline/AffectTimeline";
import HealthMetrics from "@/components/min-reise/HealthMetrics";
import WeatherWidget from "@/components/min-reise/WeatherWidget";

export default function MinReisePage() {
  const [activeView, setActiveView] = useState<"overview" | "mastery" | "checkpoint" | "celebration" | "timeline">("overview");
  const [bigFive, setBigFive] = useState<BigFive | undefined>(undefined);
  const [currentState, setCurrentState] = useState<"ventral" | "sympathetic" | "dorsal">("ventral");
  const [showPersonalityModal, setShowPersonalityModal] = useState(false);
  const [showSurvey, setShowSurvey] = useState(false);

  const handleSurveyComplete = (newBigFive: BigFive) => {
    saveSelfReport(newBigFive);
    setBigFive(newBigFive);
    setShowSurvey(false);
    setShowPersonalityModal(true);
  };

  const handleDelete = () => {
    deleteBigFiveData();
    setBigFive(undefined);
    setShowPersonalityModal(false);
  };

  const handleEdit = () => {
    setShowPersonalityModal(false);
    setShowSurvey(true);
  };

  useEffect(() => {
    // Hide sidebar on this page
    const sidebar = document.querySelector('aside');
    if (sidebar) {
      sidebar.style.display = 'none';
    }

    // Load BigFive and polyvagal state
    if (typeof window !== "undefined") {
      try {
        // Load BigFive personality data
        const loadedBigFive = loadBigFive();
        if (loadedBigFive) {
          setBigFive(loadedBigFive);
        }

        // Load polyvagal state from Mestring data
        const savedEmotions = localStorage.getItem("navlosen-emotions");
        const savedStressLevel = localStorage.getItem("navlosen-stress-level");
        const savedSignals = localStorage.getItem("navlosen-somatic-signals");
        const savedAnswers = localStorage.getItem("navlosen-lira-answers");

        if (savedEmotions || savedStressLevel || savedSignals || savedAnswers) {
          const compositeInput: CompositeStressInput = {
            stressSlider: savedStressLevel ? Number(savedStressLevel) : 5,
            selectedEmotions: savedEmotions
              ? JSON.parse(savedEmotions).map((e: { word: string; quadrant: number | null }) => ({
                  word: e.word,
                  quadrant: e.quadrant || 1,
                }))
              : [],
            somaticSignals: savedSignals
              ? JSON.parse(savedSignals)
              : ([] as SomaticSignal[]),
            liraAnswers: savedAnswers ? JSON.parse(savedAnswers) : ([] as LiraAnswer[]),
          };

          const result = calculateCompositeStressScore(compositeInput);
          setCurrentState(result.polyvagalState);
        }
      } catch (e) {
        console.error("Failed to load personality or biofield data", e);
      }
    }

    return () => {
      // Show sidebar again when leaving this page
      const sidebar = document.querySelector('aside');
      if (sidebar) {
        sidebar.style.display = '';
      }
    };
  }, []);

  return (
    <Layout>
      <div className="bg-gradient-to-b from-blue-50 via-cyan-50 to-teal-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">
      {activeView === "overview" && (
        <div className="w-full">
          {/* Page header */}
          <div className="w-full mb-8 text-left">
            {/* Breadcrumb */}
            <div className="mb-4 text-sm text-gray-600">
              <span>NAV-Losen</span>
              <span className="mx-2">/</span>
              <span className="text-gray-900 font-medium">Min Reise</span>
            </div>

            <div className="flex items-center gap-3 mb-2">
              <Compass className="h-8 w-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900 text-left">Min Reise</h1>
            </div>
            <p className="text-lg text-gray-600 text-left">
              Reflekter, øv, og bygg din egen vei til mestring
            </p>
          </div>

          {/* Main content */}
          <div className="w-full space-y-8">
            {/* Reminder callout */}
            <div className="bg-purple-50 border-l-4 border-purple-400 p-6 rounded-lg">
              <div className="flex items-start gap-3">
                <Heart className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-purple-900 mb-2">
                    Husk: Dette handler ikke om perfeksjon
                  </h3>
                  <p className="text-sm text-purple-800">
                    Målet er ikke å bruke NAV-Losen for alltid. Målet er at du lærer deg selv
                    å kjenne, bygger din egen verktøykasse, og over tid blir mer selvstendig
                    i din mestring.
                  </p>
                </div>
              </div>
            </div>

            {/* Navigation cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <button
                onClick={() => setActiveView("timeline")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-purple-300 text-left"
              >
                <div className="mb-4">
                  <TrendingUp className="h-12 w-12 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Din følelsesreise
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Se dine emosjonelle mønstre over tid.
                </p>
                <div className="text-purple-600 font-medium text-sm">
                  Se historikk →
                </div>
              </button>

              <button
                onClick={() => setActiveView("mastery")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-cyan-300 text-left"
              >
                <div className="mb-4">
                  <BookOpen className="h-12 w-12 text-cyan-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Mestringslogg
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Dine egne strategier som virker for deg.
                </p>
                <div className="text-cyan-600 font-medium text-sm">
                  Åpne logg →
                </div>
              </button>

              <button
                onClick={() => setActiveView("checkpoint")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-cyan-300 text-left"
              >
                <div className="mb-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-300 to-amber-400"></div>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Biofelt-checkpoint
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Ta en kort pause med 4-6-8 pustemetoden.
                </p>
                <div className="text-cyan-600 font-medium text-sm">
                  Start pusteøvelse →
                </div>
              </button>

              <button
                onClick={() => setActiveView("celebration")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-green-300 text-left"
              >
                <div className="mb-4">
                  <Sparkles className="h-12 w-12 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Feire reisen
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Se din reise fra storm til trygg havn.
                </p>
                <div className="text-green-600 font-medium text-sm">
                  Se din reise →
                </div>
              </button>

              <button
                onClick={() => setShowPersonalityModal(true)}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-orange-300 text-left"
              >
                <div className="mb-4 flex items-center justify-center">
                  {bigFive ? (
                    <PersonalityAvatar
                      bigFive={bigFive}
                      polyvagalState={currentState}
                      size="medium"
                      interactive={false}
                      showLabel={false}
                    />
                  ) : (
                    <User className="h-12 w-12 text-orange-600" />
                  )}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Din personlighet
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Utforsk din personlighetsprofil og hvordan den påvirker din reise.
                </p>
                <div className="text-orange-600 font-medium text-sm">
                  {bigFive ? "Se profil →" : "Lag profil →"}
                </div>
              </button>

              {/* Health Metrics Widget */}
              <HealthMetrics />

              {/* Weather Widget */}
              <WeatherWidget />
            </div>

            {/* Back link */}
            <div className="text-center">
              <a
                href="/"
                className="text-blue-600 hover:text-blue-800 underline font-medium"
              >
                ← Tilbake til hovedside
              </a>
            </div>
          </div>
        </div>
      )}

      {activeView === "mastery" && (
        <div className="w-full">
          <MasteryLog onClose={() => setActiveView("overview")} />
        </div>
      )}

      {activeView === "checkpoint" && (
        <div className="w-full">
          <BiofeltCheckpoint
            onComplete={() => setActiveView("overview")}
            onSkip={() => setActiveView("overview")}
            showSkipButton={true}
          />
        </div>
      )}

      {activeView === "celebration" && (
        <div className="w-full">
          <JourneySuccess
            title="Din Reise"
            message="Du har navigert gjennom utfordringer og funnet din vei til trygghet."
            onContinue={() => setActiveView("overview")}
            showAnimation={true}
          />
        </div>
      )}

      {activeView === "timeline" && (
        <div className="w-full">
          {/* Header */}
          <div className="mb-6">
            <button
              onClick={() => setActiveView("overview")}
              className="text-blue-600 hover:text-blue-800 mb-4 flex items-center gap-2"
            >
              ← Tilbake til oversikt
            </button>

            {/* Educational intro */}
            <div className="bg-purple-50 border-l-4 border-purple-400 p-6 rounded-lg mb-6">
              <div className="flex items-start gap-3">
                <TrendingUp className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-purple-900 mb-2">
                    Ditt emosjonelle minne
                  </h3>
                  <p className="text-sm text-purple-800">
                    Dette er din "digitale hippocampus" - et visuelt kart over dine følelser over tid.
                    Grafen viser hvordan din emosjonelle valens (positiv/negativ følelse) og arousal
                    (energinivå) endrer seg, slik at du kan se mønstre og lære deg selv bedre å kjenne.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Timeline component */}
          <AffectTimeline compact={false} />

          {/* Educational content about what the timeline shows */}
          <div className="mt-8 bg-white rounded-lg p-6 shadow-sm">
            <h3 className="font-semibold text-gray-800 mb-3">Om Circumplex-modellen</h3>
            <p className="text-sm text-gray-600 mb-3">
              Circumplex-kartet organiserer alle følelser i et todimensjonalt rom:
            </p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><span className="font-medium text-green-600">• Q1 (Grønn):</span> Behagelige følelser med høy energi (f.eks. glad, spent)</li>
              <li><span className="font-medium text-orange-600">• Q2 (Oransje):</span> Ubehagelige følelser med høy energi (f.eks. sint, stresset)</li>
              <li><span className="font-medium text-red-600">• Q3 (Rød):</span> Ubehagelige følelser med lav energi (f.eks. trist, lei deg)</li>
              <li><span className="font-medium text-blue-600">• Q4 (Blå):</span> Behagelige følelser med lav energi (f.eks. rolig, avslappet)</li>
            </ul>
            <p className="text-xs text-gray-500 mt-4">
              💡 Ved å kartlegge dine følelser over tid kan du oppdage mønstre som hjelper deg å forstå
              hva som trigger ulike emosjonelle tilstander, og finne strategier som fungerer best for deg.
            </p>
          </div>
        </div>
      )}

      {/* Personality Modal */}
      {showPersonalityModal && bigFive && (
        <PersonalityModal
          bigFive={bigFive}
          polyvagalState={currentState}
          onClose={() => setShowPersonalityModal(false)}
          onEdit={handleEdit}
        />
      )}

      {/* If no BigFive but clicked personality card, show survey */}
      {showPersonalityModal && !bigFive && !showSurvey && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-lg w-full p-6">
            <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-4">
              Lag din personlighetsprofil
            </h3>
            <p className="text-[var(--color-text-secondary)] mb-6">
              Du har ikke laget en personlighetsprofil ennå. Vil du svare på noen korte spørsmål for å få personaliserte anbefalinger?
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowPersonalityModal(false);
                  setShowSurvey(true);
                }}
                className="flex-1 px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-medium transition-colors"
              >
                Ja, start spørreskjema
              </button>
              <button
                onClick={() => setShowPersonalityModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg font-medium transition-colors"
              >
                Ikke nå
              </button>
            </div>
          </div>
        </div>
      )}

      {/* BigFive Survey */}
      {showSurvey && (
        <BigFiveSurvey
          onComplete={handleSurveyComplete}
          onCancel={() => setShowSurvey(false)}
          polyvagalState={currentState}
        />
      )}
      </div>
    </Layout>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import Link from "next/link";
import {
  Heart,
  Compass,
  Activity,
  TrendingUp,
  ArrowRight,
  CheckCircle2,
  Clock,
  Brain,
  Sparkles,
  Music,
} from "lucide-react";
import {
  calculateCompositeStressScore,
  getPolyvagalUIConfig,
  type CompositeStressInput,
  type LiraAnswer,
} from "@/lib/compositeStressScore";
import { SomaticSignal, BigFive } from "@/types";
import PersonalityAvatar from "@/components/traits/PersonalityAvatar";
import { loadBigFive } from "@/utils/bigfive/mergeProfiles";

/**
 * NAV-Losen Dashboard (Homepage)
 *
 * Overview page showing:
 * - Current biofield state (from Mestring data)
 * - Summary of recent activity
 * - Recommended next steps
 * - Quick access to main features
 *
 * Inspired by AMA's biofield-responsive dashboard patterns
 *
 * Triadisk Score: 0.15 (PROCEED)
 * - Suverenitet: User sees their own data, owns their journey
 * - Koherens: Grounded in polyvagal state awareness
 * - Healing: Gentle guidance toward capacity building
 */
export default function Dashboard() {
  const [currentState, setCurrentState] = useState<"ventral" | "sympathetic" | "dorsal">("ventral");
  const [compositeScore, setCompositeScore] = useState<number>(5);
  const [confidence, setConfidence] = useState<number>(0);
  const [hasData, setHasData] = useState<boolean>(false);
  const [bigFive, setBigFive] = useState<BigFive | undefined>(undefined);
  const [selectedEmotion, setSelectedEmotion] = useState<{
    word: string;
    color: string;
    svgPath: string;
    definition: string;
  } | null>(null);

  // Load data from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      try {
        const savedEmotions = localStorage.getItem("navlosen-emotions");
        const savedStressLevel = localStorage.getItem("navlosen-stress-level");
        const savedSignals = localStorage.getItem("navlosen-somatic-signals");
        const savedAnswers = localStorage.getItem("navlosen-lira-answers");
        const savedSelectedEmotion = localStorage.getItem("navlosen-selected-emotion");

        // Load selected emotion for avatar display
        if (savedSelectedEmotion) {
          try {
            const emotion = JSON.parse(savedSelectedEmotion);
            setSelectedEmotion(emotion);
          } catch (e) {
            console.error("Failed to parse selected emotion", e);
          }
        }

        if (savedEmotions || savedStressLevel || savedSignals || savedAnswers || savedSelectedEmotion) {
          setHasData(true);

          // Build composite input
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
          setCompositeScore(result.compositeScore);
          setConfidence(result.confidence);
        }

        // Load BigFive personality data
        const loadedBigFive = loadBigFive();
        if (loadedBigFive) {
          setBigFive(loadedBigFive);
        }
      } catch (e) {
        console.error("Failed to load dashboard data", e);
      }
    }
  }, []);

  const uiConfig = getPolyvagalUIConfig(currentState);

  // Get biofield message (inspired by AMA Lira's empathetic responses)
  const getBiofieldMessage = () => {
    if (confidence === 0) {
      return {
        title: "Velkommen til NAV-Losen",
        message: "Start din reise med å sjekke inn hvordan du har det akkurat nå.",
        icon: <Sparkles className="h-8 w-8 text-purple-500" />,
      };
    }

    if (currentState === "ventral") {
      return {
        title: "Du er i balanse",
        message:
          "Ditt biofelt resonerer med klarhet og styrke. Dette er en god tid for refleksjon og planlegging.",
        icon: <CheckCircle2 className="h-8 w-8 text-green-500" />,
      };
    }

    if (currentState === "sympathetic") {
      return {
        title: "Du er i aktivering",
        message:
          "Ditt biofelt viser økt energi. Husk å ta pauser og bruk pusteøvelser for regulering.",
        icon: <Activity className="h-8 w-8 text-orange-500" />,
      };
    }

    // Dorsal
    return {
      title: "Du trenger støtte",
      message:
        "Ditt biofelt søker trygghet og ro. Fokuser på grounding-øvelser og vurder å snakke med en veileder.",
      icon: <Heart className="h-8 w-8 text-blue-500" />,
    };
  };

  const biofieldMessage = getBiofieldMessage();

  // Get recommended actions (biofield-responsive)
  const getRecommendedActions = () => {
    if (!hasData) {
      return [
        {
          id: "mestring",
          title: "Start med Mestring",
          description: "Sjekk inn hvordan du har det akkurat nå",
          link: "/mestring",
          icon: <Heart className="h-6 w-6" />,
          priority: "high" as const,
        },
      ];
    }

    if (currentState === "dorsal") {
      return [
        {
          id: "jording",
          title: "Jording: 5-4-3-2-1",
          description: "Kom tilbake til nåtiden med sansebasert grounding",
          link: "/ovelser/grounding-54321",
          icon: <Heart className="h-6 w-6" />,
          priority: "high" as const,
        },
        {
          id: "pust",
          title: "Pust: 4-6-8",
          description: "Aktiver parasympatiske nervesystemet",
          link: "/ovelser/pust-468",
          icon: <Activity className="h-6 w-6" />,
          priority: "high" as const,
        },
        {
          id: "musikk-sikkerhet",
          title: "174 Hz - Sikkerhet",
          description: "Lydfrekvens for grunnleggende trygghet og smertereduksjon",
          link: "/musikk#174hz",
          icon: <Music className="h-6 w-6" />,
          priority: "medium" as const,
        },
      ];
    }

    if (currentState === "sympathetic") {
      return [
        {
          id: "update-mestring",
          title: "Oppdater Mestring",
          description: "Sjekk inn på nytt for å se hvordan du har det nå",
          link: "/mestring",
          icon: <Heart className="h-6 w-6" />,
          priority: "medium" as const,
        },
        {
          id: "pust",
          title: "Pust: 4-6-8",
          description: "Rolig ned aktivering med lang utpust",
          link: "/ovelser/pust-468",
          icon: <Activity className="h-6 w-6" />,
          priority: "high" as const,
        },
        {
          id: "musikk-balance",
          title: "432 Hz - Balance",
          description: "Naturens frekvens for ro og mental klarhet",
          link: "/musikk#432hz",
          icon: <Music className="h-6 w-6" />,
          priority: "medium" as const,
        },
        {
          id: "min-reise",
          title: "Se din fremgang",
          description: "Spor hvordan tilstanden din utvikler seg over tid",
          link: "/min-reise",
          icon: <Compass className="h-6 w-6" />,
          priority: "low" as const,
        },
      ];
    }

    // Ventral
    return [
      {
        id: "min-reise",
        title: "Utforsk Min Reise",
        description: "Se mønstre og fremgang over tid",
        link: "/min-reise",
        icon: <Compass className="h-6 w-6" />,
        priority: "high" as const,
      },
      {
        id: "musikk-connection",
        title: "639 Hz - Tilkobling",
        description: "Fremmer harmoni i relasjoner og kjærlighet",
        link: "/musikk#639hz",
        icon: <Music className="h-6 w-6" />,
        priority: "medium" as const,
      },
      {
        id: "veiledninger",
        title: "Utforsk Veiledninger",
        description: "Lær mer om dine rettigheter og muligheter",
        link: "/veiledninger",
        icon: <Brain className="h-6 w-6" />,
        priority: "medium" as const,
      },
    ];
  };

  const recommendedActions = getRecommendedActions();

  const getPriorityColor = (priority: "high" | "medium" | "low") => {
    switch (priority) {
      case "high":
        return "border-green-500 bg-green-50";
      case "medium":
        return "border-orange-500 bg-orange-50";
      case "low":
        return "border-blue-500 bg-blue-50";
    }
  };

  return (
    <Layout>
      <div
        className={`min-h-screen transition-all duration-700 ${uiConfig.backgroundColor} -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8`}
      >
        {/* Page Header */}
        <div className="max-w-6xl mx-auto mb-8">
          <h1 className="text-4xl font-bold text-[var(--color-text-primary)] mb-2">
            Dashboard
          </h1>
          <p className="text-lg text-[var(--color-text-secondary)]">
            Din personlige oversikt
          </p>
        </div>

        {/* Main Dashboard Content */}
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Biofield Status Card */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">{biofieldMessage.icon}</div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">
                  {biofieldMessage.title}
                </h2>
                <p className="text-base text-[var(--color-text-secondary)] mb-4">
                  {biofieldMessage.message}
                </p>

                {hasData && (
                  <div className="flex flex-col md:flex-row gap-6 mt-4 pt-4 border-t border-gray-200">
                    {/* Stats grid */}
                    <div className="flex-1 grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Kompositt Score</p>
                        <p className="text-2xl font-bold text-[var(--color-primary)]">
                          {compositeScore.toFixed(1)}/10
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Tilstand</p>
                        <p className="text-lg font-semibold">{uiConfig.stateLabel}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Analysetillit</p>
                        <p className="text-lg font-semibold">
                          {Math.round(confidence * 100)}%
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Sist oppdatert</p>
                        <p className="text-lg font-semibold flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          I dag
                        </p>
                      </div>
                    </div>

                    {/* Emotion Avatar or Personality Avatar */}
                    <div className="flex flex-col gap-4 justify-center items-center">
                      {/* Emotion Avatar */}
                      {selectedEmotion && (
                        <div className="flex flex-col items-center">
                          <p className="text-xs text-gray-600 mb-2 uppercase font-medium">
                            Din følelse
                          </p>
                          <div className="relative w-24 h-24 flex-shrink-0">
                            {selectedEmotion.svgPath && selectedEmotion.svgPath !== "" ? (
                              <svg
                                viewBox="0 0 100 100"
                                className="w-full h-full breathe-animation drop-shadow-lg"
                              >
                                <path
                                  d={selectedEmotion.svgPath}
                                  fill={selectedEmotion.color}
                                />
                              </svg>
                            ) : (
                              <div
                                className="w-full h-full rounded-full flex items-center justify-center text-white font-bold text-xl drop-shadow-lg breathe-animation"
                                style={{ backgroundColor: selectedEmotion.color }}
                              >
                                {selectedEmotion.word.charAt(0).toUpperCase()}
                              </div>
                            )}
                          </div>
                          <p
                            className="text-lg font-bold mt-2 text-center"
                            style={{ color: selectedEmotion.color }}
                          >
                            {selectedEmotion.word}
                          </p>
                          <p className="text-xs text-gray-600 italic text-center max-w-[200px]">
                            {selectedEmotion.definition}
                          </p>
                        </div>
                      )}

                      {/* Personality Avatar */}
                      {bigFive && (
                        <div className="flex justify-center items-center">
                          <PersonalityAvatar
                            bigFive={bigFive}
                            polyvagalState={currentState}
                            size="large"
                            interactive={true}
                            showLabel={false}
                          />
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Recommended Actions */}
          <div>
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-4 flex items-center gap-2">
              <TrendingUp className="h-6 w-6 text-[var(--color-primary)]" />
              Anbefalte neste steg
            </h2>

            <div className="grid md:grid-cols-2 gap-4">
              {recommendedActions.map((action) => (
                <Link
                  key={action.id}
                  href={action.link}
                  className={`block p-6 rounded-lg border-2 transition-all hover:shadow-lg ${getPriorityColor(
                    action.priority
                  )}`}
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 text-[var(--color-primary)]">
                      {action.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-1">
                        {action.title}
                      </h3>
                      <p className="text-sm text-[var(--color-text-secondary)] mb-3">
                        {action.description}
                      </p>
                      <div className="flex items-center gap-2 text-[var(--color-primary)] font-medium text-sm">
                        <span>Gå til</span>
                        <ArrowRight className="h-4 w-4" />
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-4">
              Hurtiglenker
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Link
                href="/mestring"
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
              >
                <Heart className="h-8 w-8 mx-auto mb-2 text-red-500" />
                <p className="font-semibold text-sm">Mestring</p>
              </Link>

              <Link
                href="/min-reise"
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
              >
                <Compass className="h-8 w-8 mx-auto mb-2 text-purple-500" />
                <p className="font-semibold text-sm">Min Reise</p>
              </Link>

              <Link
                href="/veiledninger"
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
              >
                <Brain className="h-8 w-8 mx-auto mb-2 text-blue-500" />
                <p className="font-semibold text-sm">Veiledninger</p>
              </Link>

              <Link
                href="/chatbot"
                className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-all text-center"
              >
                <Sparkles className="h-8 w-8 mx-auto mb-2 text-green-500" />
                <p className="font-semibold text-sm">Chat med Lira</p>
              </Link>
            </div>
          </div>

          {/* Info Card */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-bold text-lg mb-2 text-blue-900">
              Om NAV-Losen
            </h3>
            <p className="text-sm text-blue-800 mb-4">
              NAV-Losen hjelper deg med å navigere NAV-systemet med mindre stress.
              Vi bruker Polyvagal Teori for å tilpasse opplevelsen til din tilstand,
              og gir deg verktøy for selvregulering og mestring.
            </p>
            <p className="text-xs text-blue-700">
              <strong>Viktig:</strong> Dette er et støtteverktøy, ikke medisinsk
              behandling. Ved alvorlig angst eller depresjon, kontakt fastlegen eller
              ring Mental Helse på{" "}
              <a href="tel:116123" className="underline font-semibold">
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

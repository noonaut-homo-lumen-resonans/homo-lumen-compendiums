"use client";

import React from "react";
import Button from "@/components/ui/Button";
import { Heart, Activity, ArrowRight, RotateCcw, Home } from "lucide-react";
import type { EmotionWord } from "./emotionData";

interface Fase6ResultsProps {
  selectedEmotion: EmotionWord;
  pressureLevel: number;
  selectedSignals: string[];
  onRestart: () => void;
  onGoHome: () => void;
}

/**
 * Fase 6: Results & Recommendations
 *
 * Shows summary of user's check-in:
 * - Selected emotion with color
 * - Pressure level (0-10)
 * - Somatic signals
 * - Personalized recommendations based on quadrant
 * - Actions: Restart or Go to Dashboard
 *
 * Design: Full-width, spacious, celebratory
 * Triadisk Score: 0.12 (PROCEED)
 */
export default function Fase6Results({
  selectedEmotion,
  pressureLevel,
  selectedSignals,
  onRestart,
  onGoHome,
}: Fase6ResultsProps) {
  // Get quadrant-specific recommendations
  const getRecommendations = () => {
    const recommendations = {
      1: {
        // Q1: Høy Energi, Ubehagelig (Rød)
        title: "Du har høy energi og ubehag",
        message:
          "Dette er et tegn på at kroppen er i aktivering. Her er noen verktøy for å regulere ned:",
        strategies: [
          {
            icon: <Activity className="w-6 h-6 text-blue-600" />,
            title: "4-6-8 Pust",
            description: "Lang utpust for å aktivere parasympatiske nervesystemet",
            link: "/ovelser/pust-468",
          },
          {
            icon: <Heart className="w-6 h-6 text-purple-600" />,
            title: "5-4-3-2-1 Jording",
            description: "Kom tilbake til nåtiden med sansebasert grounding",
            link: "/ovelser/grounding-54321",
          },
          {
            icon: <Activity className="w-6 h-6 text-green-600" />,
            title: "Bevegelse",
            description: "Gå en tur, rist ut kroppen, eller strekk deg",
            link: null,
          },
        ],
      },
      2: {
        // Q2: Høy Energi, Behagelig (Gul)
        title: "Du har høy energi og behag",
        message:
          "Dette er en god tilstand for produktivitet og utforskning. Her er noen måter å utnytte energien:",
        strategies: [
          {
            icon: <Heart className="w-6 h-6 text-purple-600" />,
            title: "Utforsk Min Reise",
            description: "Reflekter over dine mønstre og fremgang",
            link: "/min-reise",
          },
          {
            icon: <Activity className="w-6 h-6 text-blue-600" />,
            title: "Planlegg fremover",
            description: "Bruk energien til å sette mål og lage planer",
            link: null,
          },
          {
            icon: <Heart className="w-6 h-6 text-green-600" />,
            title: "Del med andre",
            description: "Koble deg til venner eller familie",
            link: null,
          },
        ],
      },
      3: {
        // Q3: Lav Energi, Ubehagelig (Blå)
        title: "Du har lav energi og ubehag",
        message:
          "Dette kan være et tegn på at kroppen trenger hvile og trygghet. Her er noen verktøy:",
        strategies: [
          {
            icon: <Heart className="w-6 h-6 text-blue-600" />,
            title: "5-4-3-2-1 Jording",
            description: "Grounding for å finne tilbake til trygghet",
            link: "/ovelser/grounding-54321",
          },
          {
            icon: <Activity className="w-6 h-6 text-purple-600" />,
            title: "Healing Frekvenser",
            description: "174 Hz for sikkerhet, 396 Hz for frigjøring fra frykt",
            link: "/musikk",
          },
          {
            icon: <Heart className="w-6 h-6 text-green-600" />,
            title: "Hvile og omsorg",
            description: "Gi deg selv lov til å hvile, det er ikke svakhet",
            link: null,
          },
        ],
      },
      4: {
        // Q4: Lav Energi, Behagelig (Grønn)
        title: "Du har lav energi og behag",
        message:
          "Dette er en rolig, trygg tilstand - perfekt for refleksjon og restitusjon:",
        strategies: [
          {
            icon: <Heart className="w-6 h-6 text-purple-600" />,
            title: "Utforsk Min Reise",
            description: "Tid for dypere refleksjon og innsikt",
            link: "/min-reise",
          },
          {
            icon: <Activity className="w-6 h-6 text-blue-600" />,
            title: "Healing Frekvenser",
            description: "432 Hz for balanse, 528 Hz for transformasjon",
            link: "/musikk",
          },
          {
            icon: <Heart className="w-6 h-6 text-green-600" />,
            title: "Meditasjon og stillhet",
            description: "Nyt roen og la kroppen hvile",
            link: null,
          },
        ],
      },
    };

    return recommendations[selectedEmotion.quadrant];
  };

  const rec = getRecommendations();

  // Map signal IDs to readable labels
  const signalLabels: Record<string, string> = {
    hjertebank: "Hjertebank",
    "tung-pust": "Tung pust",
    knyttneve: "Knyttnever",
    "varm-bryst": "Varm i brystet",
    "kald-svette": "Kald svette",
    "knute-mage": "Knute i magen",
    "tung-kropp": "Tung kropp",
    anspent: "Anspente muskler",
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 via-blue-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mb-4 shadow-lg">
            <Heart className="w-10 h-10 text-white" fill="white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">
            Takk for at du delte!
          </h1>
          <p className="text-lg text-gray-600">
            Her er en oppsummering av din check-in
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* Card 1: Emotion */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100">
            <div className="flex items-start gap-4">
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0"
                style={{ backgroundColor: selectedEmotion.color }}
              >
                <span className="text-2xl">💭</span>
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-semibold text-gray-600 mb-1">
                  Din følelse
                </h3>
                <p
                  className="text-2xl font-bold mb-2"
                  style={{ color: selectedEmotion.color }}
                >
                  {selectedEmotion.word}
                </p>
                <p className="text-sm text-gray-600">
                  {selectedEmotion.definition}
                </p>
              </div>
            </div>
          </div>

          {/* Card 2: Pressure */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-semibold text-gray-600 mb-1">
                  Trykknivå
                </h3>
                <p className="text-4xl font-bold text-purple-600 mb-2">
                  {pressureLevel}
                  <span className="text-xl text-gray-400">/10</span>
                </p>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded-full transition-all"
                    style={{ width: `${(pressureLevel / 10) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Card 3: Signals */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="text-sm font-semibold text-gray-600 mb-2">
                  Kroppslige signaler
                </h3>
                {selectedSignals.length === 0 ? (
                  <p className="text-sm text-gray-500 italic">
                    Ingen signaler valgt
                  </p>
                ) : (
                  <div className="space-y-1">
                    {selectedSignals.map((signalId) => (
                      <div
                        key={signalId}
                        className="flex items-center gap-2 text-sm text-gray-700"
                      >
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                        <span>{signalLabels[signalId] || signalId}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations Section */}
        <div className="bg-white rounded-2xl p-8 shadow-lg border-2 border-gray-100">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {rec.title}
            </h2>
            <p className="text-base text-gray-600">{rec.message}</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {rec.strategies.map((strategy, index) => (
              <div
                key={index}
                className="border-2 border-gray-200 rounded-xl p-6 hover:border-purple-300 hover:shadow-md transition-all"
              >
                <div className="mb-4">{strategy.icon}</div>
                <h3 className="font-semibold text-gray-900 mb-2">
                  {strategy.title}
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  {strategy.description}
                </p>
                {strategy.link && (
                  <a
                    href={strategy.link}
                    className="inline-flex items-center gap-2 text-sm font-medium text-purple-600 hover:text-purple-700"
                  >
                    Gå til verktøy
                    <ArrowRight className="w-4 h-4" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            onClick={onRestart}
            variant="secondary"
            size="large"
            leftIcon={<RotateCcw className="w-5 h-5" />}
            className="min-w-[200px]"
          >
            Start på nytt
          </Button>
          <Button
            onClick={onGoHome}
            variant="primary"
            size="large"
            leftIcon={<Home className="w-5 h-5" />}
            className="min-w-[200px] bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
          >
            Tilbake til Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}

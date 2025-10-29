"use client";

import React, { useState } from "react";
import { cn } from "@/lib/utils";
import Button from "../ui/Button";
import { Heart, ArrowRight, Sparkles } from "lucide-react";

interface RAINModuleProps {
  onComplete: () => void;
  onSkip?: () => void;
  showSkipButton?: boolean;
}

/**
 * RAIN Mini-Module Component
 *
 * Guided mini-practice for self-regulation between stages.
 * RAIN = Recognize, Allow, Investigate, Nurture
 *
 * Based on Tara Brach's RAIN practice and Lira's guidance for
 * somatic awareness and self-compassion.
 *
 * Triadisk Score: -0.3 (STRONG HEALING)
 * - Port 1: Optional (skip button), user-paced
 * - Port 2: Teaches RAIN framework transparently
 * - Port 3: Builds self-regulation capacity
 */
export default function RAINModule({
  onComplete,
  onSkip,
  showSkipButton = true,
}: RAINModuleProps) {
  const [currentPhase, setCurrentPhase] = useState<number>(0);

  const phases = [
    {
      letter: "R",
      title: "Recognize",
      subtitle: "Hva la du merke til?",
      prompt:
        "Ta et øyeblikk for å legge merke til hva som er til stede akkurat nå. Kanskje en følelse, en tanke, eller en kroppsempfindelse.",
      reflection:
        "Legg merke til uten å bedømme. Bare observer hva som er der.",
      color: "blue",
      icon: "👁️",
    },
    {
      letter: "A",
      title: "Allow",
      subtitle: "La det være der",
      prompt:
        "I stedet for å skyve bort det du merker, la det få lov til å være til stede. Du trenger ikke gjøre noe med det.",
      reflection:
        "Si til deg selv: 'Det er OK at dette er her akkurat nå.' Det betyr ikke at du liker det, bare at du tillater det å være.",
      color: "green",
      icon: "🌿",
    },
    {
      letter: "I",
      title: "Investigate",
      subtitle: "Utforsk med nysgjerrighet",
      prompt:
        "Hvor i kroppen merker du dette? Hva er kvaliteten på følelsen? Tung, anspent, varm, kald?",
      reflection:
        "Utforsk med vennlig nysgjerrighet, som om du er en forsker som oppdager noe nytt.",
      color: "purple",
      icon: "🔍",
    },
    {
      letter: "N",
      title: "Nurture",
      subtitle: "Gi deg selv varme",
      prompt:
        "Hva trenger den delen av deg som kjenner dette akkurat nå? Kanskje medfølelse, ro, eller trygghet?",
      reflection:
        "Legg en hånd på hjertet eller på magen. Si noe varmt til deg selv, som du ville sagt til en venn.",
      color: "amber",
      icon: "💛",
    },
  ];

  const currentPhaseData = phases[currentPhase];
  const isLastPhase = currentPhase === phases.length - 1;

  const handleNext = () => {
    if (isLastPhase) {
      onComplete();
    } else {
      setCurrentPhase((prev) => prev + 1);
    }
  };

  const getColorClasses = (color: string) => {
    const colors = {
      blue: "from-blue-500 to-cyan-500 border-blue-300",
      green: "from-green-500 to-emerald-500 border-green-300",
      purple: "from-purple-500 to-pink-500 border-purple-300",
      amber: "from-amber-500 to-orange-500 border-amber-300",
    };
    return colors[color as keyof typeof colors] || colors.blue;
  };

  const getBackgroundColor = (color: string) => {
    const backgrounds = {
      blue: "bg-blue-50",
      green: "bg-green-50",
      purple: "bg-purple-50",
      amber: "bg-amber-50",
    };
    return backgrounds[color as keyof typeof backgrounds] || backgrounds.blue;
  };

  return (
    <div className="w-full min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12 fade-in">
      <div className="w-full max-w-5xl">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="h-7 w-7 text-purple-600" />
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Et øyeblikk for deg selv
            </h2>
          </div>
          <p className="text-lg text-gray-600">
            La oss ta en kort pause for selvregulering
          </p>
        </div>

        {/* Progress dots */}
        <div className="flex justify-center gap-3 mb-8">
          {phases.map((phase, index) => (
            <div
              key={index}
              className={cn(
                "w-3 h-3 rounded-full transition-all duration-300",
                index === currentPhase
                  ? "bg-gradient-to-r " + getColorClasses(phase.color) + " scale-125"
                  : index < currentPhase
                  ? "bg-gray-400"
                  : "bg-gray-200"
              )}
            />
          ))}
        </div>

        {/* Main card */}
        <div
          className={cn(
            "rounded-2xl p-6 sm:p-10 lg:p-14 shadow-xl transition-all duration-500",
            getBackgroundColor(currentPhaseData.color)
          )}
        >
          {/* Phase header */}
          <div className="text-center mb-8">
            <div className="text-7xl mb-5 sprout-animation">
              {currentPhaseData.icon}
            </div>
            <div
              className={cn(
                "inline-block px-6 py-2 rounded-full text-white font-bold text-lg mb-3 bg-gradient-to-r shadow-md",
                getColorClasses(currentPhaseData.color)
              )}
            >
              {currentPhaseData.letter}
            </div>
            <h3 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-2">
              {currentPhaseData.title}
            </h3>
            <p className="text-xl sm:text-2xl text-gray-700">
              {currentPhaseData.subtitle}
            </p>
          </div>

          {/* Prompt */}
          <div className="bg-white/90 backdrop-blur-sm rounded-xl p-6 sm:p-8 mb-6 shadow-sm">
            <p className="text-base sm:text-lg text-gray-800 leading-relaxed mb-5 text-left">
              {currentPhaseData.prompt}
            </p>
            <div className="border-l-4 border-gray-400 pl-5 bg-gray-50 rounded-r-lg py-3 pr-4">
              <p className="text-sm sm:text-base text-gray-700 italic text-left">
                💭 {currentPhaseData.reflection}
              </p>
            </div>
          </div>

          {/* Breathing guide (subtle) */}
          <div className="text-center mb-8">
            <div className="inline-block">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-white/60 to-white/30 breathe-animation shadow-lg" />
            </div>
            <p className="text-sm text-gray-600 mt-3 font-medium">Ta noen dype pust</p>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-4">
            {showSkipButton && onSkip ? (
              <Button
                variant="text"
                size="large"
                onClick={onSkip}
                className="text-gray-500 hover:text-gray-700 order-2 sm:order-1 w-full sm:w-auto"
              >
                Hopp over RAIN →
              </Button>
            ) : (
              <div className="hidden sm:block" />
            )}

            <Button
              variant="primary"
              size="large"
              onClick={handleNext}
              rightIcon={
                isLastPhase ? (
                  <Heart className="h-5 w-5" />
                ) : (
                  <ArrowRight className="h-5 w-5" />
                )
              }
              className="calm-hover text-base sm:text-lg px-8 py-4 order-1 sm:order-2 w-full sm:w-auto"
            >
              {isLastPhase ? "Fullfør RAIN" : `Neste: ${phases[currentPhase + 1].title}`}
            </Button>
          </div>
        </div>

        {/* Bottom info */}
        <div className="text-center mt-8">
          <p className="text-sm text-gray-500">
            RAIN-praksis fra Tara Brach • {currentPhase + 1} av {phases.length}
          </p>
        </div>
      </div>
    </div>
  );
}

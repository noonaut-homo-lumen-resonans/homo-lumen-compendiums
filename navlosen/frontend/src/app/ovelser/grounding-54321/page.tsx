"use client";

import React, { useState } from "react";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import { ArrowLeft, Check, ArrowRight } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

/**
 * 5-4-3-2-1 Grounding Exercise Page
 *
 * Interactive sensory grounding technique
 * - 5 things you see
 * - 4 things you hear
 * - 3 things you can touch
 * - 2 things you smell
 * - 1 thing you taste
 *
 * Based on mindfulness and trauma-informed care
 * Triadisk Score: 0.16 (PROCEED)
 */
export default function Grounding54321Page() {
  const [currentStep, setCurrentStep] = useState(0);
  const [responses, setResponses] = useState<string[]>([]);
  const [currentInput, setCurrentInput] = useState("");

  const steps = [
    {
      number: 5,
      sense: "Se",
      prompt: "Navngi 5 ting du kan se rundt deg akkurat nå",
      icon: "👁️",
      color: "blue",
    },
    {
      number: 4,
      sense: "Høre",
      prompt: "Navngi 4 ting du kan høre",
      icon: "👂",
      color: "green",
    },
    {
      number: 3,
      sense: "Berøre",
      prompt: "Navngi 3 ting du kan berøre (og berør dem hvis mulig)",
      icon: "✋",
      color: "orange",
    },
    {
      number: 2,
      sense: "Lukte",
      prompt: "Navngi 2 ting du kan lukte",
      icon: "👃",
      color: "purple",
    },
    {
      number: 1,
      sense: "Smake",
      prompt: "Navngi 1 ting du kan smake",
      icon: "👅",
      color: "red",
    },
  ];

  const currentStepData = steps[currentStep];
  const isComplete = currentStep >= steps.length;

  // Get responses for current step
  const currentStepResponses = responses.slice(
    steps.slice(0, currentStep).reduce((sum, step) => sum + step.number, 0),
    steps.slice(0, currentStep + 1).reduce((sum, step) => sum + step.number, 0)
  );

  const remainingForStep = currentStepData?.number - currentStepResponses.length;

  const handleAddResponse = () => {
    if (currentInput.trim()) {
      setResponses([...responses, currentInput.trim()]);
      setCurrentInput("");

      // Auto-advance to next step when step is complete
      if (remainingForStep === 1) {
        setTimeout(() => {
          setCurrentStep((prev) => prev + 1);
        }, 300);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleAddResponse();
    }
  };

  const resetExercise = () => {
    setCurrentStep(0);
    setResponses([]);
    setCurrentInput("");
  };

  const getColorClass = (color: string) => {
    const colors: Record<string, string> = {
      blue: "bg-blue-100 text-blue-700 border-blue-300",
      green: "bg-green-100 text-green-700 border-green-300",
      orange: "bg-orange-100 text-orange-700 border-orange-300",
      purple: "bg-purple-100 text-purple-700 border-purple-300",
      red: "bg-red-100 text-red-700 border-red-300",
    };
    return colors[color] || colors.blue;
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-purple-50 to-blue-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8">
        {/* Back button */}
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-[var(--color-primary)] hover:underline mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          Tilbake
        </Link>

        {/* Header */}
        <div className="max-w-2xl mx-auto text-center mb-8">
          <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-2">
            5-4-3-2-1 Jording
          </h1>
          <p className="text-lg text-[var(--color-text-secondary)]">
            En sensbasert teknikk for å bringe deg tilbake til nåtiden
          </p>
        </div>

        {/* Main content */}
        <div className="max-w-2xl mx-auto">
          {!isComplete ? (
            <>
              {/* Progress */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-[var(--color-text-secondary)]">
                    Steg {currentStep + 1} av {steps.length}
                  </span>
                  <span className="text-sm text-[var(--color-text-secondary)]">
                    {responses.length} av{" "}
                    {steps.reduce((sum, step) => sum + step.number, 0)} totalt
                  </span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-[var(--color-primary)] transition-all duration-300"
                    style={{
                      width: `${
                        (responses.length /
                          steps.reduce((sum, step) => sum + step.number, 0)) *
                        100
                      }%`,
                    }}
                  />
                </div>
              </div>

              {/* Current step card */}
              <div
                className={cn(
                  "border-2 rounded-lg p-6 mb-6",
                  getColorClass(currentStepData.color)
                )}
              >
                <div className="text-center mb-4">
                  <div className="text-6xl mb-2">{currentStepData.icon}</div>
                  <h2 className="text-2xl font-bold mb-2">
                    {currentStepData.sense}
                  </h2>
                  <p className="text-lg">{currentStepData.prompt}</p>
                </div>

                {/* Input */}
                <div className="mt-6">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={currentInput}
                      onChange={(e) => setCurrentInput(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder={`Skriv noe du kan ${currentStepData.sense.toLowerCase()}...`}
                      className="flex-1 px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:border-transparent"
                      autoFocus
                    />
                    <Button
                      variant="primary"
                      size="medium"
                      onClick={handleAddResponse}
                      disabled={!currentInput.trim()}
                    >
                      Legg til
                    </Button>
                  </div>

                  <p className="text-sm text-center mt-3">
                    {remainingForStep} til igjen i dette steget
                  </p>
                </div>

                {/* Current step responses */}
                {currentStepResponses.length > 0 && (
                  <div className="mt-6">
                    <div className="space-y-2">
                      {currentStepResponses.map((response, idx) => (
                        <div
                          key={idx}
                          className="flex items-center gap-2 bg-white/50 p-3 rounded-lg"
                        >
                          <Check className="h-5 w-5 text-green-600" />
                          <span>{response}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            // Completion screen
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mb-4">
                Flott jobbet!
              </h2>
              <p className="text-lg text-[var(--color-text-secondary)] mb-6">
                Du har fullført 5-4-3-2-1 jording-øvelsen.
                <br />
                Hvordan kjennes det nå?
              </p>

              <div className="space-y-3 mb-6">
                <Button
                  variant="primary"
                  size="large"
                  onClick={resetExercise}
                  className="w-full"
                >
                  Gjør øvelsen på nytt
                </Button>
                <Link href="/">
                  <Button variant="secondary" size="large" className="w-full">
                    Tilbake
                  </Button>
                </Link>
              </div>

              {/* Summary */}
              <div className="text-left bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold mb-3">Dine svar:</h3>
                {steps.map((step, stepIdx) => {
                  const stepResponses = responses.slice(
                    steps.slice(0, stepIdx).reduce((sum, s) => sum + s.number, 0),
                    steps
                      .slice(0, stepIdx + 1)
                      .reduce((sum, s) => sum + s.number, 0)
                  );

                  return (
                    <div key={stepIdx} className="mb-3">
                      <div className="font-medium text-sm text-gray-600 mb-1">
                        {step.icon} {step.sense}:
                      </div>
                      <ul className="list-disc list-inside text-sm space-y-1">
                        {stepResponses.map((response, idx) => (
                          <li key={idx}>{response}</li>
                        ))}
                      </ul>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="bg-white rounded-lg shadow-sm p-6 mt-6">
            <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-3">
              Om øvelsen:
            </h3>
            <p className="text-[var(--color-text-primary)] mb-4">
              5-4-3-2-1 er en grunningsteknikk som hjelper deg å fokusere på
              nåtiden gjennom sansene. Den er spesielt nyttig ved angst,
              tankespiraler eller når du føler deg koblet fra.
            </p>

            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800 mb-3">
                <strong>💡 Hvorfor virker det?</strong> Ved å bevisst fokusere på
                sanseopplevelser, bringer du oppmerksomheten bort fra bekymringer
                og tilbake til kroppen og omgivelsene. Dette aktiverer det
                parasympatiske nervesystemet.
              </p>
              <a
                href="https://www.youtube.com/results?search_query=5+4+3+2+1+grounding+technique"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-blue-700 underline hover:text-blue-900 font-medium"
              >
                📺 Se veiledning på YouTube →
              </a>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

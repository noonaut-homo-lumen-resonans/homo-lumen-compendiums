"use client";

import React, { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import { ArrowLeft, Play, Pause, RotateCcw } from "lucide-react";
import Link from "next/link";

/**
 * 4-6-8 Breathing Exercise Page
 *
 * Interactive guided breathing exercise
 * - 4 seconds inhale
 * - 6 seconds hold
 * - 8 seconds exhale
 *
 * Based on parasympathetic activation principles
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function Pust468Page() {
  const [isActive, setIsActive] = useState(false);
  const [currentPhase, setCurrentPhase] = useState<"inhale" | "hold" | "exhale">("inhale");
  const [countdown, setCountdown] = useState(4);
  const [completedCycles, setCompletedCycles] = useState(0);

  // Phase durations
  const phaseDurations = {
    inhale: 4,
    hold: 6,
    exhale: 8,
  };

  // Reset exercise
  const resetExercise = () => {
    setIsActive(false);
    setCurrentPhase("inhale");
    setCountdown(4);
    setCompletedCycles(0);
  };

  // Toggle play/pause
  const toggleExercise = () => {
    setIsActive(!isActive);
  };

  // Exercise timer logic
  useEffect(() => {
    if (!isActive) return;

    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev > 1) {
          return prev - 1;
        } else {
          // Move to next phase
          if (currentPhase === "inhale") {
            setCurrentPhase("hold");
            return phaseDurations.hold;
          } else if (currentPhase === "hold") {
            setCurrentPhase("exhale");
            return phaseDurations.exhale;
          } else {
            // Complete cycle, restart
            setCompletedCycles((c) => c + 1);
            setCurrentPhase("inhale");
            return phaseDurations.inhale;
          }
        }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isActive, currentPhase]);

  // Get phase display text
  const getPhaseText = () => {
    switch (currentPhase) {
      case "inhale":
        return "Pust inn gjennom nesen";
      case "hold":
        return "Hold pusten";
      case "exhale":
        return "Pust ut gjennom munnen";
    }
  };

  // Get phase color
  const getPhaseColor = () => {
    switch (currentPhase) {
      case "inhale":
        return "#4CAF50"; // Green
      case "hold":
        return "#FF9800"; // Orange
      case "exhale":
        return "#2196F3"; // Blue
    }
  };

  // Calculate circle scale for breathing animation
  const getCircleScale = () => {
    const progress = 1 - countdown / phaseDurations[currentPhase];

    if (currentPhase === "inhale") {
      return 1 + progress * 0.5; // Grow
    } else if (currentPhase === "exhale") {
      return 1.5 - progress * 0.5; // Shrink
    }
    return 1.5; // Hold at max
  };

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-green-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8">
        {/* Back button */}
        <Link
          href="/mestring"
          className="inline-flex items-center gap-2 text-[var(--color-primary)] hover:underline mb-6"
        >
          <ArrowLeft className="h-4 w-4" />
          Tilbake til Mestring
        </Link>

        {/* Header */}
        <div className="max-w-2xl mx-auto text-center mb-8">
          <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-2">
            4-6-8 Pustemetode
          </h1>
          <p className="text-lg text-[var(--color-text-secondary)]">
            En enkel teknikk for å roe ned nervesystemet
          </p>
        </div>

        {/* Main exercise area */}
        <div className="max-w-2xl mx-auto">
          {/* Breathing circle */}
          <div className="relative mb-8 flex items-center justify-center h-96">
            <div
              className="absolute rounded-full transition-all duration-1000 ease-in-out"
              style={{
                width: "300px",
                height: "300px",
                backgroundColor: `${getPhaseColor()}20`,
                border: `4px solid ${getPhaseColor()}`,
                transform: `scale(${getCircleScale()})`,
              }}
            />

            {/* Phase text */}
            <div className="z-10 text-center">
              <div
                className="text-6xl font-bold mb-2"
                style={{ color: getPhaseColor() }}
              >
                {countdown}
              </div>
              <div className="text-xl font-medium text-[var(--color-text-primary)]">
                {getPhaseText()}
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center justify-center gap-4 mb-6">
            <Button
              variant="primary"
              size="large"
              onClick={toggleExercise}
              leftIcon={isActive ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
            >
              {isActive ? "Pause" : "Start"}
            </Button>
            <Button
              variant="secondary"
              size="large"
              onClick={resetExercise}
              leftIcon={<RotateCcw className="h-6 w-6" />}
            >
              Nullstill
            </Button>
          </div>

          {/* Progress */}
          <div className="text-center mb-8">
            <p className="text-lg text-[var(--color-text-secondary)]">
              Fullførte runder: <strong>{completedCycles}</strong>
            </p>
            <p className="text-sm text-[var(--color-text-tertiary)] mt-2">
              Anbefalt: 3-5 runder
            </p>
          </div>

          {/* Instructions */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-3">
              Slik gjør du:
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-[var(--color-text-primary)]">
              <li>
                <strong>Pust inn (4 sek):</strong> Pust rolig inn gjennom nesen
              </li>
              <li>
                <strong>Hold (6 sek):</strong> Hold pusten på en komfortabel måte
              </li>
              <li>
                <strong>Pust ut (8 sek):</strong> Pust langsomt ut gjennom munnen
              </li>
              <li>
                <strong>Gjenta:</strong> Fortsett i 3-5 runder
              </li>
            </ol>

            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800 mb-3">
                <strong>💡 Hvorfor virker det?</strong> Lang utpust aktiverer
                parasympatiske nervesystemet, som signaliserer til kroppen at du
                er trygg. Dette reduserer stresshormoner og fremmer ro.
              </p>
              <a
                href="https://www.youtube.com/results?search_query=4-7-8+breathing+technique+guided"
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

"use client";

import React, { useState, useEffect } from "react";
import Button from "@/components/ui/Button";
import { ArrowLeft, ArrowRight, MessageCircle, Pause, Clock } from "lucide-react";
import { StressState } from "@/types";
import { uiPolicy, mapStressToState } from "@/lib/stressPolicy";

export interface LiraAnswer {
  questionId: string;
  answer: string;
}

interface LiraQuestion {
  id: string;
  text: string;
  type: "text" | "choice" | "scale";
  options?: string[];
  required?: boolean;
}

interface Stage3LiraChatProps {
  stressState: StressState;
  liraAnswers: LiraAnswer[];
  onAnswersChange: (answers: LiraAnswer[]) => void;
  onBack: () => void;
  onNext: () => void;
  polyvagalState: string;
  stressLevel?: number; // 1-10 stress level for policy calculation
}

/**
 * Stage 3: Lira Adaptive Chat
 *
 * Third step: 2-5 adaptive questions based on polyvagal state.
 * - Dorsal (8-10): 2 essential questions (safety + support)
 * - Sympathetic (4-7): 3-4 focused questions
 * - Ventral (1-3): 5 deeper questions for insight building
 *
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function Stage3LiraChat({
  stressState,
  liraAnswers,
  onAnswersChange,
  onBack,
  onNext,
  polyvagalState,
  stressLevel = 5,
}: Stage3LiraChatProps) {
  const [currentAnswers, setCurrentAnswers] = useState<Record<string, string>>({});
  const [isPaused, setIsPaused] = useState(false);

  // Get UI policy for current state
  const policy = uiPolicy(stressState);

  // Load existing answers
  useEffect(() => {
    const answersMap: Record<string, string> = {};
    liraAnswers.forEach((a) => {
      answersMap[a.questionId] = a.answer;
    });
    setCurrentAnswers(answersMap);
  }, [liraAnswers]);

  const getQuestions = (): LiraQuestion[] => {
    // Define all possible questions
    const allQuestions: LiraQuestion[] = [
      // Dorsal (safety-focused)
      {
        id: "safety",
        text: "Er du trygg akkurat nå?",
        type: "choice",
        options: ["Ja, jeg er trygg", "Nei, jeg føler meg utrygg", "Usikker"],
        required: true,
      },
      {
        id: "support",
        text: "Trenger du å snakke med noen nå?",
        type: "choice",
        options: ["Ja, jeg vil snakke med noen", "Nei, jeg klarer meg", "Kanskje senere"],
        required: true,
      },
      // Sympathetic (action-focused)
      {
        id: "trigger",
        text: "Hva skjedde som aktiverte deg i dag?",
        type: "text",
      },
      {
        id: "sleep",
        text: "Hvor mange timer sov du i natt?",
        type: "choice",
        options: ["Under 4 timer", "4-6 timer", "6-8 timer", "Over 8 timer"],
      },
      {
        id: "help-need",
        text: "Hva vil hjelpe deg mest akkurat nå?",
        type: "choice",
        options: [
          "Puste-øvelse",
          "Snakke med noen",
          "Ta en pause",
          "Gjøre noe fysisk",
          "Annet"
        ],
      },
      // Ventral (insight-focused)
      {
        id: "day-summary",
        text: "Hvordan vil du beskrive dagen din så langt?",
        type: "text",
      },
      {
        id: "energy-source",
        text: "Hva ga deg energi eller glede i dag?",
        type: "text",
      },
      {
        id: "sleep-quality",
        text: "Hvordan vil du beskrive søvnkvaliteten din?",
        type: "choice",
        options: ["Veldig god", "God", "Middels", "Dårlig", "Veldig dårlig"],
      },
      {
        id: "goal",
        text: "Hva er ditt mål akkurat nå?",
        type: "choice",
        options: [
          "Holde roen",
          "Bygge energi",
          "Fokusere bedre",
          "Slappe av",
          "Annet"
        ],
      },
      {
        id: "curiosity",
        text: "Er det noe du lurer på om deg selv eller dine følelser?",
        type: "text",
      },
    ];

    // Filter by policy.allowedTypes and limit to policy.maxQuestionsStage3
    const filtered = allQuestions
      .filter((q) => policy.allowedTypes.includes(q.type))
      .slice(0, policy.maxQuestionsStage3);

    // If dorsal, prioritize safety/support questions
    if (stressState === "dorsal") {
      return filtered.filter((q) => ["safety", "support"].includes(q.id)).slice(0, 2);
    }

    // If sympathetic, prioritize action-oriented questions
    if (stressState === "sympathetic") {
      return filtered
        .filter((q) => ["trigger", "sleep", "help-need", "safety"].includes(q.id))
        .slice(0, 4);
    }

    // Ventral: return all filtered questions
    return filtered;
  };

  const questions = getQuestions();

  const handleAnswerChange = (questionId: string, answer: string) => {
    const newAnswers = { ...currentAnswers, [questionId]: answer };
    setCurrentAnswers(newAnswers);

    // Convert to LiraAnswer array
    const answerArray: LiraAnswer[] = Object.entries(newAnswers).map(([id, ans]) => ({
      questionId: id,
      answer: ans,
    }));
    onAnswersChange(answerArray);
  };

  const canProceed = questions
    .filter((q) => q.required)
    .every((q) => currentAnswers[q.id]?.trim());

  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-green-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <div className="flex items-center justify-between">
          <p className="text-sm text-gray-600">Steg 3 av 4: Chat med Lira</p>
          <div className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-700">
            Tilstand: {polyvagalState === "ventral" ? "Rolig" : polyvagalState === "sympathetic" ? "Aktivert" : "Overveldet"}
          </div>
        </div>
      </div>

      {/* Intro text */}
      <div className="mb-8 text-left">
        <div className="flex items-center gap-3 mb-3">
          <MessageCircle className="h-8 w-8 text-purple-500" />
          <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
            Noen spørsmål fra Lira
          </h1>
        </div>
        <p className="text-lg text-[var(--color-text-secondary)]">
          Lira har {questions.length} {questions.length === 1 ? "spørsmål" : "spørsmål"} til deg
          basert på din tilstand. Svarene dine hjelper oss å gi bedre anbefalinger.
        </p>
      </div>

      {/* Questions */}
      <div className="space-y-6">
        {questions.map((question, index) => (
          <div key={question.id} className="bg-white rounded-lg shadow-sm p-6">
            <label className="block mb-3">
              <span className="text-sm font-semibold text-gray-700">
                {index + 1}. {question.text}
                {question.required && <span className="text-red-500 ml-1">*</span>}
              </span>
            </label>

            {question.type === "text" && (
              <textarea
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={3}
                placeholder="Skriv ditt svar her..."
                value={currentAnswers[question.id] || ""}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              />
            )}

            {question.type === "choice" && question.options && (
              <div className="space-y-2">
                {question.options.map((option) => (
                  <button
                    key={option}
                    onClick={() => handleAnswerChange(question.id, option)}
                    className={`w-full px-4 py-3 text-left border-2 rounded-lg transition-all ${
                      currentAnswers[question.id] === option
                        ? "border-purple-500 bg-purple-50 font-medium"
                        : "border-gray-200 hover:border-purple-300"
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {question.type === "scale" && (
              <input
                type="range"
                min="1"
                max="10"
                value={currentAnswers[question.id] || "5"}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            )}
          </div>
        ))}
      </div>

      {/* Privacy note */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>🔒 Privatliv:</strong> Dine svar lagres kun lokalt på din enhet.
          De deles ikke med NAV eller andre.
        </p>
      </div>

      {/* Navigation */}
      <div className="flex justify-between items-center mt-8">
        <Button
          variant="secondary"
          size="large"
          onClick={onBack}
          leftIcon={<ArrowLeft className="h-5 w-5" />}
        >
          Tilbake
        </Button>
        <Button
          variant="primary"
          size="large"
          onClick={onNext}
          disabled={!canProceed}
          rightIcon={<ArrowRight className="h-5 w-5" />}
        >
          Neste: Dine anbefalinger
        </Button>
      </div>
    </div>
  );
}

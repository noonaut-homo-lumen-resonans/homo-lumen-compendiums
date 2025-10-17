"use client";

import React, { useState, useEffect } from "react";
import Button from "@/components/ui/Button";
import CrisisBanner from "@/components/safety/CrisisBanner";
import { ArrowLeft, ArrowRight, MessageCircle } from "lucide-react";
import { LiraQuestion, LiraAnswer, StressState } from "@/types";

interface Stage3ChatProps {
  stressLevel: number;
  onAnswersChange: (answers: LiraAnswer[]) => void;
  onBack: () => void;
  onNext: () => void;
}

/**
 * Stage 3: Lira Contextual Chat
 *
 * AI-powered adaptive questioning (2-5 questions based on stress state).
 * Questions adapt to user's polyvagal state and previous answers.
 *
 * Triadisk Score: 0.18 (PROCEED)
 */
export default function Stage3Chat({
  stressLevel,
  onAnswersChange,
  onBack,
  onNext,
}: Stage3ChatProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<LiraAnswer[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState<string>("");

  // Determine stress state
  const getStressState = (): StressState => {
    if (stressLevel <= 3) return "ventral";
    if (stressLevel <= 7) return "sympathetic";
    return "dorsal";
  };

  const stressState = getStressState();

  // Generate adaptive questions based on stress state
  const getQuestions = (): LiraQuestion[] => {
    if (stressState === "dorsal") {
      // High stress: only 2 essential questions
      return [
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
      ];
    }

    if (stressState === "sympathetic") {
      // Medium stress: 3-4 focused questions
      return [
        {
          id: "trigger",
          text: "Hva skjedde som aktiverte deg i dag?",
          type: "text",
          required: false,
        },
        {
          id: "sleep",
          text: "Hvor mange timer sov du i natt?",
          type: "scale",
          options: ["Under 4", "4-6", "6-8", "Over 8"],
          required: false,
        },
        {
          id: "help-need",
          text: "Hva vil hjelpe deg mest akkurat nå?",
          type: "choice",
          options: [
            "Ro meg ned",
            "Få energi",
            "Bli mer fokusert",
            "Forstå følelsene mine",
          ],
          required: true,
        },
      ];
    }

    // Ventral: 5 deeper questions for insight building
    return [
      {
        id: "day-summary",
        text: "Hvordan vil du beskrive dagen din så langt?",
        type: "text",
        required: false,
      },
      {
        id: "energy-source",
        text: "Hva ga deg energi eller glede i dag?",
        type: "text",
        required: false,
      },
      {
        id: "sleep-quality",
        text: "Hvordan vil du beskrive søvnkvaliteten din?",
        type: "choice",
        options: ["Dårlig", "Middels", "God", "Veldig god"],
        required: false,
      },
      {
        id: "goal",
        text: "Hva er ditt mål akkurat nå?",
        type: "choice",
        options: [
          "Bygge resiliens",
          "Lære noe nytt",
          "Vedlikeholde balanse",
          "Utforske følelser",
        ],
        required: false,
      },
      {
        id: "curiosity",
        text: "Er det noe du lurer på om deg selv eller dine følelser?",
        type: "text",
        required: false,
      },
    ];
  };

  const questions = getQuestions();
  const currentQuestion = questions[currentQuestionIndex];
  const isLastQuestion = currentQuestionIndex === questions.length - 1;

  const handleAnswer = () => {
    if (!currentAnswer && currentQuestion.required) return;

    const newAnswer: LiraAnswer = {
      questionId: currentQuestion.id,
      answer: currentAnswer,
    };

    const updatedAnswers = [...answers, newAnswer];
    setAnswers(updatedAnswers);
    onAnswersChange(updatedAnswers);

    if (isLastQuestion) {
      // Done with questions
      return;
    }

    // Move to next question
    setCurrentQuestionIndex(currentQuestionIndex + 1);
    setCurrentAnswer("");
  };

  const handleSkip = () => {
    if (currentQuestion.required) return;

    if (isLastQuestion) {
      onNext();
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setCurrentAnswer("");
    }
  };

  const canProceed = isLastQuestion && (currentAnswer || !currentQuestion.required);

  return (
    <div className="w-full fade-in">
      {/* Progress indicator - Path nearing harbor */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full fill-path"></div>
          <div className="w-1/4 h-2 bg-gray-200 rounded-full"></div>
        </div>
        <p className="text-sm text-gray-600 text-left">Steg 3 av 4: Chat med Lira</p>
      </div>

      {/* Crisis Banner - Persistent if stress 9-10 */}
      {stressLevel >= 9 && (
        <div className="mb-6">
          <CrisisBanner visible={true} variant="compact" />
        </div>
      )}

      {/* AI Disclaimer */}
      <div className="mb-4">
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded">
          <p className="text-sm text-yellow-800">
            <strong>AI-generert innhold:</strong> Lira bruker kunstig intelligens.
            Svarene kan inneholde feil. Verifiser alltid viktig informasjon med NAV
            eller andre offisielle kilder.
          </p>
        </div>
      </div>

      {/* Intro - NVC: Empatisk tilstedeværelse */}
      <div className="mb-8 text-left">
        <div className="bg-purple-50 border-l-4 border-purple-400 p-4 mb-4 rounded">
          <p className="text-sm text-purple-800">
            💜 Takk for at du deler med meg. Dine svar hjelper meg å forstå hva du trenger akkurat nå.
          </p>
        </div>
        <div className="flex items-center gap-3 mb-3">
          <div className="wave-motion">
            <MessageCircle className="h-8 w-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
            La oss snakke litt
          </h1>
        </div>
        <p className="text-lg text-[var(--color-text-secondary)] mb-3">
          Jeg stiller noen få spørsmål for å forstå deg bedre.
          {stressState === "dorsal" && " Vi holder det enkelt."}
        </p>
        <p className="text-sm text-gray-600 italic">
          💡 Tips: Svar så ærlig du kan. Det finnes ingen «riktige» svar - bare din opplevelse.
        </p>
      </div>

      {/* Chat Interface */}
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        {/* Question counter */}
        <div className="mb-6 text-sm text-gray-500 text-left">
          Spørsmål {currentQuestionIndex + 1} av {questions.length}
        </div>

        {/* Lira's question */}
        <div className="mb-8">
          <div className="bg-blue-50 rounded-lg p-6 mb-6">
            <p className="text-lg font-medium text-gray-900 text-left">
              {currentQuestion.text}
            </p>
          </div>

          {/* Answer input */}
          {currentQuestion.type === "text" ? (
            <textarea
              value={currentAnswer}
              onChange={(e) => setCurrentAnswer(e.target.value)}
              placeholder="Skriv ditt svar her..."
              className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none min-h-[120px] text-base text-left"
            />
          ) : currentQuestion.type === "choice" || currentQuestion.type === "scale" ? (
            <div className="space-y-3">
              {currentQuestion.options?.map((option) => (
                <button
                  key={option}
                  onClick={() => setCurrentAnswer(option)}
                  className={`w-full p-4 text-left border-2 rounded-lg transition-all calm-hover ${
                    currentAnswer === option
                      ? "border-blue-500 bg-blue-50 font-medium"
                      : "border-gray-300 hover:border-gray-400"
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
          ) : null}
        </div>

        {/* Action buttons */}
        <div className="flex gap-3">
          {!currentQuestion.required && (
            <Button variant="text" size="medium" onClick={handleSkip}>
              Hopp over
            </Button>
          )}
          <Button
            variant="primary"
            size="medium"
            onClick={isLastQuestion ? onNext : handleAnswer}
            disabled={currentQuestion.required && !currentAnswer}
            className="flex-1"
          >
            {isLastQuestion ? "Fullfør" : "Neste spørsmål"}
          </Button>
        </div>
      </div>

      {/* Navigation - Triadisk Port 1: Bruker-suverenitet */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Button
            variant="secondary"
            size="large"
            onClick={onBack}
            leftIcon={<ArrowLeft className="h-5 w-5" />}
          >
            Tilbake
          </Button>
          {/* Hopp over hele chatten */}
          <Button
            variant="text"
            size="medium"
            onClick={onNext}
            className="text-gray-500 hover:text-gray-700"
          >
            Hopp over chatten →
          </Button>
        </div>
        {canProceed && (
          <Button
            variant="primary"
            size="large"
            onClick={onNext}
            rightIcon={<ArrowRight className="h-5 w-5" />}
          >
            Se anbefalinger
          </Button>
        )}
      </div>
    </div>
  );
}

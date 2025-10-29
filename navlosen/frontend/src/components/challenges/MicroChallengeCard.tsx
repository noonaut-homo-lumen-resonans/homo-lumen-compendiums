"use client";

import React, { useState, useEffect } from "react";
import {
  Target,
  Clock,
  CheckCircle2,
  X,
  Settings,
  TrendingUp,
  Heart,
  Brain,
  Users,
  Footprints,
  Sparkles,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import {
  MicroChallenge,
  MicroChallengeCategory,
  generateMicroChallenge,
  loadPreferences,
  savePreferences,
  saveCompletion,
  clearCurrentChallenge,
  getChallengeStats,
  type ChallengePreferences,
} from "@/utils/semanticTriggers";
import { getKairosWindowFromBigFive, type KairosWindow } from "@/utils/kairosMapping";
import { affectBus } from "@/utils/affectBus";
import { loadBigFive } from "@/utils/bigfive/mergeProfiles";
import {
  calculateCompositeStressScore,
  type CompositeStressInput,
  type LiraAnswer,
} from "@/lib/compositeStressScore";
import { SomaticSignal } from "@/types";

/**
 * MicroChallengeCard Component
 *
 * Displays adaptive micro-challenges based on user's Kairos Window and polyvagal state.
 *
 * Features:
 * - Shows current challenge (if user has opted in)
 * - Settings panel to configure preferences
 * - Completion tracking with optional feedback
 * - Stats display (if user wants to see them)
 *
 * Triadisk: 0.16 (PROCEED) - User controls everything, transparent reasoning
 */

interface MicroChallengeCardProps {
  compact?: boolean; // If true, show minimal version (for sidebar)
}

export default function MicroChallengeCard({ compact = false }: MicroChallengeCardProps) {
  const [preferences, setPreferences] = useState<ChallengePreferences>(loadPreferences());
  const [currentChallenge, setCurrentChallenge] = useState<MicroChallenge | null>(null);
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [showStats, setShowStats] = useState<boolean>(false);
  const [polyvagalState, setPolyvagalState] = useState<"ventral" | "sympathetic" | "dorsal">("ventral");
  const [kairosWindow, setKairosWindow] = useState<KairosWindow | null>(null);

  // Load current state and generate challenge
  useEffect(() => {
    if (!preferences.enabled) {
      setCurrentChallenge(null);
      return;
    }

    // Load polyvagal state
    if (typeof window !== "undefined") {
      try {
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
          setPolyvagalState(result.polyvagalState);
        }
      } catch (e) {
        console.error("Failed to load polyvagal state", e);
      }
    }

    // Load Kairos Window
    const bigFive = loadBigFive();
    if (bigFive) {
      const latestAffect = affectBus.getLatest();
      const window = getKairosWindowFromBigFive(bigFive, {
        valence: latestAffect?.valence ?? 0,
        arousal: latestAffect?.arousal ?? 0.5,
        hrvRmssd: latestAffect?.hrvRmssd ?? 50,
      });
      setKairosWindow(window);
    }

    // Generate challenge
    const challenge = generateMicroChallenge(polyvagalState, kairosWindow);
    setCurrentChallenge(challenge);
  }, [preferences.enabled]);

  // Handle preference changes
  const handleToggleEnabled = () => {
    const newPrefs = { ...preferences, enabled: !preferences.enabled };
    setPreferences(newPrefs);
    savePreferences(newPrefs);
  };

  const handleToggleStats = () => {
    const newPrefs = { ...preferences, showStats: !preferences.showStats };
    setPreferences(newPrefs);
    savePreferences(newPrefs);
  };

  const handleCategoryToggle = (category: MicroChallengeCategory) => {
    const newCategories = preferences.preferredCategories.includes(category)
      ? preferences.preferredCategories.filter(c => c !== category)
      : [...preferences.preferredCategories, category];

    const newPrefs = { ...preferences, preferredCategories: newCategories };
    setPreferences(newPrefs);
    savePreferences(newPrefs);
  };

  // Handle completion
  const handleComplete = (feltHelpful: boolean | null) => {
    if (!currentChallenge) return;

    saveCompletion({
      challengeId: currentChallenge.id,
      completedAt: Date.now(),
      feltHelpful,
    });

    clearCurrentChallenge();

    // Generate new challenge
    const newChallenge = generateMicroChallenge(polyvagalState, kairosWindow);
    setCurrentChallenge(newChallenge);
  };

  const handleSkip = () => {
    clearCurrentChallenge();

    // Generate new challenge
    const newChallenge = generateMicroChallenge(polyvagalState, kairosWindow);
    setCurrentChallenge(newChallenge);
  };

  // Get category icon
  const getCategoryIcon = (category: MicroChallengeCategory) => {
    switch (category) {
      case 'somatic':
        return <Heart className="h-4 w-4" />;
      case 'cognitive':
        return <Brain className="h-4 w-4" />;
      case 'social':
        return <Users className="h-4 w-4" />;
      case 'behavioral':
        return <Footprints className="h-4 w-4" />;
      case 'creative':
        return <Sparkles className="h-4 w-4" />;
    }
  };

  const getCategoryColor = (category: MicroChallengeCategory) => {
    switch (category) {
      case 'somatic':
        return 'text-red-600 bg-red-50';
      case 'cognitive':
        return 'text-blue-600 bg-blue-50';
      case 'social':
        return 'text-green-600 bg-green-50';
      case 'behavioral':
        return 'text-purple-600 bg-purple-50';
      case 'creative':
        return 'text-orange-600 bg-orange-50';
    }
  };

  const stats = getChallengeStats();

  // If challenges disabled, show opt-in prompt
  if (!preferences.enabled) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 border-l-4 border-purple-400">
        <div className="flex items-start gap-4">
          <Target className="h-6 w-6 text-purple-600 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              Daglige mikro-utfordringer
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Få små, tilpassede utfordringer basert på din tilstand. Disse er designet for å bygge
              mestring gradvis, aldri overvelde.
            </p>
            <button
              onClick={handleToggleEnabled}
              className="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-medium transition-colors"
            >
              Aktiver utfordringer
            </button>
          </div>
        </div>
      </div>
    );
  }

  // If no challenge available
  if (!currentChallenge) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 border-l-4 border-gray-300">
        <div className="flex items-start gap-4">
          <Target className="h-6 w-6 text-gray-400 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-lg font-bold text-gray-900 mb-2">
              Ingen utfordring tilgjengelig
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Vi kunne ikke finne en passende utfordring akkurat nå. Prøv å justere innstillingene dine.
            </p>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="text-purple-600 hover:text-purple-700 font-medium text-sm flex items-center gap-2"
            >
              <Settings className="h-4 w-4" />
              Innstillinger
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Main challenge display
  return (
    <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <Target className="h-6 w-6 text-purple-600" />
          <h3 className="text-lg font-bold text-gray-900">Din utfordring i dag</h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="text-gray-400 hover:text-gray-600"
            title="Innstillinger"
          >
            <Settings className="h-5 w-5" />
          </button>
          {preferences.showStats && (
            <button
              onClick={() => setShowStats(!showStats)}
              className="text-gray-400 hover:text-gray-600"
              title="Statistikk"
            >
              <TrendingUp className="h-5 w-5" />
            </button>
          )}
        </div>
      </div>

      {/* Challenge Card */}
      <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-lg p-4 mb-4">
        {/* Category badge */}
        <div className="flex items-center gap-2 mb-3">
          <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(currentChallenge.category)}`}>
            {getCategoryIcon(currentChallenge.category)}
            {currentChallenge.category}
          </span>
          <span className="text-xs text-gray-500 flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {currentChallenge.estimatedMinutes} min
          </span>
          <span className="text-xs text-gray-500 capitalize">
            ({currentChallenge.difficulty})
          </span>
        </div>

        {/* Title and description */}
        <h4 className="text-lg font-bold text-gray-900 mb-2">
          {currentChallenge.title}
        </h4>
        <p className="text-sm text-gray-700 mb-3">
          {currentChallenge.description}
        </p>

        {/* Reasoning */}
        <details className="text-xs text-gray-600 mb-3">
          <summary className="cursor-pointer hover:text-gray-800 font-medium">
            Hvorfor denne utfordringen?
          </summary>
          <p className="mt-2 pl-4 border-l-2 border-purple-300">
            {currentChallenge.reasoning}
          </p>
        </details>

        {/* Action buttons */}
        <div className="flex gap-2">
          <button
            onClick={() => handleComplete(true)}
            className="flex-1 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
          >
            <CheckCircle2 className="h-4 w-4" />
            Fullført!
          </button>
          <button
            onClick={handleSkip}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium transition-colors"
            title="Hopp over og få ny utfordring"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Optional: "Was it helpful?" after completion */}
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="bg-gray-50 rounded-lg p-4 mb-4 space-y-4">
          <h4 className="font-semibold text-gray-900">Innstillinger</h4>

          {/* Enable/disable toggle */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">Aktiver utfordringer</span>
            <button
              onClick={handleToggleEnabled}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences.enabled ? 'bg-purple-500' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences.enabled ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* Show stats toggle */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-700">Vis statistikk</span>
            <button
              onClick={handleToggleStats}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                preferences.showStats ? 'bg-purple-500' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  preferences.showStats ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* Category preferences */}
          <div>
            <p className="text-sm text-gray-700 mb-2">Kategorier du vil ha:</p>
            <div className="flex flex-wrap gap-2">
              {(['somatic', 'cognitive', 'social', 'behavioral', 'creative'] as MicroChallengeCategory[]).map(cat => (
                <button
                  key={cat}
                  onClick={() => handleCategoryToggle(cat)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    preferences.preferredCategories.includes(cat)
                      ? `${getCategoryColor(cat)} border-2 border-current`
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Stats Panel */}
      {showStats && preferences.showStats && (
        <div className="bg-blue-50 rounded-lg p-4 space-y-2">
          <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Din statistikk
          </h4>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-gray-600">Siste 7 dager</p>
              <p className="text-2xl font-bold text-purple-600">{stats.completedLast7Days}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">Siste 30 dager</p>
              <p className="text-2xl font-bold text-purple-600">{stats.completedLast30Days}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">Totalt</p>
              <p className="text-2xl font-bold text-purple-600">{stats.totalCompleted}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">Nyttige</p>
              <p className="text-2xl font-bold text-green-600">{stats.helpfulPercentage}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

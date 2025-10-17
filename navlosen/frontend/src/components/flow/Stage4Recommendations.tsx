"use client";

import React, { useMemo } from "react";
import Button from "@/components/ui/Button";
import {
  ArrowLeft,
  Play,
  Book,
  Youtube,
  Music,
  Sun,
  Activity,
  RefreshCw
} from "lucide-react";
import { Recommendation, SessionData, StressState } from "@/types";
import Link from "next/link";

interface Stage4RecommendationsProps {
  sessionData: SessionData;
  onBack: () => void;
  onRestart: () => void;
}

/**
 * Stage 4: Personalized Recommendations
 *
 * Final step: Shows personalized recommendations based on:
 * - Emotions (quadrant data)
 * - Stress level & somatic signals
 * - Lira chat answers
 * - HealthConnect data (mock for now)
 * - Weather data (mock for now)
 *
 * Categories: Øvelser, Praksiser, Kunnskap (YouTube), Musikk, Kontekst
 *
 * Triadisk Score: 0.22 (PROCEED)
 */
export default function Stage4Recommendations({
  sessionData,
  onBack,
  onRestart,
}: Stage4RecommendationsProps) {
  const getStressState = (): StressState => {
    if (sessionData.stressLevel <= 3) return "ventral";
    if (sessionData.stressLevel <= 7) return "sympathetic";
    return "dorsal";
  };

  const stressState = getStressState();

  // Generate personalized recommendations
  const recommendations = useMemo((): Recommendation[] => {
    const recs: Recommendation[] = [];

    // EXERCISES - Always prioritized
    if (stressState === "dorsal") {
      recs.push({
        id: "grounding-54321",
        type: "exercise",
        title: "Jording: 5-4-3-2-1 teknikken",
        description: "Bring deg tilbake til nåtiden med sansebasert grounding.",
        duration: "2-5 min",
        link: "/ovelser/grounding-54321",
        priority: 10,
      });
      recs.push({
        id: "breathing-468",
        type: "exercise",
        title: "Pust: 4-6-8 metoden",
        description: "Aktiver parasympatiske nervesystemet med kontrollert pust.",
        duration: "1-3 min",
        link: "/ovelser/pust-468",
        priority: 9,
      });
    } else if (stressState === "sympathetic") {
      recs.push({
        id: "breathing-468",
        type: "exercise",
        title: "Pust: 4-6-8 metoden",
        description: "Rolig ned aktivering med lang utpust.",
        duration: "1-3 min",
        link: "/ovelser/pust-468",
        priority: 10,
      });
      recs.push({
        id: "small-action",
        type: "practice",
        title: "Handling: Ett lite steg",
        description: "Bygg mestringsfølelse ved å fullføre én liten oppgave.",
        duration: "3-5 min",
        priority: 8,
      });
    } else {
      // Ventral
      recs.push({
        id: "progressive-relaxation",
        type: "exercise",
        title: "Progressiv muskelavslapning",
        description: "Bygg kroppsbevissthet og forebygg spenning.",
        duration: "5-10 min",
        priority: 8,
      });
      recs.push({
        id: "breathing-468",
        type: "exercise",
        title: "Pust: 4-6-8 metoden",
        description: "Vedlikehold ro og balanse.",
        duration: "1-3 min",
        link: "/ovelser/pust-468",
        priority: 7,
      });
    }

    // MUSIC FREQUENCIES
    if (stressState === "dorsal" || stressState === "sympathetic") {
      recs.push({
        id: "music-432hz",
        type: "music",
        title: "432 Hz - Naturlig resonans",
        description: "Beroligende frekvens som harmoniserer med naturens vibrasjon.",
        duration: "10 min",
        priority: 7,
      });
      recs.push({
        id: "music-528hz",
        type: "music",
        title: "528 Hz - Transformasjon",
        description: "Kjent som 'kjærlighetens frekvens', fremmer healing og transformasjon.",
        duration: "10 min",
        priority: 6,
      });
    }

    // KNOWLEDGE (YouTube)
    recs.push({
      id: "polyvagal-intro",
      type: "knowledge",
      title: "Forstå Polyvagal Teori",
      description: "Lær hvordan nervesystemet ditt reagerer på stress.",
      duration: "12 min",
      link: "https://www.youtube.com/watch?v=example",
      priority: 5,
    });

    // CONTEXT - Weather/Activity
    if (sessionData.weather?.condition === "sunny") {
      recs.push({
        id: "outdoor-walk",
        type: "context",
        title: "Gå en tur i solen",
        description: `Det er ${sessionData.weather.temperature}°C og sol ute. 10 minutter i dagslys kan hjelpe.`,
        duration: "10 min",
        priority: 6,
      });
    }

    // Sort by priority
    return recs.sort((a, b) => b.priority - a.priority);
  }, [sessionData, stressState]);

  const getIcon = (type: Recommendation["type"]) => {
    switch (type) {
      case "exercise":
        return <Play className="h-5 w-5" />;
      case "practice":
        return <Book className="h-5 w-5" />;
      case "knowledge":
        return <Youtube className="h-5 w-5" />;
      case "music":
        return <Music className="h-5 w-5" />;
      case "context":
        return <Sun className="h-5 w-5" />;
    }
  };

  const getCategoryColor = (type: Recommendation["type"]) => {
    switch (type) {
      case "exercise":
        return "bg-green-100 text-green-700 border-green-300";
      case "practice":
        return "bg-blue-100 text-blue-700 border-blue-300";
      case "knowledge":
        return "bg-purple-100 text-purple-700 border-purple-300";
      case "music":
        return "bg-pink-100 text-pink-700 border-pink-300";
      case "context":
        return "bg-orange-100 text-orange-700 border-orange-300";
    }
  };

  const getCategoryLabel = (type: Recommendation["type"]) => {
    switch (type) {
      case "exercise":
        return "Øvelse";
      case "practice":
        return "Praksis";
      case "knowledge":
        return "Kunnskap";
      case "music":
        return "Musikk";
      case "context":
        return "Kontekst";
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
        <p className="text-sm text-gray-600">Steg 4 av 4: Dine anbefalinger</p>
      </div>

      {/* Header */}
      <div className="mb-8 text-left">
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Anbefalinger for deg akkurat nå
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)]">
          Basert på dine svar har vi laget en personlig plan. Start hvor som helst!
        </p>
      </div>

      {/* Summary card */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-8 border-2 border-blue-200">
        <div className="flex items-start gap-4">
          <Activity className="h-8 w-8 text-blue-600 flex-shrink-0" />
          <div>
            <h3 className="font-bold text-lg mb-2">Din tilstand akkurat nå</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Følelser valgt</p>
                <p className="font-semibold">{sessionData.emotions.length}</p>
              </div>
              <div>
                <p className="text-gray-600">Stressnivå</p>
                <p className="font-semibold">{sessionData.stressLevel}/10</p>
              </div>
              <div>
                <p className="text-gray-600">Tilstand</p>
                <p className="font-semibold">
                  {stressState === "ventral" ? "Balansert" :
                   stressState === "sympathetic" ? "Aktivert" : "Overveldet"}
                </p>
              </div>
              <div>
                <p className="text-gray-600">Kroppsignaler</p>
                <p className="font-semibold">
                  {sessionData.somaticSignals.filter(s => s.checked).length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-8">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6 hover:border-blue-300 transition-all"
          >
            {/* Category badge */}
            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold mb-4 border-2 ${getCategoryColor(rec.type)}`}>
              {getIcon(rec.type)}
              {getCategoryLabel(rec.type)}
            </div>

            {/* Content */}
            <h3 className="text-lg font-bold text-gray-900 mb-2">{rec.title}</h3>
            <p className="text-sm text-gray-600 mb-4">{rec.description}</p>

            {rec.duration && (
              <p className="text-xs text-gray-500 mb-4">⏱️ {rec.duration}</p>
            )}

            {/* Action */}
            {rec.link ? (
              rec.link.startsWith("http") ? (
                <a href={rec.link} target="_blank" rel="noopener noreferrer">
                  <Button variant="primary" size="medium" className="w-full">
                    {rec.type === "knowledge" ? "Se video" : "Start"}
                  </Button>
                </a>
              ) : (
                <Link href={rec.link}>
                  <Button variant="primary" size="medium" className="w-full">
                    Start øvelse
                  </Button>
                </Link>
              )
            ) : (
              <Button variant="secondary" size="medium" className="w-full" disabled>
                Kommer snart
              </Button>
            )}
          </div>
        ))}
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

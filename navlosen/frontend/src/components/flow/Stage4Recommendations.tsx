"use client";

import React, { useMemo, useState, useEffect } from "react";
import Button from "@/components/ui/Button";
import {
  ArrowLeft,
  Play,
  Book,
  Youtube,
  Music,
  Sun,
  Activity,
  RefreshCw,
  BookOpen,
  FileText
} from "lucide-react";
import { Recommendation, SessionData, StressState } from "@/types";
import Link from "next/link";
import JourneySuccess from "@/components/mestring/JourneySuccess";
import MasteryLog from "@/components/mestring/MasteryLog";

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
  const [showSuccess, setShowSuccess] = useState(false);
  const [showMasteryLog, setShowMasteryLog] = useState(false);
  const [journalEntry, setJournalEntry] = useState<string>("");

  // Load journal entry from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedJournal = localStorage.getItem("navlosen-journal-entry");
      if (savedJournal) {
        setJournalEntry(savedJournal);
      }
    }
  }, []);

  // Save journal entry to localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-journal-entry", journalEntry);
    }
  }, [journalEntry]);

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

    // MUSIC FREQUENCIES - State-specific recommendations
    if (stressState === "dorsal") {
      // Dorsal: grounding, safety, release from fear
      recs.push({
        id: "music-174hz",
        type: "music",
        title: "174 Hz - Grunnleggende sikkerhet",
        description: "Reduserer smerte, gir følelse av trygghet og grunnlag. Virker som naturlig bedøvelse.",
        duration: "5-10 min",
        link: "/musikk#174hz",
        priority: 8,
      });
      recs.push({
        id: "music-396hz",
        type: "music",
        title: "396 Hz - Frigjøring fra frykt",
        description: "Frigjør skyld og frykt. Transformerer sorg til glede.",
        duration: "5-10 min",
        link: "/musikk#396hz",
        priority: 7,
      });
    } else if (stressState === "sympathetic") {
      // Sympathetic: calming, transformation, balance
      recs.push({
        id: "music-432hz",
        type: "music",
        title: "432 Hz - Naturens stemmefrekvens",
        description: "Harmoniserer med universets vibrasjon. Fremmer balanse, ro og mental klarhet.",
        duration: "5-10 min",
        link: "/musikk#432hz",
        priority: 7,
      });
      recs.push({
        id: "music-528hz",
        type: "music",
        title: "528 Hz - Transformasjon og mirakler",
        description: "Kjent som 'kjærlighetens frekvens'. Reparerer DNA, transformerer og mirakuløs healing.",
        duration: "5-10 min",
        link: "/musikk#528hz",
        priority: 6,
      });
    } else {
      // Ventral: expansion, connection, spiritual growth
      recs.push({
        id: "music-639hz",
        type: "music",
        title: "639 Hz - Tilkobling og relasjoner",
        description: "Fremmer harmoni i relasjoner, forståelse, toleranse og kjærlighet.",
        duration: "5-10 min",
        link: "/musikk#639hz",
        priority: 6,
      });
      recs.push({
        id: "music-852hz",
        type: "music",
        title: "852 Hz - Tilbake til åndelig orden",
        description: "Vekker intuisjon og spirituell visdom. Gjenoppretter åndelig balanse.",
        duration: "5-10 min",
        link: "/musikk#852hz",
        priority: 5,
      });
    }

    // Always show link to full music page
    recs.push({
      id: "music-page",
      type: "music",
      title: "Se alle 9 frekvenser",
      description: "Utforsk hele Solfeggio-skalaen (174-963 Hz) for ulike behov.",
      duration: "5-10 min",
      link: "/musikk",
      priority: 4,
    });

    // KNOWLEDGE (YouTube)
    recs.push({
      id: "polyvagal-intro",
      type: "knowledge",
      title: "Forstå Polyvagal Teori",
      description: "Lær hvordan nervesystemet ditt reagerer på stress.",
      duration: "12 min",
      link: "https://youtu.be/0zrlKLgnov4",
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

  // Show Mastery Log
  if (showMasteryLog) {
    return <MasteryLog onClose={() => setShowMasteryLog(false)} />;
  }

  // Show success celebration when user views recommendations
  if (showSuccess) {
    return (
      <JourneySuccess
        title="Godt jobbet!"
        message="Du navigerte gjennom følelsene dine, lyttet til kroppen, og kom trygt til anbefalinger. Dette er din styrke i praksis."
        onContinue={() => setShowSuccess(false)}
        showAnimation={true}
      />
    );
  }

  return (
    <div className="w-full max-w-6xl mx-auto">
      {/* Progress indicator - Lighthouse beam style */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-green-400 to-teal-500 rounded-full"></div>
          <div className="w-1/4 h-2 bg-gradient-to-r from-yellow-300 to-amber-400 rounded-full pulse-glow"></div>
        </div>
        <p className="text-sm text-gray-600">Steg 4 av 4: Dine anbefalinger</p>
      </div>

      {/* Header - NVC: Behov vs Forslag */}
      <div className="mb-8 text-left">
        <div className="bg-amber-50 border-l-4 border-amber-400 p-4 mb-4 rounded">
          <p className="text-sm text-amber-800">
            🌟 Dette er forslag, ikke krav. Du bestemmer selv hva som passer for deg akkurat nå.
          </p>
        </div>
        <h1 className="text-3xl font-bold text-[var(--color-text-primary)] mb-3">
          Forslag til deg akkurat nå
        </h1>
        <p className="text-lg text-[var(--color-text-secondary)] mb-3">
          Basert på det du delte, kan disse aktivitetene møte behovet ditt for ro, forståelse og mestring.
        </p>
        <p className="text-sm text-gray-600 italic">
          💡 Trenger du noe annet? Det er helt greit. Du kjenner deg selv best.
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
            className="bg-white rounded-lg shadow-sm border-2 border-gray-200 p-6 hover:border-blue-300 transition-all calm-hover fade-in"
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

      {/* Journal & Reflection - Lira's guidance (HOM-53) */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6 mb-8 border-2 border-purple-300">
        <div className="flex items-start gap-4 mb-4">
          <FileText className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Refleksjon (valgfritt)
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Hva tenker eller føler du etter å ha gått gjennom denne økten?
              Skriv fritt – dette er bare for deg.
            </p>
            <textarea
              value={journalEntry}
              onChange={(e) => setJournalEntry(e.target.value)}
              placeholder="F.eks: 'Jeg la merke til at jeg ofte kjenner angst i brystet...', 'Det hjalp å sette ord på følelsene...'"
              rows={4}
              className="w-full px-4 py-3 border-2 border-purple-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            />
            {journalEntry.trim().length > 0 && (
              <p className="text-xs text-purple-600 mt-2 italic">
                💜 Refleksjonen din er lagret lokalt og forblir privat.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Mastery Log - Port 3: Graduation */}
      <div className="bg-gradient-to-r from-green-50 to-teal-50 rounded-lg p-6 mb-8 border-2 border-green-300">
        <div className="flex items-start gap-4">
          <BookOpen className="h-6 w-6 text-green-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Bygger du mestring?
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Hvis du fant en strategi som fungerte i dag (pusteøvelse,
              gåtur, musikk), kan du lagre den i din personlige mestringslogg.
              Over tid bygger du din egen verktøykasse for selvregulering.
            </p>
            <Button
              variant="primary"
              size="medium"
              onClick={() => setShowMasteryLog(true)}
              leftIcon={<BookOpen className="h-5 w-5" />}
            >
              Åpne mestringslogg
            </Button>
            <p className="text-xs text-gray-500 mt-3 italic">
              💡 Mål: Over tid trenger du NAV-Losen mindre, fordi du vet hva
              som fungerer for deg. Det er målet vårt.
            </p>
          </div>
        </div>
      </div>

      {/* Celebration button - Show success visualization */}
      <div className="bg-gradient-to-r from-yellow-50 to-amber-50 rounded-lg p-6 mb-8 border-2 border-yellow-300">
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-900 mb-3">
            Du har fullført hele reisen! 🎉
          </p>
          <p className="text-sm text-gray-600 mb-4">
            Se hvordan du navigerte fra storm til trygg havn.
          </p>
          <Button
            variant="primary"
            size="large"
            onClick={() => setShowSuccess(true)}
          >
            Se din reise
          </Button>
        </div>
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

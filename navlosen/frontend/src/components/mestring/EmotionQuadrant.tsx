"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface EmotionQuadrantProps {
  selectedEmotions: { word: string; quadrant: number | null }[];
  onChange: (emotions: { word: string; quadrant: number | null }[]) => void;
  className?: string;
}

/**
 * EmotionQuadrant Component
 *
 * Interactive 4-quadrant emotion mapper with 100 emotion words
 * Based on Circumplex Model (Russell, 1980) and emotional granularity research
 *
 * Quadrants:
 * 1 (Top Right): Positive Valence + High Energy (Green)
 * 2 (Top Left): Positive Valence + Low Energy (Blue)
 * 3 (Bottom Left): Negative Valence + Low Energy (Gray)
 * 4 (Bottom Right): Negative Valence + High Energy (Orange)
 *
 * Triadisk Score: 0.14 (PROCEED)
 */
export default function EmotionQuadrant({
  selectedEmotions,
  onChange,
  className,
}: EmotionQuadrantProps) {
  // 100 Norwegian emotion words organized by quadrant
  const quadrantWords = {
    1: [
      // Positive + High Energy (25 words)
      "Gledelig", "Entusiastisk", "Inspirert", "Optimistisk", "Spent",
      "Energisk", "Leken", "Stolt", "Ekstatisk", "Begeistret",
      "Ivrig", "Opprømt", "Fornøyd", "Lykkelig", "Begeistring",
      "Levende", "Vital", "Motivert", "Selvsikker", "Modig",
      "Fascinert", "Engasjert", "Aktiv", "Kreativ", "Triumferende",
    ],
    2: [
      // Positive + Low Energy (25 words)
      "Rolig", "Takknemlig", "Trygg", "Tilfreds", "Fokusert",
      "Fredelig", "Håpefull", "Avslappet", "Behagelig", "Tålmodig",
      "Harmonisk", "Balansert", "Ydmyk", "Omsorgsfull", "Kjærlig",
      "Aksepterende", "Fornuftig", "Reflektert", "Konsentrert", "Stabil",
      "Mild", "Tillitsfull", "Verdsatt", "Anerkjent", "Medfølende",
    ],
    3: [
      // Negative + Low Energy (25 words)
      "Trist", "Nedfor", "Utmattet", "Sårbar", "Ensom",
      "Fortvilet", "Nummen", "Håpløs", "Deprimert", "Skuffet",
      "Mislykket", "Resignert", "Tomhet", "Sorgfull", "Tapende",
      "Ute av kontroll", "Hjelpeløs", "Tungsinn", "Uverdig", "Skamfull",
      "Skyldig", "Trett", "Passiv", "Apatisk", "Likegyldig",
    ],
    4: [
      // Negative + High Energy (25 words)
      "Frustrert", "Sint", "Irritert", "Engstelig", "Nervøs",
      "Urolig", "Overveldet", "Stresset", "Redd", "Panisk",
      "Anspent", "Presset", "Skremt", "Provosert", "Rasende",
      "Aggressiv", "Defensiv", "Bitter", "Fiendtlig", "Mistenksom",
      "Bekymret", "Urolig", "Forvirret", "Kaotisk", "Ustabil",
    ],
  };

  const getQuadrantColor = (quadrant: number): string => {
    switch (quadrant) {
      case 1: return "bg-green-50 border-green-300";
      case 2: return "bg-blue-50 border-blue-300";
      case 3: return "bg-gray-100 border-gray-300";
      case 4: return "bg-orange-50 border-orange-300";
      default: return "bg-white border-gray-300";
    }
  };

  const getQuadrantLabel = (quadrant: number): { title: string; desc: string } => {
    switch (quadrant) {
      case 1:
        return {
          title: "Positiv + Energisk",
          desc: "Bra følelse, høy aktivering"
        };
      case 2:
        return {
          title: "Positiv + Rolig",
          desc: "Bra følelse, lav aktivering"
        };
      case 3:
        return {
          title: "Negativ + Utmattet",
          desc: "Vanskelig følelse, lav energi"
        };
      case 4:
        return {
          title: "Negativ + Aktivert",
          desc: "Vanskelig følelse, høy aktivering"
        };
      default:
        return { title: "", desc: "" };
    }
  };

  const isWordSelected = (word: string): boolean => {
    return selectedEmotions.some((e) => e.word === word);
  };

  const toggleWord = (word: string, quadrant: number) => {
    if (isWordSelected(word)) {
      // Remove the word
      const updated = selectedEmotions.filter((e) => e.word !== word);
      onChange(updated);
    } else {
      // Add the word
      const updated = [...selectedEmotions, { word, quadrant }];
      onChange(updated);
    }
  };

  const renderQuadrant = (quadrant: number) => {
    const words = quadrantWords[quadrant as keyof typeof quadrantWords];
    const label = getQuadrantLabel(quadrant);

    return (
      <div
        className={cn(
          "min-h-[300px] p-4 rounded-lg border-2 transition-all",
          getQuadrantColor(quadrant)
        )}
      >
        <div className="text-center mb-4">
          <h4 className="font-bold text-sm text-gray-900">
            {label.title}
          </h4>
          <p className="text-xs text-gray-600">{label.desc}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {words.map((word) => {
            const selected = isWordSelected(word);
            return (
              <button
                key={word}
                onClick={() => toggleWord(word, quadrant)}
                className={cn(
                  "px-3 py-1.5 rounded-full text-xs font-medium transition-all",
                  selected
                    ? "bg-white shadow-md ring-2 ring-offset-1 ring-gray-900 font-semibold scale-105"
                    : "bg-white/50 hover:bg-white/80 hover:shadow-sm"
                )}
              >
                {word}
              </button>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className={cn("w-full", className)}>
      <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2 text-left">
        Hvordan kjennes det akkurat nå?
      </h3>

      <p className="text-sm text-[var(--color-text-secondary)] mb-6 text-left">
        Klikk på følelsesordene som passer for deg. Jo mer presist du kan
        navngi følelsene dine, desto lettere blir det å regulere dem.
      </p>

      {/* 4-Quadrant Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {renderQuadrant(1)}
        {renderQuadrant(2)}
        {renderQuadrant(3)}
        {renderQuadrant(4)}
      </div>

      {/* Educational Info */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="text-sm font-semibold text-blue-900 mb-2">
          💡 Hvordan bruke følelseskartet
        </h4>
        <ol className="text-xs text-blue-800 space-y-2 list-decimal list-inside">
          <li>
            <strong>Klikk på ordene</strong> som beskriver hvordan du føler deg nå
          </li>
          <li>
            <strong>Tenk over to dimensjoner:</strong> Føles det bra eller vanskelig?
            Har du mye eller lite energi?
          </li>
          <li>
            <strong>Bruk gjerne flere ord:</strong> Jo mer presist du beskriver følelsen,
            desto bedre kan du regulere den
          </li>
          <li>
            <strong>Klikk igjen for å fjerne</strong> ord du ikke lenger kjenner på
          </li>
        </ol>
        <p className="text-xs text-blue-700 mt-3 italic">
          Forskning viser at høy emosjonell granularitet (mange presise ord) gir
          bedre mental helse og reguleringsevne.
        </p>
      </div>
    </div>
  );
}

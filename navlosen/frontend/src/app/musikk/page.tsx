"use client";

import React from "react";
import Layout from "@/components/layout/Layout";
import FrequencyPlayer from "@/components/music/FrequencyPlayer";
import { MusicFrequency } from "@/types";
import { Music, ArrowLeft } from "lucide-react";
import Link from "next/link";
import Button from "@/components/ui/Button";

/**
 * Musikk Page - Healing Frequencies
 *
 * Collection of therapeutic sound frequencies based on:
 * - Solfeggio Frequencies (ancient healing tones)
 * - 432 Hz Natural Tuning (harmonic with nature)
 *
 * Each frequency has specific healing properties backed by sound therapy research.
 *
 * Triadisk Score: 0.15 (PROCEED)
 */
export default function MusikkPage() {
  // Healing frequencies with their benefits
  const frequencies: MusicFrequency[] = [
    {
      id: "174hz",
      frequency: 174,
      name: "174 Hz - Grunnleggende sikkerhet",
      benefit: "Reduserer smerte, gir følelse av trygghet og grunnlag. Virker som naturlig bedøvelse.",
    },
    {
      id: "396hz",
      frequency: 396,
      name: "396 Hz - Frigjøring fra frykt",
      benefit: "Frigjør skyld og frykt, hjelper deg å nå dine mål. Transformerer sorg til glede.",
    },
    {
      id: "417hz",
      frequency: 417,
      name: "417 Hz - Fasilitering av forandring",
      benefit: "Fjerner negativitet og blokkering, letter endring. Rydder traumatiske erfaringer.",
    },
    {
      id: "432hz",
      frequency: 432,
      name: "432 Hz - Naturens stemmefrekvens",
      benefit: "Harmoniserer med universets vibrasjon. Fremmer balanse, ro og mental klarhet.",
    },
    {
      id: "528hz",
      frequency: 528,
      name: "528 Hz - Transformasjon og mirakler",
      benefit: "Kjent som 'kjærlighetens frekvens'. Reparerer DNA, transformerer og mirakuløs healing.",
    },
    {
      id: "639hz",
      frequency: 639,
      name: "639 Hz - Tilkobling og relasjoner",
      benefit: "Fremmer harmoni i relasjoner, forståelse, toleranse og kjærlighet. Balanserer følelser.",
    },
    {
      id: "741hz",
      frequency: 741,
      name: "741 Hz - Oppvåkning av intuisjon",
      benefit: "Renser celler fra toksiner, oppvekker intuisjon og utvidelse av bevissthet.",
    },
    {
      id: "852hz",
      frequency: 852,
      name: "852 Hz - Tilbake til åndelig orden",
      benefit: "Vekker intuisjon og spirituell visdom. Gjenoppretter åndelig balanse.",
    },
    {
      id: "963hz",
      frequency: 963,
      name: "963 Hz - Guddommelig bevissthet",
      benefit: "Aktiverer 'pinealkjertelen', forbinder deg med universel energi og høyere bevissthet.",
    },
  ];

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-purple-50 to-pink-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8">
        {/* Back button */}
        <div className="mb-6">
          <Link href="/">
            <Button
              variant="secondary"
              size="medium"
              leftIcon={<ArrowLeft className="h-4 w-4" />}
            >
              Tilbake
            </Button>
          </Link>
        </div>

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-3">
            <Music className="h-10 w-10 text-purple-600" />
            <h1 className="text-4xl font-bold text-[var(--color-text-primary)]">
              Helende Frekvenser
            </h1>
          </div>
          <p className="text-lg text-[var(--color-text-secondary)]">
            Opplev kraften i terapeutiske lydfrekvenser. Hver tone har unike helende egenskaper
            basert på Solfeggio-skalaen og naturlig tuning.
          </p>
        </div>

        {/* Info card */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8 mx-auto" style={{ maxWidth: "900px" }}>
          <h2 className="text-xl font-bold text-purple-900 mb-3">
            Hvordan bruke healing frekvenser
          </h2>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex items-start gap-2">
              <span className="text-purple-600 font-bold">1.</span>
              <span>
                <strong>Finn et rolig sted:</strong> Sett deg eller legg deg komfortabelt ned
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600 font-bold">2.</span>
              <span>
                <strong>Bruk hodetelefoner:</strong> For best lydkvalitet og immersjon
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600 font-bold">3.</span>
              <span>
                <strong>Velg frekvens:</strong> Basert på hva du trenger nå (frykt, smerte, transformasjon, etc.)
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600 font-bold">4.</span>
              <span>
                <strong>Lytt i 5-10 minutter:</strong> Pust rolig og la lyden virke
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-purple-600 font-bold">5.</span>
              <span>
                <strong>Merk effekten:</strong> Legg merke til hvordan kropp og sinn reagerer
              </span>
            </li>
          </ul>
        </div>

        {/* Frequency Players Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {frequencies.map((freq) => (
            <div key={freq.id} id={freq.id}>
              <FrequencyPlayer frequency={freq} />
            </div>
          ))}
        </div>

        {/* Science info */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6 mx-auto" style={{ maxWidth: "900px" }}>
          <h3 className="text-lg font-bold text-blue-900 mb-3">
            🔬 Vitenskapelig grunnlag
          </h3>
          <p className="text-sm text-blue-800 mb-3">
            Lydterapi og frekvensbehandling har vært brukt i tusenvis av år på tvers av
            kulturer. Moderne forskning viser at spesifikke frekvenser kan påvirke:
          </p>
          <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
            <li>Nervesystemets tilstand (polyvagal respons)</li>
            <li>Hjerterytme-variabilitet (HRV)</li>
            <li>Hjernebølger (alpha, theta, delta)</li>
            <li>Stresshormon-nivåer (kortisol)</li>
            <li>Cellulær vibrasjon og resonans</li>
          </ul>
          <p className="text-xs text-blue-700 mt-3 italic">
            Forskning: Dr. Royal Rife, Dr. Leonard Horowitz, Cymatics-studier av Hans Jenny
          </p>
        </div>
      </div>
    </Layout>
  );
}

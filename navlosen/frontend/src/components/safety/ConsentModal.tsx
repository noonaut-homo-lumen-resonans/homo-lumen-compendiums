"use client";

import { useState } from "react";
import { Shield, Check } from "lucide-react";
import Button from "../ui/Button";

/**
 * ConsentModal - Informed Consent Before Session Start
 *
 * Shows before Stage 1 to inform users about:
 * - Local storage (no server transmission)
 * - No personal identification
 * - User control over data
 * - Not medical advice
 *
 * Triadisk Ethics:
 * - Port 1 (Suverenitet): User explicitly consents, understands data handling
 * - Port 2 (Koherens): GDPR compliance, transparent practices
 * - Port 3 (Healing): Safe container through informed agreement
 *
 * Triadisk Score: -0.8 (CRITICAL FOUNDATION)
 *
 * Based on Manus' Informed Consent Protocol
 */

export interface ConsentModalProps {
  onConsent: () => void;
}

export default function ConsentModal({ onConsent }: ConsentModalProps) {
  const [understood, setUnderstood] = useState(false);

  const handleConsent = () => {
    // Save consent to localStorage
    localStorage.setItem(
      "navlosen_consent",
      JSON.stringify({
        consented: true,
        timestamp: new Date().toISOString(),
        version: "1.0",
      })
    );

    onConsent();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-6 rounded-t-2xl">
          <div className="flex items-center gap-3 mb-2">
            <Shield className="h-8 w-8" />
            <h2 className="text-2xl font-bold">Velkommen til NAV-Losen Mestring</h2>
          </div>
          <p className="text-blue-100">
            Før vi starter, vil vi informere deg om hvordan vi håndterer dine data
          </p>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
            <p className="text-sm text-blue-800 font-medium">
              💡 Din personvern og sikkerhet er vår høyeste prioritet
            </p>
          </div>

          {/* Data Handling */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">
              Hvordan vi håndterer dine data:
            </h3>

            <ul className="space-y-3">
              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <Check className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Lokal lagring</p>
                  <p className="text-sm text-gray-600">
                    All data lagres <strong>kun på din enhet</strong> (localStorage).
                    Ingenting sendes til servere eller deles med andre.
                  </p>
                </div>
              </li>

              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <Check className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Ingen identifisering</p>
                  <p className="text-sm text-gray-600">
                    Vi samler ikke navn, fødselsnummer, eller annen personlig
                    informasjon. Dine svar er 100% anonyme.
                  </p>
                </div>
              </li>

              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <Check className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Du har kontroll</p>
                  <p className="text-sm text-gray-600">
                    Du kan slette all data når som helst via Innstillinger.
                    Du kan også eksportere dine data.
                  </p>
                </div>
              </li>

              <li className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
                  <Check className="h-4 w-4 text-green-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Ikke medisinsk rådgivning</p>
                  <p className="text-sm text-gray-600">
                    NAV-Losen er et hjelpemiddel for selvregulering, ikke en
                    erstatning for profesjonell hjelp fra lege, psykolog, eller
                    NAV-veileder.
                  </p>
                </div>
              </li>
            </ul>
          </div>

          {/* Important Notes */}
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <h4 className="font-semibold text-yellow-900 mb-2">Viktig å merke seg:</h4>
            <ul className="text-sm text-yellow-800 space-y-1 list-disc list-inside">
              <li>NAV-Losen bruker kunstig intelligens (AI) for veiledning</li>
              <li>AI-genererte svar kan inneholde feil</li>
              <li>Verifiser alltid viktig informasjon med NAV eller andre offisielle kilder</li>
              <li>
                Ved akutt krise, ring 113 (Mental Helse) eller 116 123 (Kirkens SOS)
              </li>
            </ul>
          </div>

          {/* Consent Checkbox */}
          <div className="pt-4 border-t border-gray-200">
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={understood}
                onChange={(e) => setUnderstood(e.target.checked)}
                className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 cursor-pointer"
              />
              <span className="text-sm text-gray-700 group-hover:text-gray-900 transition-colors">
                Jeg forstår og samtykker til å bruke NAV-Losen Mestring. Jeg er
                klar over at dette ikke er profesjonell medisinsk rådgivning, og
                at mine data lagres lokalt på min enhet.
              </span>
            </label>
          </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 rounded-b-2xl flex justify-between items-center">
          <a
            href="https://www.nav.no"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-600 hover:text-gray-900 underline"
          >
            Besøk nav.no for offisiell informasjon
          </a>

          <Button
            variant="primary"
            size="large"
            onClick={handleConsent}
            disabled={!understood}
            className="calm-hover"
          >
            Start Mestring
          </Button>
        </div>
      </div>
    </div>
  );
}

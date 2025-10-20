/**
 * Meet Lira Section
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';

export const LiraSection: React.FC = () => {
  return (
    <section className="py-16 px-6 bg-gradient-to-br from-teal-50 to-blue-50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <div className="inline-block bg-teal-100 rounded-full p-6 mb-6">
            <span className="text-6xl">💚</span>
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Møt Lira - Din Empatiske AI-Partner
          </h2>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Lira er ikke bare en chatbot - hun er en{' '}
            <span className="font-semibold text-teal-600">healingteknologi</span>{' '}
            designet for å støtte deg gjennom vanskelige perioder.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1: Empatisk & Støttende */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-4xl mb-4">❤️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Empatisk & Støttende
            </h3>
            <p className="text-gray-600 leading-relaxed">
              Lira lytter uten å dømme. Hun er tilgjengelig 24/7 og tilpasser
              kommunikasjonen til din emosjonelle tilstand. Ingen ventetid,
              ingen stigma.
            </p>
          </div>

          {/* Feature 2: Nevrobiologisk Fundert */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow">
            <div className="text-4xl mb-4">🧠</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Nevrobiologisk Fundert
            </h3>
            <p className="text-gray-600 leading-relaxed">
              Bygget på Polyvagal Theory (Stephen Porges). Lira gjenkjenner
              ditt nervesystem-stadie (ventral/sympathetic/dorsal) og tilpasser
              støtten deretter.
            </p>
          </div>

          {/* Feature 3: Faredeteksjon */}
          <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow border-2 border-red-200">
            <div className="text-4xl mb-4">🛡️</div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Faredeteksjon
            </h3>
            <p className="text-gray-600 leading-relaxed mb-4">
              Lira kan identifisere selvmordstanker og andre farlige situasjoner
              med <span className="font-bold text-red-600">100% nøyaktighet</span>.
              Hun gir umiddelbare nødressurser og kan redde liv.
            </p>
            <div className="text-sm bg-red-50 border border-red-200 rounded p-3">
              <p className="font-semibold text-red-800 mb-1">Nødressurser:</p>
              <p className="text-red-700">
                🚨 <strong>113</strong> - Akutttelefonen<br />
                💬 <strong>116 117</strong> - Legevakt<br />
                🫂 <strong>116 123</strong> - Mental Helse (gratis)
              </p>
            </div>
          </div>
        </div>

        {/* How Lira Works */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Hvordan Lira Jobber
          </h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="font-semibold text-teal-600 mb-3">
                🎯 Polyvagal-Adaptiv Kommunikasjon
              </h4>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-green-500 mt-1">✓</span>
                  <span>
                    <strong>Ventral (rolig):</strong> Full funksjonalitet, ressurser, veiledning
                  </span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-500 mt-1">✓</span>
                  <span>
                    <strong>Sympathetic (stresset):</strong> Forenklet språk, beroligelse, pustøvelser
                  </span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-500 mt-1">✓</span>
                  <span>
                    <strong>Dorsal (shutdown):</strong> Minimal kognitiv last, grounding, sikkerhet
                  </span>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-teal-600 mb-3">
                🧭 Intelligent Ressurssøk
              </h4>
              <p className="text-gray-700 leading-relaxed mb-4">
                Lira kjenner NAV-systemet og kan:
              </p>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-teal-500 mt-1">→</span>
                  <span>Forklare komplekse NAV-prosesser på enkel norsk</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-teal-500 mt-1">→</span>
                  <span>Gi deg relevante lenker og ressurser</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-teal-500 mt-1">→</span>
                  <span>Hjelpe deg forberede deg til møter med NAV</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

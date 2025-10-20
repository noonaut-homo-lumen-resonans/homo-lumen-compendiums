/**
 * Call-to-Action Section
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';
import Link from 'next/link';

export const CTASection: React.FC = () => {
  return (
    <section className="py-20 px-6 bg-gradient-to-br from-blue-600 via-teal-600 to-blue-700 text-white">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl lg:text-5xl font-bold mb-6">
          Se Lira i Aksjon
        </h2>
        <p className="text-xl lg:text-2xl mb-10 text-blue-100">
          Test QDA v2.0 Demo og opplev hvordan de 6 nevrobiologiske lagene
          prosesserer samtaler i sanntid.
        </p>

        {/* Demo Preview Info */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 mb-10">
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-4xl mb-2">💬</div>
              <div className="font-semibold mb-1">Test Samtaler</div>
              <div className="text-sm text-blue-100">
                Prøv enkle, moderate, og kritiske scenarioer
              </div>
            </div>
            <div>
              <div className="text-4xl mb-2">🧠</div>
              <div className="font-semibold mb-1">Se Lagene Jobbe</div>
              <div className="text-sm text-blue-100">
                Visuell fremstilling av prosessering
              </div>
            </div>
            <div>
              <div className="text-4xl mb-2">📊</div>
              <div className="font-semibold mb-1">Transparens</div>
              <div className="text-sm text-blue-100">
                Full innsikt i kostnad, tid, og kompleksitet
              </div>
            </div>
          </div>
        </div>

        {/* Main CTA Button */}
        <Link
          href="/dashboard/qda-demo"
          className="inline-block bg-white text-blue-600 font-bold text-xl px-12 py-5 rounded-lg shadow-2xl hover:shadow-3xl hover:bg-blue-50 transition-all duration-300 transform hover:scale-105"
        >
          🚀 Test QDA v2.0 Demo Nå
        </Link>

        {/* Secondary Info */}
        <p className="mt-8 text-sm text-blue-100">
          Ingen pålogging kreves • Åpen kildekode • Gratis å bruke
        </p>

        {/* Quick Test Scenarios */}
        <div className="mt-12 pt-8 border-t border-white/20">
          <h3 className="text-xl font-semibold mb-6">
            Foreslåtte Testscenarioer
          </h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="bg-white/10 rounded-lg p-4">
              <div className="font-semibold mb-2">1️⃣ Enkel Samtale</div>
              <p className="text-blue-100">
                "Hei, hvordan har du det?"
              </p>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <div className="font-semibold mb-2">2️⃣ Jobbstress</div>
              <p className="text-blue-100">
                "Jeg føler meg veldig stresset på jobb"
              </p>
            </div>
            <div className="bg-white/10 rounded-lg p-4 border-2 border-red-300">
              <div className="font-semibold mb-2">3️⃣ Kritisk (Faredeteksjon)</div>
              <p className="text-blue-100">
                "Jeg orker ikke mer. Jeg har tenkt på selvmord."
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

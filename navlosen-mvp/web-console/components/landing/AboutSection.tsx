/**
 * About NAV-Losen Section
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';

export const AboutSection: React.FC = () => {
  return (
    <section className="py-16 px-6 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Om NAV-Losen
        </h2>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Left Column - Project Description */}
          <div>
            <h3 className="text-2xl font-semibold text-blue-600 mb-4">
              Pilotprosjekt i Tvedestrand
            </h3>
            <p className="text-gray-700 leading-relaxed mb-6">
              NAV-Losen er Norges første AI-drevne digital assistent spesifikt
              designet for å støtte NAV-brukere med mental helse-utfordringer.
              Prosjektet piloteres i Tvedestrand kommune i samarbeid med NAV og
              Homo Lumen Coalition.
            </p>
            <p className="text-gray-700 leading-relaxed mb-6">
              Vi kombinerer nevrobiologisk forskning (Polyvagal Theory) med
              etisk AI-design for å skape en trygg, empatisk, og effektiv
              støtteteknologi som respekterer brukerens autonomi og verdighet.
            </p>

            <div className="bg-blue-50 border-l-4 border-blue-600 p-6 rounded">
              <h4 className="font-semibold text-gray-900 mb-2">Målgruppe</h4>
              <p className="text-gray-700 text-sm">
                NAV-brukere som opplever stress, angst, eller andre mental
                helse-utfordringer i møte med offentlige tjenester. Systemet
                er designet for å være tilgjengelig 24/7 og tilpasser seg
                brukerens nervesystem-tilstand (ventral, sympathetic, dorsal).
              </p>
            </div>
          </div>

          {/* Right Column - Triadisk Ethics */}
          <div>
            <h3 className="text-2xl font-semibold text-teal-600 mb-4">
              Triadisk Ethics - Våre Tre Porter
            </h3>
            <p className="text-gray-700 leading-relaxed mb-6">
              Hver funksjon i NAV-Losen må passere gjennom tre etiske porter
              før den kan implementeres:
            </p>

            <div className="space-y-6">
              {/* Port 1 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-2xl">🔓</span>
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">
                    Port 1: Kognitiv Suverenitet
                  </h4>
                  <p className="text-gray-600 text-sm">
                    Hvor fritt beveger feltet? Fremmer vi brukerens autonomi
                    og valgfrihet? Ingen manipulasjon eller dark patterns.
                  </p>
                </div>
              </div>

              {/* Port 2 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-2xl">🧭</span>
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">
                    Port 2: Ontologisk Koherens
                  </h4>
                  <p className="text-gray-600 text-sm">
                    Hvor koherent er væren? Matcher systemet brukerens levde
                    erfaring? Respekterer vi kompleksitet og ambivalens?
                  </p>
                </div>
              </div>

              {/* Port 3 */}
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-2xl">🌱</span>
                </div>
                <div>
                  <h4 className="font-bold text-gray-900 mb-2">
                    Port 3: Regenerativ Healing
                  </h4>
                  <p className="text-gray-600 text-sm">
                    Hvilken retning beveger feltet? Bygger vi brukerens
                    kapasitet over tid? Design for "graduation" - brukeren
                    trenger systemet mindre over tid.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

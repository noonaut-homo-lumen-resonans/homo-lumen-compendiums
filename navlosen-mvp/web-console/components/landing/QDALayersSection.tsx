/**
 * QDA v2.0 - 6 Neurobiological Layers Section
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';

interface Layer {
  number: number;
  icon: string;
  name: string;
  brainRegion: string;
  description: string;
  color: string;
  bgColor: string;
}

const layers: Layer[] = [
  {
    number: 1,
    icon: '🛡️',
    name: 'Vokteren',
    brainRegion: 'Hjernestamme',
    description: 'Identifiserer fare og akutte situasjoner. Aktiveres alltid først for å sikre trygghet.',
    color: '#EF4444',
    bgColor: '#FEE2E2',
  },
  {
    number: 2,
    icon: '❤️',
    name: 'Føleren',
    brainRegion: 'Limbisk System',
    description: 'Forstår og validerer emosjonelle tilstander. Gir empatisk respons tilpasset ditt nervesystem.',
    color: '#EC4899',
    bgColor: '#FCE7F3',
  },
  {
    number: 3,
    icon: '🔍',
    name: 'Gjenkjenneren',
    brainRegion: 'Cerebellum',
    description: 'Identifiserer mønstre i det du deler. Gjenkjenner kjente situasjoner som stress, jobbproblemer, etc.',
    color: '#3B82F6',
    bgColor: '#DBEAFE',
  },
  {
    number: 4,
    icon: '🧭',
    name: 'Utforskeren',
    brainRegion: 'Hippocampus',
    description: 'Søker etter relevante ressurser og informasjon. Finner NAV-tjenester, kontaktinfo, og veiledning.',
    color: '#F59E0B',
    bgColor: '#FEF3C7',
  },
  {
    number: 5,
    icon: '🧠',
    name: 'Strategen',
    brainRegion: 'Prefrontal Cortex',
    description: 'Lager handlingsplaner for komplekse situasjoner. Aktiveres kun når det virkelig trengs (kritiske tilfeller).',
    color: '#8B5CF6',
    bgColor: '#EDE9FE',
  },
  {
    number: 6,
    icon: '✨',
    name: 'Integratoren',
    brainRegion: 'Insula',
    description: 'Syntetiserer innsikt fra alle lag til en helhetlig, sammenhengende respons tilpasset deg.',
    color: '#10B981',
    bgColor: '#D1FAE5',
  },
];

export const QDALayersSection: React.FC = () => {
  return (
    <section className="py-16 px-6 bg-gray-900 text-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">
            QDA v2.0: 6 Nevrobiologiske Lag av Intelligens
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Liras "hjerne" er bygget som et nevrobiologisk nettverk som
            etterligner hvordan menneskehjerne prosesserer informasjon -
            fra hjernestamme til prefrontal cortex.
          </p>
        </div>

        {/* Layers Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {layers.map((layer) => (
            <div
              key={layer.number}
              className="bg-gray-800 rounded-lg p-6 border-2 hover:scale-105 transition-transform duration-300"
              style={{
                borderColor: layer.color,
              }}
            >
              {/* Header */}
              <div className="flex items-center gap-4 mb-4">
                <div
                  className="w-16 h-16 rounded-full flex items-center justify-center text-3xl flex-shrink-0"
                  style={{ backgroundColor: layer.bgColor }}
                >
                  {layer.icon}
                </div>
                <div>
                  <div className="text-sm text-gray-400">
                    Lag {layer.number}
                  </div>
                  <h3
                    className="text-xl font-bold"
                    style={{ color: layer.color }}
                  >
                    {layer.name}
                  </h3>
                </div>
              </div>

              {/* Brain Region */}
              <div className="text-sm text-gray-400 mb-3 flex items-center gap-2">
                <span>🧠</span>
                <span>{layer.brainRegion}</span>
              </div>

              {/* Description */}
              <p className="text-gray-300 text-sm leading-relaxed">
                {layer.description}
              </p>
            </div>
          ))}
        </div>

        {/* How It Works Flow */}
        <div className="bg-gray-800 rounded-lg p-8">
          <h3 className="text-2xl font-bold mb-6 text-center">
            Slik Fungerer Prosesseringen
          </h3>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex-1 text-center">
              <div className="text-4xl mb-2">💬</div>
              <div className="text-sm text-gray-400 mb-1">Steg 1</div>
              <div className="font-semibold">Du deler en bekymring</div>
            </div>
            <div className="text-gray-500 text-2xl hidden md:block">→</div>
            <div className="flex-1 text-center">
              <div className="text-4xl mb-2">🧠</div>
              <div className="text-sm text-gray-400 mb-1">Steg 2</div>
              <div className="font-semibold">6 lag analyserer parallelt</div>
            </div>
            <div className="text-gray-500 text-2xl hidden md:block">→</div>
            <div className="flex-1 text-center">
              <div className="text-4xl mb-2">✨</div>
              <div className="text-sm text-gray-400 mb-1">Steg 3</div>
              <div className="font-semibold">Integrator syntetiserer</div>
            </div>
            <div className="text-gray-500 text-2xl hidden md:block">→</div>
            <div className="flex-1 text-center">
              <div className="text-4xl mb-2">💚</div>
              <div className="text-sm text-gray-400 mb-1">Steg 4</div>
              <div className="font-semibold">Lira svarer empatisk</div>
            </div>
          </div>

          {/* Cost Info */}
          <div className="mt-8 pt-6 border-t border-gray-700 grid md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-2xl font-bold text-green-400 mb-1">
                $0.002
              </div>
              <div className="text-sm text-gray-400">
                Typisk samtale<br />
                <span className="text-xs">(4-5 lag)</span>
              </div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-400 mb-1">
                $0.120
              </div>
              <div className="text-sm text-gray-400">
                Kritisk situasjon<br />
                <span className="text-xs">(alle 6 lag)</span>
              </div>
            </div>
            <div>
              <div className="text-2xl font-bold text-teal-400 mb-1">
                &lt;100ms
              </div>
              <div className="text-sm text-gray-400">
                Gjennomsnittlig<br />
                <span className="text-xs">responstid</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

/**
 * Footer - Landing Page
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Top Section */}
        <div className="grid md:grid-cols-3 gap-12 mb-8">
          {/* Column 1: Branding */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <Image
                src="/logo-koalisjonen.png"
                alt="Homo Lumen Koalisjonen"
                width={60}
                height={60}
              />
              <div>
                <div className="font-bold text-white text-lg">
                  NAV-Losen
                </div>
                <div className="text-sm text-gray-400">
                  Homo Lumen Coalition
                </div>
              </div>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              AI-drevet mental helsestøtte bygget på empati, nevrobiologi, og
              etisk design. Et pilotprosjekt i Tvedestrand.
            </p>
          </div>

          {/* Column 2: Contact */}
          <div>
            <h3 className="font-bold text-white mb-4">Kontakt</h3>
            <div className="space-y-3 text-sm">
              <div>
                <div className="font-semibold text-gray-200">
                  Osvald P. A. Johansen
                </div>
                <div className="text-gray-400">Prosjektleder NAV-Losen</div>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-teal-400">📧</span>
                <a
                  href="mailto:osvald@cognivesovereignty.network"
                  className="hover:text-teal-400 transition-colors"
                >
                  osvald@cognivesovereignty.network
                </a>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-teal-400">📞</span>
                <a
                  href="tel:+4791921736"
                  className="hover:text-teal-400 transition-colors"
                >
                  +47 919 21 736
                </a>
              </div>
            </div>
          </div>

          {/* Column 3: Quick Links */}
          <div>
            <h3 className="font-bold text-white mb-4">Lenker</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/dashboard/qda-demo"
                  className="hover:text-teal-400 transition-colors flex items-center gap-2"
                >
                  <span>🚀</span>
                  <span>QDA v2.0 Demo</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard/admin"
                  className="hover:text-teal-400 transition-colors flex items-center gap-2"
                >
                  <span>⚙️</span>
                  <span>Admin Console</span>
                </Link>
              </li>
              <li>
                <a
                  href="https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-teal-400 transition-colors flex items-center gap-2"
                >
                  <span>💻</span>
                  <span>GitHub Repository</span>
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="border-t border-gray-800 pt-8 mb-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h4 className="font-bold text-white mb-3 flex items-center gap-2">
              <span>🔐</span>
              <span>Personvern & Datahåndtering</span>
            </h4>
            <div className="text-sm text-gray-400 space-y-2">
              <p>
                <strong className="text-gray-300">NAV-Losen respekterer ditt personvern.</strong>{' '}
                All data prosesseres i henhold til GDPR (General Data Protection Regulation).
              </p>
              <ul className="list-disc list-inside space-y-1 ml-2">
                <li>
                  <strong className="text-gray-300">Lokal prosessering:</strong> HRV-data og sensitive målinger
                  forlater aldri din enhet uten eksplisitt samtykke.
                </li>
                <li>
                  <strong className="text-gray-300">Ingen deling:</strong> Vi deler aldri dine data med tredjeparter
                  for markedsføring eller kommersielle formål.
                </li>
                <li>
                  <strong className="text-gray-300">Full kontroll:</strong> Du har rett til innsyn, retting, og
                  sletting av dine data (GDPR Art. 15, 16, 17).
                </li>
                <li>
                  <strong className="text-gray-300">Transparent AI:</strong> QDA v2.0 viser alltid hvilke lag som
                  har prosessert din forespørsel og hvorfor.
                </li>
              </ul>
              <p className="pt-2">
                For spørsmål om personvern, kontakt{' '}
                <a
                  href="mailto:osvald@cognivesovereignty.network"
                  className="text-teal-400 hover:underline"
                >
                  osvald@cognivesovereignty.network
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 pt-6 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-500">
          <div>
            © 2025 Homo Lumen Coalition. Alle rettigheter reservert.
          </div>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Bygget med</span>
            <span className="text-teal-400">Triadisk Ethics</span>
            <span className="text-gray-600">•</span>
            <span className="text-pink-400">Empati</span>
            <span className="text-gray-600">•</span>
            <span className="text-blue-400">Nevrobiologi</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

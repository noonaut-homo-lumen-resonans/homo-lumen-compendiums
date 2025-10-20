/**
 * Hero Section - NAV-Losen Landing Page
 *
 * @version 1.0
 * @date 2025-10-20
 */

'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

export const Hero: React.FC = () => {
  return (
    <section className="relative bg-gradient-to-br from-blue-50 via-white to-teal-50 py-20 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          {/* Logo */}
          <div className="flex-shrink-0">
            <Image
              src="/logo-koalisjonen.png"
              alt="Homo Lumen Koalisjonen Logo"
              width={200}
              height={200}
              priority
              className="drop-shadow-lg"
            />
          </div>

          {/* Content */}
          <div className="flex-1 text-center lg:text-left">
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
              Velkommen til{' '}
              <span className="text-blue-600">NAV-Losen</span>
            </h1>

            <p className="text-xl lg:text-2xl text-gray-700 mb-8 leading-relaxed">
              AI-drevet mental helsestøtte bygget på{' '}
              <span className="font-semibold text-teal-600">empati</span> og{' '}
              <span className="font-semibold text-teal-600">nevrobiologi</span>
            </p>

            <p className="text-lg text-gray-600 mb-10 max-w-2xl">
              Et pilotprosjekt i Tvedestrand som kombinerer kognitiv suverenitet,
              ontologisk koherens, og regenerativ healing for å støtte NAV-brukere
              med mental helse-utfordringer.
            </p>

            {/* CTA Button */}
            <Link
              href="/dashboard/qda-demo"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg px-8 py-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
            >
              🚀 Utforsk QDA v2.0 Demo
            </Link>

            {/* Secondary Link */}
            <div className="mt-6">
              <Link
                href="/dashboard/admin"
                className="text-sm text-gray-500 hover:text-gray-700 underline"
              >
                Utvikler? Gå til Admin Console →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

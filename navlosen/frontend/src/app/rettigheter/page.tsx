"use client";

import Layout from "@/components/layout/Layout";
import { Scale, ArrowLeft } from "lucide-react";
import Link from "next/link";

/**
 * Rettigheter Page
 *
 * Placeholder page for rights and entitlements information
 */
export default function RettigheterPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-600">
          <Link href="/" className="hover:text-blue-600">NAV-Losen</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">Rettigheter</span>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-indigo-100 rounded-full mb-6">
            <Scale className="w-10 h-10 text-indigo-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Rettigheter
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Lær om dine rettigheter og plikter
          </p>
        </div>

        {/* Under Development Notice */}
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg mb-8">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                <span className="text-2xl">🚧</span>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-yellow-900 mb-2">
                Under utvikling
              </h3>
              <p className="text-yellow-800 mb-4">
                Denne siden er under utvikling. Her vil du finne:
              </p>
              <ul className="list-disc list-inside space-y-2 text-yellow-800">
                <li>Oversikt over dine NAV-rettigheter</li>
                <li>Informasjon om forskjellige ytelser</li>
                <li>Hvem har rett til hva og hvorfor</li>
                <li>Klagerettigheter og klageprosessen</li>
                <li>Lovverk og retningslinjer</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Coming Soon Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📜 Rettighetsguide</h3>
            <p className="text-sm text-gray-600">
              Detaljert informasjon om alle NAV-ytelser og hvem som har rett
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">⚖️ Klagerett</h3>
            <p className="text-sm text-gray-600">
              Hvordan klage på vedtak og hva du kan forvente
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📚 Lovverk</h3>
            <p className="text-sm text-gray-600">
              Relevant lovverk forklart på vanlig norsk
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🛡️ Personvern</h3>
            <p className="text-sm text-gray-600">
              Dine GDPR-rettigheter og hvordan NAV håndterer data
            </p>
          </div>
        </div>

        {/* Important Notice */}
        <div className="bg-blue-50 border-l-4 border-blue-400 p-6 rounded-lg mb-8">
          <h3 className="font-semibold text-blue-900 mb-2">
            Viktig informasjon
          </h3>
          <p className="text-sm text-blue-800">
            Informasjonen på denne siden er veiledende. For spesifikke spørsmål om
            dine rettigheter, ta kontakt med NAV direkte eller sjekk{" "}
            <a
              href="https://nav.no"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-blue-600"
            >
              nav.no
            </a>
            {" "}for offisiell informasjon.
          </p>
        </div>

        {/* Back Button */}
        <div className="text-center">
          <Link
            href="/"
            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium"
          >
            <ArrowLeft className="w-4 h-4" />
            Tilbake til Dashboard
          </Link>
        </div>
      </div>
    </Layout>
  );
}

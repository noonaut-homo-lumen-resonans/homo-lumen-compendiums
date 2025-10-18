"use client";

import Layout from "@/components/layout/Layout";
import { Briefcase, ArrowLeft } from "lucide-react";
import Link from "next/link";

/**
 * Jobb Page
 *
 * Placeholder page for job search and employment services
 */
export default function JobbPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-600">
          <Link href="/" className="hover:text-blue-600">NAV-Losen</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">Jobb</span>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 rounded-full mb-6">
            <Briefcase className="w-10 h-10 text-green-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Jobb
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Jobbsøk og arbeidsmarkedstjenester
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
                <li>Ledige stillinger fra arbeidsplassen.no</li>
                <li>CV-verktøy og søknadshjelp</li>
                <li>Kurs og opplæringsmuligheter</li>
                <li>Veiledning om arbeidssøkerrettigheter</li>
                <li>Kontakt med NAV Arbeidslivssenter</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Coming Soon Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🔍 Jobbsøk</h3>
            <p className="text-sm text-gray-600">
              Søk etter ledige stillinger tilpasset din kompetanse og interesser
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📄 CV-builder</h3>
            <p className="text-sm text-gray-600">
              Lag en profesjonell CV med veiledning og maler
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🎓 Kurs og opplæring</h3>
            <p className="text-sm text-gray-600">
              Utforsk arbeidsmarkedskurs og kompetanseheving
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">💼 Veiledningstjenester</h3>
            <p className="text-sm text-gray-600">
              Få hjelp fra NAV Arbeidslivssenter til jobbsøk og karrierevalg
            </p>
          </div>
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

"use client";

import Layout from "@/components/layout/Layout";
import { BookOpen, ArrowLeft } from "lucide-react";
import Link from "next/link";

/**
 * Veiledninger Page
 *
 * Placeholder page for guides and tutorials
 * Will contain step-by-step guidance for NAV processes
 */
export default function VeiledningerPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-600">
          <Link href="/" className="hover:text-blue-600">NAV-Losen</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">Veiledninger</span>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-blue-100 rounded-full mb-6">
            <BookOpen className="w-10 h-10 text-blue-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Veiledninger
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Steg-for-steg veiledninger for NAV-prosesser
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
                <li>Steg-for-steg veiledninger for NAV-søknader</li>
                <li>Hvordan fylle ut skjemaer korrekt</li>
                <li>Tidslinjer og frister</li>
                <li>Vanlige spørsmål og svar</li>
                <li>Kontaktinformasjon for hjelp</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Coming Soon Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📝 Søknadsveiledninger</h3>
            <p className="text-sm text-gray-600">
              Detaljerte guider for ulike typer NAV-søknader med eksempler og tips
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">⏰ Frister og tidslinjer</h3>
            <p className="text-sm text-gray-600">
              Oversikt over viktige datoer og forventet saksbehandlingstid
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">❓ FAQ</h3>
            <p className="text-sm text-gray-600">
              Svar på ofte stilte spørsmål om NAV-tjenester og rettigheter
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📞 Kontakt NAV</h3>
            <p className="text-sm text-gray-600">
              Informasjon om hvordan du kan kontakte NAV for personlig veiledning
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

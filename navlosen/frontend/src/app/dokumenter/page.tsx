"use client";

import Layout from "@/components/layout/Layout";
import { FileText, ArrowLeft } from "lucide-react";
import Link from "next/link";

/**
 * Dokumenter Page
 *
 * Placeholder page for document management
 */
export default function DokumenterPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-600">
          <Link href="/" className="hover:text-blue-600">NAV-Losen</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">Dokumenter</span>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-purple-100 rounded-full mb-6">
            <FileText className="w-10 h-10 text-purple-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Dokumenter
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Håndter og organiser dine NAV-dokumenter
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
                Denne siden er under utvikling. Her vil du kunne:
              </p>
              <ul className="list-disc list-inside space-y-2 text-yellow-800">
                <li>Laste opp og lagre viktige dokumenter</li>
                <li>Kategorisere dokumenter etter type</li>
                <li>Søke i dokumentarkivet ditt</li>
                <li>Dele dokumenter sikkert med NAV</li>
                <li>Se status på innsendte dokumenter</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Coming Soon Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">📤 Last opp</h3>
            <p className="text-sm text-gray-600">
              Sikker opplasting av PDF, bilder og andre dokumenter
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🗂️ Organisering</h3>
            <p className="text-sm text-gray-600">
              Automatisk kategorisering og merking av dokumenter
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🔍 Søk</h3>
            <p className="text-sm text-gray-600">
              Rask søk i alle dine lagrede dokumenter
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-2">🔒 Sikkerhet</h3>
            <p className="text-sm text-gray-600">
              Kryptert lagring og sikker deling med NAV
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

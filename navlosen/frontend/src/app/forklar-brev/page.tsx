"use client";

import Layout from "@/components/layout/Layout";
import { Lightbulb, ArrowLeft, Upload } from "lucide-react";
import Link from "next/link";

/**
 * Forklar Brev Page
 *
 * Placeholder page for letter explanation feature
 * Will help users understand official NAV letters
 */
export default function ForklarBrevPage() {
  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12">
        {/* Breadcrumbs */}
        <div className="mb-6 text-sm text-gray-600">
          <Link href="/" className="hover:text-blue-600">NAV-Losen</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900 font-medium">Forklar brev</span>
        </div>

        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-yellow-100 rounded-full mb-6">
            <Lightbulb className="w-10 h-10 text-yellow-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Forklar brev
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Få hjelp til å forstå brev fra NAV
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
                <li>Laste opp brev fra NAV (PDF, bilde)</li>
                <li>Få AI-drevet forklaring av brevinnholdet</li>
                <li>Forstå juridiske termer på vanlig norsk</li>
                <li>Se hva du må gjøre og når</li>
                <li>Få svar på spørsmål om brevet</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Coming Soon Features */}
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3 mb-3">
              <Upload className="w-6 h-6 text-blue-600" />
              <h3 className="font-semibold text-gray-900">Last opp brev</h3>
            </div>
            <p className="text-sm text-gray-600">
              Støtte for PDF-filer, bilder og skannede dokumenter
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">🤖</span>
              <h3 className="font-semibold text-gray-900">AI-forklaring</h3>
            </div>
            <p className="text-sm text-gray-600">
              Automatisk analyse og forklaring av brevinnholdet
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">📖</span>
              <h3 className="font-semibold text-gray-900">Juridisk ordbok</h3>
            </div>
            <p className="text-sm text-gray-600">
              Forklaring av komplekse juridiske termer på vanlig norsk
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-2xl">✅</span>
              <h3 className="font-semibold text-gray-900">Handlingsplan</h3>
            </div>
            <p className="text-sm text-gray-600">
              Klar oversikt over hva du må gjøre og når
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

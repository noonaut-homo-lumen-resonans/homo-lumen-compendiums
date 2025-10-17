"use client";

import { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import { Download, Trash2, Shield, Database, AlertTriangle } from "lucide-react";

/**
 * Innstillinger (Settings) Page
 *
 * GDPR-compliant data management:
 * - View what data is stored
 * - Export all data (JSON download)
 * - Delete all data (with confirmation)
 * - Revoke consent
 *
 * Triadisk Ethics:
 * - Port 1 (Suverenitet): Full user control over their data
 * - Port 2 (Koherens): GDPR Article 15 (Right to access) & Article 17 (Right to erasure)
 * - Port 3 (Healing): Transparency builds trust
 *
 * Triadisk Score: -0.9 (CRITICAL FOUNDATION)
 *
 * Based on Manus' Data Deletion & Export Protocol
 */

export default function InnstillingerPage() {
  const [dataSize, setDataSize] = useState<number>(0);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [dataDeleted, setDataDeleted] = useState(false);
  const [dataExported, setDataExported] = useState(false);

  // Calculate total localStorage size on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      let totalSize = 0;
      for (let key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          totalSize += localStorage[key].length + key.length;
        }
      }
      setDataSize(totalSize);
    }
  }, []);

  /**
   * Export all localStorage data as JSON
   */
  const handleExportData = () => {
    const allData: Record<string, any> = {};

    // Collect all NAV-Losen data
    const keys = [
      "navlosen-current-stage",
      "navlosen-emotions",
      "navlosen-stress-level",
      "navlosen-somatic-signals",
      "navlosen-lira-answers",
      "navlosen_consent",
      "navlosen_multi_scale_events",
    ];

    keys.forEach((key) => {
      const value = localStorage.getItem(key);
      if (value) {
        try {
          allData[key] = JSON.parse(value);
        } catch {
          allData[key] = value;
        }
      }
    });

    // Create JSON blob
    const jsonString = JSON.stringify(allData, null, 2);
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    // Download file
    const link = document.createElement("a");
    link.href = url;
    link.download = `navlosen-data-${new Date().toISOString().split("T")[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    setDataExported(true);
    setTimeout(() => setDataExported(false), 3000);
  };

  /**
   * Delete all localStorage data (requires confirmation)
   */
  const handleDeleteData = () => {
    if (!showDeleteConfirm) {
      setShowDeleteConfirm(true);
      return;
    }

    // Delete all NAV-Losen data
    const keys = [
      "navlosen-current-stage",
      "navlosen-emotions",
      "navlosen-stress-level",
      "navlosen-somatic-signals",
      "navlosen-lira-answers",
      "navlosen_consent",
      "navlosen_multi_scale_events",
    ];

    keys.forEach((key) => localStorage.removeItem(key));

    setDataDeleted(true);
    setShowDeleteConfirm(false);
    setDataSize(0);

    setTimeout(() => {
      window.location.href = "/";
    }, 2000);
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
  };

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Innstillinger</h1>
          <p className="text-lg text-gray-600">
            Administrer dine data og personvern
          </p>
        </div>

        {/* Success Messages */}
        {dataExported && (
          <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-6 rounded">
            <p className="text-sm text-green-800 font-medium">
              ✅ Data eksportert! Filen er lastet ned.
            </p>
          </div>
        )}

        {dataDeleted && (
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6 rounded">
            <p className="text-sm text-blue-800 font-medium">
              ✅ All data er slettet. Sender deg tilbake til startsiden...
            </p>
          </div>
        )}

        {/* Data Overview */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Database className="h-6 w-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">Dine Data</h2>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-sm text-gray-700">Total lagringsplass brukt:</span>
              <span className="text-sm font-medium text-gray-900">
                {formatBytes(dataSize)}
              </span>
            </div>

            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-sm text-gray-700">Lagret på:</span>
              <span className="text-sm font-medium text-gray-900">
                Din enhet (localStorage)
              </span>
            </div>

            <div className="flex justify-between items-center py-2">
              <span className="text-sm text-gray-700">Delt med servere:</span>
              <span className="text-sm font-medium text-green-600">
                ❌ Nei (100% lokal)
              </span>
            </div>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <p className="text-xs text-blue-800">
              💡 All data lagres kun på din enhet. NAV-Losen sender aldri data
              til eksterne servere.
            </p>
          </div>
        </div>

        {/* Data Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="h-6 w-6 text-purple-600" />
            <h2 className="text-xl font-semibold text-gray-900">Data-kontroll</h2>
          </div>

          <div className="space-y-4">
            {/* Export Data */}
            <div className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    Eksporter data
                  </h3>
                  <p className="text-sm text-gray-600">
                    Last ned all lagret data som JSON-fil. Nyttig for
                    backup eller overføring.
                  </p>
                </div>
                <Button
                  variant="secondary"
                  size="medium"
                  onClick={handleExportData}
                  leftIcon={<Download className="h-4 w-4" />}
                  className="flex-shrink-0"
                >
                  Eksporter
                </Button>
              </div>
            </div>

            {/* Delete Data */}
            <div className="border border-red-200 rounded-lg p-4 bg-red-50">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-red-900 mb-1">
                    Slett all data
                  </h3>
                  <p className="text-sm text-red-700">
                    Permanent sletting av all lagret data. Dette kan ikke
                    angres. Du vil bli sendt tilbake til startsiden.
                  </p>

                  {showDeleteConfirm && (
                    <div className="mt-3 p-3 bg-red-100 border border-red-300 rounded">
                      <div className="flex items-start gap-2">
                        <AlertTriangle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                        <div>
                          <p className="text-sm font-medium text-red-900 mb-2">
                            Er du sikker?
                          </p>
                          <p className="text-xs text-red-800 mb-3">
                            Dette vil permanent slette alle dine svar, følelser,
                            og innstillinger. Handlingen kan ikke angres.
                          </p>
                          <div className="flex gap-2">
                            <Button
                              variant="destructive"
                              size="small"
                              onClick={handleDeleteData}
                            >
                              Ja, slett alt
                            </Button>
                            <Button
                              variant="secondary"
                              size="small"
                              onClick={() => setShowDeleteConfirm(false)}
                            >
                              Avbryt
                            </Button>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {!showDeleteConfirm && (
                  <Button
                    variant="destructive"
                    size="medium"
                    onClick={handleDeleteData}
                    leftIcon={<Trash2 className="h-4 w-4" />}
                    className="flex-shrink-0"
                  >
                    Slett
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* GDPR Information */}
        <div className="bg-gray-50 rounded-xl p-6">
          <h3 className="font-semibold text-gray-900 mb-3">
            Dine rettigheter (GDPR)
          </h3>
          <ul className="space-y-2 text-sm text-gray-700">
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>
                <strong>Rett til innsyn (Art. 15):</strong> Du har full tilgang
                til all data via "Eksporter data"
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>
                <strong>Rett til sletting (Art. 17):</strong> Du kan slette all
                data når som helst
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>
                <strong>Dataportabilitet (Art. 20):</strong> Data eksporteres i
                lesbart JSON-format
              </span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>
                <strong>Personvern ved design:</strong> Ingen data sendes til
                servere, alt lagres lokalt
              </span>
            </li>
          </ul>
        </div>

        {/* Back to Home */}
        <div className="mt-8 text-center">
          <a
            href="/"
            className="text-blue-600 hover:text-blue-800 underline font-medium"
          >
            ← Tilbake til Mestring
          </a>
        </div>
      </div>
    </Layout>
  );
}

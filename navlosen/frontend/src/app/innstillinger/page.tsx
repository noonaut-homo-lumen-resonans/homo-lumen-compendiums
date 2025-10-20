"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import GoogleSignIn from "@/components/auth/GoogleSignIn";
import { useGoogleAuth } from "@/contexts/GoogleAuthContext";
import {
  Download,
  Trash2,
  Shield,
  Database,
  AlertTriangle,
  Settings,
  Bell,
  Moon,
  Sun,
  Globe,
  Lock,
  User,
  LogOut,
  ChevronRight,
} from "lucide-react";

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
  const router = useRouter();
  const { user, isAuthenticated, signOut, hasCalendarAccess, hasGmailAccess } = useGoogleAuth();

  const [dataSize, setDataSize] = useState<number>(0);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [dataDeleted, setDataDeleted] = useState(false);
  const [dataExported, setDataExported] = useState(false);

  // Notification settings
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [pushNotifications, setPushNotifications] = useState(true);
  const [reminderNotifications, setReminderNotifications] = useState(true);

  // Appearance settings
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState("no");

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

      // Load settings from localStorage
      const savedEmailNotif = localStorage.getItem("navlosen_settings_email_notif");
      const savedPushNotif = localStorage.getItem("navlosen_settings_push_notif");
      const savedReminderNotif = localStorage.getItem("navlosen_settings_reminder_notif");
      const savedDarkMode = localStorage.getItem("navlosen_settings_dark_mode");
      const savedLanguage = localStorage.getItem("navlosen_settings_language");

      if (savedEmailNotif !== null) setEmailNotifications(savedEmailNotif === "true");
      if (savedPushNotif !== null) setPushNotifications(savedPushNotif === "true");
      if (savedReminderNotif !== null) setReminderNotifications(savedReminderNotif === "true");
      if (savedDarkMode !== null) setDarkMode(savedDarkMode === "true");
      if (savedLanguage) setLanguage(savedLanguage);
    }
  }, []);

  // Save settings to localStorage when they change
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen_settings_email_notif", String(emailNotifications));
      localStorage.setItem("navlosen_settings_push_notif", String(pushNotifications));
      localStorage.setItem("navlosen_settings_reminder_notif", String(reminderNotifications));
      localStorage.setItem("navlosen_settings_dark_mode", String(darkMode));
      localStorage.setItem("navlosen_settings_language", language);
    }
  }, [emailNotifications, pushNotifications, reminderNotifications, darkMode, language]);

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
        {/* Hero Section */}
        <div className="relative mb-8 rounded-2xl bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 p-8 overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-purple-100 rounded-full -mr-32 -mt-32 opacity-50"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-blue-100 rounded-full -ml-24 -mb-24 opacity-50"></div>

          <div className="relative flex items-start gap-6">
            <div className="flex-shrink-0">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg">
                <Settings className="h-8 w-8 text-white" />
              </div>
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Innstillinger</h1>
              <p className="text-lg text-gray-700">
                Administrer din konto, preferanser og personvern
              </p>
            </div>
          </div>
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

        {/* Account Section */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <User className="h-6 w-6 text-indigo-600" />
            <h2 className="text-xl font-semibold text-gray-900">Konto</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Google-konto
                </h3>
                <p className="text-sm text-gray-600">
                  {isAuthenticated
                    ? "Koblet til for kalender og e-post integrasjon"
                    : "Koble til Google for kalender og e-post integrasjon"}
                </p>
              </div>
              <GoogleSignIn />
            </div>

            {isAuthenticated && user && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Lock className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium text-gray-900">
                      Kalendertilgang
                    </span>
                  </div>
                  <p className="text-xs text-gray-600">
                    {hasCalendarAccess
                      ? "✓ Aktivert - kan opprette kalenderavtaler"
                      : "○ Ikke aktivert"}
                  </p>
                </div>

                <div className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Lock className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium text-gray-900">
                      E-post tilgang
                    </span>
                  </div>
                  <p className="text-xs text-gray-600">
                    {hasGmailAccess
                      ? "✓ Aktivert - kan sende e-post"
                      : "○ Ikke aktivert"}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Notification Settings */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Bell className="h-6 w-6 text-yellow-600" />
            <h2 className="text-xl font-semibold text-gray-900">Varsler</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  E-postvarsler
                </h3>
                <p className="text-sm text-gray-600">
                  Motta oppdateringer og påminnelser på e-post
                </p>
              </div>
              <button
                onClick={() => setEmailNotifications(!emailNotifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  emailNotifications ? "bg-blue-600" : "bg-gray-200"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    emailNotifications ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Push-varsler
                </h3>
                <p className="text-sm text-gray-600">
                  Motta varsler direkte i nettleseren
                </p>
              </div>
              <button
                onClick={() => setPushNotifications(!pushNotifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  pushNotifications ? "bg-blue-600" : "bg-gray-200"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    pushNotifications ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Påminnelser
                </h3>
                <p className="text-sm text-gray-600">
                  Motta påminnelser om frister og møter
                </p>
              </div>
              <button
                onClick={() => setReminderNotifications(!reminderNotifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  reminderNotifications ? "bg-blue-600" : "bg-gray-200"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    reminderNotifications ? "translate-x-6" : "translate-x-1"
                  }`}
                />
              </button>
            </div>
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <Globe className="h-6 w-6 text-purple-600" />
            <h2 className="text-xl font-semibold text-gray-900">Utseende</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Mørk modus
                </h3>
                <p className="text-sm text-gray-600">
                  Bytt mellom lyst og mørkt tema
                </p>
              </div>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  darkMode ? "bg-gray-800" : "bg-gray-200"
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform flex items-center justify-center ${
                    darkMode ? "translate-x-6" : "translate-x-1"
                  }`}
                >
                  {darkMode ? (
                    <Moon className="h-3 w-3 text-gray-800" />
                  ) : (
                    <Sun className="h-3 w-3 text-yellow-500" />
                  )}
                </span>
              </button>
            </div>

            <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  Språk
                </h3>
                <p className="text-sm text-gray-600">
                  Velg foretrukket språk for applikasjonen
                </p>
              </div>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="no">Norsk</option>
                <option value="en">English</option>
                <option value="sv">Svenska</option>
              </select>
            </div>
          </div>
        </div>

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

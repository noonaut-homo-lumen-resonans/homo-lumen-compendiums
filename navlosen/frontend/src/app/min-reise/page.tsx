"use client";

import { useState, useEffect } from "react";
import Layout from "@/components/layout/Layout";
import MasteryLog from "@/components/mestring/MasteryLog";
import BiofeltCheckpoint from "@/components/mestring/BiofeltCheckpoint";
import JourneySuccess from "@/components/mestring/JourneySuccess";
import { BookOpen, Heart, Compass, Sparkles } from "lucide-react";

export default function MinReisePage() {
  const [activeView, setActiveView] = useState<"overview" | "mastery" | "checkpoint" | "celebration">("overview");

  useEffect(() => {
    // Hide sidebar on this page
    const sidebar = document.querySelector('aside');
    if (sidebar) {
      sidebar.style.display = 'none';
    }

    return () => {
      // Show sidebar again when leaving this page
      const sidebar = document.querySelector('aside');
      if (sidebar) {
        sidebar.style.display = '';
      }
    };
  }, []);

  return (
    <Layout>
      <div className="bg-gradient-to-b from-blue-50 via-cyan-50 to-teal-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">
      {activeView === "overview" && (
        <div className="w-full">
          {/* Page header */}
          <div className="w-full mb-8 text-left">
            {/* Breadcrumb */}
            <div className="mb-4 text-sm text-gray-600">
              <span>NAV-Losen</span>
              <span className="mx-2">/</span>
              <span className="text-gray-900 font-medium">Min Reise</span>
            </div>

            <div className="flex items-center gap-3 mb-2">
              <Compass className="h-8 w-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-900 text-left">Min Reise</h1>
            </div>
            <p className="text-lg text-gray-600 text-left">
              Reflekter, øv, og bygg din egen vei til mestring
            </p>
          </div>

          {/* Main content */}
          <div className="w-full space-y-8">
            {/* Reminder callout */}
            <div className="bg-purple-50 border-l-4 border-purple-400 p-6 rounded-lg">
              <div className="flex items-start gap-3">
                <Heart className="h-6 w-6 text-purple-600 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-purple-900 mb-2">
                    Husk: Dette handler ikke om perfeksjon
                  </h3>
                  <p className="text-sm text-purple-800">
                    Målet er ikke å bruke NAV-Losen for alltid. Målet er at du lærer deg selv
                    å kjenne, bygger din egen verktøykasse, og over tid blir mer selvstendig
                    i din mestring.
                  </p>
                </div>
              </div>
            </div>

            {/* Three navigation cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <button
                onClick={() => setActiveView("mastery")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-purple-300 text-left"
              >
                <div className="mb-4">
                  <BookOpen className="h-12 w-12 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Mestringslogg
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Dine egne strategier som virker for deg.
                </p>
                <div className="text-purple-600 font-medium text-sm">
                  Åpne logg →
                </div>
              </button>

              <button
                onClick={() => setActiveView("checkpoint")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-cyan-300 text-left"
              >
                <div className="mb-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-yellow-300 to-amber-400"></div>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Biofelt-checkpoint
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Ta en kort pause med 4-6-8 pustemetoden.
                </p>
                <div className="text-cyan-600 font-medium text-sm">
                  Start pusteøvelse →
                </div>
              </button>

              <button
                onClick={() => setActiveView("celebration")}
                className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all border-2 border-transparent hover:border-green-300 text-left"
              >
                <div className="mb-4">
                  <Sparkles className="h-12 w-12 text-green-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  Feire reisen
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Se din reise fra storm til trygg havn.
                </p>
                <div className="text-green-600 font-medium text-sm">
                  Se din reise →
                </div>
              </button>
            </div>

            {/* Back link */}
            <div className="text-center">
              <a
                href="/"
                className="text-blue-600 hover:text-blue-800 underline font-medium"
              >
                ← Tilbake til hovedside
              </a>
            </div>
          </div>
        </div>
      )}

      {activeView === "mastery" && (
        <div className="w-full">
          <MasteryLog onClose={() => setActiveView("overview")} />
        </div>
      )}

      {activeView === "checkpoint" && (
        <div className="w-full">
          <BiofeltCheckpoint
            onComplete={() => setActiveView("overview")}
            onSkip={() => setActiveView("overview")}
            showSkipButton={true}
          />
        </div>
      )}

      {activeView === "celebration" && (
        <div className="w-full">
          <JourneySuccess
            title="Din Reise"
            message="Du har navigert gjennom utfordringer og funnet din vei til trygghet."
            onContinue={() => setActiveView("overview")}
            showAnimation={true}
          />
        </div>
      )}
      </div>
    </Layout>
  );
}

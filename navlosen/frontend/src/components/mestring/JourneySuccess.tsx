"use client";

import { useEffect, useState } from "react";

/**
 * JourneySuccess - Lighthouse & Harbor Visualization
 *
 * Visual Metaphor: Fyrtårn i trygg havn (Lighthouse in safe harbor)
 * Purpose: Celebrate completion, reinforce mastery, build self-efficacy
 *
 * Nyra's Vision:
 * "Etter at et klagebrev er sendt, kan vi vise et bilde av en rolig havn
 * med et opplyst fyrtårn, sammen med en melding som: 'Godt jobbet. Du
 * navigerte stormen og kom trygt i havn.' Dette understreker ikke bare
 * handlingen, men også brukerens egen styrke i prosessen."
 *
 * Triadisk Ethics:
 * - Suverenitet: User controls their journey, celebrates their achievement
 * - Koherens: Consistent with lighthouse metaphor throughout app
 * - Healing: Builds mastery, self-efficacy, emotional regulation capacity
 */

export interface JourneySuccessProps {
  title?: string;
  message?: string;
  onContinue?: () => void;
  showAnimation?: boolean;
}

export default function JourneySuccess({
  title = "Godt jobbet!",
  message = "Du navigerte stormen og kom trygt i havn.",
  onContinue,
  showAnimation = true,
}: JourneySuccessProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Delay animation slightly for smooth entrance
    const timer = setTimeout(() => setIsVisible(true), 100);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div
      className={`w-full transition-all duration-1000 ${
        isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-10"
      }`}
    >
      {/* Harbor Scene */}
      <div className="relative bg-gradient-to-b from-blue-900 via-blue-700 to-cyan-600 rounded-2xl overflow-hidden shadow-2xl">
        {/* Sky & Stars */}
        <div className="absolute inset-0 bg-gradient-to-b from-indigo-950 via-blue-900 to-transparent opacity-40">
          {/* Twinkling stars */}
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full animate-pulse"
              style={{
                top: `${Math.random() * 40}%`,
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${2 + Math.random() * 2}s`,
              }}
            ></div>
          ))}
        </div>

        {/* Harbor (safe zone) */}
        <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-teal-800 to-transparent opacity-60"></div>

        {/* Lighthouse */}
        <div className="relative z-10 flex items-center justify-center py-16">
          <div className="relative">
            {/* Lighthouse beam (rotating) */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-32">
              <div
                className={`absolute inset-0 ${
                  showAnimation ? "lighthouse-sweep" : ""
                }`}
              >
                <div
                  className="absolute top-0 left-1/2 w-1 h-32 bg-gradient-to-b from-yellow-200 to-transparent"
                  style={{ transformOrigin: "top center" }}
                ></div>
              </div>
            </div>

            {/* Lighthouse structure */}
            <div className="relative flex flex-col items-center">
              {/* Light room */}
              <div className="w-16 h-12 bg-yellow-400 rounded-t-lg pulse-glow shadow-2xl">
                <div className="w-full h-full bg-gradient-to-b from-yellow-300 to-yellow-500"></div>
              </div>

              {/* Tower */}
              <div className="w-12 h-32 bg-white border-4 border-red-500 shadow-xl">
                <div className="w-full h-1/3 bg-red-500 my-2"></div>
              </div>

              {/* Base */}
              <div className="w-16 h-8 bg-gray-700 rounded-b-lg shadow-lg"></div>

              {/* Reflection in water */}
              <div className="absolute -bottom-20 w-16 h-20 bg-gradient-to-b from-yellow-400/30 to-transparent blur-sm"></div>
            </div>
          </div>
        </div>

        {/* Waves (gentle) */}
        <div className="absolute bottom-0 left-0 right-0 h-24 overflow-hidden">
          <svg
            className="absolute bottom-0 w-full h-24 wave-motion"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1440 120"
            preserveAspectRatio="none"
          >
            <path
              d="M0,60 Q360,90 720,60 T1440,60 L1440,120 L0,120 Z"
              fill="rgba(6, 182, 212, 0.3)"
            />
          </svg>
          <svg
            className="absolute bottom-0 w-full h-20"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1440 100"
            preserveAspectRatio="none"
            style={{ animationDelay: "1s" }}
          >
            <path
              d="M0,50 Q360,70 720,50 T1440,50 L1440,100 L0,100 Z"
              fill="rgba(17, 94, 89, 0.5)"
            />
          </svg>
        </div>

        {/* Success message */}
        <div className="relative z-20 px-8 pb-16">
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl p-8 shadow-xl mx-auto" style={{ maxWidth: "600px" }}>
            {/* Sprouting seed animation */}
            <div className="mb-4 flex justify-center">
              <div
                className={`text-6xl ${showAnimation ? "sprout-animation" : ""}`}
              >
                🌱
              </div>
            </div>

            <h1 className="text-3xl font-bold text-gray-900 mb-4 text-center">{title}</h1>
            <p className="text-xl text-gray-700 mb-6 text-center">{message}</p>

            <div className="bg-blue-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-600 italic text-center">
                "Du har navigert gjennom usikkerhet og funnet din vei til trygghet.
                Dette er din styrke, din mestring, ditt lys i mørket."
              </p>
            </div>

            {onContinue && (
              <div className="flex justify-center">
                <button
                  onClick={onContinue}
                  className="px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-cyan-600 transition-all calm-hover shadow-lg"
                >
                  Fortsett reisen
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Journey map - visual path filled */}
      <div className="mt-8 bg-white rounded-lg p-6 shadow-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Din reise i dag
        </h3>

        <div className="flex items-center justify-between">
          {/* Stage markers */}
          {[
            { name: "Følelser", icon: "💚" },
            { name: "Signaler", icon: "🎯" },
            { name: "Dialog", icon: "💬" },
            { name: "Anbefalinger", icon: "✨" },
            { name: "Trygg havn", icon: "⚓" },
          ].map((stage, index) => (
            <div key={index} className="flex flex-col items-center">
              <div
                className={`w-16 h-16 rounded-full bg-gradient-to-br from-green-400 to-teal-500 flex items-center justify-center text-2xl shadow-lg ${
                  showAnimation ? "sprout-animation" : ""
                }`}
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                {stage.icon}
              </div>
              <p className="text-xs text-gray-600 mt-2 text-center">
                {stage.name}
              </p>
              {index < 4 && (
                <div className="absolute w-16 h-1 bg-green-500 -z-10 fill-path"></div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

"use client";

import React from "react";
import Button from "@/components/ui/Button";
import { Heart, TrendingUp, Calendar } from "lucide-react";

interface Fase1WelcomeProps {
  onContinue: () => void;
}

/**
 * Fase 1: Velkomsthilsen
 *
 * Introduserer brukeren til NAV-Losen Mestring med en varm, rolig velkomst.
 * Forklarer hva verktøyet prøver å hjelpe med før brukeren starter check-in.
 *
 * Design: Minimalistisk, rolig, trygg atmosfære
 * Inspirert av: How We Feel (HWF) app
 *
 * Triadisk Score: 0.10 (PROCEED)
 */
export default function Fase1Welcome({ onContinue }: Fase1WelcomeProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 via-purple-50 to-pink-50 px-4 md:px-12 lg:px-24 py-12">
      <div className="w-full max-w-3xl text-center space-y-8">
        {/* Icon */}
        <div className="flex justify-center">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
            <Heart className="w-12 h-12 text-white" fill="white" />
          </div>
        </div>

        {/* Heading */}
        <div className="space-y-3">
          <h1 className="text-4xl font-bold text-gray-900">
            Velkommen til din check-in
          </h1>
          <p className="text-lg text-gray-600">
            La oss ta et øyeblikk sammen
          </p>
        </div>

        {/* Value Propositions */}
        <div className="space-y-6 text-left bg-white rounded-2xl p-8 shadow-sm">
          <p className="text-base text-gray-700 leading-relaxed">
            NAV-Losen vil hjelpe deg med å:
          </p>

          <div className="space-y-4">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                <Heart className="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">
                  Finne de rette ordene
                </h3>
                <p className="text-sm text-gray-600">
                  Beskrive dine følelser med presisjon og nyanse
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">
                  Finne strategier som virker
                </h3>
                <p className="text-sm text-gray-600">
                  Få personaliserte verktøy tilpasset din tilstand
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <Calendar className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">
                  Identifisere mønstre
                </h3>
                <p className="text-sm text-gray-600">
                  Spore din reise gjennom daglig oppfølging
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Button */}
        <Button
          onClick={onContinue}
          variant="primary"
          size="large"
          fullWidth
          className="text-lg py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg hover:shadow-xl"
        >
          Fortsett
        </Button>

        {/* Footer note */}
        <p className="text-xs text-gray-500">
          Dette tar vanligvis 2-3 minutter
        </p>
      </div>
    </div>
  );
}

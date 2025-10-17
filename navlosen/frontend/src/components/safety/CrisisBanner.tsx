"use client";

import { AlertTriangle, Phone } from "lucide-react";

/**
 * CrisisBanner - Emergency Contact Component
 *
 * Shown when user is in high crisis state (stress 9-10 + severe emotions)
 *
 * Triadisk Ethics:
 * - Port 1 (Suverenitet): User chooses whether to use resources
 * - Port 2 (Koherens): Evidence-based crisis intervention (hotlines)
 * - Port 3 (Healing): Immediate safety net, prevents harm
 *
 * Triadisk Score: -0.9 (CRITICAL HEALING)
 *
 * Based on Manus' Crisis Safety Protocol
 */

export interface CrisisBannerProps {
  visible?: boolean;
  variant?: "full" | "compact";
}

export default function CrisisBanner({
  visible = true,
  variant = "full",
}: CrisisBannerProps) {
  if (!visible) return null;

  if (variant === "compact") {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-3 mb-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="text-red-500 h-5 w-5 flex-shrink-0" />
          <div className="flex-1">
            <p className="text-sm text-red-700 font-medium">
              Trenger du hjelp nå?{" "}
              <a
                href="tel:113"
                className="text-red-800 font-bold underline hover:text-red-900"
              >
                Ring 113
              </a>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg shadow-sm">
      <div className="flex items-start gap-3">
        <AlertTriangle className="text-red-500 h-6 w-6 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="font-semibold text-red-800 text-lg mb-2">
            Trenger du hjelp nå?
          </h3>
          <p className="text-red-700 text-sm mb-3">
            Hvis du har tanker om å skade deg selv eller andre, eller trenger
            akutt hjelp, kontakt:
          </p>

          <div className="space-y-2">
            <a
              href="tel:113"
              className="flex items-center gap-2 text-red-800 font-bold hover:text-red-900 hover:underline transition-all"
            >
              <Phone className="h-4 w-4" />
              <span>113 - Mental Helse (Akutt)</span>
            </a>

            <a
              href="tel:116123"
              className="flex items-center gap-2 text-red-800 font-bold hover:text-red-900 hover:underline transition-all"
            >
              <Phone className="h-4 w-4" />
              <span>116 123 - Kirkens SOS (24/7)</span>
            </a>

            <a
              href="tel:116006"
              className="flex items-center gap-2 text-red-800 font-bold hover:text-red-900 hover:underline transition-all"
            >
              <Phone className="h-4 w-4" />
              <span>116 006 - Kors på Halsen (Barn/Unge)</span>
            </a>
          </div>

          <div className="mt-3 pt-3 border-t border-red-200">
            <p className="text-xs text-red-600">
              Du er ikke alene. Det er styrke i å søke hjelp.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

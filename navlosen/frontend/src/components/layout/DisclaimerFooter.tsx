"use client";

import { ExternalLink } from "lucide-react";

/**
 * DisclaimerFooter - Legal & Safety Disclaimers
 *
 * Shown at bottom of every page to remind users:
 * - NAV-Losen is NOT medical advice
 * - NOT official NAV guidance
 * - Seek professional help when needed
 *
 * Triadisk Ethics:
 * - Port 1 (Suverenitet): Honest about limitations
 * - Port 2 (Koherens): Legally compliant
 * - Port 3 (Healing): Prevents harm through transparency
 *
 * Triadisk Score: -0.7 (CRITICAL FOUNDATION)
 *
 * Based on Manus' Disclaimers & Limitations Protocol
 */

export default function DisclaimerFooter() {
  return (
    <div className="bg-blue-50 border-t border-blue-200 mt-6">
      <div className="max-w-7xl mx-auto px-3 py-3">
        {/* Compact single-line disclaimer */}
        <p className="text-xs text-blue-800 leading-tight">
          <strong className="text-blue-900">Viktig:</strong> NAV-Losen er et hjelpemiddel, ikke medisinsk rådgivning.{" "}
          <a
            href="https://www.nav.no"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-700 hover:text-blue-900 underline inline-flex items-center gap-1"
          >
            Besøk nav.no
            <ExternalLink className="h-3 w-3 inline" />
          </a>
        </p>
      </div>
    </div>
  );
}

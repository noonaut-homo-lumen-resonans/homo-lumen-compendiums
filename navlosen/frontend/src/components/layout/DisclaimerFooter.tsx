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
    <div className="bg-blue-50 border-t border-blue-200 mt-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="space-y-3">
          {/* Primary Disclaimer */}
          <div>
            <p className="text-sm text-blue-900 font-medium">
              Viktig å huske:
            </p>
            <p className="text-sm text-blue-800 mt-1">
              NAV-Losen Mestring er et hjelpemiddel for selvregulering og
              veiledning. Den erstatter <strong>ikke</strong> profesjonell hjelp
              fra lege, psykolog, eller NAV-veileder. Informasjonen her er{" "}
              <strong>ikke</strong> offisiell rådgivning fra NAV.
            </p>
          </div>

          {/* Seek Help */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pt-2 border-t border-blue-300">
            <p className="text-sm text-blue-800">
              Søk alltid profesjonell hjelp hvis du trenger det.
            </p>

            <a
              href="https://www.nav.no"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-blue-700 hover:text-blue-900 font-medium underline transition-colors"
            >
              <span>Besøk nav.no for offisiell informasjon</span>
              <ExternalLink className="h-4 w-4" />
            </a>
          </div>

          {/* Version & Coalition */}
          <div className="pt-2 border-t border-blue-300">
            <p className="text-xs text-blue-600">
              NAV-Losen Mestring v1.0 | Utviklet av Homo Lumen 10-Agent Coalition
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

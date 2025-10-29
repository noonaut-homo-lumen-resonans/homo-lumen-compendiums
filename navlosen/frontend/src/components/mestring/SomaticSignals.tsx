"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { SomaticSignal } from "@/types";

interface SomaticSignalsProps {
  signals: SomaticSignal[];
  onChange: (signals: SomaticSignal[]) => void;
  className?: string;
}

/**
 * SomaticSignals Component
 *
 * Body awareness checkboxes for somatic tracking
 * Based on Polyvagal Theory - tracking nervous system signals
 *
 * Helps users recognize physical stress indicators:
 * - Ventral: Relaxed, warm, open
 * - Sympathetic: Fast pulse, tension, shallow breathing
 * - Dorsal: Numb, frozen, disconnect
 *
 * @example
 * <SomaticSignals signals={signals} onChange={setSignals} />
 */
export default function SomaticSignals({
  signals,
  onChange,
  className,
}: SomaticSignalsProps) {
  const toggleSignal = (id: string) => {
    const updated = signals.map((signal) =>
      signal.id === id ? { ...signal, checked: !signal.checked } : signal
    );
    onChange(updated);
  };

  const checkedCount = signals.filter((s) => s.checked).length;

  return (
    <div className={cn("w-full text-left", className)}>
      <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2 text-left">
        Kjenner du på noen av disse kroppslige signalene?
      </h3>

      <p className="text-sm text-[var(--color-text-secondary)] mb-4 text-left">
        Kroppen din gir deg viktig informasjon om hvordan du har det. Huk av
        for signaler du merker akkurat nå.
      </p>

      {/* Checkboxes */}
      <div className="space-y-3">
        {signals.map((signal) => (
          <label
            key={signal.id}
            className={cn(
              "flex items-center gap-3 p-4 rounded-lg border-2",
              "cursor-pointer transition-all duration-200",
              "hover:bg-gray-50",
              {
                "bg-blue-50 border-blue-300": signal.checked,
                "bg-white border-gray-200": !signal.checked,
              }
            )}
          >
            <input
              type="checkbox"
              checked={signal.checked}
              onChange={() => toggleSignal(signal.id)}
              className={cn(
                "w-5 h-5 rounded border-2 border-gray-300",
                "text-[var(--color-primary)] focus:ring-2 focus:ring-[var(--color-primary)] focus:ring-offset-2",
                "cursor-pointer"
              )}
              aria-label={signal.label}
            />
            <span
              className={cn("text-base", {
                "font-medium text-blue-900": signal.checked,
                "text-[var(--color-text-primary)]": !signal.checked,
              })}
            >
              {signal.label}
            </span>
          </label>
        ))}
      </div>

      {/* Summary */}
      {checkedCount > 0 && (
        <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
          <p className="text-sm text-orange-800">
            <strong>Du merker {checkedCount} signal(er).</strong> Dette er
            verdifull informasjon. Kroppen din forteller deg noe viktig.
          </p>
        </div>
      )}

      {/* Info box */}
      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>ℹ️ Visste du?</strong> Kroppslige signaler er nervesystemets
          måte å kommunisere på. Ved å bli bevisst på dem, kan du velge
          strategier som hjelper deg å regulere.
        </p>
      </div>
    </div>
  );
}

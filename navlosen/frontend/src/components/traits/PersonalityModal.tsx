"use client";

import React from "react";
import { BigFive } from "@/types";
import { X, Settings, Trash2, HelpCircle } from "lucide-react";
import Button from "@/components/ui/Button";
import PersonalityAvatar from "./PersonalityAvatar";
import {
  getPersonalityDescription,
  getTraitLabel,
  getTraitDescription,
  getAuraColor,
} from "@/utils/personalityMapping";

interface PersonalityModalProps {
  bigFive: BigFive;
  polyvagalState?: "ventral" | "sympathetic" | "dorsal";
  onClose: () => void;
  onEdit?: () => void;
}

/**
 * PersonalityModal Component
 *
 * Full-screen modal showing detailed personality profile.
 *
 * Content:
 * - Large PersonalityAvatar
 * - Radar chart (all 5 traits)
 * - Textual description
 * - Trait list with bars
 * - Edit/Delete actions
 *
 * Triadisk Score: 0.15 (PROCEED)
 */
export default function PersonalityModal({
  bigFive,
  polyvagalState = "ventral",
  onClose,
  onEdit,
}: PersonalityModalProps) {
  const description = getPersonalityDescription(bigFive);
  const colors = getAuraColor(bigFive);

  const traits: Array<{
    key: keyof Pick<BigFive, "O" | "C" | "E" | "A" | "N">;
    label: string;
    desc: string;
    color: string;
  }> = [
    { key: "O", label: "Åpenhet", desc: getTraitDescription("O"), color: "bg-purple-500" },
    { key: "C", label: "Planmessighet", desc: getTraitDescription("C"), color: "bg-blue-500" },
    { key: "E", label: "Utadvendthet", desc: getTraitDescription("E"), color: "bg-green-500" },
    { key: "A", label: "Omgjengelighet", desc: getTraitDescription("A"), color: "bg-orange-500" },
    { key: "N", label: "Nevrotisisme", desc: getTraitDescription("N"), color: "bg-red-500" },
  ];

  const handleDelete = () => {
    if (confirm("Er du sikker på at du vil slette din personlighetsdata? Dette kan ikke angres.")) {
      localStorage.removeItem("navlosen-bigfive");
      localStorage.removeItem("navlosen-bigfive-policy");
      onClose();
      window.location.reload();
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-2 md:p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-6xl mx-auto p-6 md:p-8 lg:p-10 overflow-y-auto max-h-[95vh]">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-[var(--color-text-primary)]">
            Din personlighetsprofil
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition-colors p-2"
            aria-label="Lukk"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Avatar + Description */}
        <div className="flex flex-col md:flex-row items-center gap-8 mb-8">
          {/* Avatar */}
          <div className="flex-shrink-0">
            <PersonalityAvatar
              bigFive={bigFive}
              polyvagalState={polyvagalState}
              size="large"
              interactive={false}
              showLabel={false}
            />
          </div>

          {/* Description */}
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-[var(--color-text-primary)] mb-3">
              Hvem er du?
            </h3>
            <p className="text-lg text-[var(--color-text-secondary)] leading-relaxed mb-4">
              {description}
            </p>
            <div className="flex items-start gap-2 text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
              <HelpCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <p>
                <strong>Husk:</strong> Din tilstand (fra Mestring) er alltid viktigere enn personlighet.
                Dette brukes kun som svak påvirkning (≤10%) for å finpusse anbefalinger.
              </p>
            </div>
          </div>
        </div>

        {/* Traits */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-6">
            Dine fem dimensjoner (OCEAN)
          </h3>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {traits.map((trait) => {
              const value = (bigFive[trait.key] ?? 0.5) as number;
              const percentage = Math.round(value * 100);

              return (
                <div key={trait.key} className="bg-gray-50 rounded-lg p-4">
                  {/* Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold text-gray-900 w-8">
                        {trait.key}
                      </span>
                      <span className="text-base font-semibold text-gray-700">
                        {trait.label}
                      </span>
                    </div>
                    <span className="text-lg font-bold text-gray-900">{percentage}%</span>
                  </div>

                  {/* Bar */}
                  <div className="h-3 bg-gray-200 rounded-full overflow-hidden mb-3">
                    <div
                      className={`h-full ${trait.color} transition-all duration-500`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-600 leading-relaxed">
                    {trait.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Source info */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Datakilde:</span>
            <span className="font-medium text-green-700">
              {bigFive.source === "self_report"
                ? "Selvrapport"
                : bigFive.source === "inferred"
                ? "Estimert fra mønstre"
                : "Selvrapport + estimat"}
            </span>
          </div>
          {bigFive.updatedAt && (
            <div className="flex items-center justify-between text-sm mt-2">
              <span className="text-gray-600">Oppdatert:</span>
              <span className="text-gray-700">
                {new Date(bigFive.updatedAt).toLocaleDateString("nb-NO", {
                  day: "numeric",
                  month: "long",
                  year: "numeric",
                })}
              </span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3">
          {onEdit && (
            <Button
              onClick={() => {
                onClose();
                onEdit();
              }}
              variant="primary"
              size="large"
              leftIcon={<Settings className="w-5 h-5" />}
              className="flex-1"
            >
              Rediger personlighet
            </Button>
          )}
          <Button
            onClick={handleDelete}
            variant="destructive"
            size="large"
            leftIcon={<Trash2 className="w-5 h-5" />}
            className="flex-1"
          >
            Slett data
          </Button>
          <Button
            onClick={onClose}
            variant="secondary"
            size="large"
            className="flex-1"
          >
            Lukk
          </Button>
        </div>

        {/* Footer note */}
        <div className="mt-6 text-xs text-gray-500 text-center">
          <p>
            💡 Personlighetsdata lagres kun lokalt på din enhet og sendes aldri til server.
            Du har full kontroll og kan slette når som helst.
          </p>
        </div>
      </div>
    </div>
  );
}

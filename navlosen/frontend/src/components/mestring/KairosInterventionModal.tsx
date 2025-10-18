"use client";

import React from "react";
import Button from "@/components/ui/Button";
import { X, Heart, Wind, Sparkles, CheckCircle2 } from "lucide-react";
import { type KairosIntervention } from "@/lib/kairosInterventions";

interface KairosInterventionModalProps {
  intervention: KairosIntervention | null;
  onAccept: () => void;
  onDismiss: () => void;
}

/**
 * KairosInterventionModal
 *
 * Displays Kairos intervention suggestions with full ethical compliance:
 * - Port 1: User can always dismiss (X button + "Nei takk" option)
 * - Port 2: Shame-free language, suggestions not demands
 * - Port 3: Graduation design (celebrate progress toward independence)
 *
 * Zara Protocol Compliance:
 * - No manipulative nudging (clear opt-out)
 * - No re-traumatization (empathetic NVC language)
 * - Transparent reasoning (confidence score shown)
 */
export default function KairosInterventionModal({
  intervention,
  onAccept,
  onDismiss,
}: KairosInterventionModalProps) {
  if (!intervention || !intervention.triggered) return null;

  const getIcon = () => {
    switch (intervention.pattern) {
      case "dorsal-shutdown":
        return <Heart className="h-8 w-8 text-blue-500" />;
      case "sympathetic-peak":
        return <Wind className="h-8 w-8 text-orange-500" />;
      case "deadline-nudge":
        return <CheckCircle2 className="h-8 w-8 text-purple-500" />;
      case "ventral-mastery":
        return <Sparkles className="h-8 w-8 text-green-500" />;
    }
  };

  const getBackgroundColor = () => {
    switch (intervention.pattern) {
      case "dorsal-shutdown":
        return "from-blue-50 to-blue-100";
      case "sympathetic-peak":
        return "from-orange-50 to-orange-100";
      case "deadline-nudge":
        return "from-purple-50 to-purple-100";
      case "ventral-mastery":
        return "from-green-50 to-green-100";
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div
        className={`bg-gradient-to-br ${getBackgroundColor()} rounded-lg shadow-2xl max-w-md w-full p-6 relative`}
      >
        {/* Close button - Port 1: Cognitive Sovereignty */}
        <button
          onClick={onDismiss}
          className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 transition-colors"
          aria-label="Lukk"
        >
          <X className="h-6 w-6" />
        </button>

        {/* Icon */}
        <div className="flex items-center justify-center mb-4">
          {getIcon()}
        </div>

        {/* Title */}
        <h2 className="text-2xl font-bold text-[var(--color-text-primary)] text-center mb-3">
          {intervention.suggestion.title}
        </h2>

        {/* Message - Port 2: Shame-free NVC language */}
        <p className="text-base text-[var(--color-text-secondary)] text-center mb-6">
          {intervention.suggestion.message}
        </p>

        {/* Confidence indicator - Epistemic Humility */}
        <div className="mb-6">
          <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
            <span>Tillit til dette forslaget:</span>
            <span className="font-semibold">
              {Math.round(intervention.confidence * 100)}%
            </span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-500 rounded-full transition-all"
              style={{ width: `${intervention.confidence * 100}%` }}
            />
          </div>
        </div>

        {/* Actions */}
        <div className="space-y-3">
          <Button
            variant="primary"
            size="large"
            onClick={onAccept}
            className="w-full"
          >
            {intervention.suggestion.actionLabel}
          </Button>

          <Button
            variant="secondary"
            size="large"
            onClick={onDismiss}
            className="w-full"
          >
            Nei takk, jeg fortsetter
          </Button>
        </div>

        {/* Ethical Note - Port 1 & 3 compliance */}
        <div className="mt-6 p-3 bg-white bg-opacity-60 rounded-lg border border-gray-300">
          <p className="text-xs text-gray-700 text-center">
            <strong>Du bestemmer:</strong> {intervention.ethicalNote}
          </p>
        </div>
      </div>
    </div>
  );
}

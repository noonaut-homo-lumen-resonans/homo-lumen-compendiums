"use client";

import React, { useState } from "react";
import { BigFive } from "@/types";
import { getAuraConfig, getPersonalityDescription } from "@/utils/personalityMapping";
import PersonalityModal from "./PersonalityModal";

interface PersonalityAvatarProps {
  bigFive?: BigFive;
  polyvagalState?: "ventral" | "sympathetic" | "dorsal";
  size?: "small" | "medium" | "large"; // 60px, 120px, 180px
  interactive?: boolean;
  showLabel?: boolean;
  onEdit?: () => void;
  className?: string;
}

/**
 * PersonalityAvatar Component
 *
 * Visual representation of Big Five personality traits as an abstract animated orb.
 *
 * Structure:
 * - Layer 1: Aura (colored glow based on dominant trait)
 * - Layer 2: Core circle (solid color, no face)
 * - Layer 3: Animations (breathing, hover, float)
 * - Text: Expanded personality description
 *
 * Design principles:
 * - Abstract, non-anthropomorphic (no facial features)
 * - Polyvagal-safe: Calm, breathing animations (4-6-8 rhythm)
 * - Rich textual description of personality traits
 * - Interactive: Click for details, hover for tooltip
 * - Accessible: Keyboard navigable, ARIA labels
 *
 * Triadisk Score: 0.12 (PROCEED - Empowering visualization)
 */
export default function PersonalityAvatar({
  bigFive,
  polyvagalState = "ventral",
  size = "medium",
  interactive = false,
  showLabel = false,
  onEdit,
  className = "",
}: PersonalityAvatarProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [showModal, setShowModal] = useState(false);

  // If no bigFive data, show placeholder
  if (!bigFive) {
    return (
      <div className={`flex flex-col items-center ${className}`}>
        <div
          className={`relative ${getSizeClass(size)} flex items-center justify-center`}
        >
          <div className="w-full h-full rounded-full bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400 text-2xl">?</span>
          </div>
        </div>
        {showLabel && (
          <p className="mt-2 text-xs text-gray-500 text-center">
            Ingen personlighetsdata
          </p>
        )}
      </div>
    );
  }

  const auraConfig = getAuraConfig(bigFive, polyvagalState);
  const description = getPersonalityDescription(bigFive);

  const handleClick = () => {
    if (!interactive) return;
    setShowModal(true);
  };

  return (
    <>
      <div className={`flex flex-col items-center ${className}`}>
        {/* Avatar Container */}
        <div
          className={`relative ${getSizeClass(size)} cursor-pointer transition-transform duration-300 ${
            isHovered && interactive ? "scale-105" : ""
          }`}
          onClick={handleClick}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          role={interactive ? "button" : undefined}
          tabIndex={interactive ? 0 : undefined}
          aria-label={interactive ? "Åpne personlighetsprofil" : "Personlighetsavatar"}
          onKeyDown={(e) => {
            if (interactive && (e.key === "Enter" || e.key === " ")) {
              e.preventDefault();
              handleClick();
            }
          }}
        >
          {/* Aura Layer (Outer glow) */}
          <div
            className="absolute inset-0 rounded-full"
            style={{
              background: `radial-gradient(circle, ${auraConfig.primaryColor}40, ${auraConfig.secondaryColor}20)`,
              filter: `blur(${auraConfig.blur}px)`,
              transform: `scale(${auraConfig.radius})`,
              borderRadius: `${auraConfig.irregularity}%`,
              animation: `breathe-aura ${auraConfig.animationDuration}s ease-in-out infinite, float 3s ease-in-out infinite`,
            }}
          />

          {/* Core circle (no face, just color) */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div
              className="w-3/5 h-3/5 rounded-full"
              style={{
                backgroundColor: auraConfig.primaryColor,
                opacity: 0.9,
                filter: "drop-shadow(0 2px 4px rgba(0,0,0,0.1))",
              }}
            />
          </div>

          {/* Hover tooltip */}
          {isHovered && interactive && (
            <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 bg-black text-white text-xs px-3 py-2 rounded shadow-lg whitespace-nowrap z-10 pointer-events-none">
              Klikk for detaljer
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-full w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-black"></div>
            </div>
          )}
        </div>

        {/* Label */}
        {showLabel && (
          <div className="mt-3 w-full px-2">
            <p className="text-sm font-semibold text-[var(--color-text-primary)] mb-2 text-center">
              Din personlighet
            </p>
            <p className="text-xs text-[var(--color-text-secondary)] leading-relaxed">
              {description}
            </p>
          </div>
        )}
      </div>

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes breathe-aura {
          0% {
            transform: scale(${auraConfig.radius}) translateY(0px);
            opacity: 0.6;
          }
          22% {
            transform: scale(${auraConfig.radius * 1.1}) translateY(0px);
            opacity: 0.8;
          }
          55% {
            transform: scale(${auraConfig.radius * 1.1}) translateY(0px);
            opacity: 0.8;
          }
          100% {
            transform: scale(${auraConfig.radius}) translateY(0px);
            opacity: 0.6;
          }
        }

        @keyframes float {
          0%,
          100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-5px);
          }
        }
      `}</style>

      {/* Modal */}
      {showModal && (
        <PersonalityModal
          bigFive={bigFive}
          polyvagalState={polyvagalState}
          onClose={() => setShowModal(false)}
          onEdit={onEdit}
        />
      )}
    </>
  );
}

/**
 * Get size class based on size prop
 */
function getSizeClass(size: "small" | "medium" | "large"): string {
  const sizes = {
    small: "w-16 h-16", // 64px
    medium: "w-32 h-32", // 128px
    large: "w-48 h-48", // 192px
  };

  return sizes[size];
}

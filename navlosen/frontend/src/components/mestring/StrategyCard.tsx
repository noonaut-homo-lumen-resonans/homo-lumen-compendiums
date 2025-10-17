"use client";

import React, { useState } from "react";
import { cn } from "@/lib/utils";
import { Strategy } from "@/types";
import { ChevronDown, ChevronUp, Clock } from "lucide-react";
import Button from "../ui/Button";
import Link from "next/link";

interface StrategyCardProps {
  strategy: Strategy;
  className?: string;
  compact?: boolean; // Compact mode for high stress states
}

/**
 * StrategyCard Component
 *
 * Displays regulation strategy with expandable details
 * Each strategy is mapped to a stress state (ventral/sympathetic/dorsal)
 *
 * Strategies:
 * - Breathing (4-6-8): All states
 * - Grounding (5-4-3-2-1): Sympathetic, Dorsal
 * - Small action: Sympathetic
 * - Progressive relaxation: Ventral
 *
 * @example
 * <StrategyCard strategy={breathingStrategy} />
 */
export default function StrategyCard({
  strategy,
  className,
  compact = false,
}: StrategyCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Map strategy IDs to exercise pages
  const exerciseMap: Record<string, string> = {
    "breathing-468": "/ovelser/pust-468",
    "grounding-54321": "/ovelser/grounding-54321",
    // Add more mappings as we build more exercises
  };

  const exerciseLink = exerciseMap[strategy.id] || null;

  const getStateColor = () => {
    switch (strategy.stressState) {
      case "ventral":
        return "bg-green-50 border-green-200";
      case "sympathetic":
        return "bg-orange-50 border-orange-200";
      case "dorsal":
        return "bg-blue-50 border-blue-200";
    }
  };

  const getStateBadge = () => {
    switch (strategy.stressState) {
      case "ventral":
        return "bg-green-100 text-green-700";
      case "sympathetic":
        return "bg-orange-100 text-orange-700";
      case "dorsal":
        return "bg-blue-100 text-blue-700";
    }
  };

  // Compact mode: Always show full description and button, no expand/collapse
  if (compact) {
    return (
      <div
        className={cn(
          "border-2 rounded-lg p-5 transition-all duration-200 text-left",
          getStateColor(),
          className
        )}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <h4 className="text-xl font-bold text-[var(--color-text-primary)] text-left">
            {strategy.title}
          </h4>
        </div>

        {/* Duration */}
        <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)] mb-4">
          <Clock className="h-4 w-4" />
          <span className="font-medium">{strategy.duration}</span>
        </div>

        {/* Action button - prominent */}
        {exerciseLink ? (
          <Link href={exerciseLink}>
            <Button variant="primary" size="large" className="w-full text-lg py-4">
              Start øvelse nå
            </Button>
          </Link>
        ) : (
          <Button variant="primary" size="large" className="w-full text-lg py-4" disabled>
            Kommer snart
          </Button>
        )}
      </div>
    );
  }

  // Full mode: Expandable with details
  return (
    <div
      className={cn(
        "border-2 rounded-lg p-5 transition-all duration-200 text-left",
        getStateColor(),
        className
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h4 className="text-lg font-semibold text-[var(--color-text-primary)] text-left">
          {strategy.title}
        </h4>
        <span
          className={cn(
            "text-xs font-semibold px-2 py-1 rounded-full",
            getStateBadge()
          )}
        >
          {strategy.stressState === "ventral"
            ? "Rolig"
            : strategy.stressState === "sympathetic"
            ? "Aktivert"
            : "Overveldet"}
        </span>
      </div>

      {/* Duration */}
      <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)] mb-3">
        <Clock className="h-4 w-4" />
        <span>{strategy.duration}</span>
      </div>

      {/* Description preview */}
      <p className="text-sm text-[var(--color-text-primary)] mb-4">
        {isExpanded
          ? strategy.description
          : `${strategy.description.slice(0, 100)}...`}
      </p>

      {/* Expand/Collapse button */}
      <Button
        variant="text"
        size="small"
        onClick={() => setIsExpanded(!isExpanded)}
        rightIcon={
          isExpanded ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )
        }
        className="mb-3"
      >
        {isExpanded ? "Vis mindre" : "Vis mer"}
      </Button>

      {/* Action button */}
      <div
        className={cn(
          "overflow-hidden transition-all duration-300",
          isExpanded ? "max-h-20 opacity-100 mt-3" : "max-h-0 opacity-0"
        )}
      >
        {exerciseLink ? (
          <Link href={exerciseLink}>
            <Button variant="primary" size="medium" className="w-full">
              Start øvelse
            </Button>
          </Link>
        ) : (
          <Button variant="primary" size="medium" className="w-full" disabled>
            Kommer snart
          </Button>
        )}
      </div>
    </div>
  );
}

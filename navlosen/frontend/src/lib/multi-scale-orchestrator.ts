/**
 * MULTI-SCALE ORCHESTRATOR
 *
 * Central coordinator for L1-L5 Multi-Scale Memory Architecture
 *
 * This orchestrator provides unified access to all 5 layers:
 * - L1: Immediate Context (current user state)
 * - L2: Project Knowledge (static design system)
 * - L3: Living Compendium (dynamic learnings)
 * - L4: External Knowledge (NotebookLM, Google Drive)
 * - L5: KÄRNFELT (frequency coordination)
 *
 * Based on Multi-Scale Architecture (LP #014)
 *
 * Usage:
 * ```ts
 * const orchestrator = new MultiScaleOrchestrator();
 * const context = orchestrator.synthesize("coding");
 * ```
 */

import {
  getCurrentContext,
  ImmediateContext,
} from "./l1-immediate-context";
import {
  getProjectKnowledge,
  getPolyvagalState,
  ProjectKnowledge,
  PolyvagalState,
} from "./l2-project-knowledge";
import {
  getClaudeCodeCompendium,
  getLearningPoint,
  AgentCompendium,
} from "./l3-living-compendium";
import {
  requestL4Validation,
  shouldUseL4Protocol,
  L4ValidationRequest,
  L4ValidationResponse,
} from "./l4-external-knowledge";
import {
  getCodeFrequency,
  getCollaboratingAgent,
  FrequencyRange,
  FrequencyBand,
} from "./l5-kaernfelt";

/**
 * Synthesized multi-scale context
 */
export interface MultiScaleContext {
  // L1: What's happening NOW
  immediate: ImmediateContext;

  // L2: Static knowledge
  projectKnowledge: ProjectKnowledge;
  polyvagalState: PolyvagalState | null;

  // L3: Dynamic learnings
  compendium: AgentCompendium;
  relevantLearnings: string[]; // LP IDs

  // L4: External validation (if needed)
  l4Required: boolean;

  // L5: Frequency coordination
  frequency: FrequencyRange;
  collaboratingAgents: string[];

  // Synthesis
  timestamp: Date;
}

/**
 * Multi-Scale Orchestrator
 */
export class MultiScaleOrchestrator {
  /**
   * Synthesize context across all 5 layers
   */
  synthesize(taskType: string = "coding"): MultiScaleContext {
    // L1: Get immediate context
    const immediate = getCurrentContext();

    // L2: Get project knowledge and polyvagal state
    const projectKnowledge = getProjectKnowledge();
    const polyvagalState = getPolyvagalState(immediate.stressLevel);

    // L3: Get compendium and relevant learnings
    const compendium = getClaudeCodeCompendium();
    const relevantLearnings = this.getRelevantLearnings(
      taskType,
      immediate.polyvagalState
    );

    // L4: Check if L4 protocol required
    const l4Required = shouldUseL4Protocol({
      type: this.categorizeTask(taskType),
      impactDays: this.estimateImpact(taskType),
    });

    // L5: Get frequency coordination
    const frequency = getCodeFrequency(taskType);
    const collaboratingAgents = getCollaboratingAgent(taskType);

    return {
      immediate,
      projectKnowledge,
      polyvagalState,
      compendium,
      relevantLearnings,
      l4Required,
      frequency,
      collaboratingAgents,
      timestamp: new Date(),
    };
  }

  /**
   * Request L4 validation for major decision
   */
  async requestExternalValidation(
    decision: string,
    context: string,
    findings: string[]
  ): Promise<L4ValidationResponse> {
    const request: L4ValidationRequest = {
      decision,
      context,
      findings,
      timestamp: new Date(),
    };

    return await requestL4Validation(request);
  }

  /**
   * Get relevant learning points based on task and state
   */
  private getRelevantLearnings(
    taskType: string,
    polyvagalState: ImmediateContext["polyvagalState"]
  ): string[] {
    const learnings: string[] = [];

    // Always relevant
    learnings.push("LP #002"); // Pattern-Matching > Approximation

    // Task-specific
    if (taskType.includes("cache") || taskType.includes("error")) {
      learnings.push("LP #001"); // Next.js Cache Invalidation
    }

    if (taskType.includes("design") || taskType.includes("ui")) {
      learnings.push("EI #001"); // Polyvagal-Informed Design
    }

    // State-specific
    if (polyvagalState === "dorsal" || polyvagalState === "sympathetic") {
      learnings.push("LP #010"); // Lira-filter (empathy-first)
    }

    // Architecture-related
    if (
      taskType.includes("architecture") ||
      taskType.includes("decision") ||
      taskType.includes("planning")
    ) {
      learnings.push("LP #013"); // 5 Skalaer
      learnings.push("LP #014"); // L1-L5 Architecture
    }

    return learnings;
  }

  /**
   * Categorize task type
   */
  private categorizeTask(
    taskType: string
  ): "architectural" | "strategic" | "tactical" {
    const architectural = [
      "architecture",
      "framework",
      "migration",
      "redesign",
    ];
    const strategic = ["feature", "planning", "decision", "design"];

    if (architectural.some((keyword) => taskType.includes(keyword))) {
      return "architectural";
    }
    if (strategic.some((keyword) => taskType.includes(keyword))) {
      return "strategic";
    }
    return "tactical";
  }

  /**
   * Estimate impact in days
   */
  private estimateImpact(taskType: string): number {
    // Simple heuristic - in production, could be more sophisticated
    if (taskType.includes("architecture")) return 30;
    if (taskType.includes("feature")) return 14;
    if (taskType.includes("design")) return 7;
    if (taskType.includes("bug") || taskType.includes("fix")) return 1;
    return 3; // Default
  }

  /**
   * Log synthesis (for debugging)
   */
  logSynthesis(context: MultiScaleContext): void {
    if (process.env.NODE_ENV === "development") {
      console.log("[Multi-Scale Orchestrator] Context Synthesis:", {
        route: context.immediate.currentRoute,
        polyvagalState: context.immediate.polyvagalState,
        stressLevel: context.immediate.stressLevel,
        frequency: `${context.frequency.band} (${context.frequency.minHz}-${context.frequency.maxHz} Hz)`,
        collaboratingAgents: context.collaboratingAgents,
        l4Required: context.l4Required,
        relevantLearnings: context.relevantLearnings,
        timestamp: context.timestamp.toISOString(),
      });
    }
  }
}

/**
 * Singleton instance
 */
export const orchestrator = new MultiScaleOrchestrator();

/**
 * Convenience function for quick synthesis
 */
export function synthesizeContext(taskType: string = "coding"): MultiScaleContext {
  return orchestrator.synthesize(taskType);
}

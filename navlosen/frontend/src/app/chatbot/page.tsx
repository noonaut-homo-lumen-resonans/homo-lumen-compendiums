"use client";

import React from "react";
import Layout from "@/components/layout/Layout";
import ChatbotInterface from "@/components/chatbot/ChatbotInterface";
import { MessageCircle } from "lucide-react";

/**
 * Lira Page - Empatisk AI-veileder for NAV
 *
 * Chat med Lira (GPT-4 via CSN Server) som forstår din emosjonelle tilstand
 * og tilpasser veiledningen basert på Mestring-data (stress, emosjoner, kropp).
 *
 * Features:
 * - Real-time GPT-4 responses via ama-backend CSN Server
 * - Polyvagal-adaptive quick actions (based on biofield context)
 * - Empathetic NAV guidance with Lira's personality
 * - Integration with Mestring biofield data (stress, emotions, somatic signals)
 * - Multi-modal input: text, voice, camera, emotion selection
 *
 * Triadisk Score: 0.2 (PROCEED)
 * - Port 1 (Suverenitet): Clear AI disclaimer, user controls conversation
 * - Port 2 (Koherens): Consistent with Lira's empathetic tone
 * - Port 3 (Healing): Teaches concepts, links to Mestring tools
 */
export default function ChatbotPage() {
  return (
    <Layout>
      <div className="w-full">
        {/* Page Header */}
        <div className="mb-8">
          {/* Breadcrumb */}
          <div className="mb-4 text-sm text-[var(--color-text-secondary)]">
            <span>NAV-Losen</span>
            <span className="mx-2">/</span>
            <span className="text-[var(--color-text-primary)] font-medium">
              Lira
            </span>
          </div>

          <div className="flex items-center gap-3 mb-2">
            <MessageCircle className="h-8 w-8 text-purple-500" />
            <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
              Chat med Lira
            </h1>
          </div>
          <p className="text-lg text-[var(--color-text-secondary)]">
            Din empatiske AI-veileder som forstår hvordan du har det. Jeg kan forklare
            NAV-begreper, foreslå neste steg og peke deg til riktige skjema - tilpasset
            din emosjonelle tilstand.
          </p>
        </div>

        {/* Chatbot Interface */}
        <ChatbotInterface />
      </div>
    </Layout>
  );
}

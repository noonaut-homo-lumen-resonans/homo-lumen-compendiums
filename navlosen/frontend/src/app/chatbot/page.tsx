"use client";

import React from "react";
import Layout from "@/components/layout/Layout";
import ChatbotInterface from "@/components/chatbot/ChatbotInterface";
import { MessageCircle } from "lucide-react";

/**
 * Chatbot Page - Lira NAV-Losen Chatbot
 *
 * Standalone chat interface with Lira (GPT-4 via CSN Server)
 * for empathetic NAV guidance and biofield-responsive support.
 *
 * Features:
 * - Real-time GPT-4 responses via ama-backend CSN Server
 * - Polyvagal-adaptive quick actions (if biofield context available)
 * - Empathetic NAV guidance with Lira's personality
 * - Integration with Mestring biofield data (optional)
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
              Chatbot
            </span>
          </div>

          <div className="flex items-center gap-3 mb-2">
            <MessageCircle className="h-8 w-8 text-purple-500" />
            <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
              Chatbot
            </h1>
          </div>
          <p className="text-lg text-[var(--color-text-secondary)]">
            Chat med Lira - din empatiske AI-veileder. Jeg kan forklare
            begreper, foreslå neste steg og peke deg til riktige skjema.
          </p>
        </div>

        {/* Chatbot Interface */}
        <ChatbotInterface />
      </div>
    </Layout>
  );
}

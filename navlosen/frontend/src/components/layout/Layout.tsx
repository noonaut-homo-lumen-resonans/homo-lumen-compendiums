"use client";

import React, { useState } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import Header from "./Header";
import Sidebar from "./Sidebar";
import { MessageSquare } from "lucide-react";

interface LayoutProps {
  children: React.ReactNode;
  className?: string;
}

/**
 * Layout Component
 *
 * Main layout wrapper for NAV-Losen
 * Based on Design System v1.0
 *
 * Structure:
 * - Header (fixed top, 64px)
 * - Sidebar (240px desktop, overlay mobile)
 * - Main content area
 * - Floating chatbot button (bottom right)
 *
 * @example
 * <Layout>
 *   <YourPageContent />
 * </Layout>
 */
export default function Layout({ children, className }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col h-screen bg-[var(--color-bg-secondary)]">
      {/* Header */}
      <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main layout: Sidebar + Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

        {/* Main content */}
        <main
          className={cn(
            "flex-1 overflow-y-auto",
            "p-4 md:p-6 lg:p-8",
            "max-w-7xl mx-auto w-full",
            className
          )}
        >
          {children}

          {/* Footer disclaimer */}
          <footer className="mt-8 p-4 bg-white rounded-lg shadow-[var(--shadow-sm)] text-center text-sm text-[var(--color-text-secondary)]">
            <p>
              <strong>Viktig:</strong> NAV-Losen er et verktøy for å hjelpe deg
              med NAV-systemet. AI-generert innhold kan inneholde feil. Ved
              tvil, kontakt en menneskelig veileder eller besøk{" "}
              <a
                href="https://www.nav.no"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[var(--color-primary)] underline hover:text-[#0056A3]"
              >
                nav.no
              </a>
              .
            </p>
          </footer>
        </main>
      </div>

      {/* Floating chatbot button */}
      <Link
        href="/chatbot"
        className={cn(
          "fixed bottom-6 right-6 z-30",
          "bg-[var(--color-secondary)] hover:bg-[#05A7BD] text-white",
          "font-semibold py-3 px-4 rounded-full",
          "shadow-[var(--shadow-lg)]",
          "flex items-center gap-2",
          "transition-transform duration-200 hover:scale-105",
          "focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-secondary)]"
        )}
        aria-label="Snakk med Lira chatbot"
      >
        <MessageSquare className="h-6 w-6" />
        <span className="hidden sm:inline">Snakk med veileder</span>
      </Link>
    </div>
  );
}

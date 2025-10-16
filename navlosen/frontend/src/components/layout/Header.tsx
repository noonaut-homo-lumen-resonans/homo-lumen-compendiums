"use client";

import React from "react";
import { cn } from "@/lib/utils";
import { UserCircle, Menu } from "lucide-react";

interface HeaderProps {
  onMenuToggle?: () => void;
  className?: string;
}

/**
 * Header Component
 *
 * Fixed top navigation bar for NAV-Losen
 * Based on Design System v1.0
 *
 * Features:
 * - NAV Blue background (#0067C5)
 * - 64px height
 * - Fixed position on scroll
 * - Responsive: Hamburger menu on mobile
 *
 * @example
 * <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
 */
export default function Header({ onMenuToggle, className }: HeaderProps) {
  return (
    <header
      className={cn(
        "h-16 bg-[var(--color-primary)] text-white",
        "flex items-center justify-between px-4 md:px-6",
        "shadow-[var(--shadow-sm)]",
        "sticky top-0 z-50",
        className
      )}
    >
      {/* Left side: Logo and menu */}
      <div className="flex items-center gap-4">
        {/* Mobile menu button */}
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 hover:bg-white/10 rounded transition-colors"
          aria-label="Åpne meny"
        >
          <Menu className="h-6 w-6" />
        </button>

        {/* Logo */}
        <h1 className="text-xl md:text-2xl font-bold">NAV-Losen</h1>
      </div>

      {/* Right side: Language switcher and user */}
      <div className="flex items-center gap-4">
        {/* Language switcher */}
        <button
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 hover:bg-white/10 rounded transition-colors text-sm"
          aria-label="Bytt språk"
        >
          <span>Bokmål</span>
        </button>

        {/* User menu */}
        <div className="flex items-center gap-2">
          <span className="hidden sm:inline text-sm">
            Velkommen, Bruker (Mock)
          </span>
          <UserCircle className="h-8 w-8" />
        </div>
      </div>
    </header>
  );
}

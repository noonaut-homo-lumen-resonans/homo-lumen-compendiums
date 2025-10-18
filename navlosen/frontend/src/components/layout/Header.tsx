"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { UserCircle, ChevronDown, Home, BookOpen, Lightbulb, Heart, Compass, Briefcase, MessageSquare, FileText, Bell, Scale, Settings } from "lucide-react";

interface HeaderProps {
  className?: string;
}

interface NavItem {
  id: string;
  label: string;
  icon: string;
  path: string;
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
 * - Dropdown navigation menu on logo click
 *
 * @example
 * <Header onMenuToggle={() => setSidebarOpen(!sidebarOpen)} />
 */
export default function Header({ className }: HeaderProps) {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const pathname = usePathname();

  const navItems: NavItem[] = [
    { id: "dashboard", label: "Dashboard", icon: "home", path: "/" },
    { id: "veiledninger", label: "Veiledninger", icon: "book", path: "/veiledninger" },
    { id: "forklar-brev", label: "Forklar brev", icon: "lightbulb", path: "/forklar-brev" },
    { id: "mestring", label: "Mestring", icon: "heart", path: "/mestring" },
    { id: "min-reise", label: "Min Reise", icon: "compass", path: "/min-reise" },
    { id: "jobb", label: "Jobb", icon: "briefcase", path: "/jobb" },
    { id: "chatbot", label: "Chatbot", icon: "chat", path: "/chatbot" },
    { id: "dokumenter", label: "Dokumenter", icon: "file", path: "/dokumenter" },
    { id: "paminnelser", label: "Påminnelser", icon: "bell", path: "/paminnelser" },
    { id: "rettigheter", label: "Rettigheter", icon: "scale", path: "/rettigheter" },
    { id: "innstillinger", label: "Innstillinger", icon: "settings", path: "/innstillinger" },
  ];

  const getIcon = (iconName: string) => {
    const iconClass = "h-5 w-5";
    switch (iconName) {
      case "home": return <Home className={iconClass} />;
      case "book": return <BookOpen className={iconClass} />;
      case "lightbulb": return <Lightbulb className={iconClass} />;
      case "heart": return <Heart className={iconClass} />;
      case "compass": return <Compass className={iconClass} />;
      case "briefcase": return <Briefcase className={iconClass} />;
      case "chat": return <MessageSquare className={iconClass} />;
      case "file": return <FileText className={iconClass} />;
      case "bell": return <Bell className={iconClass} />;
      case "scale": return <Scale className={iconClass} />;
      case "settings": return <Settings className={iconClass} />;
      default: return null;
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    if (dropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownOpen]);

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
      <div className="flex items-center gap-4 relative" ref={dropdownRef}>
        {/* Logo with dropdown */}
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="flex items-center gap-2 p-2 hover:bg-white/10 rounded transition-colors"
          aria-label="Åpne navigasjonsmeny"
        >
          <h1 className="text-xl md:text-2xl font-bold">NAV-Losen</h1>
          <ChevronDown className={cn("h-5 w-5 transition-transform duration-200", dropdownOpen && "rotate-180")} />
        </button>

        {/* Dropdown menu */}
        {dropdownOpen && (
          <div className="absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden">
            <nav className="py-2">
              {navItems.map((item) => {
                const isActive = pathname === item.path;
                return (
                  <Link
                    key={item.id}
                    href={item.path}
                    onClick={() => setDropdownOpen(false)}
                    className={cn(
                      "flex items-center gap-3 px-4 py-3",
                      "text-base font-medium transition-colors duration-200",
                      "hover:bg-gray-100",
                      {
                        "bg-[var(--color-primary)] text-white hover:bg-[#0056A3]": isActive,
                        "text-[var(--color-text-primary)]": !isActive,
                      }
                    )}
                  >
                    {getIcon(item.icon)}
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        )}
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

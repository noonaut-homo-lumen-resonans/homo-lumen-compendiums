"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { NavItem } from "@/types";
import {
  Home,
  BookOpen,
  Lightbulb,
  Heart,
  Briefcase,
  MessageSquare,
  FileText,
  Bell,
  Scale,
  Settings,
  X,
} from "lucide-react";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

/**
 * Sidebar Component
 *
 * Left navigation menu for NAV-Losen
 * Based on Design System v1.0
 *
 * Features:
 * - 240px width (desktop)
 * - Light gray background (#F5F5F5)
 * - 10 navigation items
 * - Active state highlighting
 * - Responsive: Overlay on mobile
 *
 * @example
 * <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
 */
export default function Sidebar({ isOpen, onClose, className }: SidebarProps) {
  const pathname = usePathname();

  const navItems: NavItem[] = [
    { id: "dashboard", label: "Dashboard", icon: "home", path: "/" },
    {
      id: "veiledninger",
      label: "Veiledninger",
      icon: "book",
      path: "/veiledninger",
    },
    {
      id: "forklar-brev",
      label: "Forklar brev",
      icon: "lightbulb",
      path: "/forklar-brev",
    },
    { id: "mestring", label: "Mestring", icon: "heart", path: "/mestring" },
    { id: "jobb", label: "Jobb", icon: "briefcase", path: "/jobb" },
    { id: "chatbot", label: "Chatbot", icon: "chat", path: "/chatbot" },
    {
      id: "dokumenter",
      label: "Dokumenter",
      icon: "file",
      path: "/dokumenter",
    },
    {
      id: "paminnelser",
      label: "Påminnelser",
      icon: "bell",
      path: "/paminnelser",
    },
    {
      id: "rettigheter",
      label: "Rettigheter",
      icon: "scale",
      path: "/rettigheter",
    },
    {
      id: "innstillinger",
      label: "Innstillinger",
      icon: "settings",
      path: "/innstillinger",
    },
  ];

  const getIcon = (iconName: string) => {
    const iconClass = "h-5 w-5";
    switch (iconName) {
      case "home":
        return <Home className={iconClass} />;
      case "book":
        return <BookOpen className={iconClass} />;
      case "lightbulb":
        return <Lightbulb className={iconClass} />;
      case "heart":
        return <Heart className={iconClass} />;
      case "briefcase":
        return <Briefcase className={iconClass} />;
      case "chat":
        return <MessageSquare className={iconClass} />;
      case "file":
        return <FileText className={iconClass} />;
      case "bell":
        return <Bell className={iconClass} />;
      case "scale":
        return <Scale className={iconClass} />;
      case "settings":
        return <Settings className={iconClass} />;
      default:
        return null;
    }
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed lg:static inset-y-0 left-0 z-50",
          "w-60 bg-[var(--color-bg-secondary)]",
          "border-r border-[var(--color-bg-tertiary)]",
          "transform transition-transform duration-300 ease-in-out",
          "lg:transform-none",
          "flex flex-col",
          {
            "translate-x-0": isOpen,
            "-translate-x-full": !isOpen,
          },
          className
        )}
      >
        {/* Mobile close button */}
        <div className="lg:hidden flex items-center justify-between p-4 border-b border-[var(--color-bg-tertiary)]">
          <h2 className="text-lg font-semibold text-[var(--color-primary)]">
            Meny
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-200 rounded transition-colors"
            aria-label="Lukk meny"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-2">
          <ul className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.path;

              return (
                <li key={item.id}>
                  <Link
                    href={item.path}
                    onClick={() => {
                      // Close sidebar on mobile after clicking
                      if (window.innerWidth < 1024) {
                        onClose();
                      }
                    }}
                    className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-lg",
                      "text-base font-medium transition-colors duration-200",
                      "hover:bg-gray-200",
                      {
                        "bg-[var(--color-primary)] text-white hover:bg-[#0056A3]":
                          isActive,
                        "text-[var(--color-text-primary)]": !isActive,
                      }
                    )}
                  >
                    {getIcon(item.icon)}
                    <span>{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>
    </>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import Button from "../ui/Button";
import { BookOpen, Plus, Trash2, Edit2, Save, X } from "lucide-react";

/**
 * MasteryLog Component
 *
 * Port 3 (Regenerativ Healing): User saves their own strategies for independence
 *
 * Purpose:
 * - User records what works for them personally
 * - Builds self-awareness and mastery over time
 * - Creates graduation path (reduce system use as user becomes independent)
 *
 * Lira's Guidance (HOM-53):
 * "Mastery Log component (user saves their own strategies)
 * Self-compassion guidelines (not perfection)
 * Graduation dashboard (show reduced system use over time)"
 *
 * Triadisk Ethics:
 * - Port 1 (Suverenitet): User owns their strategies, can edit/delete anytime
 * - Port 2 (Koherens): Based on reflective practice and journaling research
 * - Port 3 (Healing): Builds capacity, creates path to independence
 *
 * Triadisk Score: -0.5 (STRONG HEALING - Port 3 focused)
 */

export interface MasteryEntry {
  id: string;
  date: string;
  strategy: string;
  context?: string; // What was happening?
  effectiveness?: number; // 1-5 scale (optional)
  tags?: string[]; // e.g., ["breathing", "anxiety", "work stress"]
}

export interface MasteryLogProps {
  onClose?: () => void;
  initialEntry?: Partial<MasteryEntry>;
}

export default function MasteryLog({
  onClose,
  initialEntry,
}: MasteryLogProps) {
  const [entries, setEntries] = useState<MasteryEntry[]>([]);
  const [isAdding, setIsAdding] = useState<boolean>(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Form state
  const [newStrategy, setNewStrategy] = useState<string>(initialEntry?.strategy || "");
  const [newContext, setNewContext] = useState<string>(initialEntry?.context || "");
  const [newEffectiveness, setNewEffectiveness] = useState<number>(
    initialEntry?.effectiveness || 3
  );
  const [newTags, setNewTags] = useState<string>(
    initialEntry?.tags?.join(", ") || ""
  );

  // Load entries from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedEntries = localStorage.getItem("navlosen-mastery-log");
      if (savedEntries) {
        try {
          setEntries(JSON.parse(savedEntries));
        } catch (e) {
          console.error("Failed to parse mastery log", e);
        }
      }
    }

    // Auto-open add form if initialEntry provided
    if (initialEntry) {
      setIsAdding(true);
    }
  }, [initialEntry]);

  // Save entries to localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen-mastery-log", JSON.stringify(entries));
    }
  }, [entries]);

  const handleAddEntry = () => {
    const entry: MasteryEntry = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      strategy: newStrategy,
      context: newContext || undefined,
      effectiveness: newEffectiveness,
      tags: newTags
        ? newTags.split(",").map((t) => t.trim()).filter(Boolean)
        : undefined,
    };

    setEntries((prev) => [entry, ...prev]);
    resetForm();
    setIsAdding(false);
  };

  const handleUpdateEntry = (id: string) => {
    setEntries((prev) =>
      prev.map((entry) =>
        entry.id === id
          ? {
              ...entry,
              strategy: newStrategy,
              context: newContext || undefined,
              effectiveness: newEffectiveness,
              tags: newTags
                ? newTags.split(",").map((t) => t.trim()).filter(Boolean)
                : undefined,
            }
          : entry
      )
    );
    resetForm();
    setEditingId(null);
  };

  const handleDeleteEntry = (id: string) => {
    if (confirm("Er du sikker på at du vil slette denne strategien?")) {
      setEntries((prev) => prev.filter((entry) => entry.id !== id));
    }
  };

  const startEditing = (entry: MasteryEntry) => {
    setEditingId(entry.id);
    setNewStrategy(entry.strategy);
    setNewContext(entry.context || "");
    setNewEffectiveness(entry.effectiveness || 3);
    setNewTags(entry.tags?.join(", ") || "");
  };

  const cancelEditing = () => {
    setEditingId(null);
    resetForm();
  };

  const resetForm = () => {
    setNewStrategy("");
    setNewContext("");
    setNewEffectiveness(3);
    setNewTags("");
  };

  const formatDate = (isoString: string) => {
    const date = new Date(isoString);
    return date.toLocaleDateString("no-NO", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-2xl shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <BookOpen className="h-8 w-8 text-purple-600" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              Mestringslogg
            </h2>
            <p className="text-sm text-gray-600">
              Dine egne strategier som virker
            </p>
          </div>
        </div>
        {onClose && (
          <Button
            variant="text"
            size="medium"
            onClick={onClose}
            leftIcon={<X className="h-5 w-5" />}
          >
            Lukk
          </Button>
        )}
      </div>

      {/* Self-compassion reminder - Lira's guidance */}
      <div className="bg-purple-50 border-l-4 border-purple-400 p-4 mb-6 rounded">
        <p className="text-sm text-purple-800">
          💜 Husk: Dette handler ikke om perfeksjon. Noen strategier vil virke,
          andre vil ikke. Det er helt normalt. Dette er din logg, for deg.
        </p>
      </div>

      {/* Add new entry button */}
      {!isAdding && !editingId && (
        <Button
          variant="primary"
          size="medium"
          onClick={() => setIsAdding(true)}
          leftIcon={<Plus className="h-5 w-5" />}
          className="mb-6"
        >
          Legg til ny strategi
        </Button>
      )}

      {/* Add/Edit Form */}
      {(isAdding || editingId) && (
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 mb-6 shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {editingId ? "Rediger strategi" : "Ny strategi"}
          </h3>

          {/* Strategy input */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hva fungerte for deg? *
            </label>
            <textarea
              value={newStrategy}
              onChange={(e) => setNewStrategy(e.target.value)}
              placeholder="F.eks: 'Tok 3 dype pust når jeg kjente panikk komme', '10 min gåtur i lunsj', 'Snakket med en venn'"
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          {/* Context (optional) */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hva skjedde? (valgfritt)
            </label>
            <textarea
              value={newContext}
              onChange={(e) => setNewContext(e.target.value)}
              placeholder="F.eks: 'Følt meg overveldet på jobb', 'Konflikt med kollega', 'Dårlig søvn natten før'"
              rows={2}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          {/* Effectiveness (optional) */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hvor godt fungerte det? (1-5)
            </label>
            <div className="flex gap-2">
              {[1, 2, 3, 4, 5].map((level) => (
                <button
                  key={level}
                  onClick={() => setNewEffectiveness(level)}
                  className={cn(
                    "w-12 h-12 rounded-full font-semibold transition-all",
                    newEffectiveness === level
                      ? "bg-gradient-to-r from-purple-500 to-pink-500 text-white scale-110"
                      : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                  )}
                >
                  {level}
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-1">
              1 = Hjalp litt, 5 = Hjalp mye
            </p>
          </div>

          {/* Tags (optional) */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Stikkord (valgfritt)
            </label>
            <input
              type="text"
              value={newTags}
              onChange={(e) => setNewTags(e.target.value)}
              placeholder="F.eks: angst, pust, arbeid, sosial (komma-separert)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button
              variant="primary"
              size="medium"
              onClick={() =>
                editingId ? handleUpdateEntry(editingId) : handleAddEntry()
              }
              disabled={!newStrategy.trim()}
              leftIcon={<Save className="h-5 w-5" />}
            >
              {editingId ? "Lagre endringer" : "Lagre strategi"}
            </Button>
            <Button
              variant="text"
              size="medium"
              onClick={() =>
                editingId ? cancelEditing() : setIsAdding(false)
              }
            >
              Avbryt
            </Button>
          </div>
        </div>
      )}

      {/* Entries list */}
      <div className="space-y-4">
        {entries.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-2">Ingen strategier ennå</p>
            <p className="text-sm text-gray-500">
              Når du finner noe som fungerer for deg, kan du lagre det her.
            </p>
          </div>
        ) : (
          entries.map((entry) => (
            <div
              key={entry.id}
              className="bg-white border-2 border-gray-200 rounded-xl p-5 hover:border-purple-300 transition-all"
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <p className="text-sm text-gray-500 mb-1">
                    {formatDate(entry.date)}
                  </p>
                  <p className="text-lg text-gray-900 font-medium">
                    {entry.strategy}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => startEditing(entry)}
                    className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-all"
                    title="Rediger"
                  >
                    <Edit2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteEntry(entry.id)}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                    title="Slett"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {entry.context && (
                <div className="mb-3">
                  <p className="text-sm text-gray-600 italic">
                    Situasjon: {entry.context}
                  </p>
                </div>
              )}

              {entry.effectiveness && (
                <div className="mb-3">
                  <div className="flex gap-1">
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className={cn(
                          "w-6 h-6 rounded-full",
                          i < entry.effectiveness!
                            ? "bg-gradient-to-r from-purple-400 to-pink-400"
                            : "bg-gray-200"
                        )}
                      />
                    ))}
                  </div>
                </div>
              )}

              {entry.tags && entry.tags.length > 0 && (
                <div className="flex gap-2 flex-wrap">
                  {entry.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Graduation insight - Port 3 */}
      {entries.length >= 5 && (
        <div className="mt-8 bg-gradient-to-r from-green-50 to-teal-50 border-2 border-green-300 rounded-xl p-6">
          <div className="flex items-start gap-4">
            <div className="text-4xl sprout-animation">🌱</div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Du bygger mestring! 🎉
              </h3>
              <p className="text-gray-700 mb-3">
                Du har {entries.length} strategier som fungerer for deg. Dette
                er tegn på at du lærer deg selv å kjenne og bygger din egen
                verktøykasse.
              </p>
              <p className="text-sm text-gray-600 italic">
                💡 Mål: Over tid, vil du trenge NAV-Losen mindre fordi du vet
                hva som fungerer for deg. Det er målet vårt – at du blir
                selvstendig og trygg i din egen mestring.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import GoogleSignIn from "@/components/auth/GoogleSignIn";
import { useGoogleAuth } from "@/contexts/GoogleAuthContext";
import {
  Bell,
  Plus,
  Calendar,
  Clock,
  Check,
  X,
  Edit2,
  Trash2,
  Filter,
  Search,
  ChevronDown,
  AlertCircle,
  CheckCircle,
  MessageCircle,
  RefreshCw,
} from "lucide-react";

type ReminderCategory = "Alle" | "Meldekort" | "Møter" | "Dokumenter" | "Søknader" | "Annet";
type ReminderPriority = "Lav" | "Middels" | "Høy";
type ReminderStatus = "Aktiv" | "Fullført" | "Forfalt";

interface Reminder {
  id: string;
  title: string;
  description: string;
  category: ReminderCategory;
  priority: ReminderPriority;
  dueDate: string;
  dueTime: string;
  status: ReminderStatus;
  notifyEmail: boolean;
  notifyPush: boolean;
  createdAt: string;
}

/**
 * Påminnelser Page
 *
 * Full-featured reminder management system
 */
export default function PaminnelserPage() {
  const router = useRouter();
  const { isAuthenticated, hasCalendarAccess, requestCalendarAccess } = useGoogleAuth();

  // Reminder state
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<ReminderCategory>("Alle");
  const [selectedPriority, setSelectedPriority] = useState<ReminderPriority | "Alle">("Alle");
  const [showCompleted, setShowCompleted] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  // Form state
  const [showForm, setShowForm] = useState(false);
  const [editingReminder, setEditingReminder] = useState<Reminder | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formCategory, setFormCategory] = useState<ReminderCategory>("Annet");
  const [formPriority, setFormPriority] = useState<ReminderPriority>("Middels");
  const [formDueDate, setFormDueDate] = useState("");
  const [formDueTime, setFormDueTime] = useState("09:00");
  const [formNotifyEmail, setFormNotifyEmail] = useState(false);
  const [formNotifyPush, setFormNotifyPush] = useState(true);

  // Load reminders from localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("navlosen_reminders");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          setReminders(parsed);
        } catch (err) {
          console.error("Failed to parse reminders:", err);
        }
      }
    }
  }, []);

  // Save reminders to localStorage
  useEffect(() => {
    if (typeof window !== "undefined" && reminders.length > 0) {
      localStorage.setItem("navlosen_reminders", JSON.stringify(reminders));
    }
  }, [reminders]);

  // Check for expired reminders
  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setReminders((prev) =>
        prev.map((reminder) => {
          if (reminder.status === "Aktiv") {
            const dueDateTime = new Date(`${reminder.dueDate}T${reminder.dueTime}`);
            if (dueDateTime < now) {
              return { ...reminder, status: "Forfalt" };
            }
          }
          return reminder;
        })
      );
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, []);

  // Filter reminders
  const filteredReminders = useMemo(() => {
    return reminders.filter((reminder) => {
      // Status filter
      if (!showCompleted && reminder.status === "Fullført") return false;

      // Category filter
      if (selectedCategory !== "Alle" && reminder.category !== selectedCategory) return false;

      // Priority filter
      if (selectedPriority !== "Alle" && reminder.priority !== selectedPriority) return false;

      // Search filter
      if (searchTerm.trim()) {
        const search = searchTerm.toLowerCase();
        return (
          reminder.title.toLowerCase().includes(search) ||
          reminder.description.toLowerCase().includes(search)
        );
      }

      return true;
    });
  }, [reminders, searchTerm, selectedCategory, selectedPriority, showCompleted]);

  // Sort reminders by due date
  const sortedReminders = useMemo(() => {
    return [...filteredReminders].sort((a, b) => {
      const dateA = new Date(`${a.dueDate}T${a.dueTime}`);
      const dateB = new Date(`${b.dueDate}T${b.dueTime}`);
      return dateA.getTime() - dateB.getTime();
    });
  }, [filteredReminders]);

  // Statistics
  const stats = useMemo(() => {
    const active = reminders.filter((r) => r.status === "Aktiv").length;
    const completed = reminders.filter((r) => r.status === "Fullført").length;
    const overdue = reminders.filter((r) => r.status === "Forfalt").length;
    return { active, completed, overdue };
  }, [reminders]);

  // Add or update reminder
  const handleSubmitReminder = () => {
    if (!formTitle.trim() || !formDueDate) {
      alert("Vennligst fyll ut tittel og forfallsdato");
      return;
    }

    if (editingReminder) {
      // Update existing
      setReminders((prev) =>
        prev.map((r) =>
          r.id === editingReminder.id
            ? {
                ...r,
                title: formTitle,
                description: formDescription,
                category: formCategory,
                priority: formPriority,
                dueDate: formDueDate,
                dueTime: formDueTime,
                notifyEmail: formNotifyEmail,
                notifyPush: formNotifyPush,
              }
            : r
        )
      );
    } else {
      // Add new
      const newReminder: Reminder = {
        id: Date.now().toString(),
        title: formTitle,
        description: formDescription,
        category: formCategory,
        priority: formPriority,
        dueDate: formDueDate,
        dueTime: formDueTime,
        status: "Aktiv",
        notifyEmail: formNotifyEmail,
        notifyPush: formNotifyPush,
        createdAt: new Date().toISOString(),
      };
      setReminders((prev) => [...prev, newReminder]);
    }

    // Reset form
    resetForm();
  };

  // Reset form
  const resetForm = () => {
    setShowForm(false);
    setEditingReminder(null);
    setFormTitle("");
    setFormDescription("");
    setFormCategory("Annet");
    setFormPriority("Middels");
    setFormDueDate("");
    setFormDueTime("09:00");
    setFormNotifyEmail(false);
    setFormNotifyPush(true);
  };

  // Edit reminder
  const handleEditReminder = (reminder: Reminder) => {
    setEditingReminder(reminder);
    setFormTitle(reminder.title);
    setFormDescription(reminder.description);
    setFormCategory(reminder.category);
    setFormPriority(reminder.priority);
    setFormDueDate(reminder.dueDate);
    setFormDueTime(reminder.dueTime);
    setFormNotifyEmail(reminder.notifyEmail);
    setFormNotifyPush(reminder.notifyPush);
    setShowForm(true);
  };

  // Delete reminder
  const handleDeleteReminder = (id: string) => {
    if (confirm("Er du sikker på at du vil slette denne påminnelsen?")) {
      setReminders((prev) => prev.filter((r) => r.id !== id));
    }
  };

  // Toggle reminder status
  const toggleReminderStatus = (id: string) => {
    setReminders((prev) =>
      prev.map((r) =>
        r.id === id
          ? { ...r, status: r.status === "Fullført" ? "Aktiv" : "Fullført" }
          : r
      )
    );
  };

  // Sync with Google Calendar
  const handleCalendarSync = async () => {
    if (!hasCalendarAccess) {
      await requestCalendarAccess();
      return;
    }

    setIsSyncing(true);

    // Simulate sync
    await new Promise((resolve) => setTimeout(resolve, 2000));

    setIsSyncing(false);

    alert(
      "Demo-modus: Google Calendar synkronisering\n\n" +
      `${reminders.filter(r => r.status === "Aktiv").length} påminnelser ble synkronisert til Google Calendar.\n\n` +
      "I produksjon ville dette:\n" +
      "• Opprette kalenderhendelser for hver påminnelse\n" +
      "• Legge til varsler basert på forfallsdato\n" +
      "• Holde endringer synkronisert begge veier\n" +
      "• Importere hendelser fra Google Calendar som påminnelser"
    );
  };

  // Format date
  const formatDate = (dateStr: string, timeStr: string): string => {
    const date = new Date(`${dateStr}T${timeStr}`);
    const now = new Date();
    const diffMs = date.getTime() - now.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "I dag";
    if (diffDays === 1) return "I morgen";
    if (diffDays === -1) return "I går";
    if (diffDays > 1 && diffDays <= 7) return `Om ${diffDays} dager`;
    if (diffDays < -1) return `${Math.abs(diffDays)} dager siden`;

    return date.toLocaleDateString("nb-NO", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  };

  // Priority color
  const getPriorityColor = (priority: ReminderPriority): string => {
    switch (priority) {
      case "Høy":
        return "text-red-600 bg-red-50";
      case "Middels":
        return "text-yellow-600 bg-yellow-50";
      case "Lav":
        return "text-green-600 bg-green-50";
    }
  };

  // Status color
  const getStatusColor = (status: ReminderStatus): string => {
    switch (status) {
      case "Aktiv":
        return "text-blue-600 bg-blue-50";
      case "Fullført":
        return "text-green-600 bg-green-50";
      case "Forfalt":
        return "text-red-600 bg-red-50";
    }
  };

  const categories: ReminderCategory[] = ["Alle", "Meldekort", "Møter", "Dokumenter", "Søknader", "Annet"];
  const priorities: (ReminderPriority | "Alle")[] = ["Alle", "Høy", "Middels", "Lav"];

  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-[var(--color-bg-primary)] to-[var(--color-bg-secondary)] py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
          {/* Breadcrumbs */}
          <div className="mb-6 text-sm text-[var(--color-text-secondary)]">
            <Link href="/" className="hover:text-[var(--color-brand-primary)]">
              NAV-Losen
            </Link>
            <span className="mx-2">/</span>
            <span className="text-[var(--color-text-primary)] font-medium">Påminnelser</span>
          </div>

          {/* Hero Section */}
          <div className="mb-8 text-center">
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-brand-primary)] shadow-lg">
                <Bell className="h-8 w-8 text-white" />
              </div>
            </div>
            <h1 className="mb-2 text-4xl font-bold text-[var(--color-text-primary)]">
              Påminnelser
            </h1>
            <p className="text-xl text-[var(--color-text-secondary)]">
              Hold oversikt over alle viktige frister og hendelser
            </p>
          </div>

          {/* Statistics */}
          <div className="mb-8 grid gap-4 sm:grid-cols-3">
            <div className="rounded-xl bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
                  <Clock className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.active}</p>
                  <p className="text-sm text-gray-600">Aktive påminnelser</p>
                </div>
              </div>
            </div>

            <div className="rounded-xl bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.completed}</p>
                  <p className="text-sm text-gray-600">Fullførte</p>
                </div>
              </div>
            </div>

            <div className="rounded-xl bg-white p-6 shadow-sm">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100">
                  <AlertCircle className="h-6 w-6 text-red-600" />
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">{stats.overdue}</p>
                  <p className="text-sm text-gray-600">Forfalte</p>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Card */}
          <div className="rounded-2xl bg-white shadow-lg">
            {/* Search and Actions */}
            <div className="border-b border-gray-200 p-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Søk etter påminnelser..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                  />
                </div>

                <Button
                  variant="primary"
                  size="medium"
                  leftIcon={<Plus className="h-5 w-5" />}
                  onClick={() => {
                    resetForm();
                    setShowForm(true);
                  }}
                >
                  Ny påminnelse
                </Button>
              </div>

              {/* Filters */}
              <div className="mt-4 flex flex-wrap gap-3">
                {/* Category Filter */}
                <div className="flex items-center gap-2">
                  <Filter className="h-4 w-4 text-gray-500" />
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value as ReminderCategory)}
                    className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                  >
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Priority Filter */}
                <select
                  value={selectedPriority}
                  onChange={(e) => setSelectedPriority(e.target.value as ReminderPriority | "Alle")}
                  className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                >
                  {priorities.map((pri) => (
                    <option key={pri} value={pri}>
                      {pri === "Alle" ? "Alle prioriteter" : `${pri} prioritet`}
                    </option>
                  ))}
                </select>

                {/* Show Completed Toggle */}
                <label className="flex items-center gap-2 rounded-lg border border-gray-300 px-3 py-1.5 text-sm">
                  <input
                    type="checkbox"
                    checked={showCompleted}
                    onChange={(e) => setShowCompleted(e.target.checked)}
                    className="rounded border-gray-300"
                  />
                  <span>Vis fullførte</span>
                </label>
              </div>
            </div>

            {/* Reminders List */}
            <div className="p-6">
              {sortedReminders.length === 0 ? (
                <div className="py-12 text-center">
                  <Bell className="mx-auto mb-4 h-12 w-12 text-gray-300" />
                  <h3 className="mb-2 text-lg font-semibold text-gray-900">
                    Ingen påminnelser
                  </h3>
                  <p className="mb-6 text-gray-600">
                    {searchTerm || selectedCategory !== "Alle" || selectedPriority !== "Alle"
                      ? "Ingen påminnelser matcher søket ditt"
                      : "Kom i gang ved å opprette din første påminnelse"}
                  </p>
                  {!searchTerm && selectedCategory === "Alle" && selectedPriority === "Alle" && (
                    <Button
                      variant="primary"
                      size="medium"
                      leftIcon={<Plus className="h-5 w-5" />}
                      onClick={() => {
                        resetForm();
                        setShowForm(true);
                      }}
                    >
                      Opprett påminnelse
                    </Button>
                  )}
                </div>
              ) : (
                <div className="space-y-3">
                  {sortedReminders.map((reminder) => (
                    <div
                      key={reminder.id}
                      className={`rounded-lg border p-4 transition-all hover:shadow-md ${
                        reminder.status === "Fullført"
                          ? "border-gray-200 bg-gray-50 opacity-60"
                          : "border-gray-200 bg-white"
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        {/* Checkbox */}
                        <button
                          onClick={() => toggleReminderStatus(reminder.id)}
                          className={`mt-1 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full border-2 transition-colors ${
                            reminder.status === "Fullført"
                              ? "border-green-500 bg-green-500"
                              : "border-gray-300 hover:border-[var(--color-brand-primary)]"
                          }`}
                        >
                          {reminder.status === "Fullført" && (
                            <Check className="h-4 w-4 text-white" />
                          )}
                        </button>

                        {/* Content */}
                        <div className="flex-1">
                          <div className="mb-2 flex flex-wrap items-start gap-2">
                            <h3
                              className={`text-lg font-semibold ${
                                reminder.status === "Fullført"
                                  ? "text-gray-500 line-through"
                                  : "text-gray-900"
                              }`}
                            >
                              {reminder.title}
                            </h3>
                            <span
                              className={`rounded-full px-2 py-0.5 text-xs font-medium ${getPriorityColor(
                                reminder.priority
                              )}`}
                            >
                              {reminder.priority}
                            </span>
                            <span
                              className={`rounded-full px-2 py-0.5 text-xs font-medium ${getStatusColor(
                                reminder.status
                              )}`}
                            >
                              {reminder.status}
                            </span>
                          </div>

                          {reminder.description && (
                            <p className="mb-3 text-sm text-gray-600">
                              {reminder.description}
                            </p>
                          )}

                          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              <span>
                                {formatDate(reminder.dueDate, reminder.dueTime)}
                              </span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Clock className="h-4 w-4" />
                              <span>{reminder.dueTime}</span>
                            </div>
                            <div className="rounded-full bg-gray-100 px-2 py-0.5 text-xs">
                              {reminder.category}
                            </div>
                            {reminder.notifyEmail && (
                              <span className="text-xs">📧 E-post</span>
                            )}
                            {reminder.notifyPush && (
                              <span className="text-xs">🔔 Push</span>
                            )}
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex gap-1">
                          <button
                            onClick={() => handleEditReminder(reminder)}
                            className="rounded-lg p-2 hover:bg-gray-100"
                            title="Rediger"
                          >
                            <Edit2 className="h-4 w-4 text-gray-600" />
                          </button>
                          <button
                            onClick={() => handleDeleteReminder(reminder.id)}
                            className="rounded-lg p-2 hover:bg-red-50"
                            title="Slett"
                          >
                            <Trash2 className="h-4 w-4 text-red-600" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Google Calendar Integration */}
            <div className="border-t border-gray-200 bg-gradient-to-br from-blue-50 to-indigo-50 p-6">
              <div className="mb-4 flex items-start justify-between">
                <div className="flex-1">
                  <div className="mb-2 flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-blue-600" />
                    <h3 className="font-semibold text-gray-900">
                      Google Calendar Synkronisering
                    </h3>
                  </div>
                  <p className="mb-3 text-sm text-gray-600">
                    {hasCalendarAccess
                      ? "Synkroniser påminnelser med din Google Calendar for å få varsler på alle enheter"
                      : "Koble til Google Calendar for automatisk synkronisering av påminnelser"}
                  </p>
                  {hasCalendarAccess && (
                    <div className="flex flex-wrap gap-2 text-xs text-gray-600">
                      <span className="flex items-center gap-1 rounded-full bg-white px-2 py-1">
                        <CheckCircle className="h-3 w-3 text-green-600" />
                        Tilgang gitt
                      </span>
                      <span className="flex items-center gap-1 rounded-full bg-white px-2 py-1">
                        <Clock className="h-3 w-3 text-blue-600" />
                        {stats.active} aktive påminnelser
                      </span>
                    </div>
                  )}
                </div>
                {!isAuthenticated && (
                  <div className="ml-4">
                    <GoogleSignIn />
                  </div>
                )}
              </div>

              {isAuthenticated && (
                <div className="flex gap-2">
                  <Button
                    variant={hasCalendarAccess ? "primary" : "secondary"}
                    size="medium"
                    leftIcon={
                      isSyncing ? (
                        <RefreshCw className="h-5 w-5 animate-spin" />
                      ) : (
                        <RefreshCw className="h-5 w-5" />
                      )
                    }
                    onClick={handleCalendarSync}
                    disabled={isSyncing}
                  >
                    {isSyncing
                      ? "Synkroniserer..."
                      : hasCalendarAccess
                      ? "Synkroniser nå"
                      : "Aktiver synkronisering"}
                  </Button>
                </div>
              )}

              {!isAuthenticated && (
                <div className="mt-4 rounded-lg border border-blue-200 bg-blue-50 p-4">
                  <p className="text-sm text-blue-800">
                    💡 Logg inn med Google for å aktivere automatisk synkronisering med
                    Google Calendar
                  </p>
                </div>
              )}
            </div>

            {/* Lira Integration */}
            <div className="border-t border-gray-200 bg-gray-50 p-6">
              <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900">
                    Trenger du hjelp med påminnelser?
                  </h3>
                  <p className="text-sm text-gray-600">
                    Lira kan hjelpe deg å planlegge og organisere dine påminnelser
                  </p>
                </div>
                <Button
                  variant="secondary"
                  size="medium"
                  leftIcon={<MessageCircle className="h-5 w-5" />}
                  onClick={() => router.push("/chatbot")}
                >
                  Chat med Lira
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-2xl rounded-2xl bg-white shadow-xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between border-b border-gray-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {editingReminder ? "Rediger påminnelse" : "Ny påminnelse"}
              </h2>
              <button
                onClick={resetForm}
                className="rounded-lg p-2 hover:bg-gray-100"
              >
                <X className="h-6 w-6 text-gray-600" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="max-h-[calc(100vh-200px)] overflow-y-auto p-6">
              <div className="space-y-4">
                {/* Title */}
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    Tittel *
                  </label>
                  <input
                    type="text"
                    value={formTitle}
                    onChange={(e) => setFormTitle(e.target.value)}
                    placeholder="F.eks. Send meldekort"
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                  />
                </div>

                {/* Description */}
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    Beskrivelse
                  </label>
                  <textarea
                    value={formDescription}
                    onChange={(e) => setFormDescription(e.target.value)}
                    placeholder="Legg til detaljer..."
                    rows={3}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                  />
                </div>

                {/* Category and Priority */}
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                      Kategori
                    </label>
                    <select
                      value={formCategory}
                      onChange={(e) => setFormCategory(e.target.value as ReminderCategory)}
                      className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                    >
                      {categories.filter((c) => c !== "Alle").map((cat) => (
                        <option key={cat} value={cat}>
                          {cat}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                      Prioritet
                    </label>
                    <select
                      value={formPriority}
                      onChange={(e) => setFormPriority(e.target.value as ReminderPriority)}
                      className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                    >
                      <option value="Lav">Lav</option>
                      <option value="Middels">Middels</option>
                      <option value="Høy">Høy</option>
                    </select>
                  </div>
                </div>

                {/* Date and Time */}
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                      Forfallsdato *
                    </label>
                    <input
                      type="date"
                      value={formDueDate}
                      onChange={(e) => setFormDueDate(e.target.value)}
                      className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                    />
                  </div>

                  <div>
                    <label className="mb-1 block text-sm font-medium text-gray-700">
                      Tidspunkt
                    </label>
                    <input
                      type="time"
                      value={formDueTime}
                      onChange={(e) => setFormDueTime(e.target.value)}
                      className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-[var(--color-brand-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-brand-primary)]/20"
                    />
                  </div>
                </div>

                {/* Notifications */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-700">
                    Varsler
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formNotifyEmail}
                        onChange={(e) => setFormNotifyEmail(e.target.checked)}
                        className="rounded border-gray-300"
                      />
                      <span className="text-sm text-gray-700">
                        Send e-postvarsel
                      </span>
                    </label>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={formNotifyPush}
                        onChange={(e) => setFormNotifyPush(e.target.checked)}
                        className="rounded border-gray-300"
                      />
                      <span className="text-sm text-gray-700">
                        Send push-varsel
                      </span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-3 border-t border-gray-200 p-6">
              <Button variant="secondary" size="medium" onClick={resetForm}>
                Avbryt
              </Button>
              <Button
                variant="primary"
                size="medium"
                onClick={handleSubmitReminder}
              >
                {editingReminder ? "Lagre endringer" : "Opprett påminnelse"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}

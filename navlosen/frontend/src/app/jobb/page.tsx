"use client";

import { useState, useMemo, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import GoogleSignIn from "@/components/auth/GoogleSignIn";
import { useGoogleAuth } from "@/contexts/GoogleAuthContext";
import {
  Briefcase,
  Search,
  FileText,
  GraduationCap,
  Users,
  MapPin,
  Clock,
  Building2,
  TrendingUp,
  BookOpen,
  Calendar,
  ChevronRight,
  Sparkles,
  MessageCircle,
  Filter,
  Star,
  CheckCircle2,
  Loader2,
  AlertCircle,
  Mail,
  Send,
  Inbox,
  FolderOpen,
  X,
} from "lucide-react";

type JobCategory = "Alle" | "Helse" | "Service" | "Teknologi" | "Håndverk" | "Kontor";

interface JobListing {
  id: string;
  title: string;
  company: string;
  location: string;
  type: "Heltid" | "Deltid" | "Midlertidig";
  category: JobCategory;
  posted: string;
  deadline: string;
  description: string;
  featured?: boolean;
}

interface Course {
  id: string;
  title: string;
  provider: string;
  duration: string;
  level: "Nybegynner" | "Videregående" | "Avansert";
  startDate: string;
  description: string;
  spots: number;
}

const courses: Course[] = [
  {
    id: "course-1",
    title: "CV-skriving og jobbsøkerteknikk",
    provider: "NAV Arbeidslivssenter",
    duration: "2 dager",
    level: "Nybegynner",
    startDate: "5. november 2025",
    description: "Lær å skrive en effektiv CV og mestrende jobbintervjuer med selvtillit.",
    spots: 8,
  },
  {
    id: "course-2",
    title: "Grunnleggende IT-kompetanse",
    provider: "Voksenopplæringen",
    duration: "4 uker",
    level: "Nybegynner",
    startDate: "12. november 2025",
    description: "Word, Excel, e-post og internett for deg som trenger en oppfriskning.",
    spots: 3,
  },
  {
    id: "course-3",
    title: "Introduksjon til programmering",
    provider: "Kodehode",
    duration: "8 uker",
    level: "Videregående",
    startDate: "20. november 2025",
    description: "Lær Python fra bunnen av. Ingen forkunnskaper nødvendig.",
    spots: 12,
  },
  {
    id: "course-4",
    title: "Yrkessjåførkurs (klasse C)",
    provider: "Trafikkskolen AS",
    duration: "6 uker",
    level: "Videregående",
    startDate: "1. desember 2025",
    description: "Sertifisering for tungbilsjåfør. Teori og praktisk opplæring inkludert.",
    spots: 5,
  },
];

const categories: JobCategory[] = ["Alle", "Helse", "Service", "Teknologi", "Håndverk", "Kontor"];

export default function JobbPage() {
  const router = useRouter();
  const { isAuthenticated, hasGmailAccess, requestGmailAccess} = useGoogleAuth();
  const [selectedCategory, setSelectedCategory] = useState<JobCategory>("Alle");
  const [searchTerm, setSearchTerm] = useState("");
  const [jobListings, setJobListings] = useState<JobListing[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [useMockData, setUseMockData] = useState(false);

  // New filter states
  const [jobType, setJobType] = useState<string>("Alle");
  const [location, setLocation] = useState<string>("");
  const [deadline, setDeadline] = useState<string>("");
  const [sortBy, setSortBy] = useState<string>("relevant");

  // Gmail state
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<JobListing | null>(null);
  const [emailSubject, setEmailSubject] = useState("");
  const [emailBody, setEmailBody] = useState("");
  const [isSending, setIsSending] = useState(false);

  // Fetch jobs from API
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const params = new URLSearchParams({
          page: "0",
          size: "50",
        });

        if (searchTerm.trim()) {
          params.append("q", searchTerm.trim());
        }

        if (selectedCategory !== "Alle") {
          params.append("category", selectedCategory);
        }

        if (jobType && jobType !== "Alle") {
          params.append("jobType", jobType);
        }

        if (location && location.trim()) {
          params.append("location", location.trim());
        }

        if (deadline) {
          params.append("deadline", deadline);
        }

        if (sortBy && sortBy !== "relevant") {
          params.append("sortBy", sortBy);
        }

        const response = await fetch(`/api/jobs?${params.toString()}`);

        if (!response.ok) {
          throw new Error("Failed to fetch jobs");
        }

        const data = await response.json();

        // Transform API data to match our interface
        const transformedJobs: JobListing[] = data.content.map((job: any) => ({
          id: job.uuid,
          title: job.title,
          company: job.employer.name,
          location: job.employer.location?.city || job.employer.location?.municipal || "Norge",
          type: job.properties.extent === "Heltid"
            ? "Heltid"
            : job.properties.extent === "Deltid"
            ? "Deltid"
            : "Midlertidig",
          category: job.categoryList?.[0]?.name || "Alle",
          posted: formatDate(new Date(job.published)),
          deadline: formatDeadline(new Date(job.expires)),
          description: job.description || "Ingen beskrivelse tilgjengelig",
          featured: false, // Can be randomized or based on recency
        }));

        // Mark first 3 as featured
        transformedJobs.slice(0, 3).forEach(job => job.featured = true);

        setJobListings(transformedJobs);
        setUseMockData(data.useMockData || false);
      } catch (err) {
        console.error("Error fetching jobs:", err);
        setError("Kunne ikke laste stillinger. Vennligst prøv igjen senere.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchJobs();
  }, [selectedCategory, searchTerm, jobType, location, deadline, sortBy]);

  const filteredJobs = useMemo(() => {
    return jobListings;
  }, [jobListings]);

  const featuredJobs = useMemo(
    () => jobListings.filter((job) => job.featured),
    [jobListings]
  );

  // Helper function to format date
  function formatDate(date: Date): string {
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "I dag";
    if (diffDays === 1) return "1 dag siden";
    if (diffDays < 7) return `${diffDays} dager siden`;
    if (diffDays < 14) return "1 uke siden";
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} uker siden`;
    return date.toLocaleDateString("no-NO");
  }

  // Helper function to format deadline
  function formatDeadline(date: Date): string {
    return date.toLocaleDateString("no-NO", {
      day: "numeric",
      month: "long",
      year: "numeric"
    });
  }

  // Handle opening email modal
  const handleApplyWithEmail = (job: JobListing) => {
    if (!hasGmailAccess) {
      requestGmailAccess();
      return;
    }

    setSelectedJob(job);
    setEmailSubject(`Søknad på stilling som ${job.title} hos ${job.company}`);
    setEmailBody(
      `Hei,\n\n` +
      `Jeg ønsker å søke på stillingen som ${job.title} hos ${job.company}.\n\n` +
      `[Skriv din søknad her...]\n\n` +
      `Med vennlig hilsen,\n` +
      `[Ditt navn]`
    );
    setShowEmailModal(true);
  };

  // Handle sending email
  const handleSendEmail = async () => {
    setIsSending(true);

    // Simulate sending
    await new Promise((resolve) => setTimeout(resolve, 2000));

    setIsSending(false);
    setShowEmailModal(false);

    alert(
      "Demo-modus: E-post sendt via Gmail\n\n" +
      `E-post til ${selectedJob?.company} er sendt!\n\n` +
      "I produksjon ville dette:\n" +
      "• Sende e-post via Gmail API\n" +
      "• Lagre kopi i 'Sendt'-mappen\n" +
      "• Spore svar fra arbeidsgiver\n" +
      "• Organisere søknader i egne mapper\n" +
      "• Varsle deg når du får svar"
    );

    setSelectedJob(null);
    setEmailSubject("");
    setEmailBody("");
  };

  return (
    <Layout>
      <div className="space-y-12">
        {/* Breadcrumb */}
        <div className="text-sm text-[var(--color-text-secondary)]">
          <Link
            href="/"
            className="transition-colors hover:text-[var(--color-primary)]"
          >
            NAV-Losen
          </Link>
          <span className="mx-2">/</span>
          <span className="text-[var(--color-text-primary)] font-medium">Jobb</span>
        </div>

        {/* Hero Section */}
        <section className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-8 rounded-3xl bg-white/80 p-8 md:p-12 shadow-sm backdrop-blur">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
              <Sparkles className="h-4 w-4" />
              Jobbsøk og karriereveiledning
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-[var(--color-text-primary)] md:text-5xl">
              Finn din neste jobb
            </h1>
            <p className="text-lg text-[var(--color-text-secondary)]">
              Søk i ledige stillinger, bygg en sterk CV, og få veiledning fra NAV Arbeidslivssenter. Vi hjelper deg hele veien fra søknad til ansettelse.
            </p>
            <div className="flex flex-wrap gap-4 text-sm text-[var(--color-text-secondary)]">
              <span className="inline-flex items-center gap-2">
                <Briefcase className="h-4 w-4 text-green-500" />
                {jobListings.length} ledige stillinger
              </span>
              <span className="inline-flex items-center gap-2">
                <GraduationCap className="h-4 w-4 text-green-500" />
                {courses.length} kurs tilgjengelig
              </span>
            </div>
          </div>
          <div className="hidden lg:flex items-start justify-center">
            <div className="flex h-24 w-24 items-center justify-center rounded-2xl bg-green-100">
              <Briefcase className="h-12 w-12 text-green-600" />
            </div>
          </div>

          {/* Search and Filter */}
          <div className="lg:col-span-2 space-y-4">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Søk etter stillingstittel, bedrift eller sted..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-xl border-2 border-gray-200 bg-white py-3 pl-12 pr-4 text-base transition-colors focus:border-[var(--color-primary)] focus:outline-none"
              />
            </div>

            {/* Category Filters */}
            <div className="flex flex-wrap gap-2" role="tablist" aria-label="Filtrer jobber etter kategori">
              {categories.map((category) => {
                const isActive = selectedCategory === category;
                return (
                  <button
                    key={category}
                    type="button"
                    role="tab"
                    aria-selected={isActive}
                    onClick={() => setSelectedCategory(category)}
                    className={`rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
                      isActive
                        ? "border-[var(--color-primary)] bg-[var(--color-primary)] text-white"
                        : "border-gray-200 bg-white text-[var(--color-text-secondary)] hover:border-[var(--color-primary)]/60 hover:text-[var(--color-primary)]"
                    }`}
                  >
                    {category}
                  </button>
                );
              })}
            </div>

            {/* Advanced Filters */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 border-t border-gray-100">
              {/* Job Type Filter */}
              <div>
                <label htmlFor="jobType" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                  Stillingsstørrelse
                </label>
                <select
                  id="jobType"
                  value={jobType}
                  onChange={(e) => setJobType(e.target.value)}
                  className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition-colors focus:border-[var(--color-primary)] focus:outline-none"
                >
                  <option value="Alle">Alle</option>
                  <option value="Heltid">Heltid</option>
                  <option value="Deltid">Deltid</option>
                  <option value="Midlertidig">Midlertidig</option>
                </select>
              </div>

              {/* Location Filter */}
              <div>
                <label htmlFor="location" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                  Sted
                </label>
                <input
                  type="text"
                  id="location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  placeholder="Oslo, Bergen..."
                  className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition-colors focus:border-[var(--color-primary)] focus:outline-none"
                />
              </div>

              {/* Deadline Filter */}
              <div>
                <label htmlFor="deadline" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                  Søknadsfrist
                </label>
                <select
                  id="deadline"
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                  className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition-colors focus:border-[var(--color-primary)] focus:outline-none"
                >
                  <option value="">Alle</option>
                  <option value="today">I dag</option>
                  <option value="week">Innen 7 dager</option>
                  <option value="month">Innen 30 dager</option>
                  <option value="later">Mer enn 30 dager</option>
                </select>
              </div>

              {/* Sort By Filter */}
              <div>
                <label htmlFor="sortBy" className="block text-sm font-medium text-[var(--color-text-secondary)] mb-2">
                  Sorter etter
                </label>
                <select
                  id="sortBy"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition-colors focus:border-[var(--color-primary)] focus:outline-none"
                >
                  <option value="relevant">Mest relevant</option>
                  <option value="newest">Nyeste først</option>
                  <option value="deadline">Frist nærmest</option>
                </select>
              </div>
            </div>
          </div>
        </section>

        {/* Mock Data Notice */}
        {useMockData && (
          <section>
            <div className="rounded-2xl border-2 border-yellow-200 bg-yellow-50 p-4 shadow-sm">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-5 w-5 flex-shrink-0 text-yellow-600" />
                <div className="flex-1">
                  <p className="text-sm text-yellow-800">
                    <strong>Demo-modus:</strong> Viser eksempeldata. For å hente reelle stillinger fra Arbeidsplassen.no, kontakt{" "}
                    <a
                      href="mailto:nav.team.arbeidsplassen@nav.no"
                      className="underline hover:no-underline"
                    >
                      nav.team.arbeidsplassen@nav.no
                    </a>{" "}
                    for å få API-nøkkel.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Lira Chatbot CTA */}
        <section>
          <div className="rounded-2xl border-2 border-[var(--color-secondary)] bg-gradient-to-r from-teal-50 to-blue-50 p-6 shadow-sm">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-[var(--color-secondary)]">
                <MessageCircle className="h-6 w-6 text-white" />
              </div>
              <div className="flex-1 space-y-3">
                <h3 className="text-lg font-bold text-[var(--color-text-primary)]">
                  Usikker på hva slags jobb du skal søke?
                </h3>
                <p className="text-sm text-[var(--color-text-secondary)]">
                  Lira kan hjelpe deg med å finne stillinger som passer din kompetanse, interesser og livssituasjon.
                </p>
                <Button
                  variant="primary"
                  size="medium"
                  leftIcon={<MessageCircle className="h-5 w-5" />}
                  onClick={() => router.push("/chatbot")}
                >
                  Chat med Lira om karriere
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Featured Jobs */}
        {featuredJobs.length > 0 && (
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Anbefalte stillinger
              </h2>
              <span className="inline-flex items-center gap-1 text-sm text-[var(--color-text-secondary)]">
                <Star className="h-4 w-4 text-yellow-500" />
                Kurert for deg
              </span>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
              {featuredJobs.map((job) => (
                <article
                  key={job.id}
                  className="flex flex-col rounded-2xl border border-green-100 bg-white p-6 shadow-sm transition-transform hover:-translate-y-1 hover:shadow-md"
                >
                  <div className="mb-3 flex items-center justify-between">
                    <span className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                      {job.category}
                    </span>
                    <Star className="h-4 w-4 fill-yellow-500 text-yellow-500" />
                  </div>
                  <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
                    {job.title}
                  </h3>
                  <div className="mt-2 space-y-1 text-sm text-[var(--color-text-secondary)]">
                    <div className="flex items-center gap-2">
                      <Building2 className="h-4 w-4" />
                      {job.company}
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      {job.location}
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      {job.type}
                    </div>
                  </div>
                  <p className="mt-3 text-sm text-[var(--color-text-secondary)]">
                    {job.description}
                  </p>
                  <div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-4 text-xs text-[var(--color-text-tertiary)]">
                    <span>Publisert {job.posted}</span>
                    <span>Frist: {job.deadline}</span>
                  </div>
                  <div className="mt-4">
                    <Button
                      variant="primary"
                      size="small"
                      className="w-full"
                      rightIcon={<ChevronRight className="h-4 w-4" />}
                    >
                      Se stillingsannonse
                    </Button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* All Job Listings */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Alle stillinger
            </h2>
            {!isLoading && (
              <span className="text-sm text-[var(--color-text-secondary)]">
                Viser {filteredJobs.length} av {jobListings.length}
              </span>
            )}
          </div>

          {/* Loading State */}
          {isLoading && (
            <div className="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white p-12">
              <Loader2 className="h-12 w-12 animate-spin text-[var(--color-primary)]" />
              <p className="mt-4 text-[var(--color-text-secondary)]">Laster stillinger...</p>
            </div>
          )}

          {/* Error State */}
          {error && !isLoading && (
            <div className="rounded-2xl border-2 border-red-200 bg-red-50 p-6">
              <div className="flex items-start gap-3">
                <AlertCircle className="h-6 w-6 flex-shrink-0 text-red-600" />
                <div>
                  <p className="font-semibold text-red-900">Kunne ikke laste stillinger</p>
                  <p className="mt-1 text-sm text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Empty State */}
          {!isLoading && !error && filteredJobs.length === 0 && (
            <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center text-[var(--color-text-secondary)]">
              <Search className="mx-auto mb-4 h-12 w-12 text-gray-300" />
              <p className="text-lg font-semibold">Ingen stillinger funnet</p>
              <p className="mt-2 text-sm">
                Prøv å justere søket eller kategoriene dine, eller chat med Lira for personlige anbefalinger.
              </p>
            </div>
          )}

          {/* Job Listings */}
          {!isLoading && !error && filteredJobs.length > 0 && (
            <div className="grid gap-6 md:grid-cols-2">
              {filteredJobs.map((job) => (
                <article
                  key={job.id}
                  className="flex flex-col rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
                >
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-xs text-[var(--color-text-tertiary)]">
                      {job.category}
                    </span>
                    <span className="text-xs text-[var(--color-text-tertiary)]">
                      {job.posted}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
                    {job.title}
                  </h3>
                  <div className="mt-2 space-y-1 text-sm text-[var(--color-text-secondary)]">
                    <div className="flex items-center gap-2">
                      <Building2 className="h-4 w-4" />
                      {job.company}
                    </div>
                    <div className="flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      {job.location} · {job.type}
                    </div>
                  </div>
                  <p className="mt-3 text-sm text-[var(--color-text-secondary)]">
                    {job.description}
                  </p>
                  <div className="mt-4 rounded-xl bg-gray-50 p-3 text-xs text-[var(--color-text-tertiary)]">
                    Søknadsfrist: {job.deadline}
                  </div>
                  <div className="mt-4 flex flex-col gap-2">
                    <div className="flex gap-2">
                      <Button
                        variant="primary"
                        size="small"
                        className="flex-1"
                        rightIcon={<ChevronRight className="h-4 w-4" />}
                      >
                        Se annonse
                      </Button>
                      <Button variant="secondary" size="small">
                        Lagre
                      </Button>
                    </div>
                    <Button
                      variant="secondary"
                      size="small"
                      leftIcon={<Mail className="h-4 w-4" />}
                      onClick={() => handleApplyWithEmail(job)}
                    >
                      {hasGmailAccess ? "Søk via Gmail" : "Aktiver Gmail"}
                    </Button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {/* CV Builder Section */}
        <section className="rounded-3xl bg-gradient-to-r from-purple-50 to-pink-50 p-8 md:p-12">
          <div className="grid gap-8 md:grid-cols-[1fr_2fr]">
            <div className="flex items-center justify-center">
              <div className="flex h-32 w-32 items-center justify-center rounded-3xl bg-purple-100">
                <FileText className="h-16 w-16 text-purple-600" />
              </div>
            </div>
            <div className="space-y-4">
              <h2 className="text-3xl font-bold text-[var(--color-text-primary)]">
                Bygg en sterk CV
              </h2>
              <p className="text-lg text-[var(--color-text-secondary)]">
                Vår CV-builder hjelper deg med å lage en profesjonell CV som skiller seg ut. Med maler, tips og eksempler får du en CV som viser dine styrker. Eller chat med Lira for personlig veiledning.
              </p>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  Profesjonelle maler tilpasset norske arbeidsgivere
                </div>
                <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  Steg-for-steg veiledning og eksempler
                </div>
                <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  Lira gir personlige råd basert på din erfaring
                </div>
                <div className="flex items-center gap-2 text-sm text-[var(--color-text-secondary)]">
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  Eksporter som PDF eller Word
                </div>
              </div>
              <div className="flex flex-wrap gap-3">
                <Button
                  variant="primary"
                  size="medium"
                  leftIcon={<FileText className="h-5 w-5" />}
                >
                  Start CV-builder
                </Button>
                <Button
                  variant="secondary"
                  size="medium"
                  leftIcon={<MessageCircle className="h-5 w-5" />}
                  onClick={() => router.push("/chatbot")}
                >
                  Chat med Lira
                </Button>
                <Button variant="secondary" size="medium">
                  Se eksempler
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* Courses and Training */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Kurs og opplæring
            </h2>
            <span className="text-sm text-[var(--color-text-secondary)]">
              {courses.length} kurs tilgjengelig
            </span>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {courses.map((course) => (
              <article
                key={course.id}
                className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
              >
                <div className="mb-3 flex items-center justify-between">
                  <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                    {course.level}
                  </span>
                  <span className="text-xs text-[var(--color-text-tertiary)]">
                    {course.spots} plasser igjen
                  </span>
                </div>
                <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
                  {course.title}
                </h3>
                <div className="mt-2 space-y-1 text-sm text-[var(--color-text-secondary)]">
                  <div className="flex items-center gap-2">
                    <GraduationCap className="h-4 w-4" />
                    {course.provider}
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    {course.duration}
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Start: {course.startDate}
                  </div>
                </div>
                <p className="mt-3 text-sm text-[var(--color-text-secondary)]">
                  {course.description}
                </p>
                <div className="mt-4 flex gap-2">
                  <Button
                    variant="primary"
                    size="small"
                    className="flex-1"
                    rightIcon={<ChevronRight className="h-4 w-4" />}
                  >
                    Meld interesse
                  </Button>
                  <Button variant="secondary" size="small">
                    Les mer
                  </Button>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Services Section */}
        <section className="grid gap-6 md:grid-cols-2">
          <div className="rounded-2xl border border-blue-100 bg-gradient-to-br from-blue-50 to-white p-8">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="mb-2 text-xl font-bold text-[var(--color-text-primary)]">
              NAV Arbeidslivssenter
            </h3>
            <p className="mb-4 text-sm text-[var(--color-text-secondary)]">
              Få personlig veiledning fra erfarne karriererådgivere. Vi hjelper deg med jobbsøk, CV, intervjutrening og karriereplanlegging.
            </p>
            <Button variant="secondary" size="medium" rightIcon={<ChevronRight className="h-4 w-4" />}>
              Book gratis samtale
            </Button>
          </div>

          <div className="rounded-2xl border border-green-100 bg-gradient-to-br from-green-50 to-white p-8">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="mb-2 text-xl font-bold text-[var(--color-text-primary)]">
              Arbeidsmarkedsstatistikk
            </h3>
            <p className="mb-4 text-sm text-[var(--color-text-secondary)]">
              Se hvilke bransjer som vokser, hvilke kompetanser som er etterspurt, og hva du kan forvente i lønn.
            </p>
            <Button variant="secondary" size="medium" rightIcon={<ChevronRight className="h-4 w-4" />}>
              Utforsk statistikk
            </Button>
          </div>
        </section>

        {/* Support CTA */}
        <section className="flex flex-col md:flex-row md:items-start md:justify-between gap-6 rounded-3xl border border-green-200 bg-gradient-to-r from-green-500 to-teal-500 p-8 text-white shadow-lg">
          <div className="space-y-2 md:flex-1">
            <h2 className="text-2xl font-bold">Klar til å ta neste steg?</h2>
            <p className="text-sm text-white/90">
              Enten du skal søke jobb, bygge CV eller ta et kurs – vi støtter deg hele veien. Alle verktøy er gratis og tilgjengelige for alle arbeidssøkere.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 md:flex-shrink-0">
            <Button
              variant="secondary"
              size="medium"
              className="bg-white text-[var(--color-primary)] hover:bg-white/90"
              onClick={() => router.push("/chatbot")}
            >
              Chat med Lira
            </Button>
            <Button
              variant="text"
              size="medium"
              className="text-white hover:text-white/80"
              onClick={() => router.push("/min-reise")}
            >
              Gå til Min Reise
            </Button>
          </div>
        </section>
      </div>

      {/* Gmail Email Modal */}
      {showEmailModal && selectedJob && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-3xl rounded-2xl bg-white shadow-xl">
            {/* Modal Header */}
            <div className="flex items-center justify-between border-b border-gray-200 p-6">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                  <Mail className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">
                    Send søknad via Gmail
                  </h2>
                  <p className="text-sm text-gray-600">
                    {selectedJob.company} - {selectedJob.title}
                  </p>
                </div>
              </div>
              <button
                onClick={() => {
                  setShowEmailModal(false);
                  setSelectedJob(null);
                }}
                className="rounded-lg p-2 hover:bg-gray-100"
              >
                <X className="h-6 w-6 text-gray-600" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 space-y-4">
              {/* Email Subject */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Emne
                </label>
                <input
                  type="text"
                  value={emailSubject}
                  onChange={(e) => setEmailSubject(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                />
              </div>

              {/* Email Body */}
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">
                  Melding
                </label>
                <textarea
                  value={emailBody}
                  onChange={(e) => setEmailBody(e.target.value)}
                  rows={12}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 font-mono text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                />
              </div>

              {/* Features Info */}
              <div className="rounded-lg bg-blue-50 p-4">
                <p className="text-sm font-medium text-blue-900 mb-2">
                  📧 Gmail-integrasjon aktiv
                </p>
                <ul className="space-y-1 text-xs text-blue-800">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3 w-3" />
                    E-posten sendes via din Gmail-konto
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3 w-3" />
                    Kopi lagres automatisk i 'Sendt'-mappen
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3 w-3" />
                    Du får varsling når arbeidsgiveren svarer
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="h-3 w-3" />
                    Organiseres i egen mappe for jobbsøknader
                  </li>
                </ul>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-3 border-t border-gray-200 p-6">
              <Button
                variant="secondary"
                size="medium"
                onClick={() => {
                  setShowEmailModal(false);
                  setSelectedJob(null);
                }}
                disabled={isSending}
              >
                Avbryt
              </Button>
              <Button
                variant="primary"
                size="medium"
                leftIcon={
                  isSending ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )
                }
                onClick={handleSendEmail}
                disabled={isSending || !emailSubject.trim() || !emailBody.trim()}
              >
                {isSending ? "Sender..." : "Send søknad"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}

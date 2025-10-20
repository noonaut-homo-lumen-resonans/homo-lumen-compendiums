"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import {
  BookOpen,
  ChevronRight,
  ClipboardList,
  Clock,
  Search,
  Sparkles,
} from "lucide-react";

type GuideCategory =
  | "Arbeidsledighet"
  | "Sykdom"
  | "Familie og barn"
  | "Økonomi";

interface Guide {
  id: string;
  title: string;
  category: GuideCategory;
  summary: string;
  estimatedTime: string;
  stepsCount: number;
  updated: string;
  firstStep: string;
}

const guides: Guide[] = [
  {
    id: "dagpenger",
    title: "Slik søker du dagpenger",
    category: "Arbeidsledighet",
    summary:
      "For deg som nylig har mistet jobben. Vi følger deg gjennom krav, dokumentasjon og innsending i Altinn.",
    estimatedTime: "15 minutter",
    stepsCount: 6,
    updated: "Oppdatert 10. oktober 2025",
    firstStep: "Finn siste lønnsslipp og arbeidsforholdsdokumentasjon.",
  },
  {
    id: "sykepenger",
    title: "Slik fungerer sykepenger",
    category: "Sykdom",
    summary:
      "Oversikt over krav til deg og arbeidsgiver, og hvordan du følger søknaden i NAV-kontoen din.",
    estimatedTime: "12 minutter",
    stepsCount: 5,
    updated: "Oppdatert 3. oktober 2025",
    firstStep:
      "Registrer sykefraværet og send egenmelding eller sykmelding fra lege.",
  },
  {
    id: "barnetrygd",
    title: "Slik fungerer barnetrygd",
    category: "Familie og barn",
    summary:
      "Hvem har rett, hvordan søker du, og når kommer utbetalingen? Alt i én guide.",
    estimatedTime: "8 minutter",
    stepsCount: 4,
    updated: "Oppdatert 25. september 2025",
    firstStep:
      "Sjekk at barnet er registrert i Folkeregisteret på din adresse.",
  },
  {
    id: "foreldrepenger",
    title: "Slik søker du foreldrepenger",
    category: "Familie og barn",
    summary:
      "Planlegg permisjonen, del perioden og send søknaden før termin for å unngå forsinkelser.",
    estimatedTime: "18 minutter",
    stepsCount: 7,
    updated: "Oppdatert 9. oktober 2025",
    firstStep: "Avklar fordeling av uker med den andre forelderen.",
  },
  {
    id: "kontantstotte",
    title: "Slik søker du kontantstøtte",
    category: "Familie og barn",
    summary:
      "For foreldre med barn mellom ett og to år som ikke går i barnehage med offentlig støtte.",
    estimatedTime: "6 minutter",
    stepsCount: 3,
    updated: "Oppdatert 7. oktober 2025",
    firstStep:
      "Bekreft at barnet ikke mottar barnehagestøtte eller 20 timer gratis SFO.",
  },
  {
    id: "sfo",
    title: "Slik søker du redusert betaling i SFO",
    category: "Familie og barn",
    summary:
      "Finn kommunens ordninger, dokumenter inntekt og send søknaden før søknadsfristen.",
    estimatedTime: "9 minutter",
    stepsCount: 4,
    updated: "Oppdatert 1. oktober 2025",
    firstStep:
      "Hent fjorårets skattemelding og dokumentasjon på endret inntekt.",
  },
  {
    id: "sosialhjelp",
    title: "Slik søker du økonomisk sosialhjelp",
    category: "Økonomi",
    summary:
      "Vurder behov, dokumenter situasjonen og forbered møte med NAV-kontoret på en trygg måte.",
    estimatedTime: "20 minutter",
    stepsCount: 6,
    updated: "Oppdatert 18. oktober 2025",
    firstStep:
      "Lag en oversikt over faste utgifter, inntekter og oppsparte midler.",
  },
  {
    id: "boutgifter",
    title: "Slik får du hjelp med boutgifter",
    category: "Økonomi",
    summary:
      "Sammenligner bostøtte, sosialhjelp og kommunale ordninger slik at du finner riktig tiltak.",
    estimatedTime: "11 minutter",
    stepsCount: 5,
    updated: "Oppdatert 30. september 2025",
    firstStep:
      "Sjekk om du allerede mottar bostøtte eller andre tilskudd fra kommunen.",
  },
  {
    id: "kvalifiseringsprogram",
    title: "Veiledning for kvalifiseringsprogrammet",
    category: "Økonomi",
    summary:
      "Hvem kan delta, hva inneholder programmet og hvordan søker du? Alt samlet på ett sted.",
    estimatedTime: "14 minutter",
    stepsCount: 6,
    updated: "Oppdatert 5. oktober 2025",
    firstStep: "Bestill samtale med NAV-veileder for å avklare behov og mål.",
  },
];

const categories: (GuideCategory | "Alle")[] = [
  "Alle",
  ...Array.from(new Set(guides.map((guide) => guide.category))),
];

const recommendedIds = new Set(["dagpenger", "sykepenger", "sosialhjelp"]);

const faqItems = [
  {
    id: "faq-1",
    question: "Hvordan vet jeg hvilke dokumenter jeg trenger?",
    answer:
      "Hver veiledning starter med en sjekkliste for dokumenter. Vi oppdaterer listene fortløpende når NAV endrer krav. Mangler du noe, viser vi hvordan du bestiller det.",
  },
  {
    id: "faq-2",
    question: "Kan jeg skrive ut en PDF av veiledningen?",
    answer:
      "Ja. Nederst i hver veiledning finner du «Last ned som PDF». Den inkluderer alle steg, sjekklister og viktige lenker.",
  },
  {
    id: "faq-3",
    question: "Hva gjør jeg hvis jeg trenger hjelp underveis?",
    answer:
      "Klikk «Chat med Lira» for å få svar med utgangspunkt i guiden du står i. Ved behov kan du booke time med NAV-veileder direkte fra veiledningen.",
  },
];

export default function VeiledningerPage() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] =
    useState<(typeof categories)[number]>("Alle");

  const normalizedSearch = searchTerm.trim().toLowerCase();

  const filteredGuides = useMemo(() => {
    return guides.filter((guide) => {
      const matchesCategory =
        selectedCategory === "Alle" || guide.category === selectedCategory;
      if (!matchesCategory) {
        return false;
      }

      if (!normalizedSearch) {
        return true;
      }

      const haystack = `${guide.title} ${guide.summary} ${guide.category}`.toLowerCase();
      return haystack.includes(normalizedSearch);
    });
  }, [normalizedSearch, selectedCategory]);

  const recommendedGuides = useMemo(
    () => guides.filter((guide) => recommendedIds.has(guide.id)),
    []
  );

  const handleOpenGuide = (guideId: string) => {
    router.push(`/veiledninger/${guideId}`);
  };

  return (
    <Layout>
      <div className="bg-gradient-to-b from-blue-50 via-white to-purple-50 -m-4 md:-m-6 lg:-m-8 p-4 md:p-6 lg:p-8 min-h-screen">
        <div className="mx-auto max-w-6xl space-y-12">
          {/* Breadcrumb */}
          <div className="text-sm text-[var(--color-text-secondary)]">
            <Link
              href="/"
              className="transition-colors hover:text-[var(--color-primary)]"
            >
              NAV-Losen
            </Link>
            <span className="mx-2">/</span>
            <span className="text-[var(--color-text-primary)] font-medium">
              Veiledninger
            </span>
          </div>

          {/* Hero */}
          <section className="grid gap-6 rounded-3xl bg-white/80 p-8 md:p-12 shadow-sm backdrop-blur">
            <div className="flex flex-wrap items-start justify-between gap-6">
              <div className="max-w-2xl space-y-4">
                <div className="inline-flex items-center gap-2 rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                  <Sparkles className="h-4 w-4" />
                  Steg-for-steg veiledning
                </div>
                <h1 className="text-4xl font-bold tracking-tight text-[var(--color-text-primary)] md:text-5xl">
                  Veiledninger
                </h1>
                <p className="text-lg text-[var(--color-text-secondary)]">
                  Finn trygge, oppdaterte veiledninger for NAV-prosesser. Vi
                  følger deg fra forberedelser til innsending og oppfølging.
                </p>
                <div className="flex flex-wrap gap-4 text-sm text-[var(--color-text-secondary)]">
                  <span className="inline-flex items-center gap-2">
                    <ClipboardList className="h-4 w-4 text-blue-500" />
                    9 temaguider klare
                  </span>
                  <span className="inline-flex items-center gap-2">
                    <Clock className="h-4 w-4 text-blue-500" />
                    Estimert tid 6–20 min per guide
                  </span>
                </div>
              </div>
              <div className="hidden md:block">
                <div className="flex h-24 w-24 items-center justify-center rounded-2xl bg-blue-100">
                  <BookOpen className="h-12 w-12 text-blue-600" />
                </div>
              </div>
            </div>

            {/* Search */}
            <div className="relative">
              <Search className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
              <input
                type="search"
                value={searchTerm}
                onChange={(event) => setSearchTerm(event.target.value)}
                placeholder="Søk i veiledninger..."
                className="w-full rounded-2xl border border-gray-200 bg-white py-3 pl-12 pr-4 text-base shadow-sm focus:border-[var(--color-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)]/50"
                aria-label="Søk i veiledninger"
              />
            </div>

            {/* Categories */}
            <div
              className="flex flex-wrap gap-2"
              role="tablist"
              aria-label="Filtrer veiledninger etter kategori"
            >
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
          </section>

          {/* Recommended guides */}
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Anbefalt å starte med
              </h2>
              <span className="text-sm text-[var(--color-text-secondary)]">
                Kurert av NAV-veiledere – høyest etterspørsel siste 90 dager
              </span>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
              {recommendedGuides.map((guide) => (
                <article
                  key={guide.id}
                  className="rounded-2xl border border-blue-100 bg-white p-6 shadow-sm transition-transform hover:-translate-y-1 hover:shadow-md"
                >
                  <span className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                    {guide.category}
                  </span>
                  <h3 className="mt-3 text-lg font-semibold text-[var(--color-text-primary)]">
                    {guide.title}
                  </h3>
                  <p className="mt-2 text-sm text-[var(--color-text-secondary)]">
                    {guide.summary}
                  </p>
                  <div className="mt-4 text-xs text-[var(--color-text-tertiary)]">
                    {guide.updated} · {guide.estimatedTime}
                  </div>
                  <Button
                    variant="secondary"
                    size="small"
                    className="mt-4 w-full justify-between"
                    rightIcon={<ChevronRight className="h-4 w-4" />}
                    onClick={() => handleOpenGuide(guide.id)}
                  >
                    Åpne veiledning
                  </Button>
                </article>
              ))}
            </div>
          </section>

          {/* All guides */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Alle veiledninger
              </h2>
              <span className="text-sm text-[var(--color-text-secondary)]">
                Viser {filteredGuides.length} av {guides.length}
              </span>
            </div>

            {filteredGuides.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center text-[var(--color-text-secondary)]">
                Ingen veiledninger matcher søket ditt ennå. Prøv en annen
                kategori eller et annet søkeord.
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2">
                {filteredGuides.map((guide) => (
                  <article
                    key={guide.id}
                    className="flex h-full flex-col justify-between rounded-2xl border border-gray-200 bg-white p-6 shadow-sm"
                  >
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-xs text-[var(--color-text-tertiary)]">
                        <span>{guide.category}</span>
                        <span>{guide.updated}</span>
                      </div>
                      <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
                        {guide.title}
                      </h3>
                      <p className="text-sm text-[var(--color-text-secondary)]">
                        {guide.summary}
                      </p>
                      <div className="rounded-xl bg-[var(--color-primary)]/5 p-4 text-sm text-[var(--color-text-secondary)]">
                        <p className="font-medium text-[var(--color-text-primary)]">
                          Første steg
                        </p>
                        <p>{guide.firstStep}</p>
                        <div className="mt-2 flex items-center gap-3 text-xs text-[var(--color-text-tertiary)]">
                          <span>{guide.stepsCount} steg</span>
                          <span>·</span>
                          <span>{guide.estimatedTime}</span>
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 flex flex-wrap items-center gap-3">
                      <Button
                        variant="primary"
                        size="small"
                        className="flex-1 justify-center"
                        rightIcon={<ChevronRight className="h-4 w-4" />}
                        onClick={() => handleOpenGuide(guide.id)}
                      >
                        Gå til veiledning
                      </Button>
                      <button
                        type="button"
                        className="text-sm font-medium text-[var(--color-primary)] underline-offset-2 transition-colors hover:underline"
                      >
                        Lagre til senere
                      </button>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>

          {/* FAQ */}
          <section className="grid gap-6 rounded-3xl bg-white/80 p-8 shadow-sm backdrop-blur">
            <h2 className="text-2xl font-bold text-[var(--color-text-primary)]">
              Vanlige spørsmål
            </h2>
            {faqItems.map((faq) => (
              <details
                key={faq.id}
                className="group rounded-2xl border border-gray-200 bg-white p-4"
              >
                <summary className="cursor-pointer text-base font-semibold text-[var(--color-text-primary)] group-open:text-[var(--color-primary)]">
                  {faq.question}
                </summary>
                <p className="mt-3 text-sm text-[var(--color-text-secondary)]">
                  {faq.answer}
                </p>
              </details>
            ))}
          </section>

          {/* Support CTA */}
          <section className="flex flex-col items-start gap-6 rounded-3xl border border-blue-200 bg-gradient-to-r from-blue-500 to-purple-500 p-8 text-white shadow-lg">
            <div className="space-y-2">
              <h2 className="text-2xl font-bold">
                Trenger du hjelp med neste steg?
              </h2>
              <p className="max-w-2xl text-sm text-white/90">
                Kontakt NAV-veileder eller lagre veiledningen til senere. Vi
                synkroniserer det du gjør her med Min Reise-dashbordet ditt.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Button
                variant="secondary"
                size="medium"
                className="bg-white text-[var(--color-primary)] hover:bg-white/90"
              >
                Book veiledningssamtale
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
      </div>
    </Layout>
  );
}

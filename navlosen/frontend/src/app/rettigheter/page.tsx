"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Layout from "@/components/layout/Layout";
import Button from "@/components/ui/Button";
import {
  Scale,
  ChevronDown,
  ChevronRight,
  MessageCircle,
  FileText,
  Shield,
  AlertCircle,
  CheckCircle,
  Info,
  Users,
  Briefcase,
  Heart,
  Home,
  Baby,
  GraduationCap,
  DollarSign,
  Calendar,
} from "lucide-react";

type BenefitCategory = "Arbeidsledighet" | "Sykdom" | "Funksjonsnedsettelse" | "Familie" | "Økonomi" | "Annet";

interface Benefit {
  id: string;
  title: string;
  category: BenefitCategory;
  description: string;
  whoCanApply: string[];
  requirements: string[];
  amount: string;
  duration: string;
  applyLink?: string;
  icon: React.ReactNode;
}

interface Right {
  id: string;
  title: string;
  description: string;
  details: string[];
}

const benefits: Benefit[] = [
  {
    id: "dagpenger",
    title: "Dagpenger",
    category: "Arbeidsledighet",
    description: "Økonomisk støtte når du er arbeidsledig",
    whoCanApply: [
      "Du som har mistet jobben",
      "Du som er permittert",
      "Du som jobber redusert og tjener mindre enn før",
    ],
    requirements: [
      "Hatt pensjonsgivende inntekt på minst 1,5 G siste 12 mnd eller 3 G siste 36 mnd",
      "Registrert som arbeidssøker hos NAV",
      "Være villig til å ta ethvert passende arbeid",
      "Sende meldekort hver 14. dag",
    ],
    amount: "Inntil 62,4% av tidligere inntekt (maks 6 G)",
    duration: "Inntil 104 uker (2 år)",
    applyLink: "https://www.nav.no/dagpenger",
    icon: <Briefcase className="h-6 w-6" />,
  },
  {
    id: "sykepenger",
    title: "Sykepenger",
    category: "Sykdom",
    description: "Inntektssikring når du er syk og ikke kan jobbe",
    whoCanApply: [
      "Du som er ansatt og blir syk",
      "Du som er selvstendig næringsdrivende",
      "Du som er frilanser",
    ],
    requirements: [
      "Sykmelding fra lege eller annen behandler",
      "Vært i arbeid minst 4 uker før sykdom",
      "Minst 20% arbeidsuførhet",
    ],
    amount: "100% av inntektsgrunnlaget (maks 6 G)",
    duration: "Inntil 52 uker",
    applyLink: "https://www.nav.no/sykepenger",
    icon: <Heart className="h-6 w-6" />,
  },
  {
    id: "aap",
    title: "Arbeidsavklaringspenger (AAP)",
    category: "Funksjonsnedsettelse",
    description: "Støtte når sykdom eller skade reduserer arbeidsevnen din",
    whoCanApply: [
      "Du som har hatt vesentlig nedsatt arbeidsevne i minst 52 uker",
      "Du som trenger bistand fra NAV for å komme i arbeid",
    ],
    requirements: [
      "Minst 50% nedsatt arbeidsevne",
      "Aktiv deltakelse i helsehjelp eller arbeidsrettede tiltak",
      "Inntekt minst 1,5 G siste år eller gjennomsnitt 1,5 G siste 3 år",
    ],
    amount: "66% av inntektsgrunnlaget",
    duration: "Maks 4 år (kan forlenges)",
    applyLink: "https://www.nav.no/aap",
    icon: <Shield className="h-6 w-6" />,
  },
  {
    id: "foreldrepenger",
    title: "Foreldrepenger",
    category: "Familie",
    description: "Inntektssikring ved fødsel eller adopsjon",
    whoCanApply: [
      "Foreldre som venter barn",
      "Foreldre som har adoptert",
    ],
    requirements: [
      "Hatt pensjonsgivende inntekt 6 av de siste 10 månedene",
      "Minst 46 968 kr samlet inntekt (0,5 G)",
    ],
    amount: "80% eller 100% av inntekt (avhenger av valgt kvote)",
    duration: "49 uker (100%) eller 59 uker (80%)",
    applyLink: "https://www.nav.no/foreldrepenger",
    icon: <Baby className="h-6 w-6" />,
  },
  {
    id: "uforetrygd",
    title: "Uføretrygd",
    category: "Funksjonsnedsettelse",
    description: "Varig inntektssikring ved varig nedsatt arbeidsevne",
    whoCanApply: [
      "Du som har varig nedsatt inntektsevne med minst 50%",
      "Du som har prøvd arbeidsrettede tiltak uten å komme i jobb",
    ],
    requirements: [
      "Mellom 18 og 67 år",
      "Medlem i folketrygden siste 5 år",
      "Varig nedsatt inntektsevne med minst 50%",
      "Alle muligheter for behandling og arbeidsrettede tiltak er prøvd",
    ],
    amount: "Avhenger av tidligere inntekt og uføregrad",
    duration: "Varig, til du fyller 67 år",
    applyLink: "https://www.nav.no/uforetrygd",
    icon: <Shield className="h-6 w-6" />,
  },
  {
    id: "økonomisk-sosialhjelp",
    title: "Økonomisk sosialhjelp",
    category: "Økonomi",
    description: "Midlertidig støtte når du ikke kan forsørge deg selv",
    whoCanApply: [
      "Du som ikke har nok penger til å dekke grunnleggende behov",
      "Du som ikke har rett til andre ytelser",
    ],
    requirements: [
      "Alle andre muligheter må være utprøvd",
      "Kan ikke forsørge deg selv",
      "Må søke om det",
    ],
    amount: "Individuell vurdering basert på situasjon",
    duration: "Kortvarig, månedlig søknad",
    applyLink: "https://www.nav.no/sosialhjelp",
    icon: <DollarSign className="h-6 w-6" />,
  },
];

const rights: Right[] = [
  {
    id: "right-information",
    title: "Rett til informasjon",
    description: "Du har rett til å få informasjon om dine rettigheter og plikter",
    details: [
      "NAV skal gi deg informasjon om hvilke rettigheter og plikter du har",
      "Du har rett til å få vite hvilke opplysninger NAV har om deg",
      "NAV skal informere deg på et språk du forstår",
      "Du kan be om skriftlig informasjon",
    ],
  },
  {
    id: "right-guidance",
    title: "Rett til veiledning",
    description: "Du har rett til å få hjelp og veiledning fra NAV",
    details: [
      "NAV skal veilede deg i kontakten med dem",
      "Du kan be om hjelp til å fylle ut søknader",
      "NAV skal hjelpe deg med å finne riktig ytelse",
      "Du kan be om møte med NAV-veileder",
    ],
  },
  {
    id: "right-appeal",
    title: "Rett til å klage",
    description: "Du har rett til å klage på vedtak fra NAV",
    details: [
      "Du kan klage på vedtak innen 6 uker fra mottatt vedtak",
      "Klagen sendes til samme NAV-kontor som fattet vedtaket",
      "Du trenger ikke å begrunne klagen først",
      "NAV skal vurdere saken på nytt",
      "Hvis NAV ikke endrer vedtaket, sendes saken til NAV Klageinstans",
    ],
  },
  {
    id: "right-interpreter",
    title: "Rett til tolk",
    description: "Du har rett til tolk hvis du ikke snakker norsk",
    details: [
      "NAV skal tilby gratis tolk ved møter",
      "Du kan be om tolk på forhånd",
      "Tolk skal være upartisk og ha taushetsplikt",
      "Du kan be om nytt møte hvis tolken ikke var god nok",
    ],
  },
  {
    id: "right-privacy",
    title: "Rett til personvern",
    description: "Dine personopplysninger skal behandles forsvarlig",
    details: [
      "NAV må ha lovhjemmel for å behandle personopplysninger",
      "Du har rett til innsyn i hva NAV har registrert om deg",
      "Du kan kreve retting av feil opplysninger",
      "Du kan klage til Datatilsynet hvis du mener rettighetene dine er krenket",
    ],
  },
];

/**
 * Rettigheter Page
 *
 * Comprehensive rights and benefits information page
 */
export default function RettigheterPage() {
  const router = useRouter();
  const [selectedCategory, setSelectedCategory] = useState<BenefitCategory | "Alle">("Alle");
  const [expandedBenefit, setExpandedBenefit] = useState<string | null>(null);
  const [expandedRight, setExpandedRight] = useState<string | null>(null);

  const categories: (BenefitCategory | "Alle")[] = [
    "Alle",
    "Arbeidsledighet",
    "Sykdom",
    "Funksjonsnedsettelse",
    "Familie",
    "Økonomi",
  ];

  const filteredBenefits =
    selectedCategory === "Alle"
      ? benefits
      : benefits.filter((b) => b.category === selectedCategory);

  const getCategoryIcon = (category: BenefitCategory) => {
    switch (category) {
      case "Arbeidsledighet":
        return <Briefcase className="h-5 w-5" />;
      case "Sykdom":
        return <Heart className="h-5 w-5" />;
      case "Funksjonsnedsettelse":
        return <Shield className="h-5 w-5" />;
      case "Familie":
        return <Baby className="h-5 w-5" />;
      case "Økonomi":
        return <DollarSign className="h-5 w-5" />;
      default:
        return <Info className="h-5 w-5" />;
    }
  };

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
            <span className="text-[var(--color-text-primary)] font-medium">Rettigheter</span>
          </div>

          {/* Hero Section */}
          <div className="mb-8 text-center">
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[var(--color-brand-primary)] shadow-lg">
                <Scale className="h-8 w-8 text-white" />
              </div>
            </div>
            <h1 className="mb-2 text-4xl font-bold text-[var(--color-text-primary)]">
              Rettigheter og Ytelser
            </h1>
            <p className="text-xl text-[var(--color-text-secondary)]">
              Lær om dine rettigheter og hvilke ytelser du kan ha krav på
            </p>
          </div>

          {/* Important Notice */}
          <div className="mb-8 rounded-2xl border border-blue-200 bg-blue-50 p-6">
            <div className="flex items-start gap-3">
              <Info className="h-6 w-6 flex-shrink-0 text-blue-600" />
              <div>
                <h3 className="mb-1 font-semibold text-blue-900">Viktig informasjon</h3>
                <p className="text-sm text-blue-800">
                  Denne informasjonen er veiledende. For oppdatert og spesifikk informasjon om dine
                  rettigheter, besøk{" "}
                  <a
                    href="https://www.nav.no"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline hover:text-blue-600"
                  >
                    nav.no
                  </a>{" "}
                  eller kontakt NAV direkte.
                </p>
              </div>
            </div>
          </div>

          {/* NAV Benefits Section */}
          <div className="mb-12 rounded-2xl bg-white shadow-lg">
            <div className="border-b border-gray-200 p-6">
              <h2 className="mb-4 text-2xl font-bold text-gray-900">NAV-ytelser</h2>
              <p className="mb-6 text-gray-600">
                Oversikt over de mest vanlige ytelsene fra NAV
              </p>

              {/* Category Filter */}
              <div className="flex flex-wrap gap-2">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                      selectedCategory === cat
                        ? "bg-[var(--color-brand-primary)] text-white"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
                  >
                    {cat !== "Alle" && getCategoryIcon(cat as BenefitCategory)}
                    <span>{cat}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="p-6">
              <div className="space-y-4">
                {filteredBenefits.map((benefit) => (
                  <div
                    key={benefit.id}
                    className="rounded-xl border border-gray-200 bg-white transition-shadow hover:shadow-md"
                  >
                    <button
                      onClick={() =>
                        setExpandedBenefit(expandedBenefit === benefit.id ? null : benefit.id)
                      }
                      className="flex w-full items-start gap-4 p-6 text-left"
                    >
                      <div className="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                        {benefit.icon}
                      </div>
                      <div className="flex-1">
                        <div className="mb-1 flex items-center gap-2">
                          <h3 className="text-lg font-semibold text-gray-900">{benefit.title}</h3>
                          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600">
                            {benefit.category}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">{benefit.description}</p>
                      </div>
                      {expandedBenefit === benefit.id ? (
                        <ChevronDown className="h-5 w-5 flex-shrink-0 text-gray-400" />
                      ) : (
                        <ChevronRight className="h-5 w-5 flex-shrink-0 text-gray-400" />
                      )}
                    </button>

                    {expandedBenefit === benefit.id && (
                      <div className="border-t border-gray-200 bg-gray-50 p-6">
                        <div className="grid gap-6 md:grid-cols-2">
                          <div>
                            <h4 className="mb-2 font-semibold text-gray-900">Hvem kan søke?</h4>
                            <ul className="space-y-1 text-sm text-gray-600">
                              {benefit.whoCanApply.map((item, i) => (
                                <li key={i} className="flex items-start gap-2">
                                  <CheckCircle className="h-4 w-4 flex-shrink-0 text-green-600" />
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          <div>
                            <h4 className="mb-2 font-semibold text-gray-900">Krav</h4>
                            <ul className="space-y-1 text-sm text-gray-600">
                              {benefit.requirements.map((item, i) => (
                                <li key={i} className="flex items-start gap-2">
                                  <AlertCircle className="h-4 w-4 flex-shrink-0 text-blue-600" />
                                  <span>{item}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          <div>
                            <h4 className="mb-2 font-semibold text-gray-900">Beløp</h4>
                            <p className="text-sm text-gray-600">{benefit.amount}</p>
                          </div>

                          <div>
                            <h4 className="mb-2 font-semibold text-gray-900">Varighet</h4>
                            <p className="text-sm text-gray-600">{benefit.duration}</p>
                          </div>
                        </div>

                        {benefit.applyLink && (
                          <div className="mt-4">
                            <a
                              href={benefit.applyLink}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-2 text-sm font-medium text-[var(--color-brand-primary)] hover:underline"
                            >
                              Les mer og søk på nav.no
                              <ChevronRight className="h-4 w-4" />
                            </a>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Your Rights Section */}
          <div className="mb-12 rounded-2xl bg-white shadow-lg">
            <div className="border-b border-gray-200 p-6">
              <h2 className="mb-2 text-2xl font-bold text-gray-900">Dine rettigheter</h2>
              <p className="text-gray-600">Viktige rettigheter du har i kontakt med NAV</p>
            </div>

            <div className="p-6">
              <div className="space-y-4">
                {rights.map((right) => (
                  <div
                    key={right.id}
                    className="rounded-xl border border-gray-200 bg-white transition-shadow hover:shadow-md"
                  >
                    <button
                      onClick={() => setExpandedRight(expandedRight === right.id ? null : right.id)}
                      className="flex w-full items-start gap-4 p-6 text-left"
                    >
                      <Scale className="h-6 w-6 flex-shrink-0 text-indigo-600" />
                      <div className="flex-1">
                        <h3 className="mb-1 text-lg font-semibold text-gray-900">{right.title}</h3>
                        <p className="text-sm text-gray-600">{right.description}</p>
                      </div>
                      {expandedRight === right.id ? (
                        <ChevronDown className="h-5 w-5 flex-shrink-0 text-gray-400" />
                      ) : (
                        <ChevronRight className="h-5 w-5 flex-shrink-0 text-gray-400" />
                      )}
                    </button>

                    {expandedRight === right.id && (
                      <div className="border-t border-gray-200 bg-gray-50 p-6">
                        <ul className="space-y-2 text-sm text-gray-600">
                          {right.details.map((detail, i) => (
                            <li key={i} className="flex items-start gap-2">
                              <CheckCircle className="h-4 w-4 flex-shrink-0 text-green-600" />
                              <span>{detail}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Complaint Process Section */}
          <div className="mb-12 rounded-2xl bg-gradient-to-br from-amber-50 to-orange-50 p-8">
            <div className="mb-6 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-amber-100">
                <FileText className="h-6 w-6 text-amber-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Hvordan klage</h2>
                <p className="text-sm text-gray-600">Trinn-for-trinn guide til klageprosessen</p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="rounded-xl bg-white p-6">
                <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-amber-100 text-sm font-bold text-amber-600">
                  1
                </div>
                <h3 className="mb-2 font-semibold text-gray-900">Send klage</h3>
                <p className="text-sm text-gray-600">
                  Send klage til samme NAV-kontor som fattet vedtaket innen 6 uker
                </p>
              </div>

              <div className="rounded-xl bg-white p-6">
                <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-amber-100 text-sm font-bold text-amber-600">
                  2
                </div>
                <h3 className="mb-2 font-semibold text-gray-900">NAV vurderer</h3>
                <p className="text-sm text-gray-600">
                  NAV vurderer klagen og kan endre vedtaket eller sende saken videre
                </p>
              </div>

              <div className="rounded-xl bg-white p-6">
                <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-full bg-amber-100 text-sm font-bold text-amber-600">
                  3
                </div>
                <h3 className="mb-2 font-semibold text-gray-900">Klageinstans</h3>
                <p className="text-sm text-gray-600">
                  Hvis NAV ikke endrer, sendes saken til NAV Klageinstans som gjør endelig vedtak
                </p>
              </div>
            </div>
          </div>

          {/* Lira CTA */}
          <div className="rounded-2xl border border-gray-200 bg-white p-8">
            <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
              <div className="flex-1">
                <h3 className="mb-2 text-xl font-bold text-gray-900">
                  Trenger du hjelp med rettigheter?
                </h3>
                <p className="text-gray-600">
                  Lira kan hjelpe deg å finne ut hvilke rettigheter og ytelser du har krav på
                </p>
              </div>
              <Button
                variant="primary"
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
    </Layout>
  );
}

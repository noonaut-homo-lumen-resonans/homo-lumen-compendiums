import { NextRequest, NextResponse } from "next/server";

/**
 * Jobs API Route
 *
 * Fetches job listings from Arbeidsplassen.no API
 * Falls back to mock data if API key is not configured
 *
 * To use real data:
 * 1. Contact nav.team.arbeidsplassen@nav.no to get API key
 * 2. Add ARBEIDSPLASSEN_API_KEY to .env.local
 *
 * API Documentation: https://navikt.github.io/pam-stilling-feed/
 */

interface JobAd {
  uuid: string;
  title: string;
  employer: {
    name: string;
    location?: {
      city?: string;
      municipal?: string;
    };
  };
  properties: {
    extent?: string;
    jobtitle?: string;
    workday?: string[];
  };
  published: string;
  expires: string;
  description?: string;
  categoryList?: Array<{
    name: string;
    categoryType: string;
  }>;
}

// Mock data - samme format som Arbeidsplassen.no API
const mockJobs: JobAd[] = [
  {
    uuid: "mock-1",
    title: "Helsefagarbeider",
    employer: {
      name: "Oslo Kommune",
      location: {
        city: "Oslo",
        municipal: "Oslo"
      }
    },
    properties: {
      extent: "Heltid",
      jobtitle: "Helsefagarbeider"
    },
    published: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 20 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Vi søker motiverte helsefagarbeidere til hjemmetjenesten i Oslo vest.",
    categoryList: [
      {
        name: "Helse",
        categoryType: "STYRK08"
      }
    ]
  },
  {
    uuid: "mock-2",
    title: "Butikkmedarbeider",
    employer: {
      name: "Rema 1000",
      location: {
        city: "Bergen",
        municipal: "Bergen"
      }
    },
    properties: {
      extent: "Deltid",
      jobtitle: "Butikkmedarbeider"
    },
    published: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 25 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Deltidsstilling i trivelig butikk. Erfaring ikke nødvendig - vi lærer deg opp!",
    categoryList: [
      {
        name: "Service",
        categoryType: "STYRK08"
      }
    ]
  },
  {
    uuid: "mock-3",
    title: "Junior Utvikler",
    employer: {
      name: "Telenor",
      location: {
        city: "Fornebu",
        municipal: "Bærum"
      }
    },
    properties: {
      extent: "Heltid",
      jobtitle: "Systemutvikler"
    },
    published: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 35 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Nyutdannet? Vi tilbyr trainee-program for junior utviklere med fokus på skyteknologi.",
    categoryList: [
      {
        name: "Teknologi",
        categoryType: "STYRK08"
      }
    ]
  },
  {
    uuid: "mock-4",
    title: "Rørlegger",
    employer: {
      name: "VVS-Service AS",
      location: {
        city: "Trondheim",
        municipal: "Trondheim"
      }
    },
    properties: {
      extent: "Heltid",
      jobtitle: "Rørlegger"
    },
    published: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Erfaren rørlegger til veletablert bedrift. Gode betingelser og firmabil.",
    categoryList: [
      {
        name: "Håndverk",
        categoryType: "STYRK08"
      }
    ]
  },
  {
    uuid: "mock-5",
    title: "Kontormedarbeider",
    employer: {
      name: "Statens Vegvesen",
      location: {
        city: "Stavanger",
        municipal: "Stavanger"
      }
    },
    properties: {
      extent: "Midlertidig",
      jobtitle: "Kontormedarbeider"
    },
    published: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Vikariat i 6 måneder med mulighet for fast ansettelse. God kjennskap til Office 365 ønskelig.",
    categoryList: [
      {
        name: "Kontor",
        categoryType: "STYRK08"
      }
    ]
  },
  {
    uuid: "mock-6",
    title: "Sykepleier",
    employer: {
      name: "Haukeland Sykehus",
      location: {
        city: "Bergen",
        municipal: "Bergen"
      }
    },
    properties: {
      extent: "Heltid",
      jobtitle: "Sykepleier"
    },
    published: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    expires: new Date(Date.now() + 23 * 24 * 60 * 60 * 1000).toISOString(),
    description: "Autoriserte sykepleiere til kirurgisk avdeling. Fast turnus og gode utviklingsmuligheter.",
    categoryList: [
      {
        name: "Helse",
        categoryType: "STYRK08"
      }
    ]
  }
];

async function fetchFromArbeidsplassen(
  page: number = 0,
  size: number = 10,
  searchTerm?: string,
  category?: string
): Promise<{ content: JobAd[]; totalElements: number; useMockData: boolean }> {
  const apiKey = process.env.ARBEIDSPLASSEN_API_KEY;

  // If no API key, return mock data
  if (!apiKey || apiKey === "") {
    console.log("No Arbeidsplassen API key found, using mock data");
    let filteredJobs = [...mockJobs];

    // Apply filters to mock data
    if (searchTerm && searchTerm.trim() !== "") {
      const searchLower = searchTerm.toLowerCase();
      filteredJobs = filteredJobs.filter(
        (job) =>
          job.title.toLowerCase().includes(searchLower) ||
          job.employer.name.toLowerCase().includes(searchLower) ||
          job.employer.location?.city?.toLowerCase().includes(searchLower)
      );
    }

    if (category && category !== "Alle") {
      filteredJobs = filteredJobs.filter((job) =>
        job.categoryList?.some((cat) => cat.name === category)
      );
    }

    return {
      content: filteredJobs,
      totalElements: filteredJobs.length,
      useMockData: true
    };
  }

  // Try to fetch from real API
  try {
    const baseUrl = "https://arbeidsplassen.api.no/public-feed/api/v1/ads";
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
    });

    if (searchTerm) {
      params.append("q", searchTerm);
    }

    const response = await fetch(`${baseUrl}?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
        Accept: "application/json",
      },
      cache: "no-store", // Don't cache for fresh data
    });

    if (!response.ok) {
      console.error("Arbeidsplassen API error:", response.status, response.statusText);
      throw new Error(`API request failed: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      content: data.content || [],
      totalElements: data.totalElements || 0,
      useMockData: false
    };
  } catch (error) {
    console.error("Failed to fetch from Arbeidsplassen API, falling back to mock data:", error);

    // Fallback to mock data on error
    let filteredJobs = [...mockJobs];

    if (searchTerm && searchTerm.trim() !== "") {
      const searchLower = searchTerm.toLowerCase();
      filteredJobs = filteredJobs.filter(
        (job) =>
          job.title.toLowerCase().includes(searchLower) ||
          job.employer.name.toLowerCase().includes(searchLower) ||
          job.employer.location?.city?.toLowerCase().includes(searchLower)
      );
    }

    if (category && category !== "Alle") {
      filteredJobs = filteredJobs.filter((job) =>
        job.categoryList?.some((cat) => cat.name === category)
      );
    }

    return {
      content: filteredJobs,
      totalElements: filteredJobs.length,
      useMockData: true
    };
  }
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const page = parseInt(searchParams.get("page") || "0");
    const size = parseInt(searchParams.get("size") || "10");
    const searchTerm = searchParams.get("q") || undefined;
    const category = searchParams.get("category") || undefined;

    const result = await fetchFromArbeidsplassen(page, size, searchTerm, category);

    return NextResponse.json(result);
  } catch (error) {
    console.error("Error in jobs API route:", error);
    return NextResponse.json(
      {
        error: "Failed to fetch job listings",
        content: [],
        totalElements: 0,
        useMockData: true
      },
      { status: 500 }
    );
  }
}

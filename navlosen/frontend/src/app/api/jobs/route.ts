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

interface FilterParams {
  page?: number;
  size?: number;
  searchTerm?: string;
  category?: string;
  jobType?: string;
  location?: string;
  experienceLevel?: string;
  deadline?: string;
  sortBy?: string;
}

async function fetchFromArbeidsplassen(
  filters: FilterParams
): Promise<{ content: JobAd[]; totalElements: number; useMockData: boolean }> {
  const apiKey = process.env.ARBEIDSPLASSEN_API_KEY;
  const { page = 0, size = 10, searchTerm, category, jobType, location, experienceLevel, deadline, sortBy } = filters;

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

    // Job type filter
    if (jobType && jobType !== "Alle") {
      filteredJobs = filteredJobs.filter((job) =>
        job.properties.extent === jobType
      );
    }

    // Location filter
    if (location && location.trim() !== "") {
      const locationLower = location.toLowerCase();
      filteredJobs = filteredJobs.filter((job) =>
        job.employer.location?.city?.toLowerCase().includes(locationLower) ||
        job.employer.location?.municipal?.toLowerCase().includes(locationLower)
      );
    }

    // Deadline filter
    if (deadline) {
      const now = new Date();
      filteredJobs = filteredJobs.filter((job) => {
        const expiresDate = new Date(job.expires);
        const daysUntilExpiry = Math.ceil((expiresDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

        switch (deadline) {
          case 'today':
            return daysUntilExpiry === 0;
          case 'week':
            return daysUntilExpiry <= 7;
          case 'month':
            return daysUntilExpiry <= 30;
          case 'later':
            return daysUntilExpiry > 30;
          default:
            return true;
        }
      });
    }

    // Sorting
    if (sortBy) {
      const now = new Date();
      filteredJobs.sort((a, b) => {
        switch (sortBy) {
          case 'newest':
            return new Date(b.published).getTime() - new Date(a.published).getTime();
          case 'deadline':
            return new Date(a.expires).getTime() - new Date(b.expires).getTime();
          case 'relevant':
          default:
            // Keep original order (most relevant based on search)
            return 0;
        }
      });
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

    if (location) {
      params.append("location", location);
    }

    if (jobType && jobType !== "Alle") {
      params.append("extent", jobType);
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

    // Apply client-side filters not supported by API
    let jobs = data.content || [];

    if (category && category !== "Alle") {
      jobs = jobs.filter((job: JobAd) =>
        job.categoryList?.some((cat) => cat.name === category)
      );
    }

    if (deadline) {
      const now = new Date();
      jobs = jobs.filter((job: JobAd) => {
        const expiresDate = new Date(job.expires);
        const daysUntilExpiry = Math.ceil((expiresDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

        switch (deadline) {
          case 'today':
            return daysUntilExpiry === 0;
          case 'week':
            return daysUntilExpiry <= 7;
          case 'month':
            return daysUntilExpiry <= 30;
          case 'later':
            return daysUntilExpiry > 30;
          default:
            return true;
        }
      });
    }

    // Sorting
    if (sortBy) {
      jobs.sort((a: JobAd, b: JobAd) => {
        switch (sortBy) {
          case 'newest':
            return new Date(b.published).getTime() - new Date(a.published).getTime();
          case 'deadline':
            return new Date(a.expires).getTime() - new Date(b.expires).getTime();
          case 'relevant':
          default:
            return 0;
        }
      });
    }

    return {
      content: jobs,
      totalElements: jobs.length,
      useMockData: false
    };
  } catch (error) {
    console.error("Failed to fetch from Arbeidsplassen API, falling back to mock data:", error);

    // Fallback to mock data on error - use same filtering logic as above
    return fetchFromArbeidsplassen({ ...filters, page, size });
  }
}

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;

    const filters: FilterParams = {
      page: parseInt(searchParams.get("page") || "0"),
      size: parseInt(searchParams.get("size") || "10"),
      searchTerm: searchParams.get("q") || undefined,
      category: searchParams.get("category") || undefined,
      jobType: searchParams.get("jobType") || undefined,
      location: searchParams.get("location") || undefined,
      experienceLevel: searchParams.get("experienceLevel") || undefined,
      deadline: searchParams.get("deadline") || undefined,
      sortBy: searchParams.get("sortBy") || undefined,
    };

    const result = await fetchFromArbeidsplassen(filters);

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

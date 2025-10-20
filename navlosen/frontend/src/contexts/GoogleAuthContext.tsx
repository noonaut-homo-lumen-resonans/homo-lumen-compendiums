"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

interface GoogleUser {
  id: string;
  email: string;
  name: string;
  picture: string;
}

interface GoogleAuthContextType {
  user: GoogleUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signInWithGoogle: () => Promise<void>;
  signOut: () => void;
  hasCalendarAccess: boolean;
  hasGmailAccess: boolean;
  requestCalendarAccess: () => Promise<void>;
  requestGmailAccess: () => Promise<void>;
}

const GoogleAuthContext = createContext<GoogleAuthContextType | undefined>(undefined);

export function GoogleAuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<GoogleUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [hasCalendarAccess, setHasCalendarAccess] = useState(false);
  const [hasGmailAccess, setHasGmailAccess] = useState(false);

  // Load user from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUser = localStorage.getItem("navlosen_google_user");
      const storedCalendarAccess = localStorage.getItem("navlosen_google_calendar_access");
      const storedGmailAccess = localStorage.getItem("navlosen_google_gmail_access");

      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (err) {
          console.error("Failed to parse stored user:", err);
        }
      }

      if (storedCalendarAccess === "true") {
        setHasCalendarAccess(true);
      }

      if (storedGmailAccess === "true") {
        setHasGmailAccess(true);
      }

      setIsLoading(false);
    }
  }, []);

  // Save user to localStorage
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (user) {
        localStorage.setItem("navlosen_google_user", JSON.stringify(user));
      } else {
        localStorage.removeItem("navlosen_google_user");
      }
    }
  }, [user]);

  const signInWithGoogle = async () => {
    // Mock implementation - in production, this would use Google OAuth
    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const mockUser: GoogleUser = {
      id: "mock_user_id",
      email: "bruker@example.com",
      name: "Demo Bruker",
      picture: "https://via.placeholder.com/150",
    };

    setUser(mockUser);
    setIsLoading(false);

    // Show info about mock mode
    alert(
      "Demo-modus: Google-innlogging\n\n" +
      "Dette er en demonstrasjon av Google-innlogging.\n\n" +
      "I produksjon ville dette:\n" +
      "• Åpne Google OAuth-vindu\n" +
      "• Be om brukerens samtykke\n" +
      "• Returnere ekte brukerdata\n\n" +
      "For å aktivere ekte Google-integrasjon, trenger du:\n" +
      "1. Google Cloud Project\n" +
      "2. OAuth 2.0 credentials\n" +
      "3. Backend for token-håndtering"
    );
  };

  const signOut = () => {
    setUser(null);
    setHasCalendarAccess(false);
    setHasGmailAccess(false);

    if (typeof window !== "undefined") {
      localStorage.removeItem("navlosen_google_user");
      localStorage.removeItem("navlosen_google_calendar_access");
      localStorage.removeItem("navlosen_google_gmail_access");
    }
  };

  const requestCalendarAccess = async () => {
    if (!user) {
      alert("Vennligst logg inn med Google først");
      return;
    }

    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    setHasCalendarAccess(true);

    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen_google_calendar_access", "true");
    }

    setIsLoading(false);

    alert(
      "Demo-modus: Google Calendar-tilgang\n\n" +
      "Tilgang til Google Calendar er nå aktivert.\n\n" +
      "I produksjon ville dette:\n" +
      "• Be om tillatelse til å lese/skrive kalenderhendelser\n" +
      "• Få OAuth-token med calendar.events scope\n" +
      "• Synkronisere påminnelser med din Google Calendar\n\n" +
      "Påminnelser vil nå kunne synkroniseres med kalenderen din."
    );
  };

  const requestGmailAccess = async () => {
    if (!user) {
      alert("Vennligst logg inn med Google først");
      return;
    }

    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    setHasGmailAccess(true);

    if (typeof window !== "undefined") {
      localStorage.setItem("navlosen_google_gmail_access", "true");
    }

    setIsLoading(false);

    alert(
      "Demo-modus: Gmail-tilgang\n\n" +
      "Tilgang til Gmail er nå aktivert.\n\n" +
      "I produksjon ville dette:\n" +
      "• Be om tillatelse til å sende/lese e-post\n" +
      "• Få OAuth-token med gmail.send og gmail.readonly scopes\n" +
      "• Kunne sende jobbsøknader via Gmail\n" +
      "• Spore e-postkommunikasjon med arbeidsgivere\n\n" +
      "Du kan nå sende jobbsøknader via Gmail."
    );
  };

  const value: GoogleAuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    signInWithGoogle,
    signOut,
    hasCalendarAccess,
    hasGmailAccess,
    requestCalendarAccess,
    requestGmailAccess,
  };

  return (
    <GoogleAuthContext.Provider value={value}>
      {children}
    </GoogleAuthContext.Provider>
  );
}

export function useGoogleAuth() {
  const context = useContext(GoogleAuthContext);
  if (context === undefined) {
    throw new Error("useGoogleAuth must be used within a GoogleAuthProvider");
  }
  return context;
}

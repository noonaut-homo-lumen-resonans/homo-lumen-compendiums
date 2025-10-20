"use client";

import { GoogleAuthProvider } from "@/contexts/GoogleAuthContext";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <GoogleAuthProvider>
      {children}
    </GoogleAuthProvider>
  );
}

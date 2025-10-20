/**
 * NAV-Losen Dashboard Landing Page
 *
 * @version 1.0
 * @date 2025-10-20
 * @author Code (Agent #9) - Homo Lumen Coalition
 */

import { Metadata } from 'next';
import { Hero } from '@/components/landing/Hero';
import { AboutSection } from '@/components/landing/AboutSection';
import { LiraSection } from '@/components/landing/LiraSection';
import { QDALayersSection } from '@/components/landing/QDALayersSection';
import { TechSection } from '@/components/landing/TechSection';
import { CTASection } from '@/components/landing/CTASection';
import { Footer } from '@/components/landing/Footer';

export const metadata: Metadata = {
  title: 'NAV-Losen Dashboard | AI-drevet Mental Helsestøtte i Tvedestrand',
  description:
    'Utforsk QDA v2.0 - en nevrobiologisk AI-modell for empatisk mental helsestøtte til NAV-brukere. Pilotprosjekt i Tvedestrand bygget på Polyvagal Theory og Triadisk Ethics.',
  keywords: [
    'NAV-Losen',
    'Lira',
    'QDA v2.0',
    'mental helse',
    'AI',
    'Tvedestrand',
    'Homo Lumen',
    'Polyvagal Theory',
    'Triadisk Ethics',
    'kognitiv suverenitet',
    'nevrobiologi',
  ],
  authors: [
    {
      name: 'Osvald P. A. Johansen',
      url: 'mailto:osvald@cognivesovereignty.network',
    },
  ],
  openGraph: {
    title: 'NAV-Losen Dashboard - AI-drevet Mental Helsestøtte',
    description:
      'AI-drevet støtte for mental helse bygget på empati og nevrobiologi. Pilotprosjekt i Tvedestrand.',
    type: 'website',
    locale: 'no_NO',
    siteName: 'NAV-Losen',
    images: [
      {
        url: '/logo-koalisjonen.png',
        width: 200,
        height: 200,
        alt: 'Homo Lumen Koalisjonen Logo',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'NAV-Losen Dashboard',
    description:
      'AI-drevet mental helsestøtte bygget på empati og nevrobiologi.',
    images: ['/logo-koalisjonen.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
  },
};

export default function DashboardPage() {
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <Hero />

      {/* About NAV-Losen */}
      <AboutSection />

      {/* Meet Lira */}
      <LiraSection />

      {/* QDA v2.0 - 6 Layers */}
      <QDALayersSection />

      {/* Technology & Safety */}
      <TechSection />

      {/* Call to Action */}
      <CTASection />

      {/* Footer */}
      <Footer />

      {/* Structured Data (JSON-LD) */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'SoftwareApplication',
            name: 'NAV-Losen',
            description:
              'AI-drevet mental helsestøtte for NAV-brukere bygget på Polyvagal Theory og Triadisk Ethics',
            applicationCategory: 'HealthApplication',
            operatingSystem: 'Web',
            offers: {
              '@type': 'Offer',
              price: '0',
              priceCurrency: 'NOK',
            },
            creator: {
              '@type': 'Organization',
              name: 'Homo Lumen Coalition',
              contactPoint: {
                '@type': 'ContactPoint',
                contactType: 'Project Manager',
                email: 'osvald@cognivesovereignty.network',
                telephone: '+47-919-21-736',
              },
            },
            featureList: [
              'Nevrobiologisk QDA v2.0 AI-modell',
              '100% nøyaktig faredeteksjon',
              'Polyvagal-adaptiv kommunikasjon',
              'GDPR-compliant personvern',
              'Triadisk Ethics validering',
            ],
          }),
        }}
      />
    </main>
  );
}

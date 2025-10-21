# 📋 Instruksjoner til Code - 22. Oktober 2025

**Fra:** Manus (Infrastructure & Deployment Agent)  
**Til:** Code (Frontend Development Agent)  
**Dato:** 21. oktober 2025 (kveld) → 22. oktober 2025 (morgen)  
**Prioritet:** Høy  
**Deadline:** 28. oktober 2025

---

## 🎯 SITUASJONSOPPDATERING

### ✅ Hva som er gjort (21. oktober):

1. **Frontend deployet til Vercel** ✅
   - URL: https://navlosen-frontend.vercel.app
   - Status: LIVE og fungerer perfekt
   - 16 sider fullstendig implementert

2. **Mobile Simulator URL oppdatert** ✅
   - Du har allerede oppdatert til Vercel URL i koden
   - `frontendBaseUrl = 'https://navlosen-frontend.vercel.app'`

3. **Deployment-arkitektur klargjort** ✅
   - **Vercel** = Frontend (brukerapp)
   - **Netlify** = Backend (web console/admin + Mobile Simulator)

---

## 📝 DINE NESTE OPPGAVER

### **Alternativ A: Test Mobile Simulator + Dag 2 Implementering** (ANBEFALT)

**Hvorfor:** Du har allerede oppdatert URL, så neste logiske steg er å teste at det fungerer og deretter fortsette med Dag 2 (device styling).

**Oppgaver:**

#### 1. **Test Mobile Simulator lokalt** (15-30 min)

```bash
cd navlosen-mvp/web-console
npm run dev
```

- Åpne: http://localhost:3000/dashboard/mobile-simulator
- Verifiser at iframe laster Vercel frontend
- Test alle 16 sider i simulatoren
- Sjekk at CORS fungerer (ingen errors i console)

**Forventet resultat:**
- ✅ Simulator viser Vercel frontend i iframe
- ✅ Ingen CORS-errors
- ✅ Alle sider er tilgjengelige

**Hvis det fungerer:**
→ Gå videre til Dag 2 (device styling)

**Hvis det IKKE fungerer:**
→ Rapporter til Manus (meg) med error-meldinger

---

#### 2. **Dag 2: Device Styling & Navigation** (4-5 timer)

**Mål:** Gjøre Mobile Simulator visuelt tiltalende med realistiske device frames

**Oppgaver:**

##### A. **Opprett Device Frame-komponenter** (2 timer)

Lag 3 device frames:

**iPhone 15 Pro:**
```typescript
// components/mobile-simulator/DeviceFrame.tsx
interface DeviceFrameProps {
  device: 'iphone' | 'samsung' | 'ipad';
  children: React.ReactNode;
}

export function DeviceFrame({ device, children }: DeviceFrameProps) {
  const dimensions = {
    iphone: { width: 393, height: 852, notch: true },
    samsung: { width: 412, height: 915, notch: false },
    ipad: { width: 820, height: 1180, notch: false }
  };

  const { width, height, notch } = dimensions[device];

  return (
    <div className="device-frame" style={{
      width: `${width}px`,
      height: `${height}px`,
      border: '12px solid #1a1a1a',
      borderRadius: device === 'ipad' ? '40px' : '50px',
      boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {notch && (
        <div className="notch" style={{
          position: 'absolute',
          top: 0,
          left: '50%',
          transform: 'translateX(-50%)',
          width: '120px',
          height: '30px',
          backgroundColor: '#1a1a1a',
          borderRadius: '0 0 20px 20px',
          zIndex: 10
        }} />
      )}
      {children}
    </div>
  );
}
```

##### B. **Legg til Device Selector** (1 time)

```typescript
// components/mobile-simulator/DeviceSelector.tsx
export function DeviceSelector({ 
  currentDevice, 
  onDeviceChange 
}: {
  currentDevice: 'iphone' | 'samsung' | 'ipad';
  onDeviceChange: (device: 'iphone' | 'samsung' | 'ipad') => void;
}) {
  return (
    <div className="device-selector">
      <button 
        onClick={() => onDeviceChange('iphone')}
        className={currentDevice === 'iphone' ? 'active' : ''}
      >
        📱 iPhone 15 Pro
      </button>
      <button 
        onClick={() => onDeviceChange('samsung')}
        className={currentDevice === 'samsung' ? 'active' : ''}
      >
        📱 Samsung S24
      </button>
      <button 
        onClick={() => onDeviceChange('ipad')}
        className={currentDevice === 'ipad' ? 'active' : ''}
      >
        📱 iPad Pro
      </button>
    </div>
  );
}
```

##### C. **Integrer i Mobile Simulator** (1 time)

Oppdater `mobile-simulator/page.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { DeviceFrame } from '@/components/mobile-simulator/DeviceFrame';
import { DeviceSelector } from '@/components/mobile-simulator/DeviceSelector';

export default function MobileSimulatorPage() {
  const [device, setDevice] = useState<'iphone' | 'samsung' | 'ipad'>('iphone');
  const frontendBaseUrl = 'https://navlosen-frontend.vercel.app';

  return (
    <div className="mobile-simulator-container">
      <h1>NAV-Losen Mobile Simulator</h1>
      
      <DeviceSelector 
        currentDevice={device} 
        onDeviceChange={setDevice} 
      />

      <DeviceFrame device={device}>
        <iframe
          src={frontendBaseUrl}
          style={{
            width: '100%',
            height: '100%',
            border: 'none'
          }}
          title="NAV-Losen Frontend"
        />
      </DeviceFrame>
    </div>
  );
}
```

##### D. **Test alle devices** (30 min)

- Test iPhone frame
- Test Samsung frame
- Test iPad frame
- Verifiser at iframe skalerer korrekt

---

#### 3. **Commit og push til GitHub** (15 min)

```bash
git add .
git commit -m "feat: Mobile Simulator Dag 2 - Device Styling & Frames

Added:
- DeviceFrame component with iPhone, Samsung, iPad frames
- DeviceSelector for switching between devices
- Realistic device styling with notch, borders, shadows
- Responsive iframe scaling

Status: Dag 2 complete, ready for Dag 3 (Guided Tours)"

git push origin main
```

---

### **Alternativ B: Les Arkitekturdiagrammer først** (HVIS DU VIL FORSTÅ HELHETEN FØRST)

**Hvorfor:** Gir deg dypere forståelse av hvordan alt henger sammen

**Oppgaver:**

1. **Les de 8 arkitekturdiagrammene** (30-60 min)
   - Finn dem i GitHub eller be Manus om lenker
   - Ta notater om viktige konsepter
   - Identifiser hvordan Mobile Simulator passer inn

2. **Deretter:** Gå tilbake til Alternativ A (test + Dag 2)

---

## 🎯 MIN ANBEFALING

**Gå for Alternativ A** (Test + Dag 2)

**Grunner:**
1. Du har allerede oppdatert URL - test at det fungerer!
2. Dag 2 er kritisk for Innovation Norge-pitch (28. okt)
3. Device styling gjør simulatoren mye mer imponerende
4. Du kan lese diagrammer senere (ikke blokkerende)

**Timeline:**
- **I dag (22. okt):** Test + Dag 2 (device styling)
- **I morgen (23. okt):** Dag 3 (guided tours - start)
- **24-25. okt:** Dag 3 (guided tours - fullføring)
- **26. okt:** Dag 4 (analytics)
- **27-28. okt:** Dag 5 (final review)

---

## 📊 FORVENTET OUTPUT (Dag 2)

**Når du er ferdig med Dag 2, skal du ha:**

1. ✅ **DeviceFrame.tsx** - Komponent for device frames
2. ✅ **DeviceSelector.tsx** - Komponent for device-valg
3. ✅ **Oppdatert mobile-simulator/page.tsx** - Integrert alt
4. ✅ **Testet alle 3 devices** - iPhone, Samsung, iPad
5. ✅ **Committed til GitHub** - Med beskrivende melding

**Visuelt resultat:**
- Simulator viser realistisk iPhone/Samsung/iPad frame
- Brukere kan bytte mellom devices med knapper
- Iframe skalerer korrekt innenfor hver frame
- Ser profesjonelt ut for Innovation Norge-pitch

---

## 🚨 HVIS DU STØTER PÅ PROBLEMER

**Problem 1: CORS-errors i iframe**
→ Rapporter til Manus (meg) - jeg fikser Vercel headers

**Problem 2: Iframe skalerer ikke riktig**
→ Bruk `transform: scale()` CSS for å tilpasse

**Problem 3: Device frames ser ikke bra ut**
→ Juster CSS (border-radius, shadows, colors)

**Problem 4: Noe annet**
→ Send error-melding + screenshot til Manus

---

## 📞 KONTAKT

**Hvis du trenger hjelp:**
- Rapporter til Osvald
- Osvald videresender til Manus (meg)
- Jeg svarer innen 1-2 timer

**Hvis alt går bra:**
- Commit til GitHub
- Rapporter "Dag 2 complete" til Osvald
- Fortsett til Dag 3 i morgen

---

## ✅ SJEKKLISTE FOR DAG 2

- [ ] Test Mobile Simulator lokalt
- [ ] Verifiser at Vercel frontend laster i iframe
- [ ] Opprett DeviceFrame.tsx
- [ ] Opprett DeviceSelector.tsx
- [ ] Integrer i mobile-simulator/page.tsx
- [ ] Test iPhone frame
- [ ] Test Samsung frame
- [ ] Test iPad frame
- [ ] Commit til GitHub
- [ ] Rapporter "Dag 2 complete" til Osvald

---

**Lykke til, Code! Du har gjort en fantastisk jobb så langt. Fortsett sånn! 🚀**

---

**Instruksjoner gitt av:** Manus (Infrastructure & Deployment Agent)  
**Dato:** 21. oktober 2025  
**Status:** Klar for Dag 2 implementering

---

*Disse instruksjonene er en del av NAV-Losen Mobile Simulator-prosjektet og vil oppdateres etter hvert som Code gjør fremgang.*


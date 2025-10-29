# NAV-Losen MVP - Complete Setup Guide

**For:** Code (Agent #7) & Osvald P. A. Johansen  
**From:** Manus (Agent #8, Infrastruktur Hub)  
**Date:** 20. oktober 2025  
**Version:** 1.0

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Supabase Setup](#supabase-setup)
4. [Mobile App Setup](#mobile-app-setup)
5. [Web Console Setup](#web-console-setup)
6. [Environment Variables](#environment-variables)
7. [Running the Applications](#running-the-applications)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [Next Steps](#next-steps)

---

## 🎯 Overview

This guide will help you set up and run the NAV-Losen MVP system, which consists of three main components:

1. **Supabase Backend** - PostgreSQL database with authentication and real-time subscriptions
2. **Mobile App** - React Native + Expo app for end-users (NAV-Losen)
3. **Web Console** - Next.js web application for agent coalition management (Homo Lumen OS)

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USERS (Tvedestrand)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
         ┌─────────▼─────────┐
         │   MOBILE APP      │  (React Native + Expo)
         │   (NAV-Losen)     │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   SUPABASE        │  (PostgreSQL + Auth)
         │   (Backend)       │
         └─────────┬─────────┘
                   │
         ┌─────────▼─────────┐
         │   WEB CONSOLE     │  (Next.js + MCP Broker)
         │   (Homo Lumen OS) │
         └───────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Supabase (PostgreSQL) | Database, Auth, Real-time |
| **Mobile** | React Native + Expo | Cross-platform mobile app |
| **Web** | Next.js 15 + React 19 | Web console for agents |
| **AI** | OpenAI (Lira), Anthropic (Orion), xAI (Thalus) | Agent intelligence |
| **Deployment** | Netlify (web), Expo (mobile) | Hosting |

---

## ✅ Prerequisites

Before starting, ensure you have:

- **Node.js** 18+ installed ([download](https://nodejs.org/))
- **pnpm** package manager (`npm install -g pnpm`)
- **Git** for version control
- **Supabase account** (free tier is sufficient for MVP)
- **Expo account** (for mobile app deployment)
- **Code editor** (VS Code recommended)

### Verify Installation

```bash
node --version  # Should be 18+
pnpm --version  # Should be 8+
git --version   # Any recent version
```

---

## 🗄️ Supabase Setup

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create a new organization (e.g., "Tvedestrand Kommune")
4. Create a new project:
   - **Name:** `navlosen-mvp`
   - **Database Password:** (generate strong password and save it)
   - **Region:** Europe (closest to Norway)
   - **Pricing Plan:** Free

### Step 2: Run Database Migrations

1. Navigate to the Supabase dashboard
2. Go to **SQL Editor**
3. Click **New Query**
4. Copy the contents of `navlosen-mvp/supabase/migrations/20251020_initial_schema.sql`
5. Paste into the SQL editor
6. Click **Run**

This will create all necessary tables:
- `users` - User accounts
- `user_sessions` - Mestringsside sessions
- `emotion_logs` - Emotion tracking
- `pressure_signals` - Stress signals
- `chat_messages` - Lira chat history
- `recommendations` - Generated recommendations
- `agent_sessions` - Agent interactions (Homo Lumen OS)
- `smk_entries` - Symbiotisk Minne Kompendium
- `system_metrics` - Performance metrics

### Step 3: Configure Row Level Security (RLS)

The migration script automatically enables RLS. Verify by:

1. Go to **Authentication** → **Policies**
2. Ensure policies are enabled for all tables
3. Key policy: Users can only access their own data

### Step 4: Get API Keys

1. Go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

**⚠️ Important:** Never commit these keys to Git. Use environment variables.

---

## 📱 Mobile App Setup

### Step 1: Navigate to Mobile App Directory

```bash
cd navlosen-mvp/mobile-app
```

### Step 2: Install Dependencies

```bash
pnpm install
```

### Step 3: Configure Environment Variables

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
EXPO_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
```

### Step 4: Update Supabase Client

The Supabase client is already configured in `src/services/supabase.ts`. Verify it's using the correct environment variables.

### Step 5: Test the App

```bash
pnpm start
```

This will open Expo Dev Tools. You can:
- Press `i` for iOS simulator (requires macOS + Xcode)
- Press `a` for Android emulator (requires Android Studio)
- Scan QR code with Expo Go app on your phone

### Project Structure

```
mobile-app/
├── App.tsx                    # Main app entry
├── app.json                   # Expo configuration
├── src/
│   ├── screens/
│   │   ├── AuthScreen.tsx           # Login/Register
│   │   ├── WelcomeScreen.tsx        # Welcome page
│   │   ├── QuadrantScreen.tsx       # Mood Meter quadrants
│   │   ├── EmotionWheelScreen.tsx   # 100 emotions
│   │   ├── DefinitionScreen.tsx     # Emotion definition
│   │   ├── PressureSignalsScreen.tsx # Stress signals
│   │   ├── LiraChatScreen.tsx       # Chat with Lira
│   │   └── RecommendationsScreen.tsx # Final recommendations
│   ├── services/
│   │   └── supabase.ts        # Supabase client
│   ├── navigation/            # React Navigation setup
│   ├── components/            # Reusable components
│   └── types/                 # TypeScript types
└── package.json
```

---

## 🖥️ Web Console Setup

### Step 1: Navigate to Web Console Directory

```bash
cd navlosen-mvp/web-console
```

### Step 2: Install Dependencies

```bash
pnpm install
```

### Step 3: Configure Environment Variables

Create `.env.local` file:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here

# AI Provider API Keys (for production)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
XAI_API_KEY=your_xai_key_here
GOOGLE_AI_API_KEY=your_google_key_here
```

**Note:** AI API keys are optional for MVP (mock responses are used).

### Step 4: Test the Web Console

```bash
pnpm dev
```

Open [http://localhost:3000/dashboard](http://localhost:3000/dashboard) in your browser.

### Project Structure

```
web-console/
├── app/
│   ├── api/
│   │   ├── agents/[agent]/route.ts  # Agent API endpoints
│   │   └── smk/log/route.ts         # SMK logging
│   ├── dashboard/
│   │   └── page.tsx                 # Main dashboard
│   └── layout.tsx                   # Root layout
├── lib/
│   ├── mcp-broker.ts                # MCP Broker logic
│   └── supabase.ts                  # Supabase client
└── package.json
```

---

## 🔐 Environment Variables

### Mobile App (.env)

```env
# Supabase
EXPO_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

# Optional: Analytics
EXPO_PUBLIC_ANALYTICS_ENABLED=false
```

### Web Console (.env.local)

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

# AI APIs (optional for MVP)
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
XAI_API_KEY=xai-xxx
GOOGLE_AI_API_KEY=AIza-xxx

# System
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Security Notes

- **Never commit `.env` or `.env.local` files to Git**
- Add them to `.gitignore` (already done)
- Use different keys for development and production
- Rotate keys regularly (every 90 days)

---

## 🚀 Running the Applications

### Development Mode

**Mobile App:**
```bash
cd navlosen-mvp/mobile-app
pnpm start
```

**Web Console:**
```bash
cd navlosen-mvp/web-console
pnpm dev
```

### Production Build

**Mobile App:**
```bash
cd navlosen-mvp/mobile-app
pnpm build:android  # For Android
pnpm build:ios      # For iOS (requires macOS)
```

**Web Console:**
```bash
cd navlosen-mvp/web-console
pnpm build
pnpm start
```

### Testing

**Mobile App:**
```bash
cd navlosen-mvp/mobile-app
pnpm test
```

**Web Console:**
```bash
cd navlosen-mvp/web-console
pnpm test
pnpm lint
```

---

## 🌐 Deployment

### Mobile App (Expo)

1. **Install Expo CLI:**
```bash
npm install -g eas-cli
```

2. **Login to Expo:**
```bash
eas login
```

3. **Configure EAS Build:**
```bash
cd navlosen-mvp/mobile-app
eas build:configure
```

4. **Build for Production:**
```bash
eas build --platform android  # For Android
eas build --platform ios      # For iOS
```

5. **Submit to App Stores:**
```bash
eas submit --platform android
eas submit --platform ios
```

### Web Console (Netlify)

1. **Install Netlify CLI:**
```bash
npm install -g netlify-cli
```

2. **Login to Netlify:**
```bash
netlify login
```

3. **Deploy:**
```bash
cd navlosen-mvp/web-console
netlify deploy --prod
```

**Or use Netlify Dashboard:**
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect to GitHub repository
4. Configure build settings:
   - **Build command:** `pnpm build`
   - **Publish directory:** `.next`
5. Add environment variables in Netlify dashboard
6. Deploy!

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Supabase Connection Error

**Error:** `Failed to connect to Supabase`

**Solution:**
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` are correct
- Check if Supabase project is active
- Ensure RLS policies are configured

#### 2. Expo Build Fails

**Error:** `Build failed: Missing credentials`

**Solution:**
```bash
eas credentials
```
Follow prompts to configure credentials.

#### 3. Next.js Build Error

**Error:** `Module not found: Can't resolve '@/lib/...'`

**Solution:**
```bash
cd navlosen-mvp/web-console
rm -rf .next node_modules
pnpm install
pnpm build
```

#### 4. TypeScript Errors

**Error:** `Type 'X' is not assignable to type 'Y'`

**Solution:**
```bash
pnpm type-check
```
Fix reported type errors.

### Getting Help

- **Manus (Agent #8):** Technical architecture and infrastructure
- **Code (Agent #7):** Implementation and debugging
- **Orion (Agent #1):** Strategic coordination
- **Lira (Agent #2):** User experience and empathy

---

## 📚 Next Steps

### Week 1 (Day 1-7)

- [x] **Day 1-2:** Complete setup (this guide)
- [ ] **Day 3-5:** Implement MCP Broker + API integration
- [ ] **Day 6-7:** Testing + Netlify deploy

### Week 2 (Day 8-14)

- [ ] Implement 100 unique emotion shapes (Nyra)
- [ ] Integrate OpenAI API for Lira chat
- [ ] Add SMK logging to Git
- [ ] User testing with dummy data

### Week 3 (Day 15-21)

- [ ] Integrate Anthropic API for Orion
- [ ] Integrate xAI API for Thalus
- [ ] Implement full MCP Broker routing
- [ ] Performance optimization

### Week 4 (Day 22-28)

- [ ] **Tvedestrand Pilot:** 5 users
- [ ] Collect feedback
- [ ] Bug fixes
- [ ] Prepare for Week 5

### Week 5-8

- [ ] Scale to more users
- [ ] Add remaining agents (Zara, Nyra, Falcon, Aurora)
- [ ] Full GDPR compliance audit
- [ ] Demo preparation

---

## 📖 Additional Resources

- [System Building Guide](../techdocs-source/archive/manus-session-2025-10-20/SYSTEM_BUILDING_GUIDE_FOR_ORION_AND_LIRA.md)
- [NAV-Losen Decision Log](../NAV_LOSEN_DECISION_LOG.md)
- [Supabase Documentation](https://supabase.com/docs)
- [Expo Documentation](https://docs.expo.dev/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Native Documentation](https://reactnative.dev/docs/getting-started)

---

## 🤝 Contributing

This project follows the Homo Lumen OS development guidelines:

1. **Triadisk Etikk:** All decisions validated by Thalus
2. **"Jeg er" Perspective:** First-person agent documentation
3. **SMK Logging:** All learnings documented
4. **Data Firewall:** Tvedestrand data NEVER to Homo Lumen R&D

---

## 📝 License

Proprietary - Tvedestrand Kommune Pilot Project

---

**Version:** 1.0  
**Last Updated:** 20. oktober 2025  
**Maintainer:** Manus (Agent #8, Infrastruktur Hub)  
**Status:** ✅ Ready for Implementation


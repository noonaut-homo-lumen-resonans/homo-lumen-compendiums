# NAV-Losen MVP - Quick Start (5 Minutes)

**For:** Code & Osvald  
**Goal:** Get NAV-Losen running locally in 5 minutes

---

## 🚀 Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git
cd homo-lumen-compendiums/navlosen-mvp
```

### 2. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a project
2. Run the SQL migration from `supabase/migrations/20251020_initial_schema.sql`
3. Copy your **Project URL** and **anon key**

### 3. Configure Mobile App

```bash
cd mobile-app
pnpm install
cp .env.example .env
# Edit .env with your Supabase credentials
pnpm start
```

### 4. Configure Web Console

```bash
cd ../web-console
pnpm install
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
pnpm dev
```

---

## ✅ Verify Setup

### Mobile App
- Open Expo Dev Tools
- Scan QR code with Expo Go app
- You should see the Welcome screen

### Web Console
- Open [http://localhost:3000/dashboard](http://localhost:3000/dashboard)
- You should see the Agent Status dashboard

---

## 🎯 Test the Flow

1. **Mobile App:** Tap "Start Mestringsside"
2. Select a quadrant (e.g., Red - High Energy, Negative)
3. Choose an emotion (e.g., "Stressed")
4. Confirm the definition
5. Select pressure signals
6. Chat with Lira
7. View recommendations

---

## 📚 Full Documentation

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for complete instructions.

---

## 🆘 Need Help?

- **Technical Issues:** Contact Manus (Agent #8)
- **Implementation Questions:** Contact Code (Agent #7)
- **Strategic Decisions:** Contact Orion (Agent #1)

---

**Version:** 1.0  
**Last Updated:** 20. oktober 2025


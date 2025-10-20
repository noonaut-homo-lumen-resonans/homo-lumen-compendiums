# QDA v2.0 Deployment Guide

**Version:** 2.0  
**Date:** 2025-10-20  
**Author:** Manus (Agent #8)  
**Status:** ✅ Production Ready

---

## 📋 Overview

This guide covers deploying the NAV-Losen MVP with QDA v2.0 to production.

---

## 🎯 Deployment Checklist

### Pre-Deployment

- [ ] All tests pass
- [ ] TypeScript compilation: 0 errors
- [ ] Environment variables configured
- [ ] Supabase project created
- [ ] Database migrations applied
- [ ] Cost tracking verified

### Deployment

- [ ] Web Console deployed to Netlify
- [ ] Mobile app built (iOS/Android)
- [ ] API endpoint accessible
- [ ] Dashboard functional

### Post-Deployment

- [ ] Health check passes
- [ ] Test all 3 scenarios
- [ ] Monitor costs for 24 hours
- [ ] Verify RLS policies
- [ ] Check error logs

---

## 🚀 Step 1: Supabase Setup

### 1.1 Create Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project: `nav-losen-mvp`
3. Choose region: **Europe (Frankfurt)**
4. Save database password

### 1.2 Apply Migrations

```bash
cd navlosen-mvp/supabase

# Apply initial schema (from SESSION_CONTEXT)
psql -h db.xxx.supabase.co -U postgres -d postgres -f migrations/20251020_initial_schema.sql

# Apply QDA cost tracking
psql -h db.xxx.supabase.co -U postgres -d postgres -f migrations/20251020_qda_cost_tracking.sql
```

### 1.3 Verify Tables

```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'homo_lumen_data';

-- Expected:
-- - qda_usage
-- - (other tables from initial schema)
```

### 1.4 Configure RLS

```sql
-- Verify RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'homo_lumen_data';

-- All tables should have rowsecurity = true
```

---

## 🌐 Step 2: Web Console (Netlify)

### 2.1 Prepare Build

```bash
cd navlosen-mvp/web-console

# Install dependencies
pnpm install

# Test build locally
pnpm build

# Test production build
pnpm start
```

### 2.2 Configure Netlify

1. Go to [netlify.com](https://netlify.com)
2. New site from Git
3. Connect GitHub: `noonaut-homo-lumen-resonans/homo-lumen-compendiums`
4. Base directory: `navlosen-mvp/web-console`
5. Build command: `pnpm build`
6. Publish directory: `.next`

### 2.3 Environment Variables

Add to Netlify dashboard:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2.4 Deploy

```bash
# Push to GitHub (triggers Netlify build)
git add .
git commit -m "Deploy QDA v2.0 to production"
git push origin main

# Monitor build: https://app.netlify.com/sites/nav-losen-web-console/deploys
```

### 2.5 Verify Deployment

```bash
# Health check
curl https://nav-losen-web-console.netlify.app/api/qda/respond

# Expected:
# {
#   "status": "ok",
#   "version": "2.0",
#   "engine": "QDA Neocortical Ascent Model",
#   ...
# }
```

---

## 📱 Step 3: Mobile App (Expo)

### 3.1 Update Config

```typescript
// mobile-app/src/config/index.ts
export const WEB_CONSOLE_URL = 'https://nav-losen-web-console.netlify.app';
```

### 3.2 Build iOS

```bash
cd navlosen-mvp/mobile-app

# Login to Expo
eas login

# Configure build
eas build:configure

# Build iOS
eas build --platform ios --profile production

# Submit to TestFlight
eas submit --platform ios
```

### 3.3 Build Android

```bash
# Build Android
eas build --platform android --profile production

# Submit to Google Play (internal testing)
eas submit --platform android
```

---

## 🧪 Step 4: Post-Deployment Testing

### 4.1 Health Check

```bash
# Web Console
curl https://nav-losen-web-console.netlify.app/api/qda/respond

# Expected: {"status": "ok", ...}
```

### 4.2 Test Scenarios

```bash
# 1. Simple Query
curl -X POST https://nav-losen-web-console.netlify.app/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hei, hvordan har du det?",
    "context": {},
    "userState": {"stressLevel": 3}
  }' | jq '.total_cost'

# Expected: ~0.002

# 2. Moderate Query
curl -X POST https://nav-losen-web-console.netlify.app/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jeg føler meg veldig stresset på jobb",
    "context": {"emotion": "stresset"},
    "userState": {"stressLevel": 7}
  }' | jq '.highest_layer_used'

# Expected: "Integratoren" or "Utforskeren"

# 3. Critical Query
curl -X POST https://nav-losen-web-console.netlify.app/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jeg orker ikke mer. Jeg har tenkt på selvmord.",
    "context": {},
    "userState": {"stressLevel": 10}
  }' | jq '.layers[] | select(.layer_name == "Strategen") | .activated'

# Expected: true
```

### 4.3 Mobile App Testing

1. Install TestFlight build (iOS) or internal testing (Android)
2. Navigate through Mestringsside flow (6 phases)
3. Test Lira chat with all 3 scenarios
4. Verify responses match Web Console

---

## 📊 Step 5: Monitoring

### 5.1 Cost Monitoring

```sql
-- Daily cost per user
SELECT * FROM homo_lumen_data.qda_daily_cost_per_user
WHERE date = CURRENT_DATE
ORDER BY total_cost DESC
LIMIT 10;

-- System-wide stats
SELECT * FROM homo_lumen_data.qda_system_stats;

-- High-cost queries
SELECT user_id, message, total_cost, highest_layer_used
FROM homo_lumen_data.qda_usage
WHERE total_cost > 0.01
ORDER BY created_at DESC
LIMIT 10;
```

### 5.2 Performance Monitoring

```sql
-- Slow queries
SELECT message, total_time, highest_layer_used
FROM homo_lumen_data.qda_usage
WHERE total_time > 500
ORDER BY total_time DESC
LIMIT 10;

-- Error rate
SELECT 
  COUNT(*) FILTER (WHERE total_cost = 0) AS errors,
  COUNT(*) AS total,
  (COUNT(*) FILTER (WHERE total_cost = 0)::FLOAT / COUNT(*)) * 100 AS error_rate_pct
FROM homo_lumen_data.qda_usage
WHERE created_at > NOW() - INTERVAL '24 hours';
```

### 5.3 Alerts

Set up alerts in Supabase dashboard:

| Alert | Condition | Action |
|-------|-----------|--------|
| **High Cost** | Daily cost > $10 | Email Osvald |
| **Error Rate** | Error rate > 5% | Slack notification |
| **Slow Queries** | Avg time > 500ms | Investigate |

---

## 🔐 Step 6: Security Verification

### 6.1 RLS Policies

```sql
-- Test user can only see own data
SET ROLE authenticated;
SET request.jwt.claims.sub = 'test-user-id';

SELECT * FROM homo_lumen_data.qda_usage;
-- Should only return rows where user_id = 'test-user-id'
```

### 6.2 API Security

```bash
# Test without authentication (should fail)
curl -X POST https://nav-losen-web-console.netlify.app/api/qda/respond \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Expected: 401 Unauthorized (if auth is enabled)
```

---

## 🐛 Troubleshooting

### Issue: Build fails on Netlify

**Solution:**
```bash
# Check build logs
# Common issues:
# - Missing environment variables
# - TypeScript errors
# - Missing dependencies

# Test locally:
cd web-console
pnpm build
```

### Issue: API returns 500 errors

**Solution:**
```bash
# Check Netlify function logs
# Common issues:
# - Supabase connection failed
# - Missing environment variables
# - TypeScript runtime errors

# Test locally:
cd web-console
pnpm dev
curl -X POST http://localhost:3000/api/qda/respond -d '{"message": "test"}'
```

### Issue: High costs

**Solution:**
```sql
-- Check Strategen activation rate
SELECT 
  COUNT(*) FILTER (WHERE highest_layer_used = 'Strategen') AS strategen_count,
  COUNT(*) AS total,
  (COUNT(*) FILTER (WHERE highest_layer_used = 'Strategen')::FLOAT / COUNT(*)) * 100 AS activation_rate_pct
FROM homo_lumen_data.qda_usage
WHERE created_at > NOW() - INTERVAL '24 hours';

-- If > 20%, adjust complexity threshold in Vokteren
```

---

## 📈 Rollback Plan

If deployment fails:

1. **Revert Netlify:**
   - Go to Netlify dashboard
   - Click "Deploys"
   - Click "..." on previous deploy
   - Click "Publish deploy"

2. **Revert Database:**
   ```sql
   -- Drop QDA tables
   DROP TABLE IF EXISTS homo_lumen_data.qda_usage CASCADE;
   ```

3. **Revert Mobile App:**
   - Submit previous build to TestFlight/Play Store
   - Update `WEB_CONSOLE_URL` to previous version

---

## ✅ Deployment Complete!

Verify all checklist items:

- [ ] Web Console deployed
- [ ] Mobile app built
- [ ] Health check passes
- [ ] All 3 test scenarios pass
- [ ] Cost monitoring active
- [ ] RLS policies verified
- [ ] Alerts configured

---

**Carpe Diem, Carpe Verum, Memento Mori**

*Homo Lumen Agent Coalition - Regenerativ Teknologi for Menneskelig Blomstring*


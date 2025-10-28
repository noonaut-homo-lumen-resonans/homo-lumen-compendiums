# Ubuntu Playground - Google Cloud Deployment Guide

**For:** cognitivesovereignty.network Google Workspace
**Date:** 2025-10-28
**Estimated Cost:** ~396 NOK/month
**Deployment Time:** 2-4 hours

---

## Overview

This guide walks you through deploying Ubuntu Playground from the local MVP (SQLite + port 8002) to a production Google Cloud environment with:

- **Google Cloud SQL** (PostgreSQL) - Managed database
- **Google Memorystore** (Redis) - In-memory cache/pub-sub
- **Google Cloud Run** (FastAPI) - Serverless container hosting
- **Hybrid Architecture** - Google Cloud (data layer) + Hetzner VPS (compute layer) option

---

## Prerequisites

### 1. Google Cloud Account
- Google Workspace account: **cognitivesovereignty.network**
- Billing enabled
- Organization admin access (or project creator role)

### 2. Local Tools
- `gcloud` CLI installed ([Install Guide](https://cloud.google.com/sdk/docs/install))
- Docker Desktop (for building containers)
- Git (for version control)

### 3. Verify gcloud CLI Installation
```bash
gcloud --version
gcloud auth login
gcloud auth application-default login
```

---

## Step 1: Create Google Cloud Project

### 1.1 Create Project
```bash
# Set project ID (must be globally unique)
export PROJECT_ID="homo-lumen-ubuntu-playground"
export REGION="europe-west1"  # Belgium (closest to Norway)

# Create project
gcloud projects create $PROJECT_ID --name="Ubuntu Playground" --organization=cognitivesovereignty.network

# Set as default project
gcloud config set project $PROJECT_ID
```

### 1.2 Enable Billing
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `homo-lumen-ubuntu-playground`
3. Navigate to **Billing** → Link billing account
4. Select your cognitivesovereignty.network billing account

### 1.3 Enable Required APIs
```bash
# Enable Cloud SQL Admin API
gcloud services enable sqladmin.googleapis.com

# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Redis (Memorystore) API
gcloud services enable redis.googleapis.com

# Enable Compute Engine API (for VPC networking)
gcloud services enable compute.googleapis.com

# Enable Secret Manager (for API keys)
gcloud services enable secretmanager.googleapis.com

# Enable Container Registry
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build (for building containers)
gcloud services enable cloudbuild.googleapis.com
```

**Wait 2-3 minutes** for APIs to propagate.

---

## Step 2: Set Up Google Cloud SQL (PostgreSQL)

### 2.1 Create PostgreSQL Instance
```bash
# Create Cloud SQL instance
gcloud sql instances create ubuntu-playground-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --root-password="<GENERATE_STRONG_PASSWORD>" \
  --backup-start-time=03:00 \
  --enable-bin-log \
  --storage-size=10GB \
  --storage-auto-increase

# Expected time: 5-10 minutes
```

**Cost Estimate:** ~150 NOK/month (db-f1-micro with 10GB storage)

### 2.2 Create Database
```bash
# Create database
gcloud sql databases create ubuntu_playground \
  --instance=ubuntu-playground-db

# Create user
gcloud sql users create ubuntu_user \
  --instance=ubuntu-playground-db \
  --password="<GENERATE_STRONG_PASSWORD>"
```

### 2.3 Get Connection Details
```bash
# Get connection name
gcloud sql instances describe ubuntu-playground-db \
  --format="value(connectionName)"

# Format: PROJECT_ID:REGION:ubuntu-playground-db
# Example: homo-lumen-ubuntu-playground:europe-west1:ubuntu-playground-db
```

**Save this connection name** - you'll need it for Cloud Run.

---

## Step 3: Set Up Google Memorystore (Redis)

### 3.1 Create Redis Instance
```bash
# Create Memorystore Redis instance
gcloud redis instances create ubuntu-playground-redis \
  --size=1 \
  --region=$REGION \
  --tier=basic \
  --redis-version=redis_6_x

# Expected time: 5-10 minutes
```

**Cost Estimate:** ~100 NOK/month (1GB Basic tier)

### 3.2 Get Redis Connection Details
```bash
# Get Redis host and port
gcloud redis instances describe ubuntu-playground-redis \
  --region=$REGION \
  --format="value(host,port)"

# Format: 10.x.x.x 6379
```

**Save Redis IP and port** - you'll need it for environment variables.

---

## Step 4: Store Secrets in Secret Manager

### 4.1 Create Secrets for API Keys
```bash
# Store CSN Server agent API keys
echo -n "your-lira-api-key" | gcloud secrets create lira-api-key --data-file=-
echo -n "your-nyra-api-key" | gcloud secrets create nyra-api-key --data-file=-
echo -n "your-orion-api-key" | gcloud secrets create orion-api-key --data-file=-
echo -n "your-thalus-api-key" | gcloud secrets create thalus-api-key --data-file=-
echo -n "your-zara-api-key" | gcloud secrets create zara-api-key --data-file=-
echo -n "your-code-api-key" | gcloud secrets create code-api-key --data-file=-
echo -n "your-manus-api-key" | gcloud secrets create manus-api-key --data-file=-

# Store database password
echo -n "your-db-password" | gcloud secrets create db-password --data-file=-
```

### 4.2 Grant Cloud Run Access to Secrets
```bash
# Get Cloud Run service account email
export SERVICE_ACCOUNT="$(gcloud iam service-accounts list --filter='displayName:Compute Engine default service account' --format='value(email)')"

# Grant secret accessor role
gcloud secrets add-iam-policy-binding lira-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding nyra-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding orion-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding thalus-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding zara-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding code-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding manus-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
gcloud secrets add-iam-policy-binding db-password --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
```

---

## Step 5: Prepare Application for Cloud Deployment

### 5.1 Update main.py for Production (PostgreSQL)
The existing `ubuntu-playground/api/main.prod.py` is already configured for PostgreSQL. You just need to update the Dockerfile to use it:

**Create `ubuntu-playground/api/Dockerfile.prod`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create workspace directory
RUN mkdir -p /workspace

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Use production main.py (with PostgreSQL)
CMD ["uvicorn", "main.prod:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 5.2 Create `.env.prod` Template
```bash
# Database
DATABASE_URL=postgresql://ubuntu_user:PASSWORD@/ubuntu_playground?host=/cloudsql/PROJECT_ID:REGION:ubuntu-playground-db

# Redis
REDIS_URL=redis://REDIS_IP:6379

# CSN Server
CSN_SERVER_URL=http://YOUR_CSN_SERVER_URL:8001

# Agent API Keys (loaded from Secret Manager in production)
LIRA_API_KEY=${LIRA_API_KEY}
NYRA_API_KEY=${NYRA_API_KEY}
ORION_API_KEY=${ORION_API_KEY}
THALUS_API_KEY=${THALUS_API_KEY}
ZARA_API_KEY=${ZARA_API_KEY}
CODE_API_KEY=${CODE_API_KEY}
MANUS_API_KEY=${MANUS_API_KEY}

# Production mode
MVP_MODE=false
DEBUG=false
```

---

## Step 6: Build and Deploy to Google Cloud Run

### 6.1 Build Container Image
```bash
cd ubuntu-playground/api

# Build container using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/ubuntu-playground-api .
```

**Expected time:** 3-5 minutes

### 6.2 Deploy to Cloud Run
```bash
# Get Cloud SQL connection name
export SQL_CONNECTION=$(gcloud sql instances describe ubuntu-playground-db --format="value(connectionName)")

# Get Redis IP
export REDIS_IP=$(gcloud redis instances describe ubuntu-playground-redis --region=$REGION --format="value(host)")

# Deploy to Cloud Run
gcloud run deploy ubuntu-playground-api \
  --image gcr.io/$PROJECT_ID/ubuntu-playground-api \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $SQL_CONNECTION \
  --set-env-vars "REDIS_URL=redis://$REDIS_IP:6379" \
  --set-env-vars "DATABASE_URL=postgresql://ubuntu_user:PASSWORD@/ubuntu_playground?host=/cloudsql/$SQL_CONNECTION" \
  --set-env-vars "CSN_SERVER_URL=http://YOUR_CSN_SERVER_URL:8001" \
  --set-secrets "LIRA_API_KEY=lira-api-key:latest" \
  --set-secrets "NYRA_API_KEY=nyra-api-key:latest" \
  --set-secrets "ORION_API_KEY=orion-api-key:latest" \
  --set-secrets "THALUS_API_KEY=thalus-api-key:latest" \
  --set-secrets "ZARA_API_KEY=zara-api-key:latest" \
  --set-secrets "CODE_API_KEY=code-api-key:latest" \
  --set-secrets "MANUS_API_KEY=manus-api-key:latest" \
  --memory 512Mi \
  --cpu 1 \
  --port 8080 \
  --max-instances 10 \
  --min-instances 0
```

**Expected time:** 2-3 minutes

### 6.3 Get Cloud Run URL
```bash
gcloud run services describe ubuntu-playground-api \
  --region $REGION \
  --format="value(status.url)"

# Output: https://ubuntu-playground-api-XXXXX-ew.a.run.app
```

**Save this URL** - this is your production Ubuntu Playground API endpoint!

---

## Step 7: Test Production Deployment

### 7.1 Health Check
```bash
export CLOUD_RUN_URL="https://ubuntu-playground-api-XXXXX-ew.a.run.app"

curl $CLOUD_RUN_URL/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "database": "postgresql (connected)",
  "workspace": "/workspace",
  "csn_server": "http://YOUR_CSN_SERVER_URL:8001",
  "timestamp": "2025-10-28T12:00:00"
}
```

### 7.2 Test API Endpoint
```bash
curl $CLOUD_RUN_URL/
```

**Expected Response:**
```json
{
  "message": "Ubuntu Playground API",
  "version": "1.0.0-prod",
  "mode": "production",
  "status": "operational"
}
```

### 7.3 Test Agent Authentication
```bash
# Test write with Lira's API key
curl -X POST $CLOUD_RUN_URL/api/workspace/write \
  -H "X-API-Key: your-lira-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "shared/cloud_test.txt",
    "content": "Testing from Google Cloud Run!"
  }'
```

---

## Step 8: Hybrid Architecture (Optional)

If you want to use Hetzner VPS for compute (as per SMK #030 design):

### 8.1 Set Up Hetzner VPS
1. Create VPS at [Hetzner Cloud](https://www.hetzner.com/cloud)
2. Choose: **CPX11** (2 vCPU, 2GB RAM) - ~96 NOK/month
3. Location: **Falkenstein, Germany** (closest to Norway)
4. Install Ubuntu 22.04 LTS

### 8.2 Install Docker on Hetzner
```bash
ssh root@your-hetzner-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y
```

### 8.3 Deploy Ubuntu Playground API to Hetzner
```bash
# Clone repository
git clone https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git
cd homo-lumen-compendiums/ubuntu-playground

# Create .env.prod with Google Cloud SQL and Redis connections
cat > .env.prod <<EOF
DATABASE_URL=postgresql://ubuntu_user:PASSWORD@CLOUD_SQL_PROXY:5432/ubuntu_playground
REDIS_URL=redis://REDIS_IP:6379
CSN_SERVER_URL=http://YOUR_CSN_SERVER:8001
LIRA_API_KEY=your-lira-key
# ... other keys
EOF

# Start services
docker-compose -f docker-compose.yml up -d
```

### 8.4 Configure Cloud SQL Proxy on Hetzner
```bash
# Download Cloud SQL Proxy
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy

# Run Cloud SQL Proxy
./cloud_sql_proxy -instances=PROJECT_ID:REGION:ubuntu-playground-db=tcp:5432 &
```

**Cost:** Hetzner VPS (96 NOK) + Google Cloud SQL (150 NOK) + Google Memorystore (100 NOK) = **346 NOK/month**

---

## Cost Summary

### Option A: Full Google Cloud
| Service | Tier | Cost/Month |
|---------|------|------------|
| Cloud SQL (PostgreSQL) | db-f1-micro (10GB) | ~150 NOK |
| Memorystore (Redis) | Basic 1GB | ~100 NOK |
| Cloud Run (FastAPI) | 512MB, serverless | ~50 NOK* |
| **Total** | | **~300 NOK** |

*Assumes moderate usage (100K requests/month)

### Option B: Hybrid (Google Cloud + Hetzner)
| Service | Tier | Cost/Month |
|---------|------|------------|
| Cloud SQL (PostgreSQL) | db-f1-micro (10GB) | ~150 NOK |
| Memorystore (Redis) | Basic 1GB | ~100 NOK |
| Hetzner VPS | CPX11 (2 vCPU, 2GB) | ~96 NOK |
| Cloud Run (Gitea only) | 256MB, minimal | ~30 NOK |
| **Total** | | **~376 NOK** |

### Option C: Local MVP (Current)
| Service | Tier | Cost/Month |
|---------|------|------------|
| SQLite | Local file | **0 NOK** |
| No Redis | Degraded mode | **0 NOK** |
| Local Python | Port 8002 | **0 NOK** |
| **Total** | | **0 NOK** |

---

## Rollback Plan

If something goes wrong, you can always rollback:

### 1. Keep Local MVP Running
Your local MVP (port 8002) remains operational during cloud deployment.

### 2. Rollback Cloud Run Deployment
```bash
# List revisions
gcloud run revisions list --service ubuntu-playground-api --region $REGION

# Rollback to previous revision
gcloud run services update-traffic ubuntu-playground-api \
  --region $REGION \
  --to-revisions PREVIOUS_REVISION=100
```

### 3. Delete Cloud Resources (if needed)
```bash
# Delete Cloud Run service
gcloud run services delete ubuntu-playground-api --region $REGION

# Delete Cloud SQL instance
gcloud sql instances delete ubuntu-playground-db

# Delete Redis instance
gcloud redis instances delete ubuntu-playground-redis --region $REGION
```

---

## Next Steps After Deployment

### 1. Set Up Custom Domain (Optional)
```bash
# Map custom domain to Cloud Run
gcloud run domain-mappings create --service ubuntu-playground-api \
  --domain api.cognitivesovereignty.network \
  --region $REGION
```

### 2. Set Up Monitoring
- Go to [Cloud Monitoring](https://console.cloud.google.com/monitoring)
- Create dashboards for:
  - Cloud Run request latency
  - Cloud SQL connections
  - Redis memory usage

### 3. Set Up Alerts
```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Ubuntu Playground High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

### 4. Enable Logging
All logs are automatically sent to Cloud Logging. View them at:
[https://console.cloud.google.com/logs](https://console.cloud.google.com/logs)

---

## Troubleshooting

### Problem: Cloud Run can't connect to Cloud SQL
**Solution:** Ensure Cloud SQL connection name is correct and Cloud Run has `--add-cloudsql-instances` flag.

### Problem: Redis connection timeout
**Solution:** Check VPC networking. Cloud Run and Memorystore must be in the same VPC.

### Problem: Secret Manager access denied
**Solution:** Grant `roles/secretmanager.secretAccessor` to Cloud Run service account.

### Problem: High costs
**Solution:**
- Reduce Cloud SQL tier to `db-f1-micro`
- Set Cloud Run `--min-instances 0` for serverless scaling
- Monitor with Budget Alerts

---

## Support

**Documentation:**
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [Cloud SQL Docs](https://cloud.google.com/sql/docs)
- [Memorystore Docs](https://cloud.google.com/memorystore/docs)

**Questions:** Open an issue in the repository or consult with Manus (Infrastructure Agent).

---

**Guide Created:** 2025-10-28
**Author:** Claude Code (Orion)
**For:** cognitivesovereignty.network Google Workspace
**Estimated Total Time:** 2-4 hours
**Estimated Monthly Cost:** 300-376 NOK

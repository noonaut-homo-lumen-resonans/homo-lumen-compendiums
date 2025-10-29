# Ubuntu Playground - Google Cloud Deployment Checklist

**For:** cognitivesovereignty.network
**Estimated Time:** 2-4 hours
**Estimated Cost:** 300-376 NOK/month

---

## Pre-Deployment Checklist

- [ ] Google Workspace account verified: **cognitivesovereignty.network**
- [ ] Billing enabled on Google Cloud
- [ ] `gcloud` CLI installed and authenticated
- [ ] Docker Desktop installed (for local testing)
- [ ] API keys generated for all agents (Lira, Nyra, Orion, Thalus, Zara, Code, Manus)

---

## Step 1: Google Cloud Project Setup (15 minutes)

- [ ] Create Google Cloud project: `homo-lumen-ubuntu-playground`
- [ ] Link billing account
- [ ] Enable APIs:
  - [ ] Cloud SQL Admin API
  - [ ] Cloud Run API
  - [ ] Redis (Memorystore) API
  - [ ] Compute Engine API
  - [ ] Secret Manager API
  - [ ] Container Registry API
  - [ ] Cloud Build API
- [ ] Set default region: `europe-west1` (Belgium)

**Commands:**
```bash
export PROJECT_ID="homo-lumen-ubuntu-playground"
export REGION="europe-west1"
gcloud projects create $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud services enable sqladmin.googleapis.com run.googleapis.com redis.googleapis.com compute.googleapis.com secretmanager.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com
```

---

## Step 2: Google Cloud SQL Setup (15 minutes)

- [ ] Create PostgreSQL instance: `ubuntu-playground-db`
- [ ] Tier: `db-f1-micro` (150 NOK/month)
- [ ] Region: `europe-west1`
- [ ] Generate strong root password (save securely!)
- [ ] Create database: `ubuntu_playground`
- [ ] Create user: `ubuntu_user` with password
- [ ] Save connection name: `PROJECT_ID:REGION:ubuntu-playground-db`

**Commands:**
```bash
gcloud sql instances create ubuntu-playground-db --database-version=POSTGRES_15 --tier=db-f1-micro --region=$REGION --root-password="<PASSWORD>"
gcloud sql databases create ubuntu_playground --instance=ubuntu-playground-db
gcloud sql users create ubuntu_user --instance=ubuntu-playground-db --password="<PASSWORD>"
```

---

## Step 3: Google Memorystore (Redis) Setup (15 minutes)

- [ ] Create Redis instance: `ubuntu-playground-redis`
- [ ] Tier: `basic` (100 NOK/month)
- [ ] Size: 1GB
- [ ] Region: `europe-west1`
- [ ] Save Redis IP and port

**Commands:**
```bash
gcloud redis instances create ubuntu-playground-redis --size=1 --region=$REGION --tier=basic --redis-version=redis_6_x
gcloud redis instances describe ubuntu-playground-redis --region=$REGION --format="value(host,port)"
```

---

## Step 4: Secret Manager Setup (10 minutes)

- [ ] Store API keys in Secret Manager:
  - [ ] `lira-api-key`
  - [ ] `nyra-api-key`
  - [ ] `orion-api-key`
  - [ ] `thalus-api-key`
  - [ ] `zara-api-key`
  - [ ] `code-api-key`
  - [ ] `manus-api-key`
  - [ ] `db-password`
- [ ] Grant Cloud Run service account access to secrets

**Commands:**
```bash
echo -n "your-lira-api-key" | gcloud secrets create lira-api-key --data-file=-
# ... repeat for all keys
export SERVICE_ACCOUNT="$(gcloud iam service-accounts list --filter='displayName:Compute Engine default service account' --format='value(email)')"
gcloud secrets add-iam-policy-binding lira-api-key --member="serviceAccount:$SERVICE_ACCOUNT" --role="roles/secretmanager.secretAccessor"
```

---

## Step 5: Build Container Image (10 minutes)

- [ ] Navigate to `ubuntu-playground/api/`
- [ ] Create `Dockerfile.prod` (use production main.py)
- [ ] Build container with Cloud Build
- [ ] Verify image in Container Registry

**Commands:**
```bash
cd ubuntu-playground/api
gcloud builds submit --tag gcr.io/$PROJECT_ID/ubuntu-playground-api .
```

---

## Step 6: Deploy to Cloud Run (10 minutes)

- [ ] Deploy container to Cloud Run
- [ ] Connect to Cloud SQL instance
- [ ] Configure Redis URL
- [ ] Load secrets from Secret Manager
- [ ] Set memory: 512MB
- [ ] Set CPU: 1 vCPU
- [ ] Enable autoscaling (0-10 instances)
- [ ] Get Cloud Run URL

**Commands:**
```bash
export SQL_CONNECTION=$(gcloud sql instances describe ubuntu-playground-db --format="value(connectionName)")
export REDIS_IP=$(gcloud redis instances describe ubuntu-playground-redis --region=$REGION --format="value(host)")
gcloud run deploy ubuntu-playground-api \
  --image gcr.io/$PROJECT_ID/ubuntu-playground-api \
  --region $REGION \
  --add-cloudsql-instances $SQL_CONNECTION \
  --set-env-vars "REDIS_URL=redis://$REDIS_IP:6379" \
  --set-secrets "LIRA_API_KEY=lira-api-key:latest" \
  # ... (see full command in DEPLOYMENT_GUIDE_GOOGLE_CLOUD.md)
```

---

## Step 7: Test Deployment (15 minutes)

- [ ] Test health endpoint: `curl $CLOUD_RUN_URL/health`
  - [ ] Status: `healthy`
  - [ ] Redis: `connected`
  - [ ] Database: `postgresql (connected)`
- [ ] Test root endpoint: `curl $CLOUD_RUN_URL/`
- [ ] Test agent authentication with API key
- [ ] Test workspace write operation
- [ ] Test workspace read operation
- [ ] Test action execution endpoint

**Commands:**
```bash
export CLOUD_RUN_URL="https://ubuntu-playground-api-XXXXX-ew.a.run.app"
curl $CLOUD_RUN_URL/health
curl $CLOUD_RUN_URL/
curl -X POST $CLOUD_RUN_URL/api/workspace/write -H "X-API-Key: your-key" -H "Content-Type: application/json" -d '{"path": "shared/test.txt", "content": "Test from cloud!"}'
```

---

## Step 8: Connect CSN Server (Optional)

- [ ] Update CSN Server environment variable: `UBUNTU_PLAYGROUND_URL`
- [ ] Point to Cloud Run URL: `https://ubuntu-playground-api-XXXXX-ew.a.run.app`
- [ ] Test CSN Server → Ubuntu Playground integration
- [ ] Verify actions are logged in Cloud SQL

---

## Step 9: Monitoring & Alerts (15 minutes)

- [ ] Set up Cloud Monitoring dashboard
- [ ] Create alert for high error rate (>5%)
- [ ] Create alert for high latency (>2s)
- [ ] Set up budget alert (>500 NOK/month)
- [ ] Configure log-based metrics

**Go to:**
- [Cloud Monitoring](https://console.cloud.google.com/monitoring)
- [Cloud Logging](https://console.cloud.google.com/logs)
- [Billing Budgets](https://console.cloud.google.com/billing/budgets)

---

## Step 10: Documentation & Handoff (10 minutes)

- [ ] Document Cloud Run URL
- [ ] Document database connection details
- [ ] Document Redis IP
- [ ] Update repository README with cloud deployment info
- [ ] Create SMK document for cloud deployment
- [ ] Share credentials securely with team

---

## Post-Deployment Checklist

- [ ] Verify all 5/5 integration tests pass on cloud
- [ ] Monitor costs for first week
- [ ] Set up automatic backups (Cloud SQL)
- [ ] Configure custom domain (optional): `api.cognitivesovereignty.network`
- [ ] Enable HTTPS (automatic with Cloud Run)
- [ ] Review security settings
- [ ] Plan migration strategy from local MVP to cloud

---

## Rollback Plan (If Needed)

- [ ] Keep local MVP running on port 8002
- [ ] Document rollback commands:
  ```bash
  gcloud run services delete ubuntu-playground-api --region $REGION
  gcloud sql instances delete ubuntu-playground-db
  gcloud redis instances delete ubuntu-playground-redis --region $REGION
  ```

---

## Success Criteria

✅ Cloud Run service is `healthy`
✅ PostgreSQL database is connected
✅ Redis is connected
✅ All agent API keys work
✅ Integration tests pass (5/5)
✅ CSN Server can communicate with Ubuntu Playground
✅ Monthly cost < 400 NOK

---

## Time Estimate

| Phase | Time |
|-------|------|
| Project setup | 15 min |
| Cloud SQL | 15 min |
| Memorystore | 15 min |
| Secret Manager | 10 min |
| Build container | 10 min |
| Deploy Cloud Run | 10 min |
| Testing | 15 min |
| Monitoring | 15 min |
| Documentation | 10 min |
| **Total** | **~2 hours** |

**Buffer for troubleshooting:** +1-2 hours

---

## Cost Estimate

| Service | Monthly Cost |
|---------|--------------|
| Cloud SQL (db-f1-micro) | 150 NOK |
| Memorystore (1GB basic) | 100 NOK |
| Cloud Run (serverless) | 50 NOK |
| **Total** | **~300 NOK** |

---

## Support Resources

- **Full Guide:** [DEPLOYMENT_GUIDE_GOOGLE_CLOUD.md](DEPLOYMENT_GUIDE_GOOGLE_CLOUD.md)
- **Google Cloud Docs:** [cloud.google.com/docs](https://cloud.google.com/docs)
- **Homo Lumen Repository:** [github.com/noonaut-homo-lumen-resonans](https://github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums)

---

**Checklist Created:** 2025-10-28
**Author:** Claude Code (Orion)
**Status:** Ready for deployment

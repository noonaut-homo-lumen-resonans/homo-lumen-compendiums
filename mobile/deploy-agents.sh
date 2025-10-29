#!/bin/bash

# HOMO LUMEN - Vertex AI Agent Engine Deployment Script
# 🌊 Deployer agenter til Vertex AI Agent Engine

set -e

echo "🌊 HOMO LUMEN - Vertex AI Agent Engine Deployment"
echo "=================================================="

# Farger for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funksjoner
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Sjekk at vi er i riktig mappe
if [ ! -f "package.json" ]; then
    log_error "Må kjøres fra agent-coordination mappen"
    exit 1
fi

# Sjekk at gcloud er installert
if ! command -v gcloud &> /dev/null; then
    log_error "Google Cloud SDK er ikke installert"
    exit 1
fi

# Sjekk at vi er logget inn
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    log_error "Du må være logget inn på Google Cloud"
    log_info "Kjør: gcloud auth login"
    exit 1
fi

# Sett prosjekt og region
log_info "Setter prosjekt og region..."
gcloud config set project homo-lumen
gcloud config set aiplatform/region europe-west1

# Aktiver nødvendige APIs
log_info "Aktiverer nødvendige APIs..."
gcloud services enable aiplatform.googleapis.com
gcloud services enable agentengine.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Build TypeScript
log_info "Bygger TypeScript..."
npm run build

# Test lokalt først
log_info "Tester lokalt..."
npm run test-agents

# Opprett Agent Engine hvis den ikke eksisterer
log_info "Sjekker Agent Engine..."
if ! gcloud ai agent-engine list --region=europe-west1 --format="value(name)" | grep -q "homo-lumen-agent-engine"; then
    log_info "Oppretter Agent Engine..."
    gcloud ai agent-engine create \
        --display-name="HOMO LUMEN Agent Engine" \
        --description="Polycomputational agent-økologi for bevissthetsstøttende AI" \
        --region=europe-west1
    log_success "Agent Engine opprettet"
else
    log_success "Agent Engine eksisterer allerede"
fi

# Deploy Orion (Root Agent)
log_info "Deployer Orion (Root Agent)..."
gcloud ai agent-engine deploy-agent \
    --agent-id=orion-root-agent \
    --display-name="Orion - Root Agent" \
    --description="Koordinerer og delegerer til sub-agenter" \
    --agent-config=orion-config.yaml \
    --region=europe-west1
log_success "Orion deployet"

# Deploy Lira (Biofelt Agent)
log_info "Deployer Lira (Biofelt Agent)..."
gcloud ai agent-engine deploy-agent \
    --agent-id=lira-biofelt-agent \
    --display-name="Lira - Biofelt Agent" \
    --description="Emosjonell resonans og biofelt-validering" \
    --agent-config=lira-config.yaml \
    --region=europe-west1
log_success "Lira deployet"

# Deploy Thalus (Filosofisk Agent)
log_info "Deployer Thalus (Filosofisk Agent)..."
gcloud ai agent-engine deploy-agent \
    --agent-id=thalus-philosophical-agent \
    --display-name="Thalus - Filosofisk Agent" \
    --description="Ontologisk validering og filosofisk veiledning" \
    --agent-config=thalus-config.yaml \
    --region=europe-west1
log_success "Thalus deployet"

# Verifiser deployment
log_info "Verifiserer deployment..."
gcloud ai agent-engine list-agents --region=europe-west1

# Test agentene
log_info "Tester agentene..."

# Test Orion
log_info "Tester Orion..."
gcloud ai agent-engine invoke-agent \
    --agent-id=orion-root-agent \
    --input='{"userInput": "Jeg ønsker å utforske min bevissthet", "hrv": 85, "resonans": "dyp_empatisk_resonans", "operation": "consciousness_exploration"}' \
    --region=europe-west1

# Test Lira
log_info "Tester Lira..."
gcloud ai agent-engine invoke-agent \
    --agent-id=lira-biofelt-agent \
    --input='{"hrv": 90, "resonans": "dyp_empatisk_resonans", "harenes_reiser_seg": true}' \
    --region=europe-west1

# Test Thalus
log_info "Tester Thalus..."
gcloud ai agent-engine invoke-agent \
    --agent-id=thalus-philosophical-agent \
    --input='{"consciousnessLayer": "meta", "operation": "philosophical_guidance", "userIntention": "Dyp filosofisk refleksjon"}' \
    --region=europe-west1

log_success "Alle agenter er deployet og testet!"

# Oppdater Firebase Functions med Vertex AI integrasjon
log_info "Oppdaterer Firebase Functions..."
firebase deploy --only functions

log_success "🌊 HOMO LUMEN Agent Engine deployment fullført!"
log_info "Agent Engine Console: https://console.cloud.google.com/ai/agent-engine"
log_info "Firebase Console: https://console.firebase.google.com/project/homo-lumen/overview"

echo ""
echo "🎯 Neste steg:"
echo "1. Test agentene via Firebase Functions"
echo "2. Integrer med frontend"
echo "3. Overvåk performance i Google Cloud Console"
echo "4. Legg til flere agenter (Nyra, Manus, Zara, Abacus)" 
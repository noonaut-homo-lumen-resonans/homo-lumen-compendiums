# Setup Local Vercel Token Storage
# Henter token fra Secret Manager og lagrer lokalt i Windows Credential Manager

Write-Host ""
Write-Host "=== Setup Lokal Vercel Token ===" -ForegroundColor Cyan
Write-Host "Henter token fra Google Secret Manager..." -ForegroundColor Gray

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Hent token fra Secret Manager
$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "vercel-access-token"

Write-Host ""
Write-Host "📥 Henter Vercel token fra Secret Manager..." -ForegroundColor Cyan
$vercelToken = gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Kunne ikke hente token fra Secret Manager" -ForegroundColor Red
    Write-Host "   Feil: $vercelToken" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Sjekk at:" -ForegroundColor Yellow
    Write-Host "   1. Du er autentisert: gcloud auth login" -ForegroundColor Gray
    Write-Host "   2. Secret eksisterer: gcloud secrets list --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host "   3. Du har tilgang til secret" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📝 For å lagre token først:" -ForegroundColor Yellow
    Write-Host "   .\scripts\save_vercel_token_to_secret_manager.ps1" -ForegroundColor Gray
    exit 1
}

if ([string]::IsNullOrWhiteSpace($vercelToken)) {
    Write-Host ""
    Write-Host "❌ Token er tomt" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Token hentet (starter med: $($vercelToken.Substring(0,[Math]::Min(10,$vercelToken.Length)))...)" -ForegroundColor Green

# Test token før lagring (valgfritt - Vercel API krever autentisering)
Write-Host ""
Write-Host "💡 Vercel token vil bli lagret lokalt" -ForegroundColor Cyan
Write-Host "   (For å teste token, bruk: vercel whoami)" -ForegroundColor Gray

# Slett eksisterende credential hvis den finnes
Write-Host ""
Write-Host "🗑️  Sletter eksisterende credential (hvis finnes)..." -ForegroundColor Gray
cmdkey /delete:VercelAPI:vercel.com 2>$null | Out-Null

# Lagre i Windows Credential Manager
Write-Host "💾 Lagrer token i Windows Credential Manager..." -ForegroundColor Cyan
$result = & cmdkey /generic:VercelAPI:vercel.com /user:vercel-mcp /pass:$vercelToken 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Vercel token lagret lokalt!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Token er nå tilgjengelig fra:" -ForegroundColor Cyan
    Write-Host "   - Google Secret Manager (produksjon)" -ForegroundColor Gray
    Write-Host "   - Windows Credential Manager (lokalt)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 For å bruke token:" -ForegroundColor Yellow
    Write-Host "   - VS Code Extension leser automatisk fra VERCEL_TOKEN env var" -ForegroundColor Gray
    Write-Host "   - Eller fra Secret Manager: gcloud secrets versions access latest --secret=vercel-access-token --project=$PROJECT_ID" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Kunne ikke lagre token: $result" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Ferdig!" -ForegroundColor Green


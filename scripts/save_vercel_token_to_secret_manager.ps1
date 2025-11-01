# Save Vercel Access Token to Google Secret Manager
# Usage: .\scripts\save_vercel_token_to_secret_manager.ps1

Write-Host ""
Write-Host "=== Lagrer Vercel Access Token til Secret Manager ===" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "vercel-access-token"

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Be om token
$secureToken = Read-Host "Lim inn Vercel Access Token (starter med 'vercel_')" -AsSecureString
$VERCEL_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureToken)
)

if ([string]::IsNullOrWhiteSpace($VERCEL_TOKEN)) {
    Write-Host "❌ Ingen token gitt" -ForegroundColor Red
    exit 1
}

# Valider format
if (-not $VERCEL_TOKEN.StartsWith("vercel_")) {
    Write-Host "⚠️  Advarsel: Token starter ikke med 'vercel_' - er du sikker?" -ForegroundColor Yellow
    $confirm = Read-Host "Fortsett? (y/n)"
    if ($confirm -ne "y") {
        exit 1
    }
}

# Lagre til Secret Manager
Write-Host "💾 Lagrer til Secret Manager..." -ForegroundColor Cyan
$VERCEL_TOKEN | gcloud secrets create $SECRET_NAME --data-file=- --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Vercel Access Token lagret!" -ForegroundColor Green
    Write-Host ""
    Write-Host "For å hente token:" -ForegroundColor Yellow
    Write-Host "  gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For å lagre lokalt:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup_local_vercel_token.ps1" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "⚠️  Secret finnes kanskje allerede. Prøver å oppdatere..." -ForegroundColor Yellow
    $VERCEL_TOKEN | gcloud secrets versions add $SECRET_NAME --data-file=- --project=$PROJECT_ID

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Vercel Access Token oppdatert!" -ForegroundColor Green
        Write-Host ""
        Write-Host "For å lagre lokalt:" -ForegroundColor Yellow
        Write-Host "  .\scripts\setup_local_vercel_token.ps1" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "❌ Kunne ikke lagre/oppdatere secret" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Ferdig!" -ForegroundColor Green


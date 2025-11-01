# Save Notion API Key to Google Secret Manager
# Usage: .\scripts\save_notion_key_to_secret_manager.ps1

Write-Host ""
Write-Host "=== Lagrer Notion API Key til Secret Manager ===" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "notion-api-key"

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Be om API key
$secureKey = Read-Host "Lim inn Notion API Key (starter med 'secret_' eller 'notion_')" -AsSecureString
$NOTION_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
)

if ([string]::IsNullOrWhiteSpace($NOTION_KEY)) {
    Write-Host "❌ Ingen API key gitt" -ForegroundColor Red
    exit 1
}

# Lagre til Secret Manager
Write-Host "💾 Lagrer til Secret Manager..." -ForegroundColor Cyan
$NOTION_KEY | gcloud secrets create $SECRET_NAME --data-file=- --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Notion API Key lagret!" -ForegroundColor Green
    Write-Host ""
    Write-Host "For å hente token:" -ForegroundColor Yellow
    Write-Host "  gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "⚠️  Secret finnes kanskje allerede. Prøver å oppdatere..." -ForegroundColor Yellow
    $NOTION_KEY | gcloud secrets versions add $SECRET_NAME --data-file=- --project=$PROJECT_ID

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Notion API Key oppdatert!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Kunne ikke lagre/oppdatere secret" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "✅ Ferdig!" -ForegroundColor Green




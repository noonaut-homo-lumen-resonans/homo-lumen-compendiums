# Setup Local Notion API Key Storage
# Henter nøkkel fra Secret Manager og lagrer lokalt i Windows Credential Manager

Write-Host ""
Write-Host "=== Setup Lokal Notion API Key ===" -ForegroundColor Cyan
Write-Host "Henter nøkkel fra Google Secret Manager..." -ForegroundColor Gray

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Hent nøkkel fra Secret Manager
$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "notion-api-key"

Write-Host ""
Write-Host "📥 Henter Notion API Key fra Secret Manager..." -ForegroundColor Cyan
$notionKey = gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Kunne ikke hente nøkkel fra Secret Manager" -ForegroundColor Red
    Write-Host "   Feil: $notionKey" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Sjekk at:" -ForegroundColor Yellow
    Write-Host "   1. Du er autentisert: gcloud auth login" -ForegroundColor Gray
    Write-Host "   2. Secret eksisterer: gcloud secrets list --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host "   3. Du har tilgang til secret" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📝 For å lagre nøkkel først:" -ForegroundColor Yellow
    Write-Host "   .\scripts\save_notion_key_to_secret_manager.ps1" -ForegroundColor Gray
    exit 1
}

if ([string]::IsNullOrWhiteSpace($notionKey)) {
    Write-Host ""
    Write-Host "❌ Nøkkel er tom" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Nøkkel hentet (starter med: $($notionKey.Substring(0,10))...)" -ForegroundColor Green

# Test nøkkel før lagring
Write-Host ""
Write-Host "🔍 Tester nøkkel mot Notion API..." -ForegroundColor Cyan
$headers = @{
    "Authorization" = "Bearer $notionKey"
    "Notion-Version" = "2022-06-28"
}
try {
    $result = Invoke-RestMethod -Uri "https://api.notion.com/v1/users/me" -Headers $headers -ErrorAction Stop
    Write-Host "✅ Nøkkel fungerer! (Bot ID: $($result.id))" -ForegroundColor Green
} catch {
    Write-Host "❌ Nøkkel fungerer ikke: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "   Detaljer: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
    exit 1
}

# Slett eksisterende credential hvis den finnes
Write-Host ""
Write-Host "🗑️  Sletter eksisterende credential (hvis finnes)..." -ForegroundColor Gray
cmdkey /delete:NotionAPI:notion.so 2>$null | Out-Null

# Lagre i Windows Credential Manager
Write-Host "💾 Lagrer nøkkel i Windows Credential Manager..." -ForegroundColor Cyan
$result = & cmdkey /generic:NotionAPI:notion.so /user:notion-mcp /pass:$notionKey 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Notion API Key lagret lokalt!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Nøkkel er nå tilgjengelig fra:" -ForegroundColor Cyan
    Write-Host "   - Google Secret Manager (produksjon)" -ForegroundColor Gray
    Write-Host "   - Windows Credential Manager (lokalt)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 For å hente nøkkel programmatisk:" -ForegroundColor Yellow
    Write-Host "   Python: Se scripts/get_notion_key_from_secret.py" -ForegroundColor Gray
    Write-Host "   PowerShell: gcloud secrets versions access latest --secret=notion-api-key --project=$PROJECT_ID" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "❌ Kunne ikke lagre nøkkel: $result" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Ferdig!" -ForegroundColor Green


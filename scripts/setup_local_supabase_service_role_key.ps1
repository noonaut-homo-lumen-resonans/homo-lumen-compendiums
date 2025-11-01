# Setup Local Supabase Service Role Key Storage
# Henter nøkkel fra Secret Manager og lagrer lokalt i Windows Credential Manager
#
# WARNING: Service Role Key har FULL tilgang til databasen!
# Aldri eksponer denne i frontend eller klientkode!

Write-Host ""
Write-Host "=== Setup Lokal Supabase Service Role Key ===" -ForegroundColor Cyan
Write-Host "Henter nøkkel fra Google Secret Manager..." -ForegroundColor Gray
Write-Host ""
Write-Host "ADVARSEL: Service Role Key har FULL tilgang til databasen!" -ForegroundColor Red
Write-Host "   Aldri eksponer denne i frontend eller klientkode!" -ForegroundColor Red
Write-Host ""

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Hent nøkkel fra Secret Manager
$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "supabase-service-role-key"

Write-Host ""
Write-Host "Henter Supabase Service Role Key fra Secret Manager..." -ForegroundColor Cyan
$output = gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Kunne ikke hente nøkkel fra Secret Manager" -ForegroundColor Red
    Write-Host "   Feil: $output" -ForegroundColor Red
    Write-Host ""
    Write-Host "Sjekk at:" -ForegroundColor Yellow
    Write-Host "   1. Du er autentisert: gcloud auth login" -ForegroundColor Gray
    Write-Host "   2. Secret eksisterer: gcloud secrets list --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host "   3. Du har tilgang til secret" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For å lagre nøkkel først:" -ForegroundColor Yellow
    Write-Host "   .\scripts\save_supabase_service_role_key_to_secret_manager.ps1" -ForegroundColor Gray
    exit 1
}

# Håndter array output fra gcloud
if ($output -is [array]) {
    $serviceRoleKey = $output -join "`n"
} else {
    $serviceRoleKey = $output.ToString()
}

if ([string]::IsNullOrWhiteSpace($serviceRoleKey)) {
    Write-Host ""
    Write-Host "Nøkkel er tom" -ForegroundColor Red
    exit 1
}

# Trim whitespace og newlines
$serviceRoleKey = $serviceRoleKey.Trim()

if ($serviceRoleKey.Length -ge 10) {
    Write-Host "Nøkkel hentet (starter med: $($serviceRoleKey.Substring(0,10))...)" -ForegroundColor Green
} else {
    Write-Host "Nøkkel hentet (lengde: $($serviceRoleKey.Length) tegn)" -ForegroundColor Green
}

# Slett eksisterende credential hvis den finnes
Write-Host ""
Write-Host "Sletter eksisterende credential (hvis finnes)..." -ForegroundColor Gray
cmdkey /delete:SupabaseAPI:service-role-key 2>$null | Out-Null

# Lagre i Windows Credential Manager
Write-Host "Lagrer nøkkel i Windows Credential Manager..." -ForegroundColor Cyan
$result = & cmdkey /generic:SupabaseAPI:service-role-key /user:supabase-service-role /pass:$serviceRoleKey 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Supabase Service Role Key lagret lokalt!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Nøkkel er nå tilgjengelig fra:" -ForegroundColor Cyan
    Write-Host "   - Google Secret Manager (produksjon)" -ForegroundColor Gray
    Write-Host "   - Windows Credential Manager (lokalt)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Husk: Bruk KUN server-side!" -ForegroundColor Red
} else {
    Write-Host ""
    Write-Host "Kunne ikke lagre nøkkel: $result" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Ferdig!" -ForegroundColor Green



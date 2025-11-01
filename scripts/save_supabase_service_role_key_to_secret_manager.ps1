# Save Supabase Service Role Key to Google Secret Manager
# Usage: .\scripts\save_supabase_service_role_key_to_secret_manager.ps1
#
# ⚠️ VIKTIG: Service Role Key har FULL tilgang til databasen!
# Aldri eksponer denne i frontend eller klientkode!

Write-Host ""
Write-Host "=== Lagrer Supabase Service Role Key til Secret Manager ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "ADVARSEL: Service Role Key har FULL tilgang til databasen!" -ForegroundColor Red
Write-Host "   Aldri eksponer denne i frontend eller klientkode!" -ForegroundColor Red
Write-Host ""

$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "supabase-service-role-key"

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Sjekk om key er satt som miljøvariabel
$SERVICE_ROLE_KEY = $env:SUPABASE_SERVICE_ROLE_KEY

if ([string]::IsNullOrWhiteSpace($SERVICE_ROLE_KEY)) {
    Write-Host "Supabase Dashboard:" -ForegroundColor Yellow
    Write-Host "   https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Finn 'service_role' 'secret' key og kopier den" -ForegroundColor Yellow
    Write-Host "   ADVARSEL: Du ma kanskje klikke 'Reveal' eller 'Show' for a se den" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Sett nokkel som miljovariabel forst:" -ForegroundColor Cyan
    Write-Host "   `$env:SUPABASE_SERVICE_ROLE_KEY = 'eyJ...'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Eller sett permanent:" -ForegroundColor Cyan
    Write-Host "   [System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', 'eyJ...', 'User')" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Deretter kjor dette scriptet igjen." -ForegroundColor Yellow
    exit 1
}

Write-Host "Fant Service Role Key (starter med: $($SERVICE_ROLE_KEY.Substring(0,[Math]::Min(10,$SERVICE_ROLE_KEY.Length)))...)" -ForegroundColor Green
Write-Host ""

# Valider format
if (-not $SERVICE_ROLE_KEY.StartsWith("eyJ")) {
    Write-Host "ADVARSEL: Key starter ikke med 'eyJ' - er du sikker?" -ForegroundColor Yellow
    Write-Host "Fortsetter uansett..." -ForegroundColor Yellow
    Write-Host ""
}

# Bekreft at brukeren forstår sikkerhetsrisiko
Write-Host "SIKKERHETSBEKREFTELSE:" -ForegroundColor Red
Write-Host "   Service Role Key har FULL tilgang til databasen." -ForegroundColor Yellow
Write-Host "   Den kan bypasse Row Level Security (RLS)." -ForegroundColor Yellow
Write-Host "   Bruk KUN server-side, ALDRI i frontend!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Fortsetter med lagring..." -ForegroundColor Cyan
Write-Host ""

# Lagre til Secret Manager
Write-Host ""
Write-Host "Lagrer til Secret Manager..." -ForegroundColor Cyan
echo $SERVICE_ROLE_KEY | gcloud secrets create $SECRET_NAME --data-file=- --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "OK: Supabase Service Role Key lagret!" -ForegroundColor Green
    Write-Host ""
    Write-Host "For a hente key:" -ForegroundColor Yellow
    Write-Host "  gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host ""
    Write-Host "ADVARSEL: Husk: Bruk KUN server-side!" -ForegroundColor Red
    Write-Host ""
    Write-Host "For a lagre lokalt:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup_local_supabase_service_role_key.ps1" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "ADVARSEL: Secret finnes kanskje allerede. Prover a oppdatere..." -ForegroundColor Yellow
    echo $SERVICE_ROLE_KEY | gcloud secrets versions add $SECRET_NAME --data-file=- --project=$PROJECT_ID

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "OK: Supabase Service Role Key oppdatert!" -ForegroundColor Green
        Write-Host ""
        Write-Host "ADVARSEL: Husk: Bruk KUN server-side!" -ForegroundColor Red
        Write-Host ""
        Write-Host "For a lagre lokalt:" -ForegroundColor Yellow
        Write-Host "  .\scripts\setup_local_supabase_service_role_key.ps1" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "FEIL: Kunne ikke lagre/oppdatere secret" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Ferdig!" -ForegroundColor Green



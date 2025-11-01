# Save Supabase Anon Key to Google Secret Manager
# Usage: .\scripts\save_supabase_anon_key_to_secret_manager.ps1

Write-Host ""
Write-Host "=== Lagrer Supabase Anon Key til Secret Manager ===" -ForegroundColor Cyan
Write-Host ""

$PROJECT_ID = "dotted-stage-476513-r4"
$SECRET_NAME = "supabase-anon-key"

# Legg til gcloud i PATH hvis ikke allerede
$gcloudPath = "C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
if ($env:Path -notlike "*$gcloudPath*") {
    $env:Path += ";$gcloudPath"
}

# Sjekk om key er satt som miljøvariabel
$ANON_KEY = $env:SUPABASE_ANON_KEY

if ([string]::IsNullOrWhiteSpace($ANON_KEY)) {
    Write-Host "Supabase Dashboard:" -ForegroundColor Yellow
    Write-Host "   https://supabase.com/dashboard/project/guhtqmoxurfroailltsc/settings/api" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Finn 'anon' 'public' key og kopier den" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Sett nokkel som miljovariabel forst:" -ForegroundColor Cyan
    Write-Host "   `$env:SUPABASE_ANON_KEY = 'eyJ...'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Eller sett permanent:" -ForegroundColor Cyan
    Write-Host "   [System.Environment]::SetEnvironmentVariable('SUPABASE_ANON_KEY', 'eyJ...', 'User')" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Deretter kjor dette scriptet igjen." -ForegroundColor Yellow
    exit 1
}

Write-Host "Fant Anon Key (starter med: $($ANON_KEY.Substring(0,[Math]::Min(10,$ANON_KEY.Length)))...)" -ForegroundColor Green
Write-Host ""

# Valider format
if (-not $ANON_KEY.StartsWith("eyJ")) {
    Write-Host "[WARNING] Key starter ikke med 'eyJ' - er du sikker?" -ForegroundColor Yellow
    Write-Host "Fortsetter uansett..." -ForegroundColor Yellow
    Write-Host ""
}

# Lagre til Secret Manager
Write-Host ""
Write-Host "Lagrer til Secret Manager..." -ForegroundColor Cyan
echo $ANON_KEY | gcloud secrets create $SECRET_NAME --data-file=- --project=$PROJECT_ID 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] Supabase Anon Key lagret!" -ForegroundColor Green
    Write-Host ""
    Write-Host "For a hente key:" -ForegroundColor Yellow
    Write-Host "  gcloud secrets versions access latest --secret=$SECRET_NAME --project=$PROJECT_ID" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For a lagre lokalt:" -ForegroundColor Yellow
    Write-Host "  .\scripts\setup_local_supabase_anon_key.ps1" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "[WARNING] Secret finnes kanskje allerede. Prover a oppdatere..." -ForegroundColor Yellow
    echo $ANON_KEY | gcloud secrets versions add $SECRET_NAME --data-file=- --project=$PROJECT_ID

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Supabase Anon Key oppdatert!" -ForegroundColor Green
        Write-Host ""
        Write-Host "For a lagre lokalt:" -ForegroundColor Yellow
        Write-Host "  .\scripts\setup_local_supabase_anon_key.ps1" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "[ERROR] Kunne ikke lagre/oppdatere secret" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "[OK] Ferdig!" -ForegroundColor Green


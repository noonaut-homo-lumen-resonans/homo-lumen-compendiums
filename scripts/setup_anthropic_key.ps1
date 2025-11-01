# Setup Anthropic API Key - PowerShell Script
# Usage: .\scripts\setup_anthropic_key.ps1

Write-Host ""
Write-Host "=== Setup Anthropic API Key ===" -ForegroundColor Cyan
Write-Host ""

# Be om API key (skjult input)
Write-Host "Lim inn din Anthropic API key (starter med sk-ant-...):" -ForegroundColor Yellow
$api_key = Read-Host -AsSecureString

# Konverter til plain text
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($api_key)
$plain_key = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Valider at key ikke er tom
if ([string]::IsNullOrWhiteSpace($plain_key)) {
    Write-Host "[X] Ingen API key gitt. Avslutter." -ForegroundColor Red
    exit 1
}

# Valider format
if (-not ($plain_key -match "^sk-ant-")) {
    Write-Host "[!] ADVARSEL: API key ser ikke ut til å ha riktig format (sk-ant-...)" -ForegroundColor Yellow
    $confirm = Read-Host "Fortsett likevel? (y/N)"
    if ($confirm -ne "y") {
        Write-Host "Avbrutt." -ForegroundColor Gray
        exit 1
    }
}

# Spør om lagring
Write-Host ""
Write-Host "Hvor vil du lagre API key?" -ForegroundColor Cyan
Write-Host "1. Environment variable (kun denne sesjonen)"
Write-Host "2. Environment variable (permanent - User level)"
Write-Host "3. Google Secret Manager (produksjon - anbefalt)"
$choice = Read-Host "Velg (1/2/3)"

switch ($choice) {
    "1" {
        # Sett environment variable (kun denne sesjonen)
        $env:ANTHROPIC_API_KEY = $plain_key
        Write-Host ""
        Write-Host "[OK] API key satt som environment variable (kun denne sesjonen)" -ForegroundColor Green
        Write-Host ""
        Write-Host "For å gjøre permanent, velg alternativ 2" -ForegroundColor Gray
    }
    "2" {
        # Lagre permanent (User level)
        [System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", $plain_key, "User")
        $env:ANTHROPIC_API_KEY = $plain_key
        Write-Host ""
        Write-Host "[OK] API key lagret permanent (User level)" -ForegroundColor Green
        Write-Host ""
        Write-Host "Restart PowerShell for at endringen skal tre i kraft" -ForegroundColor Yellow
    }
    "3" {
        # Lagre i Google Secret Manager
        Write-Host ""
        Write-Host "Lagrer i Google Secret Manager..." -ForegroundColor Cyan

        # Prøv å opprette nytt secret
        $result = echo -n $plain_key | gcloud secrets create anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] API key lagret i Google Secret Manager" -ForegroundColor Green
        } else {
            # Secret kan allerede eksistere, prøv å oppdatere
            $result = echo -n $plain_key | gcloud secrets versions add anthropic-api-key --data-file=- --project=dotted-stage-476513-r4 2>&1

            if ($LASTEXITCODE -eq 0) {
                Write-Host "[OK] API key oppdatert i Google Secret Manager" -ForegroundColor Green
            } else {
                Write-Host "[X] Kunne ikke lagre i Secret Manager" -ForegroundColor Red
                Write-Host "    Sjekk at du er autentisert: gcloud auth login" -ForegroundColor Yellow
                exit 1
            }
        }

        # Sett også environment variable for testing
        $env:ANTHROPIC_API_KEY = $plain_key
    }
    default {
        Write-Host "[X] Ugyldig valg. Avslutter." -ForegroundColor Red
        exit 1
    }
}

# Nullstill key i minnet
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR([System.Security.SecureString]::new())
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)

# Test at det fungerer
Write-Host ""
Write-Host "Tester API key..." -ForegroundColor Cyan
python scripts/test_anthropic_sdk.py


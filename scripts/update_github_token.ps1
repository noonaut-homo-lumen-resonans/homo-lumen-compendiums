# Script for å oppdatere GitHub token i Google Secret Manager
# Usage: .\scripts\update_github_token.ps1

Write-Host "`n=== Oppdater GitHub Token i Secret Manager ===" -ForegroundColor Cyan
Write-Host "Prosjekt: dotted-stage-476513-r4" -ForegroundColor Gray
Write-Host "Secret: github-token`n" -ForegroundColor Gray

# Be bruker om nytt token
Write-Host "Lim inn ditt nye GitHub token (tokenet vises ikke):" -ForegroundColor Yellow
$token = Read-Host -AsSecureString

# Konverter til plain text
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$plainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Verifiser token format
if (-not ($plainToken -match "^gh(p|o|u)_")) {
    Write-Host "`n⚠️  ADVARSEL: Token ser ikke ut som et gyldig GitHub token format" -ForegroundColor Yellow
    Write-Host "Forventet format: ghp_..., gho_..., eller ghu_..." -ForegroundColor Gray
    $confirm = Read-Host "Fortsett likevel? (y/N)"
    if ($confirm -ne "y") {
        Write-Host "Avbrutt." -ForegroundColor Red
        exit 1
    }
}

# Lagre token i Secret Manager
Write-Host "`n💾 Lagrer nytt token i Secret Manager..." -ForegroundColor Cyan
try {
    $plainToken | gcloud secrets versions add github-token --data-file=- --project=dotted-stage-476513-r4

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Token oppdatert vellykket!" -ForegroundColor Green
        Write-Host "`n📋 Verifiser med:" -ForegroundColor Cyan
        Write-Host "   gcloud secrets versions access latest --secret=github-token" -ForegroundColor Gray
    } else {
        Write-Host "`n❌ Feil ved lagring. Sjekk feilmeldingen over." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "`n❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Nullstill token i minnet
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR([System.Security.SecureString]::new())
[System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)

Write-Host "`n✅ Ferdig!" -ForegroundColor Green


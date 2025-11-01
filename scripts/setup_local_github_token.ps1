# Setup Local GitHub Token Storage
# Henter token fra Secret Manager og lagrer lokalt i Windows Credential Manager

Write-Host ""
Write-Host "=== Setup Lokal GitHub Token ===" -ForegroundColor Cyan
Write-Host "Henter token fra Google Secret Manager..." -ForegroundColor Gray

# Hent token fra Secret Manager
$token = gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Kunne ikke hente token fra Secret Manager" -ForegroundColor Red
    Write-Host "   Feil: $token" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Sjekk at du er autentisert:" -ForegroundColor Yellow
    Write-Host "   gcloud auth login" -ForegroundColor Gray
    exit 1
}

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Host ""
    Write-Host "❌ Token er tomt" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Token hentet (starter med: $($token.Substring(0,15))...)" -ForegroundColor Green

# Test token før lagring
Write-Host ""
Write-Host "🔍 Tester token mot GitHub API..." -ForegroundColor Cyan
$headers = @{ "Authorization" = "token $token" }
try {
    $result = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers -ErrorAction Stop
    Write-Host "✅ Token fungerer! (Bruker: $($result.login))" -ForegroundColor Green
} catch {
    Write-Host "❌ Token fungerer ikke: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Slett eksisterende credential hvis den finnes
Write-Host ""
Write-Host "🗑️  Sletter eksisterende credential (hvis finnes)..." -ForegroundColor Gray
cmdkey /delete:git:https://github.com 2>$null | Out-Null

# Lagre i Windows Credential Manager
Write-Host "💾 Lagrer token i Windows Credential Manager..." -ForegroundColor Cyan
$result = & cmdkey /generic:git:https://github.com /user:noonaut-homo-lumen-resonans /pass:$token 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Token lagret lokalt!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Du kan nå bruke Git normalt:" -ForegroundColor Cyan
    Write-Host "   git push origin main" -ForegroundColor Gray
    Write-Host "   git pull origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💡 Token hentes automatisk fra Windows Credential Manager" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Kunne ikke lagre token: $result" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Ferdig!" -ForegroundColor Green

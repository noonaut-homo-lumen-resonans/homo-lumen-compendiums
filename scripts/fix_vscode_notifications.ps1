# Fix VS Code Notifications - Quick Setup Script
# Dette scriptet hjelper deg med å løse VS Code notifikasjoner

Write-Host ""
Write-Host "=== Fix VS Code Notifications ===" -ForegroundColor Cyan
Write-Host ""

# Sjekk Claude CLI
Write-Host "1. Sjekker Claude CLI..." -ForegroundColor Yellow
$claudeVersion = claude --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Claude CLI installert: $claudeVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Claude CLI ikke funnet" -ForegroundColor Red
    Write-Host "   💡 Installer med: winget install Anthropic.Claude" -ForegroundColor Gray
}

# Sjekk Claude API Key
Write-Host ""
Write-Host "2. Sjekker Claude API Key..." -ForegroundColor Yellow
$apiKey = claude config get api-key 2>&1
if ($apiKey -match "sk-" -or $env:ANTHROPIC_API_KEY) {
    Write-Host "   ✅ Claude API Key konfigurert" -ForegroundColor Green
} else {
    Write-Host "   ❌ Claude API Key mangler" -ForegroundColor Red
    Write-Host "   💡 Sett med: claude config set api-key YOUR_KEY" -ForegroundColor Gray
    Write-Host "   💡 Eller: \$env:ANTHROPIC_API_KEY = 'YOUR_KEY'" -ForegroundColor Gray
}

# Sjekk Vercel Token
Write-Host ""
Write-Host "3. Sjekker Vercel Token..." -ForegroundColor Yellow
if ($env:VERCEL_TOKEN) {
    Write-Host "   ✅ VERCEL_TOKEN environment variable satt" -ForegroundColor Green
} else {
    Write-Host "   ❌ VERCEL_TOKEN ikke satt" -ForegroundColor Red
    Write-Host "   💡 Sett med: \$env:VERCEL_TOKEN = 'vercel_YOUR_TOKEN'" -ForegroundColor Gray
    Write-Host "   💡 Hent token fra: https://vercel.com/account/tokens" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Instruksjoner ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "For å fikse feilene:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Claude MCP Provider:" -ForegroundColor White
Write-Host "   a) Hent API key: https://console.anthropic.com/settings/keys" -ForegroundColor Gray
Write-Host "   b) Sett: claude config set api-key YOUR_KEY" -ForegroundColor Gray
Write-Host "   c) Restart VS Code" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Vercel Access Token:" -ForegroundColor White
Write-Host "   a) Hent token: https://vercel.com/account/tokens" -ForegroundColor Gray
Write-Host "   b) Sett: \$env:VERCEL_TOKEN = 'vercel_YOUR_TOKEN'" -ForegroundColor Gray
Write-Host "   c) Eller legg til i User Settings (JSON):" -ForegroundColor Gray
Write-Host "      'vercelVSCode.accessToken': 'vercel_YOUR_TOKEN'" -ForegroundColor Gray
Write-Host "   d) Restart VS Code" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Multiple Workspace Files:" -ForegroundColor White
Write-Host "   ⚠️  Dette er bare en info - klikk 'Select Workspace' eller ignorer" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Se også: docs/VS_CODE_NOTIFICATIONS_FIX.md for detaljert guide" -ForegroundColor Cyan


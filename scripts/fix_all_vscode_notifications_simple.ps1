# Fix All VS Code Notifications - Simple Version
Write-Host ""
Write-Host "=== Fix All VS Code Notifications ===" -ForegroundColor Cyan
Write-Host ""

$issues = @()

# 1. Claude Code MCP Provider
Write-Host "1. Sjekker Claude Code MCP Provider..." -ForegroundColor Yellow

$claudeCheck = Get-Command claude -ErrorAction SilentlyContinue
if ($claudeCheck) {
    Write-Host "   ✅ Claude CLI installert" -ForegroundColor Green

    $apiKeyEnv = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
    if ($apiKeyEnv -match "sk-ant-") {
        Write-Host "   ✅ ANTHROPIC_API_KEY funnet i environment" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  ANTHROPIC_API_KEY mangler" -ForegroundColor Yellow
        Write-Host "   💡 Sett: [System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'YOUR_KEY', 'User')" -ForegroundColor Gray
        $issues += "Claude API key mangler"
    }
} else {
    Write-Host "   ❌ Claude CLI ikke installert" -ForegroundColor Red
    Write-Host "   💡 Installer med: winget install Anthropic.Claude" -ForegroundColor Gray
    $issues += "Claude CLI ikke installert"
}

# 2. Vercel Access Token
Write-Host ""
Write-Host "2. Sjekker Vercel Access Token..." -ForegroundColor Yellow

$vercelToken = [System.Environment]::GetEnvironmentVariable("VERCEL_TOKEN", "User")
if ($vercelToken -match "vercel_") {
    Write-Host "   ✅ VERCEL_TOKEN funnet" -ForegroundColor Green
    Write-Host "   💡 Husk å sette i VS Code Settings (Ctrl+,)" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  VERCEL_TOKEN ikke satt" -ForegroundColor Yellow
    Write-Host "   💡 Opprett: https://vercel.com/account/tokens" -ForegroundColor Gray
    $issues += "Vercel token mangler"
}

# 3. GitHub Actions
Write-Host ""
Write-Host "3. Sjekker GitHub Actions..." -ForegroundColor Yellow

$githubToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")
if ($githubToken -match "ghp_") {
    Write-Host "   ✅ GITHUB_TOKEN funnet" -ForegroundColor Green
} else {
    # Prøv Secret Manager
    $env:Path += ";C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
    $githubTokenSecret = gcloud secrets versions access latest --secret="github-token" --project="dotted-stage-476513-r4" 2>&1

    if ($githubTokenSecret -match "ghp_") {
        [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $githubTokenSecret, "User")
        Write-Host "   ✅ GitHub token hentet fra Secret Manager og lagret" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  GitHub token mangler" -ForegroundColor Yellow
        Write-Host "   💡 Klikk 'Sign in to GitHub' i notifikasjonen" -ForegroundColor Gray
        $issues += "GitHub token mangler"
    }
}

# Oppsummering
Write-Host ""
Write-Host "=== Oppsummering ===" -ForegroundColor Cyan
Write-Host ""

if ($issues.Count -eq 0) {
    Write-Host "✅ Alle notifikasjoner skal være fikset!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Neste steg: Restart VS Code / Cursor" -ForegroundColor Yellow
} else {
    Write-Host "⚠️  Må fikses manuelt:" -ForegroundColor Yellow
    foreach ($issue in $issues) {
        Write-Host "   • $issue" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "📖 Se: docs/VS_CODE_NOTIFICATIONS_FIX.md" -ForegroundColor Cyan
}

Write-Host ""



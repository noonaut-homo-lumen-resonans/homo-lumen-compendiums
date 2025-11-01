# Fix All VS Code Notifications - Comprehensive Fix Script
# Dette scriptet løser alle tre VS Code notifikasjoner

Write-Host ""
Write-Host "=== Fix All VS Code Notifications ===" -ForegroundColor Cyan
Write-Host ""

$issues = @()

# ============================================
# 1. Claude Code MCP Provider
# ============================================
Write-Host "1. Fikser Claude Code MCP Provider..." -ForegroundColor Yellow

# Sjekk om Claude CLI er installert
try {
    $claudeVersion = claude --version 2>&1
    if ($?) {
        Write-Host "   ✅ Claude CLI installert: $claudeVersion" -ForegroundColor Green

        # Sjekk om API key er satt i Claude CLI config
        $claudeConfig = claude config get api-key 2>&1
        $apiKeyEnv = [System.Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")

        if ($claudeConfig -match "sk-ant-" -or $apiKeyEnv) {
            Write-Host "   ✅ Claude API Key konfigurert" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Claude API Key mangler" -ForegroundColor Yellow
            Write-Host "   💡 Hent fra Secret Manager eller sett manuelt:" -ForegroundColor Gray

            # Prøv å hente fra Secret Manager
            $env:Path += ";C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
            $anthropicKey = & gcloud secrets versions access latest --secret="anthropic-api-key" --project="dotted-stage-476513-r4" 2>&1

            if ($? -and $anthropicKey -match "sk-ant-") {
                Write-Host "   ✅ Fant API key i Secret Manager" -ForegroundColor Green
                Write-Host "   🔧 Setter API key i Claude CLI..." -ForegroundColor Yellow

                claude config set api-key $anthropicKey

                if ($?) {
                    Write-Host "   ✅ Claude CLI konfigurert!" -ForegroundColor Green
                } else {
                    Write-Host "   ⚠️  Kunne ikke sette i Claude CLI config" -ForegroundColor Yellow
                    Write-Host "   💡 Sett manuelt: claude config set api-key YOUR_KEY" -ForegroundColor Gray
                    $issues += "Claude CLI API key må settes manuelt"
                }
            } else {
                Write-Host "   💡 Hent API key fra: https://console.anthropic.com/settings/keys" -ForegroundColor Gray
                Write-Host "   💡 Sett med: claude config set api-key YOUR_KEY" -ForegroundColor Gray
                Write-Host "   💡 Eller: [System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'YOUR_KEY', 'User')" -ForegroundColor Gray
                $issues += "Claude API key mangler"
            }
        }
    } else {
        Write-Host "   ❌ Claude CLI ikke funnet" -ForegroundColor Red
        $issues += "Claude CLI ikke installert"
    }
} catch {
    Write-Host "   ❌ Claude CLI ikke installert" -ForegroundColor Red
    Write-Host "   💡 Installer med: winget install Anthropic.Claude" -ForegroundColor Gray
    $issues += "Claude CLI ikke installert"
}

# ============================================
# 2. Vercel Access Token
# ============================================
Write-Host ""
Write-Host "2. Fikser Vercel Access Token..." -ForegroundColor Yellow

# Sjekk om token er satt
$vercelToken = [System.Environment]::GetEnvironmentVariable("VERCEL_TOKEN", "User")

if ($vercelToken -match "vercel_") {
    Write-Host "   ✅ VERCEL_TOKEN funnet i environment variables" -ForegroundColor Green
    Write-Host "   💡 Husk å sette i VS Code Settings også:" -ForegroundColor Gray
    Write-Host "      Ctrl+, → søk 'vercel access token' → lim inn token" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  VERCEL_TOKEN ikke satt" -ForegroundColor Yellow
    Write-Host "   💡 Opprett token: https://vercel.com/account/tokens" -ForegroundColor Gray
    Write-Host "   💡 Sett permanent:" -ForegroundColor Gray
    Write-Host "      [System.Environment]::SetEnvironmentVariable('VERCEL_TOKEN', 'vercel_YOUR_TOKEN', 'User')" -ForegroundColor Gray
    Write-Host "   💡 Eller i VS Code Settings (Ctrl+,): søk 'vercel access token'" -ForegroundColor Gray
    $issues += "Vercel token mangler"
}

# ============================================
# 3. GitHub Actions Sign-In
# ============================================
Write-Host ""
Write-Host "3. Fikser GitHub Actions Sign-In..." -ForegroundColor Yellow

# Sjekk om GitHub token er satt
$githubToken = [System.Environment]::GetEnvironmentVariable("GITHUB_TOKEN", "User")

if ($githubToken -match "ghp_") {
    Write-Host "   ✅ GITHUB_TOKEN funnet" -ForegroundColor Green
    Write-Host "   💡 GitHub Actions bør automatisk fungere" -ForegroundColor Gray
} else {
    # Prøv å hente fra Secret Manager
    $env:Path += ";C:\Users\onigo\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
    $githubTokenSecret = & gcloud secrets versions access latest --secret="github-token" --project="dotted-stage-476513-r4" 2>&1

    if ($? -and $githubTokenSecret -match "ghp_") {
        Write-Host "   ✅ Fant GitHub token i Secret Manager" -ForegroundColor Green
        Write-Host "   🔧 Setter som environment variable..." -ForegroundColor Yellow

        [System.Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $githubTokenSecret, "User")
        Write-Host "   ✅ GITHUB_TOKEN lagret permanent" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  GitHub token mangler" -ForegroundColor Yellow
        Write-Host "   💡 Klikk 'Sign in to GitHub' i notifikasjonen" -ForegroundColor Gray
        Write-Host "   💡 Eller sett GITHUB_TOKEN environment variable" -ForegroundColor Gray
        $issues += "GitHub token mangler"
    }
}

# ============================================
# Oppsummering
# ============================================
Write-Host ""
Write-Host "=== Oppsummering ===" -ForegroundColor Cyan
Write-Host ""

if ($issues.Count -eq 0) {
    Write-Host "✅ Alle notifikasjoner skal være fikset!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Neste steg:" -ForegroundColor Yellow
    Write-Host "   1. Restart VS Code / Cursor" -ForegroundColor Gray
    Write-Host "   2. Notifikasjonene skal være borte" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Følgende må fikses manuelt:" -ForegroundColor Yellow
    foreach ($issue in $issues) {
        Write-Host "   • $issue" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "📖 Se detaljert guide: docs/VS_CODE_NOTIFICATIONS_FIX.md" -ForegroundColor Cyan
}

Write-Host ""


# Test CS Parser Locally
# This proves the parser works - if this succeeds, GitHub Actions just needs secrets configured

Write-Host "Testing CS Parser Locally..." -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check if required packages are installed
Write-Host "Checking Python packages..." -ForegroundColor Yellow
$packages = @("requests", "pyyaml")
foreach ($pkg in $packages) {
    python -c "import $pkg" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing $pkg..." -ForegroundColor Yellow
        pip install $pkg
    }
}

Write-Host ""
Write-Host "Setting environment variables..." -ForegroundColor Yellow
$env:NOTION_API_KEY = Read-Host "Enter NOTION_API_KEY"
if ([string]::IsNullOrWhiteSpace($env:NOTION_API_KEY)) {
    Write-Host "ERROR: NOTION_API_KEY required" -ForegroundColor Red
    Write-Host "Get it from: https://www.notion.so/my-integrations" -ForegroundColor Yellow
    exit 1
}

$env:CS_DATABASE_ID = "2988fec9-2931-803a-8703-000bb973304e"

Write-Host ""
Write-Host "Running CS Parser..." -ForegroundColor Cyan
Write-Host "This will parse CODE_LIVING_COMPENDIUM_V1.4.md and sync CS entries to Notion" -ForegroundColor Gray
Write-Host ""

# Run the parser
python scripts/parse_cs.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Parser ran without errors." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Check Notion CS Database for CS #004 entry" -ForegroundColor White
    Write-Host "2. If entry appears -> Parser works!" -ForegroundColor White
    Write-Host "3. If entry appears -> GitHub Actions just needs secrets configured" -ForegroundColor White
    Write-Host "4. Follow GITHUB_SECRETS_SETUP.md to add secrets" -ForegroundColor White
    Write-Host ""
    Write-Host "Notion CS Database: https://www.notion.so/2988fec9293180a8703000bb973304e" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "ERROR: Parser failed. Check error message above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "- Wrong NOTION_API_KEY (should start with ntn_ or secret_)" -ForegroundColor White
    Write-Host "- Database not shared with integration" -ForegroundColor White
    Write-Host "- Network/firewall blocking Notion API" -ForegroundColor White
}

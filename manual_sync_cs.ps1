# Manual CS Sync to Notion
# Run this to manually sync CS entries from Code's LK to Notion

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Manual CS Sync to Notion" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "scripts/parse_cs.py")) {
    Write-Host "ERROR: Must run from homo-lumen-compendiums directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python not found" -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
pip install -q requests pyyaml 2>$null

# Check if secrets are set
if (-not $env:NOTION_API_KEY) {
    Write-Host "ERROR: NOTION_API_KEY not set" -ForegroundColor Red
    Write-Host "Get it from: https://www.notion.so/my-integrations" -ForegroundColor Yellow
    Write-Host "Then set it: `$env:NOTION_API_KEY = 'your-key-here'" -ForegroundColor Yellow
    exit 1
}

if (-not $env:CS_DATABASE_ID) {
    Write-Host "Setting CS_DATABASE_ID..." -ForegroundColor Yellow
    $env:CS_DATABASE_ID = "2988fec9-2931-803a-8703-000bb973304e"
}

Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  NOTION_API_KEY: $($env:NOTION_API_KEY.Substring(0,10))..." -ForegroundColor Gray
Write-Host "  CS_DATABASE_ID: $env:CS_DATABASE_ID" -ForegroundColor Gray
Write-Host ""

Write-Host "Running CS Parser..." -ForegroundColor Cyan
Write-Host "This will parse: agents/claude-code/LK/CODE_LIVING_COMPENDIUM_V1.4.md" -ForegroundColor Gray
Write-Host ""

# Run the parser
python scripts/parse_cs.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Check Notion for results" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Notion CS Database:" -ForegroundColor Cyan
    Write-Host "https://www.notion.so/2988fec9293180a8703000bb973304e" -ForegroundColor White
    Write-Host ""
    Write-Host "Look for these entries:" -ForegroundColor Cyan
    Write-Host "  - CS #001: 4-Database Mycelial Intelligence Implementation" -ForegroundColor White
    Write-Host "  - CS #002: UTF-8 Encoding Fix for Notion Database Discovery" -ForegroundColor White
    Write-Host "  - CS #003: Database ID Discovery via Relations" -ForegroundColor White
    Write-Host "  - CS #004: 17-Database Ecosystem Discovery & Mycelial Architecture Design" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "ERROR: Parser failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check error message above for details" -ForegroundColor Yellow
}

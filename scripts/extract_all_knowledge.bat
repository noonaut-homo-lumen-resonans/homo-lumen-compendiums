@echo off
REM Extract All Knowledge Base Content
REM Runs voktere, dimensjoner, and pulser extraction scripts

echo ======================================================================
echo KNOWLEDGE BASE EXTRACTION - ALL
echo ======================================================================
echo.

echo [1/3] Extracting Voktere (40+ files)...
python scripts/extract_voktere.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Voktere extraction failed!
    pause
    exit /b 1
)
echo.

echo [2/3] Extracting Dimensjoner (13 files)...
python scripts/extract_dimensjoner.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Dimensjoner extraction failed!
    pause
    exit /b 1
)
echo.

echo [3/3] Extracting Pulser (10 files)...
python scripts/extract_pulser.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Pulser extraction failed!
    pause
    exit /b 1
)
echo.

echo ======================================================================
echo EXTRACTION COMPLETE!
echo ======================================================================
echo.
echo Output:
echo   - knowledge_base_structured/voktere/ (40+ files)
echo   - knowledge_base_structured/dimensjoner/ (13 files)
echo   - knowledge_base_structured/pulser/ (10 files)
echo.
echo Next step:
echo   Run: python scripts/sync_to_csn_drive.py
echo.
pause

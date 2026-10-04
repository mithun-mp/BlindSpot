# ==============================================================================
# BlindSpot: Behavioral and Explainable-AI Framework for Auditing Text Classifiers
# PowerShell Execution Launcher Script (run.ps1)
# ==============================================================================

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [ValidateSet("cli", "dashboard", "test", "docs", "help")]
    [string]$Mode = "cli",

    [Parameter(Position=1)]
    [string]$Sentence = "This is awesome.",

    [Parameter(Position=2)]
    [string]$Model = "distilbert-base-uncased-finetuned-sst-2-english",

    [Parameter()]
    [string]$Explainer = "lime",

    [Parameter()]
    [string]$OutputDir = "audit_reports"
)

$ErrorActionPreference = "Stop"
$WorkspaceDir = $PSScriptRoot

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host " BlindSpot: Text Classifier Auditing Framework Launcher " -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan

# Ensure script runs from project root
Set-Location -Path $WorkspaceDir

switch ($Mode.ToLower()) {
    "cli" {
        Write-Host "[+] Running Audit Pipeline via CLI..." -ForegroundColor Green
        Write-Host "  - Target Model: $Model" -ForegroundColor Gray
        Write-Host "  - Sentence:     '$Sentence'" -ForegroundColor Gray
        Write-Host "  - Explainer:    $Explainer" -ForegroundColor Gray
        Write-Host "  - Output Dir:   $OutputDir" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m blindspot.cli --model $Model --sentence $Sentence --explainer $Explainer --output-dir $OutputDir
    }

    "dashboard" {
        Write-Host "[+] Launching Streamlit Interactive Web Dashboard..." -ForegroundColor Green
        Write-Host "  - Local URL: http://localhost:8501" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m streamlit run blindspot/app.py
    }

    "test" {
        Write-Host "[!] Test suite files have been cleaned from the project." -ForegroundColor Yellow
    }

    "docs" {
        Write-Host "[+] Serving MkDocs Technical Documentation..." -ForegroundColor Green
        Write-Host "  - Local Docs Server: http://127.0.0.1:8000" -ForegroundColor Gray
        Write-Host "------------------------------------------------------------------------" -ForegroundColor Cyan
        
        python -m mkdocs serve
    }

    "help" {
        Write-Host "Usage Guidelines for run.ps1:" -ForegroundColor Yellow
        Write-Host "  .\run.ps1 cli -Sentence 'The food was great.'     Run CLI audit on a sentence" -ForegroundColor White
        Write-Host "  .\run.ps1 dashboard                               Launch Streamlit web dashboard" -ForegroundColor White
        Write-Host "  .\run.ps1 test                                    Run unit test suite" -ForegroundColor White
        Write-Host "  .\run.ps1 docs                                    Serve MkDocs documentation" -ForegroundColor White
    }
}

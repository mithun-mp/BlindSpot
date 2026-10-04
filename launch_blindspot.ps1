# BlindSpot Workstation PowerShell Launcher
# Double-click or run from PowerShell prompt

$ErrorActionPreference = "Continue"
$host.UI.RawUI.WindowTitle = "BlindSpot Workstation"

Set-Location $PSScriptRoot
$env:PYTHONPATH = "$PSScriptRoot;$env:PYTHONPATH"

try {
    & python -m blindspot.launcher $args
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n[ERROR] BlindSpot exited with code $LASTEXITCODE." -ForegroundColor Red
        Read-Host "Press Enter to exit..."
    }
}
catch {
    Write-Host "`n[ERROR] Failed to execute Python launcher: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
}

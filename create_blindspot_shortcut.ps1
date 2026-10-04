# ==============================================================================
# Create Desktop & Project Shortcuts for BlindSpot Workstation
# Sets custom application icon from BSLogo.png / bslogo.ico
# ==============================================================================

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $ScriptDir) {
    $ScriptDir = Get-Location | Select-Object -ExpandProperty Path
}

$TargetPath = Join-Path $ScriptDir "launch_blindspot.bat"
$PngLogo = Join-Path $ScriptDir "BSLogo.png"
$IcoLogo = Join-Path $ScriptDir "BSLogo.ico"

if (-not (Test-Path $TargetPath)) {
    Write-Host "[ERROR] Target launcher '$TargetPath' not found." -ForegroundColor Red
    exit 1
}

# Ensure .ico file is valid Windows icon and generated from BSLogo.png
$NeedRegen = (-not (Test-Path $IcoLogo))
if ($NeedRegen -and (Test-Path $PngLogo)) {
    Write-Host "[+] Generating bslogo.ico from BSLogo.png..." -ForegroundColor Cyan
    try {
        & python -c "from PIL import Image; img = Image.open(r'$PngLogo'); img.save(r'$IcoLogo', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])"
        Write-Host "[+] Created bslogo.ico successfully." -ForegroundColor Green
    } catch {
        Write-Host "[!] Warning: Could not auto-generate .ico: $_" -ForegroundColor Yellow
    }
}

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)

# Remove legacy duplicate shortcut if present
$OldWorkstation = Join-Path $DesktopPath "BlindSpot Workstation.lnk"
if (Test-Path $OldWorkstation) {
    try {
        Remove-Item $OldWorkstation -Force
        Write-Host "[CLEANUP] Removed legacy duplicate: $OldWorkstation" -ForegroundColor Yellow
    } catch {}
}

# Target shortcut locations: Desktop and Project Root
$ShortcutLocations = @(
    (Join-Path $DesktopPath "BlindSpot.lnk"),
    (Join-Path $ScriptDir "BlindSpot.lnk")
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " CREATING BLINDSPOT SHORTCUTS WITH APP ICON             " -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

foreach ($ShortcutPath in $ShortcutLocations) {
    try {
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        $Shortcut.TargetPath = $TargetPath
        $Shortcut.WorkingDirectory = $ScriptDir
        $Shortcut.Description = "BlindSpot - Multimodel AI Auditing Workstation"
        
        if (Test-Path $IcoLogo) {
            $Shortcut.IconLocation = "$IcoLogo, 0"
        }
        
        $Shortcut.Save()
        Write-Host "[OK] Created: $ShortcutPath" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to create shortcut at $ShortcutPath : $_" -ForegroundColor Red
    }
}

# Notify Windows Shell to refresh icon cache immediately
try {
    $code = @'
[System.Runtime.InteropServices.DllImport("shell32.dll")]
public static extern void SHChangeNotify(int wEventId, int uFlags, IntPtr dwItem1, IntPtr dwItem2);
'@
    $type = Add-Type -MemberDefinition $code -Name ShellUtil -PassThru -ErrorAction SilentlyContinue
    if ($type) {
        $type::SHChangeNotify(0x08000000, 0x1000, [IntPtr]::Zero, [IntPtr]::Zero)
    }
} catch {}


Write-Host ""
Write-Host "Icon Source : $IcoLogo" -ForegroundColor Gray
Write-Host "Launcher    : $TargetPath" -ForegroundColor Gray
Write-Host ""
Write-Host "You can now double-click 'BlindSpot' on your Desktop or in the project folder to start the server and open the app." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan



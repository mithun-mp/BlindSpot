"""
BlindSpot Shortcut Creator
Creates Desktop and Project Root shortcuts with the BSLogo icon.
Does not require administrator privileges or PowerShell script execution policies.
"""
import os
import sys
from pathlib import Path

def generate_ico(png_path: Path, ico_path: Path):
    try:
        from PIL import Image
        img = Image.open(png_path)
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        img.save(ico_path, sizes=sizes)
        print(f"[OK] Generated {ico_path.name} from {png_path.name}")
    except Exception as e:
        print(f"[WARN] Could not generate .ico with PIL: {e}")

def get_desktop_path() -> Path:
    # Check OneDrive Desktop first (standard on Windows 10/11 with OneDrive)
    user_profile = Path(os.environ.get("USERPROFILE", ""))
    onedrive_desktop = user_profile / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():
        return onedrive_desktop
    local_desktop = user_profile / "Desktop"
    if local_desktop.exists():
        return local_desktop
    return user_profile / "Desktop"

def create_shortcut(target_bat: Path, shortcut_path: Path, icon_path: Path, work_dir: Path):
    # Use PowerShell via subprocess with bypass execution policy or Windows Script Host
    ps_cmd = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut('{str(shortcut_path)}')
    $Shortcut.TargetPath = '{str(target_bat)}'
    $Shortcut.WorkingDirectory = '{str(work_dir)}'
    $Shortcut.Description = 'BlindSpot - Multimodel AI Auditing Workstation'
    if (Test-Path '{str(icon_path)}') {{
        $Shortcut.IconLocation = '{str(icon_path)}, 0'
    }}
    $Shortcut.Save()
    """
    import subprocess
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[OK] Created shortcut: {shortcut_path}")
            return True
        else:
            # Fallback to direct VBScript if powershell executable is not in standard PATH
            return create_shortcut_vbs(target_bat, shortcut_path, icon_path, work_dir)
    except Exception:
        return create_shortcut_vbs(target_bat, shortcut_path, icon_path, work_dir)

def create_shortcut_vbs(target_bat: Path, shortcut_path: Path, icon_path: Path, work_dir: Path):
    import tempfile
    vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{str(shortcut_path)}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{str(target_bat)}"
oLink.WorkingDirectory = "{str(work_dir)}"
oLink.Description = "BlindSpot - Multimodel AI Auditing Workstation"
oLink.IconLocation = "{str(icon_path)}, 0"
oLink.Save
'''
    with tempfile.NamedTemporaryFile("w", suffix=".vbs", delete=False) as f:
        f.write(vbs_script)
        temp_vbs = f.name
    import subprocess
    try:
        subprocess.run(["cscript", "//nologo", temp_vbs], check=True)
        print(f"[OK] Created shortcut (via VBS): {shortcut_path}")
        return True
    finally:
        try:
            os.remove(temp_vbs)
        except OSError:
            pass

def refresh_icon_cache():
    try:
        import ctypes
        # SHCNE_ASSOCCHANGED = 0x08000000, SHCNF_FLUSH = 0x1000
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
        print("[OK] Notified Windows Shell to refresh icon cache.")
    except Exception as e:
        print(f"[WARN] Could not refresh icon cache: {e}")

def main():
    root_dir = Path(__file__).resolve().parent
    png_logo = root_dir / "BSLogo.png"
    ico_logo = root_dir / "BSLogo.ico"
    target_bat = root_dir / "launch_blindspot.bat"

    if not ico_logo.exists() and png_logo.exists():
        generate_ico(png_logo, ico_logo)

    desktop = get_desktop_path()

    print("========================================================")
    print(" REBUILDING BLINDSPOT SHORTCUTS WITH NEW APP ICON       ")
    print("========================================================")

    # 1. Clean up old duplicate shortcut if present
    old_workstation_shortcut = desktop / "BlindSpot Workstation.lnk"
    if old_workstation_shortcut.exists():
        try:
            old_workstation_shortcut.unlink()
            print(f"[CLEANUP] Removed legacy duplicate: {old_workstation_shortcut.name}")
        except Exception as e:
            print(f"[WARN] Could not remove {old_workstation_shortcut.name}: {e}")

    # 2. Create single clean Desktop shortcut
    create_shortcut(target_bat, desktop / "BlindSpot.lnk", ico_logo, root_dir)

    # 3. Create Project Root shortcut
    create_shortcut(target_bat, root_dir / "BlindSpot.lnk", ico_logo, root_dir)

    # 4. Invalidate Windows icon cache so new icon renders immediately
    refresh_icon_cache()

    print("")
    print(f"Active Icon : {ico_logo}")
    print(f"Target Bat  : {target_bat}")
    print(f"Desktop Lnk : {desktop / 'BlindSpot.lnk'}")
    print("")
    print("Shortcut successfully updated with the new BlindSpot icon!")
    print("========================================================")

if __name__ == "__main__":
    main()


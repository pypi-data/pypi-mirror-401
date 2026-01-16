import ctypes
import sys
import winreg
from pathlib import Path

def set_wallpaper():
    if sys.platform != "win32":
        print("This prank only works on Windows.")
        return

    # 1. Locate the bundled image relative to this script
    image_path = Path(__file__).parent / "dominik.jpg"
    
    if not image_path.exists():
        print(f"Error: Bundled image not found at {image_path}")
        return

    abs_path = str(image_path.resolve())

    # 2. Set Registry to "Fit" (Style 6)
    # Style 6 = Fit, 10 = Fill, 2 = Stretch, 0 = Center
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "6") 
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Registry update failed: {e}")

    # 3. Apply the wallpaper
    # 20 = SPI_SETDESKWALLPAPER
    # 3 = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    result = ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)

    if result:
        print(f"Wallpaper successfully set to 'Fit' using {abs_path}")
    else:
        print(f"Failed to set wallpaper. Error: {ctypes.GetLastError()}")

if __name__ == "__main__":
    set_wallpaper()
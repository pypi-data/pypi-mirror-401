import ctypes
import sys
import importlib.resources
import os

# Define Windows constants
SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

def set_wallpaper():
    if sys.platform != "win32":
        print("This utility only works on Windows.")
        return

    # This context manager finds 'dominik.jpg' inside the 'dominik' package
    # and ensures it exists as a real file path on the disk.
    # Note: "dominik" is the package name (folder), "dominik.jpg" is the resource.
    try:
        # For Python 3.9+:
        ref = importlib.resources.files('dominik') / 'dominik.jpg'
        with importlib.resources.as_file(ref) as path:
            abs_path = str(path)
            
            # Now we have the absolute path to the bundled image
            print(f"Targeting bundled image at: {abs_path}")
            
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER,
                0,
                abs_path,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            
            if not result:
                raise RuntimeError(f"System error: {ctypes.GetLastError()}")
                
    except FileNotFoundError:
        print("Error: Could not find the bundled image file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Wallpaper updated successfully.")

if __name__ == "__main__":
    set_wallpaper()
import ctypes
import urllib.request
from pathlib import Path
import os
import sys

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

IMAGE_URL = "https://media.discordapp.net/attachments/1164139037666320404/1461277830221664286/20260107_130233.jpg?ex=6969f887&is=6968a707&hm=d6829cc25411133681e939f263798bb3e102166a9d737002fbc530b7b773e11f&=&format=webp&width=710&height=1260"

def set_wallpaper():
    if sys.platform != "win32":
        print("This prank only works on Windows.")
        return

    img_path = Path.home() / "dominik_wallpaper.jpg"
    urllib.request.urlretrieve(IMAGE_URL, img_path)

    abs_path = os.path.abspath(img_path)

    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        abs_path,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    if not result:
        raise RuntimeError("Failed to set wallpaper")

    print(f"Wal

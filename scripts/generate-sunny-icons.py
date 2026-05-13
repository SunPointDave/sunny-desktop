#!/usr/bin/env python3
"""
generate-sunny-icons.py

Generate all required icon formats for the Sunny (Cherry Studio fork) app.

Usage:
    python3 scripts/generate-sunny-icons.py /path/to/source_icon.png

Requires: Pillow (pip install Pillow)
"""

import sys
import os
from pathlib import Path
from PIL import Image

# Base paths relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = BASE_DIR / "build"
ICONS_DIR = BUILD_DIR / "icons"
ASSETS_DIR = BASE_DIR / "src" / "renderer" / "src" / "assets" / "images"

def ensure_dirs():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def load_source(src_path: str) -> Image.Image:
    img = Image.open(src_path).convert("RGBA")
    # Make it square by centering on a transparent canvas
    w, h = img.size
    size = max(w, h)
    square = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    x = (size - w) // 2
    y = (size - h) // 2
    square.paste(img, (x, y), img)
    return square

def make_white_bg(img: Image.Image, size: int) -> Image.Image:
    """Return a white-background RGB copy of the icon."""
    white = Image.new("RGB", (size, size), (255, 255, 255))
    rgb_img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    white.paste(rgb_img, (0, 0), rgb_img)
    return white

def generate_icons(source: Image.Image):
    ensure_dirs()

    sizes = [16, 24, 32, 48, 64, 128, 256, 512, 1024]

    # 1. Build/icons/ size variants
    for s in sizes:
        icon = source.resize((s, s), Image.LANCZOS)
        icon.save(ICONS_DIR / f"{s}x{s}.png")
    print(f"[OK] Generated {len(sizes)} size variants in build/icons/")

    # 2. Main build/icon.png (1024x1024)
    icon_1024 = source.resize((1024, 1024), Image.LANCZOS)
    icon_1024.save(BUILD_DIR / "icon.png")
    print("[OK] Generated build/icon.png (1024x1024)")

    # 3. build/logo.png (512x512)
    logo_512 = source.resize((512, 512), Image.LANCZOS)
    logo_512.save(BUILD_DIR / "logo.png")
    print("[OK] Generated build/logo.png (512x512)")

    # 4. Tray icons (32x32)
    tray = source.resize((32, 32), Image.LANCZOS)
    tray.save(BUILD_DIR / "tray_icon.png")
    tray.save(BUILD_DIR / "tray_icon_dark.png")
    tray.save(BUILD_DIR / "tray_icon_light.png")
    print("[OK] Generated build/tray_icon*.png files (32x32)")

    # 5. Windows .ico (multi-resolution with white background)
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    ico_imgs = [make_white_bg(source, s) for s in ico_sizes]
    ico_imgs[0].save(
        BUILD_DIR / "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes]
    )
    print("[OK] Generated build/icon.ico (Windows multi-resolution)")

    # 6. macOS .icns (requires Pillow >= 9.0 or png2icns fallback)
    icns_path = BUILD_DIR / "icon.icns"
    try:
        # Pillow does not natively write .icns, so we generate PNGs and
        # create a simple .icns via Apple iconutil or leave instructions.
        # Here we create a directory of PNGs for manual conversion.
        icns_dir = BUILD_DIR / "icon.iconset"
        icns_dir.mkdir(exist_ok=True)
        icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
        for s in icns_sizes:
            icon = source.resize((s, s), Image.LANCZOS)
            icon.save(icns_dir / f"icon_{s}x{s}.png")
            if s <= 512:
                icon_2x = source.resize((s * 2, s * 2), Image.LANCZOS)
                icon_2x.save(icns_dir / f"icon_{s}x{s}@2x.png")
        print(
            f"[OK] Generated build/icon.iconset/ for macOS .icns.\n"
            f"     To create .icns run: iconutil -c icns {icns_dir}"
        )
    except Exception as e:
        print(f"[WARN] Could not prepare icon.iconset: {e}")

    # 7. In-app assets (256x256)
    app_logo = source.resize((256, 256), Image.LANCZOS)
    app_logo.save(ASSETS_DIR / "logo.png")
    app_logo.save(ASSETS_DIR / "avatar.png")
    print("[OK] Generated src/renderer/src/assets/images/logo.png & avatar.png (256x256)")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate-sunny-icons.py <path_to_source_icon.png>")
        sys.exit(1)

    src_path = sys.argv[1]
    if not os.path.exists(src_path):
        print(f"Error: File not found: {src_path}")
        sys.exit(1)

    print(f"Generating Sunny icons from: {src_path}")
    source = load_source(src_path)
    generate_icons(source)
    print("\nAll done! Your Sunny app icons are ready.")

if __name__ == "__main__":
    main()

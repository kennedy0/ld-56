from pathlib import Path

from bont import generate_bitmap_font
from sprak import SpritePacker

# Paths
project_root = Path(__file__).parent
assets_folder = project_root / "assets"
content_folder = project_root / "content"
fonts_src = assets_folder / "fonts"
fonts_dst = content_folder / "fonts"
sprites_src = assets_folder / "sprites"

# Fonts
fonts_dst.mkdir(parents=True, exist_ok=True)
generate_bitmap_font(fonts_src / "udon.ttf", fonts_dst, 16)

# Atlas
packer = SpritePacker()
packer.add_source_folder(sprites_src)
packer.pack(content_folder)

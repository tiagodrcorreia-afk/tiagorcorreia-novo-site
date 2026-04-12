#!/usr/bin/env python3
"""
Fix project list images - revert to direct src (data-desktop-src not working)
but use proper dimensions and orientation from actual files
"""
import json, re, struct
from pathlib import Path

BASE = Path("/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2")

with open("/tmp/trc_projects.json", "r") as f:
    projects = json.load(f)

def get_image_dimensions(filepath):
    """Get width/height from image file header (JPEG/PNG)"""
    try:
        with open(filepath, 'rb') as f:
            header = f.read(32)
            if header[:8] == b'\x89PNG\r\n\x1a\n':
                w, h = struct.unpack('>II', header[16:24])
                return w, h
            f.seek(0)
            data = f.read()
            idx = 2
            while idx < len(data) - 8:
                if data[idx] != 0xFF:
                    break
                marker = data[idx+1]
                if marker in (0xC0, 0xC2):
                    h = struct.unpack('>H', data[idx+5:idx+7])[0]
                    w = struct.unpack('>H', data[idx+7:idx+9])[0]
                    return w, h
                else:
                    length = struct.unpack('>H', data[idx+2:idx+4])[0]
                    idx += 2 + length
    except:
        pass
    return 2560, 1440

with open(BASE / "index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Fix each project's list image
for p in projects:
    slug = p["slug"]
    pid = p["id"]
    proj_dir = BASE / "assets" / "images" / "projetos" / slug

    # Find thumb file
    thumb_file = None
    thumb_path = ""
    for ext in ['.jpg', '.png', '.jpeg']:
        candidate = proj_dir / f"thumb{ext}"
        if candidate.exists():
            thumb_file = candidate
            thumb_path = f"assets/images/projetos/{slug}/thumb{ext}"
            break
    if not thumb_file:
        files = sorted(proj_dir.iterdir()) if proj_dir.exists() else []
        if files:
            thumb_file = files[0]
            thumb_path = f"assets/images/projetos/{slug}/{files[0].name}"
    if not thumb_file:
        continue

    w, h = get_image_dimensions(thumb_file)
    orientation = "-landscape" if w >= h else "-portrait"

    # Replace data-desktop-src pattern back to direct src
    # Current: data-desktop-src="path" src="data:image/svg+xml,..." width="w" height="h"
    # Target: src="path" width="w" height="h"
    regex = re.compile(
        r'(data-scroll-target="#projectList-' + str(pid) + r'".*?<img\s+)'
        r'class="(-landscape|-portrait)"\s+'
        r'data-desktop-src="([^"]+)"\s+'
        r'src="data:image/svg\+xml[^"]*"\s+'
        r'width="\d+"\s+height="\d+"\s+'
        r'alt="([^"]*)"',
        re.DOTALL
    )

    def make_replacement(m):
        return (
            f'{m.group(1)}'
            f'class="{orientation}"\n'
            f'                            src="{thumb_path}" '
            f'width="{w}" height="{h}" '
            f'alt="{m.group(4)}"'
        )

    content = regex.sub(make_replacement, content)

with open(BASE / "index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Fixed list images: reverted to direct src with correct dimensions")
print(f"   Updated {len(projects)} project thumbnails")

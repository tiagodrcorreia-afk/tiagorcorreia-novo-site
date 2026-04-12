#!/usr/bin/env python3
"""
Fix audit issues:
1. Replace old HTA grid with new projects grid
2. Clean htarchitecte.com references from head/meta
3. Fix vendors.js reference
"""
import json, re, html as html_mod, struct
from pathlib import Path

BASE = Path("/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2")

with open("/tmp/trc_projects.json", "r") as f:
    projects = json.load(f)

with open(BASE / "index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

content = "".join(lines)

# ─── 1. REPLACE THE OLD GRID ─────────────────────────────────
# Find grid start and end
grid_start = content.find('<div class="c-grid" data-module-grid')
grid_search_end = content.find('</div>\n\n', grid_start + 100)
# Find the actual closing </div> of the grid by counting
# The grid ends with </div>\n    </div>\n after last column
# Let's use a more reliable approach: find the c-projects-list that follows
projects_list_start = content.find('<div class="c-projects-list"', grid_start)

if grid_start == -1 or projects_list_start == -1:
    print("ERROR: Could not find grid boundaries")
    exit(1)

# The grid HTML sits between grid_start and projects_list_start
# But there might be some whitespace/closing tags between them
# Let's find the last </div> before projects_list_start that closes the grid
old_grid = content[grid_start:projects_list_start]
print(f"Old grid: {len(old_grid)} chars, {old_grid.count('htarchitecte.com')} HTA refs")

# Build new grid
def get_image_dimensions(filepath):
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
                if data[idx] != 0xFF: break
                marker = data[idx+1]
                if marker in (0xC0, 0xC2):
                    h = struct.unpack('>H', data[idx+5:idx+7])[0]
                    w = struct.unpack('>H', data[idx+7:idx+9])[0]
                    return w, h
                length = struct.unpack('>H', data[idx+2:idx+4])[0]
                idx += 2 + length
    except: pass
    return 2560, 1440

num_projects = len(projects)
num_cols = (num_projects + 1) // 2
col_width = round(100 / num_cols, 7)
grid_size = f"{num_cols * 35}vw"

grid_html = f'<div class="c-grid" data-module-grid data-grid-projects-number="{num_projects}" style="--gridSize: {grid_size}">\n'
proj_idx = 0
for col in range(num_cols):
    grid_html += f'    <div class="c-grid_col js-grid-col" data-index={col+1} style="width: {col_width}%">\n'
    for _ in range(2):
        if proj_idx >= num_projects: break
        p = projects[proj_idx]
        slug = p["slug"]
        title = p["title"]
        href = f"{slug}.html"
        proj_dir = BASE / "assets" / "images" / "projetos" / slug

        # Get up to 3 images for grid
        grid_imgs = []
        if proj_dir.exists():
            files = sorted(proj_dir.iterdir())
            for f_img in files[:3]:
                img_path = f"assets/images/projetos/{slug}/{f_img.name}"
                w, h = get_image_dimensions(f_img)
                grid_imgs.append({"path": img_path, "w": w, "h": h})

        grid_html += f'        <div class="c-grid_col_project" data-grid="project">\n'
        for img in grid_imgs:
            grid_html += f'''            <div class="c-grid_item" data-grid="item">
                <figure class="c-grid_figure" data-grid="plane" data-src="{img["path"]}" data-id={p["id"]} data-href="{href}">
                    <img loading="lazy" data-src="{img["path"]}" width="{img["w"]}" height="{img["h"]}" alt="{title}">
                    <span data-load="project" data-load-delay="0">{title}</span>
                </figure>
            </div>
'''
        grid_html += '        </div>\n'
        proj_idx += 1
    grid_html += '    </div>\n'
grid_html += '</div>\n'

content = content[:grid_start] + grid_html + content[projects_list_start:]
print(f"New grid: {len(grid_html)} chars, {grid_html.count('htarchitecte.com')} HTA refs")

# ─── 2. CLEAN HEAD REFERENCES ────────────────────────────────
# Replace HTA favicons with local placeholders
content = content.replace(
    '<link rel="author" href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/humans.txt" />',
    '<!-- author link removed -->'
)
content = content.replace(
    'href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/favicons/apple-touch-icon.png"',
    'href="assets/images/favicons/apple-touch-icon.png"'
)
content = content.replace(
    'href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/favicons/favicon-32x32.png"',
    'href="assets/images/favicons/favicon-32x32.png"'
)
content = content.replace(
    'href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/favicons/favicon-16x16.png"',
    'href="assets/images/favicons/favicon-16x16.png"'
)
content = content.replace(
    'href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/favicons/site.webmanifest"',
    'href="assets/images/favicons/site.webmanifest"'
)
content = content.replace(
    'href="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/favicons/safari-pinned-tab.svg"',
    'href="assets/images/favicons/safari-pinned-tab.svg"'
)

# Fix OG meta tags
content = content.replace(
    '<meta property="og:url" content="https://htarchitecte.com/en/"/>',
    '<meta property="og:url" content="https://www.tiagorcorreia.com/"/>'
)
content = content.replace(
    '<meta property="og:title" content="Home" />',
    '<meta property="og:title" content="Tiago R. Correia Arquitectos" />'
)
content = content.replace(
    '<meta property="og:image" content="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/opengraph.png" />',
    '<meta property="og:image" content="assets/images/opengraph.png" />'
)

# Fix shortlink
content = content.replace(
    "href='https://htarchitecte.com/'",
    "href='https://www.tiagorcorreia.com/'"
)

# Fix WP block library CSS (external)
content = re.sub(
    r"<link rel='stylesheet'[^>]*href='https://htarchitecte\.com/wp-includes/[^']*'[^>]*/>",
    '<!-- WP block styles removed -->',
    content
)

# Fix logo in sidebar/nav
content = content.replace(
    'src="https://htarchitecte.com/wp-content/themes/qh-timber/theme/dist/assets/images/logo.svg"',
    'src="assets/images/sprite.svg#logo"'
)
# Actually fix the whole img tag for logo
content = content.replace(
    '<img src="assets/images/sprite.svg#logo"  alt="HTA Logo">',
    '<svg role="img" class="c-header_logo_svg"><use href="assets/images/sprite.svg#logo"></use></svg>'
)

# ─── 3. FIX VENDORS.JS ───────────────────────────────────────
# Check if vendors.js exists at root level (not in assets/scripts)
vendors_root = BASE / "vendors.js"
vendors_assets = BASE / "assets" / "scripts" / "vendors.js"
if vendors_root.exists():
    print(f"vendors.js exists at root: {vendors_root.stat().st_size} bytes")
elif vendors_assets.exists():
    content = content.replace('src="vendors.js"', 'src="assets/scripts/vendors.js"')
    print("Fixed vendors.js path to assets/scripts/")
else:
    print("⚠ vendors.js not found anywhere - keeping reference as-is")

# ─── 4. UPDATE CSS VARIABLE ──────────────────────────────────
content = re.sub(r'--gridSize:\s*\d+vw;', f'--gridSize: {grid_size};', content)

# ─── WRITE ────────────────────────────────────────────────────
with open(BASE / "index.html", "w", encoding="utf-8") as f:
    f.write(content)

# Count remaining HTA refs
remaining = content.count('htarchitecte.com')
print(f"\n✅ Audit fixes applied")
print(f"   Remaining htarchitecte.com refs: {remaining}")

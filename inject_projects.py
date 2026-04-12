#!/usr/bin/env python3
"""
Inject real projects into index.html
Replaces the HTA grid and projects-list with tiagorcorreia.com projects
"""
import json, re, html as html_mod
from pathlib import Path

BASE = Path("/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2")

with open("/tmp/trc_projects.json", "r") as f:
    projects = json.load(f)

with open(BASE / "index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Load local image info
with open(BASE / "projects-data.json", "r") as f:
    proj_index = json.load(f)
thumb_map = {p["slug"]: p["thumb"] for p in proj_index}

# Get categories
categories = sorted(set(html_mod.unescape(p["cat"]) for p in projects))

# ─── 1. REPLACE CATEGORIES FILTER ───────────────────────────
cat_items = ""
for cat in categories:
    cat_items += f'''                    <li class="c-select_list_item " data-category="" data-filter="item">
                        <a href="index.html?category={cat.lower().replace(' ', '-')}" data-load="projects">
                            {cat}
                        </a>
                    </li>
'''

cat_items += '''                <li class="c-select_list_item -footer is-current" data-category="" data-filter="item">
                    <a href="index.html?category=allcategories" data-load="projects">
                        Todas as categorias
                    </a>
                </li>'''

# Replace categories in select list
cat_pattern = r'(<span class="c-select_list">\s*<ul>)(.*?)(</ul>)'
def replace_cats(m):
    return m.group(1) + "\n" + cat_items + "\n            " + m.group(3)
content = re.sub(cat_pattern, replace_cats, content, flags=re.DOTALL)

# Replace "All categories" button text
content = content.replace(
    '                    All categories\n                                <svg',
    '                    Todas as categorias\n                                <svg'
)

# ─── 2. REPLACE GRID (data-module-grid) ─────────────────────
# 17 projects, each with up to 3 grid images
# Original has 14 columns with 2 projects each = 28 projects
# We'll use ceil(17/2) = 9 columns with 2 projects each (last col has 1)
num_projects = len(projects)
num_cols = (num_projects + 1) // 2  # 9 columns
col_width = round(100 / num_cols, 7)  # ~11.111%
grid_size = f"{num_cols * 35}vw"  # approximate grid width

grid_html = ""
proj_idx = 0
for col in range(num_cols):
    grid_html += f'            <div class="c-grid_col js-grid-col" data-index={col+1} style="width: {col_width}%">\n'

    # Each column has up to 2 projects
    for _ in range(2):
        if proj_idx >= num_projects:
            break
        p = projects[proj_idx]
        slug = p["slug"]
        title = p["title"]
        href = f"{slug}.html"
        thumb_path = thumb_map.get(slug, "")

        # Get up to 3 images for grid thumbnails
        local_dir = BASE / "assets" / "images" / "projetos" / slug
        grid_imgs = []
        if local_dir.exists():
            files = sorted(local_dir.iterdir())
            for f in files[:3]:
                grid_imgs.append(f"assets/images/projetos/{slug}/{f.name}")

        if not grid_imgs and thumb_path:
            grid_imgs = [thumb_path]

        grid_html += f'''
                <div class="c-grid_col_project" data-grid="project">
'''
        for img_path in grid_imgs:
            # Guess dimensions based on typical aspect ratios
            w, h = 600, 685  # default tall
            if grid_imgs.index(img_path) == 1:
                w, h = 600, 425  # middle one wider
            grid_html += f'''                    <div class="c-grid_item" data-grid="item">
                        <figure class="c-grid_figure" data-grid="plane" data-src="{img_path}" data-id={p["id"]} data-href="{href}">
                            <img loading="lazy" data-src="{img_path}" width="{w}" height="{h}" alt="{title}">
                            <span data-load="project" data-load-delay="0">{title}</span>
                        </figure>
                    </div>
'''
        grid_html += '                </div>\n'
        proj_idx += 1

    grid_html += '            </div>\n'

# Replace the entire grid div
grid_pattern = r'<div class="c-grid" data-module-grid data-grid-projects-number="\d+" style="--gridSize: \d+vw">.*?</div>\s*(?=<div class="c-projects-list"|</section>)'
new_grid = f'<div class="c-grid" data-module-grid data-grid-projects-number="{num_projects}" style="--gridSize: {grid_size}">\n    \n{grid_html}</div>\n'
content = re.sub(grid_pattern, new_grid, content, flags=re.DOTALL)

# Also update the --gridSize CSS variable
content = re.sub(r'--gridSize:\s*\d+vw;', f'--gridSize: {grid_size};', content)

# ─── 3. REPLACE PROJECTS LIST (horizontal scroll list) ──────
list_html = ""
for p in projects:
    slug = p["slug"]
    title = p["title"]
    cat = html_mod.unescape(p["cat"])
    href = f"{slug}.html"
    pid = p["id"]
    thumb_path = thumb_map.get(slug, "")

    # Get slider images (up to 3 for mobile)
    local_dir = BASE / "assets" / "images" / "projetos" / slug
    slider_imgs = []
    if local_dir.exists():
        files = sorted(local_dir.iterdir())
        for f_img in files[:3]:
            slider_imgs.append(f"assets/images/projetos/{slug}/{f_img.name}")

    slider_html = ""
    for img_path in slider_imgs:
        slider_html += f'''                            <div class="swiper-slide">
                                <img loading="lazy" src="{img_path}" width="600" height="685" alt="{title}">
                            </div>
'''

    # Determine orientation class for desktop thumbnail
    orientation = "-landscape"
    thumb_w, thumb_h = 1500, 1000
    # Find the thumb image dimensions from project data
    for img_info in p["imgs"]:
        if img_info["url"] == p["thumb"]:
            if img_info["h"] > img_info["w"]:
                orientation = "-portrait"
                thumb_w, thumb_h = 1000, 1500
            break

    list_html += f'''        <section class="c-projects-list_item" data-scroll="item">
            <a href="{href}" class="c-projects-list_item_image" data-load="project" data-load-delay="0" id="projectList-{pid}">
                <span class="c-projects-list_item_arrow u-none@from-medium">
                    <svg role="img"><use href="assets/images/sprite.svg#arrow-right"></use></svg>
                </span>
                <p class="c-projects-list_item_name c-heading -h2">
                    {title}
                </p>
                <p class="u-text-gray-dark u-none@from-medium">
                    {cat}
                </p>
                <div class="c-projects_list_item_slider u-none@from-medium" data-module-slider>
                    <div class="swiper" data-slider="slider">
                        <div class="swiper-wrapper">
{slider_html}                        </div>
                    </div>
                </div>
                <div class="c-projects-list_item_image_inner u-none@to-medium">
                    <div
                        data-scroll="item"
                        data-scroll-target="#projectList-{pid}"
                        data-module-timeline="projectList{pid}"
                        data-timeline-mobile
                        data-scroll-progress-call="progress,Timeline,projectList{pid}"
                        data-timeline-from='{{"x":"-4vw"}}'
                        data-timeline-to='{{"x":"4vw"}}'
                        data-timeline-mobile-from='{{"y":"-5vh"}}'
                        data-timeline-mobile-to='{{"y":"5vh"}}'
                    >
                        <img
                            class="{orientation}"
                            src="{thumb_path}"
                            width="{thumb_w}" height="{thumb_h}" alt="{title}">
                    </div>
                </div>
            </a>
        </section>
'''

# Replace the projects-list_inner contents
list_pattern = r'(<div class="c-projects-list_inner">)\s*(.*?)\s*(</div>\s*</div>)\s*(?=<script type="text/javascript">)'
def replace_list(m):
    return m.group(1) + "\n" + list_html + "    " + m.group(3) + "\n"
content = re.sub(list_pattern, replace_list, content, flags=re.DOTALL)

# ─── 4. WRITE OUTPUT ────────────────────────────────────────
with open(BASE / "index.html", "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ index.html updated:")
print(f"   - {num_projects} projects in grid ({num_cols} columns)")
print(f"   - {num_projects} projects in horizontal list")
print(f"   - {len(categories)} categories: {', '.join(categories)}")
print(f"   - Grid size: {grid_size}")

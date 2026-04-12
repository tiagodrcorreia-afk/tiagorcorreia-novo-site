#!/usr/bin/env python3
"""
Build project pages for novo-site-v2
Downloads images from WordPress and generates HTML using HTA template
"""
import json, os, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path("/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2")
IMG_BASE = BASE / "assets" / "images" / "projetos"

with open("/tmp/trc_projects.json", "r") as f:
    projects = json.load(f)

# ─── 1. DOWNLOAD IMAGES ────────────────────────────────────────
def download_image(url, dest):
    """Download a single image, skip if already exists"""
    if dest.exists() and dest.stat().st_size > 0:
        return f"SKIP {dest.name}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(dest, "wb") as out:
                out.write(resp.read())
        return f"  OK {dest.name}"
    except Exception as e:
        return f"FAIL {dest.name}: {e}"

# Build download queue
download_queue = []
for proj in projects:
    slug = proj["slug"]
    proj_dir = IMG_BASE / slug

    # Collect all unique image URLs (thumb + gallery)
    seen_urls = set()
    all_imgs = []

    # Add thumbnail first if not in gallery
    thumb_url = proj["thumb"]
    if thumb_url:
        seen_urls.add(thumb_url)
        ext = os.path.splitext(thumb_url.split("?")[0])[1] or ".jpg"
        fname = f"thumb{ext}"
        all_imgs.append({"url": thumb_url, "fname": fname})

    # Add gallery images
    for i, img in enumerate(proj["imgs"]):
        url = img["url"]
        if url in seen_urls:
            # thumb was already added, mark it
            continue
        seen_urls.add(url)
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        fname = f"{i+1:02d}{ext}"
        all_imgs.append({"url": url, "fname": fname, "w": img["w"], "h": img["h"]})

    proj["_local_imgs"] = all_imgs

    for img_info in all_imgs:
        dest = proj_dir / img_info["fname"]
        download_queue.append((img_info["url"], dest))

print(f"=== Downloading {len(download_queue)} images for {len(projects)} projects ===")

downloaded = 0
skipped = 0
failed = 0

with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_image, url, dest): (url, dest) for url, dest in download_queue}
    for future in as_completed(futures):
        result = future.result()
        if "SKIP" in result:
            skipped += 1
        elif "OK" in result:
            downloaded += 1
        else:
            failed += 1
            print(result)

print(f"  Downloaded: {downloaded} | Skipped: {skipped} | Failed: {failed}")
print()

# ─── 2. GENERATE HTML PAGES ────────────────────────────────────

def generate_image_block(img_path, width, height, alt, timeline_id):
    """Generate a single image block matching the HTA template"""
    return f'''                    <div class="c-project_images">
                        <div class="c-project_image">
                            <div class="c-image">
                                <div class="c-image_wrap" data-scroll="item">
                                    <div class="c-image_inner u-cover"
                                        data-scroll="item"
                                        data-module-timeline="{timeline_id}"
                                        data-scroll-progress-call="progress,Timeline,{timeline_id}"
                                        data-timeline-from='{{"y":"-15%"}}'
                                        data-timeline-to='{{"y":"15%"}}'
                                        data-timeline-mobile
                                    >
                                        <img src="{img_path}" width="{width}" height="{height}" alt="{alt}">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>'''

def generate_project_html(proj):
    """Generate a complete project HTML page"""
    slug = proj["slug"]
    title = proj["title"]
    cat = proj["cat"]

    # Build image blocks (skip thumb, use gallery images)
    img_blocks = []
    # Use first image as hero (thumbnail)
    hero_img = None
    gallery_imgs = []

    for img_info in proj["_local_imgs"]:
        fname = img_info["fname"]
        local_path = f"assets/images/projetos/{slug}/{fname}"
        w = img_info.get("w", 2560)
        h = img_info.get("h", 1440)

        if fname.startswith("thumb"):
            hero_img = {"path": local_path, "w": w, "h": h}
        else:
            gallery_imgs.append({"path": local_path, "w": w, "h": h, "fname": fname})

    # If no separate thumb, use first gallery image as hero
    if not hero_img and gallery_imgs:
        hero_img = gallery_imgs[0]
        gallery_imgs = gallery_imgs[1:]
    elif not hero_img:
        hero_img = {"path": "assets/images/projetos/placeholder.jpg", "w": 2560, "h": 1440}

    # Generate gallery HTML
    gallery_html = ""
    for i, img in enumerate(gallery_imgs):
        timeline_id = f"img-{slug}-{i}"
        gallery_html += generate_image_block(img["path"], img["w"], img["h"], title, timeline_id) + "\n"

    html = f'''<!doctype html>
<html class="no-js no-svg" lang="pt-PT" data-template="single">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>{title} — Tiago R. Correia Arquitectos</title>
    <meta property="og:title" content="{title}" />
    <meta property="og:type" content="website" />
    <link rel="stylesheet" href="assets/styles/main.css" type="text/css" media="screen" />
    <link rel="stylesheet" href="assets/styles/main.css" media="all"
        onload="this.media='all'; this.onload=null; this.isLoaded=true">
    <style>
        :root {{
            --gridSize: 315vw;
            --app-availheight: 100vh;
            --app-height: 100vh;
            --app-height-negative: -100vh;
        }}
    </style>
</head>
<body class="project-template-default single single-project postid-{proj['id']}" data-module-load>
    <span class="c-spinner -mobile">
        <svg role="img"><use href="assets/images/sprite.svg#spinner"></use></svg>
    </span>
    <div data-load-container data-template="single">

<div class="c-popups_container is-loaded">
    <div class="c-popups" data-load-container="project" data-template="single">
        <div class="c-popup_container is-loaded" id="popup-project">
            <div class="c-popup">

<div class="c-popup_scroll"
    data-module-popup="project"
    data-popup-transition="project"
    data-popup-closing-href="index.html"
    data-module-scroll="popupproject"
    data-scroll-wrapper="#popup-project"
>
    <button class="c-project_infos_button_wrap"
        data-load="projectInfos"
        data-load-delay="0"
        data-module-project-infos-button="main"
        data-project-infos-button-href="{slug}.html"
    >
        <span class="c-project_infos_button c-button-round">
            <svg role="img"><use href="assets/images/sprite.svg#info"></use></svg>
        </span>
    </button>
    <span class="c-popup_progress" data-scroll="progress"></span>

    <div class="c-popup_inner" id="popupInner">
        <article class="c-project">
            <header class="c-project_header" id="headerProject">
                <div class="c-project_header_heading o-container -small">
                    <h1 class="c-project_header_title c-heading -h1">{title}</h1>
                </div>
                <div class="c-project_header_background u-cover"
                    data-scroll="item"
                    data-module-timeline="headerBackgroundProject"
                    data-scroll-progress-call="progress,Timeline,headerBackgroundProject"
                    data-timeline-from='{{"filter":"blur(0px)"}}'
                    data-timeline-to='{{"filter":"blur(10px)"}}'
                    data-scroll-start="top top"
                    data-scroll-target="#headerProject"
                    data-timeline-mobile
                >
                    <img
                        data-scroll="item"
                        data-module-timeline="headerBackgroundProjectImage"
                        data-scroll-progress-call="progress,Timeline,headerBackgroundProjectImage"
                        data-timeline-from='{{"y":"0"}}'
                        data-timeline-to='{{"y":"60%"}}'
                        data-scroll-start="top top"
                        data-scroll-target="#headerProject"
                        data-timeline-mobile
                        data-timeline-mobile-from='{{"y":"0"}}'
                        data-timeline-mobile-to='{{"y":"30%"}}'
                        src="{hero_img['path']}"
                        width="{hero_img['w']}"
                        height="{hero_img['h']}"
                        alt="{title}">
                </div>
                <span class="c-theme_trigger"
                    data-scroll="item"
                    data-scroll-call="trigger,Theme,main"
                    data-trigger-inside="light"
                    data-trigger-outside="dark"
                    data-scroll-repeat
                ></span>
            </header>

            <div class="o-container -small"
                data-scroll="item"
                data-scroll-repeat
                data-scroll-start="top 90%"
                data-scroll-call="trigger,ProjectInfosButton,main"
                id="popupProjectContent">
{gallery_html}
            </div>
        </article>
    </div>
    <span class="c-popup_footer"
        data-scroll="item"
        data-scroll-id="popupFooterPproject"
        data-scroll-progress-call="progress,Timeline"
        data-scroll-end="bottom bottom"
        data-module-timeline="popupFooterPproject"
        data-timeline-from='{{"opacity": 1}}'
        data-timeline-to='{{"opacity": 0}}'
        data-timeline-mobile
    ></span>
    <span
        class="c-popup_close_trigger"
        data-scroll="item"
        data-scroll-call="close,Popup,project"
    ></span>
</div>
            </div>
        </div>
    </div>
</div>

<!-- Header -->
<header class="c-header" data-module-header>
    <div class="c-header_inner">
        <a href="index.html" class="c-header_logo" data-load="home">
            <svg role="img"><use href="assets/images/sprite.svg#logo"></use></svg>
        </a>
        <div class="c-header_menu">
            <button class="c-header_menu_button" data-module-nav-button type="button">
                <span class="c-header_menu_label">Menu</span>
            </button>
        </div>
    </div>
</header>

<!-- Navigation -->
<nav class="c-nav" data-module-nav>
    <div class="c-nav_background" data-nav="background"></div>
    <div class="c-nav_inner">
        <ul class="c-nav_list">
            <li class="c-nav_list_item">
                <a href="index.html" data-load="home" class="c-nav_list_link c-heading -h1">Projectos</a>
            </li>
            <li class="c-nav_list_item">
                <a href="#" class="c-nav_list_link c-heading -h1">Sobre</a>
            </li>
            <li class="c-nav_list_item">
                <a href="#" class="c-nav_list_link c-heading -h1">Contacto</a>
            </li>
        </ul>
    </div>
</nav>

    </div>

    <script src="assets/scripts/app.js" defer></script>
</body>
</html>'''
    return html


print("=== Generating HTML pages ===")
for proj in projects:
    slug = proj["slug"]
    html = generate_project_html(proj)
    output_path = BASE / f"{slug}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    img_count = len(proj["_local_imgs"])
    print(f"  ✓ {slug}.html ({img_count} images)")

print(f"\n=== Done! {len(projects)} project pages generated ===")

# Also generate a projects index JSON for the homepage
index = []
for proj in projects:
    slug = proj["slug"]
    thumb_info = proj["_local_imgs"][0] if proj["_local_imgs"] else None
    thumb_path = f"assets/images/projetos/{slug}/{thumb_info['fname']}" if thumb_info else ""
    index.append({
        "id": proj["id"],
        "title": proj["title"],
        "slug": slug,
        "category": proj["cat"],
        "thumb": thumb_path,
        "href": f"{slug}.html",
        "imageCount": len(proj["_local_imgs"])
    })

with open(BASE / "projects-data.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"  ✓ projects-data.json (index for homepage)")

#!/usr/bin/env python3
"""
Static site generator for tiagorcorreia.com
Reads WordPress data from JSON files and generates static HTML pages.
"""

import json
import os
import re
from html import escape, unescape
from datetime import datetime

# ── Paths ──
BASE_DIR = "/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2"
DATA_DIR = "/Users/tiagocorreia/.claude/projects/-Users-tiagocorreia-Documents-Claude-website/07338bbb-992e-465c-8448-14e9681cfdee/tool-results"

PORTFOLIO_FILE = os.path.join(DATA_DIR, "toolu_01QTR6zhfiF8BA12qboiom1d.txt")
BLOG_FILE = os.path.join(DATA_DIR, "mcp-novamira-tiagorcorreia-com-mcp-adapter-execute-ability-1775929824559.txt")
PAGES_FILE = os.path.join(DATA_DIR, "mcp-novamira-tiagorcorreia-com-mcp-adapter-execute-ability-1775929828068.txt")


# ── Load data ──
def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['data']['return_value']


portfolio_items = load_json(PORTFOLIO_FILE)
blog_posts = load_json(BLOG_FILE)
all_pages = load_json(PAGES_FILE)

# Build page lookup
pages_by_slug = {p['slug']: p for p in all_pages}


# ── Helpers ──
def clean_content(html_content):
    """Remove data-path-to-node and data-index-in-node attributes, convert WP URLs to local."""
    if not html_content:
        return ''
    # Remove data attributes
    html_content = re.sub(r'\s*data-path-to-node="[^"]*"', '', html_content)
    html_content = re.sub(r'\s*data-index-in-node="[^"]*"', '', html_content)
    html_content = re.sub(r'\s*data-elementor-[a-z-]+="[^"]*"', '', html_content)
    # Convert WordPress image URLs to local
    html_content = localize_images(html_content)
    # Fix internal links
    html_content = fix_internal_links(html_content)
    return html_content


def localize_images(html_content):
    """Convert https://www.tiagorcorreia.com/wp-content/uploads/... to assets/images/wp-content/uploads/..."""
    if not html_content:
        return ''
    html_content = html_content.replace(
        'https://www.tiagorcorreia.com/wp-content/uploads/',
        'assets/images/wp-content/uploads/'
    )
    return html_content


def localize_images_for_subdir(html_content):
    """Same but for pages in noticias/ subfolder — needs ../assets/..."""
    if not html_content:
        return ''
    html_content = html_content.replace(
        'https://www.tiagorcorreia.com/wp-content/uploads/',
        '../assets/images/wp-content/uploads/'
    )
    return html_content


def fix_internal_links(html_content, prefix=''):
    """Convert WordPress URLs to local static paths."""
    if not html_content:
        return ''
    # Portfolio item links
    for item in portfolio_items:
        slug = item['slug']
        html_content = html_content.replace(
            f'https://www.tiagorcorreia.com/portfolio-item/{slug}/',
            f'{prefix}{slug}.html'
        )
        html_content = html_content.replace(
            f'/portfolio-item/{slug}/',
            f'{prefix}{slug}.html'
        )
    # Blog post links
    for post in blog_posts:
        slug = post['slug']
        html_content = html_content.replace(
            f'https://www.tiagorcorreia.com/{slug}/',
            f'{prefix}noticias/{slug}.html'
        )
    # Page links
    link_map = {
        '/servicos/': f'{prefix}servicos.html',
        '/sobre-nos/': f'{prefix}sobre-nos.html',
        '/contactos/': f'{prefix}contactos.html',
        '/noticias/': f'{prefix}noticias.html',
        '/projetos/': f'{prefix}projetos.html',
        'https://www.tiagorcorreia.com/servicos/': f'{prefix}servicos.html',
        'https://www.tiagorcorreia.com/sobre-nos/': f'{prefix}sobre-nos.html',
        'https://www.tiagorcorreia.com/contactos/': f'{prefix}contactos.html',
        'https://www.tiagorcorreia.com/noticias/': f'{prefix}noticias.html',
        'https://www.tiagorcorreia.com/projetos/': f'{prefix}projetos.html',
        'https://www.tiagorcorreia.com/': f'{prefix}index.html',
        'https://www.tiagorcorreia.com': f'{prefix}index.html',
    }
    for old, new in link_map.items():
        html_content = html_content.replace(old, new)
    return html_content


def localize_thumbnail(url, prefix=''):
    """Convert thumbnail URL to local path."""
    if not url:
        return f'{prefix}assets/images/opengraph.png'
    return url.replace(
        'https://www.tiagorcorreia.com/wp-content/uploads/',
        f'{prefix}assets/images/wp-content/uploads/'
    )


def excerpt_from_content(content, max_len=160):
    """Strip HTML and get first N chars for meta description."""
    if not content:
        return 'Tiago R. Correia Arquitectos - Arquitectura e Design em Lisboa'
    text = re.sub(r'<[^>]+>', '', content)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_len:
        text = text[:max_len-3].rsplit(' ', 1)[0] + '...'
    return text


def format_date(date_str):
    """Format WordPress date to readable Portuguese format."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        months_pt = {1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',
                     7:'Julho',8:'Agosto',9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
        return f'{dt.day} {months_pt[dt.month]} {dt.year}'
    except:
        return date_str


def format_date_short(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d.%m.%Y')
    except:
        return date_str


# ── CSS shared across all generated pages ──
INLINE_CSS = """
        /* ── TRC Static Page Styles ── */
        *, *::before, *::after { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            color: #212122;
            background: #fff;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        a { color: inherit; }
        img { max-width: 100%; height: auto; display: block; }

        /* ── Menu Button ── */
        .trc-menu-btn {
            position: fixed;
            top: 28px;
            right: 32px;
            z-index: 200;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 13px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #1a1a1a;
            background: none;
            border: none;
            cursor: pointer;
            padding: 8px 0;
            -webkit-font-smoothing: antialiased;
            -webkit-appearance: none;
            appearance: none;
        }
        .trc-menu-btn_icon {
            display: inline-flex;
            flex-direction: column;
            justify-content: center;
            gap: 3.5px;
            width: 18px;
            height: 14px;
            flex-shrink: 0;
            margin-right: 10px;
            position: relative;
        }
        .trc-menu-btn_icon span {
            display: block;
            height: 1.5px;
            width: 100%;
            background: currentColor;
            transition: transform 0.35s cubic-bezier(0.16,1,0.3,1), opacity 0.25s ease;
            transform-origin: center;
        }
        html.trc-menu-open .trc-menu-btn_icon span:nth-child(1) {
            transform: translateY(3.25px) rotate(45deg);
        }
        html.trc-menu-open .trc-menu-btn_icon span:nth-child(2) { opacity: 0; }
        html.trc-menu-open .trc-menu-btn_icon span:nth-child(3) {
            transform: translateY(-3.25px) rotate(-45deg);
        }

        /* ── Backdrop ── */
        .trc-menu-backdrop {
            position: fixed;
            inset: 0;
            z-index: 140;
            background: rgba(0,0,0,0.25);
            backdrop-filter: blur(2px);
            -webkit-backdrop-filter: blur(2px);
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.45s ease, visibility 0s 0.45s;
            cursor: pointer;
        }
        html.trc-menu-open .trc-menu-backdrop {
            opacity: 1;
            visibility: visible;
            transition: opacity 0.45s ease, visibility 0s 0s;
        }

        /* ── Overlay Panel ── */
        .trc-menu-overlay {
            position: fixed;
            top: 0; right: 0;
            z-index: 150;
            width: 420px;
            max-width: 50vw;
            height: 100vh;
            height: 100dvh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: #fff;
            transform: translateX(100%);
            transition: transform 0.55s cubic-bezier(0.16,1,0.3,1);
            box-shadow: -20px 0 60px rgba(0,0,0,0.08);
            overflow-y: auto;
        }
        html.trc-menu-open .trc-menu-overlay { transform: translateX(0); }

        .trc-menu-content {
            display: flex;
            flex-direction: column;
            padding: 80px 48px 48px;
            flex: 1;
        }
        .trc-menu-nav {
            list-style: none;
            margin: 0 0 48px 0;
            padding: 0;
        }
        .trc-menu-nav li { overflow: hidden; }
        .trc-menu-nav a {
            display: block;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-size: clamp(2rem, 3.5vw, 3rem);
            font-weight: 200;
            letter-spacing: 0.04em;
            line-height: 1.35;
            color: #1a1a1a;
            text-decoration: none;
            transform: translateX(40px);
            opacity: 0;
            transition: transform 0.55s cubic-bezier(0.16,1,0.3,1), opacity 0.45s ease, color 0.3s ease;
            -webkit-font-smoothing: antialiased;
        }
        .trc-menu-nav a:hover { color: #888; }
        html.trc-menu-open .trc-menu-nav a { transform: translateX(0); opacity: 1; }
        .trc-menu-nav li:nth-child(1) a { transition-delay: 0.10s; }
        .trc-menu-nav li:nth-child(2) a { transition-delay: 0.15s; }
        .trc-menu-nav li:nth-child(3) a { transition-delay: 0.20s; }
        .trc-menu-nav li:nth-child(4) a { transition-delay: 0.25s; }
        .trc-menu-nav li:nth-child(5) a { transition-delay: 0.30s; }
        html:not(.trc-menu-open) .trc-menu-nav a { transition-delay: 0s; }

        .trc-menu-divider {
            width: 40px;
            height: 1px;
            background: #ccc;
            margin-bottom: 32px;
        }
        .trc-menu-info {
            display: flex;
            flex-direction: column;
            opacity: 0;
            transform: translateY(15px);
            transition: opacity 0.5s ease 0.25s, transform 0.5s cubic-bezier(0.16,1,0.3,1) 0.25s;
        }
        html.trc-menu-open .trc-menu-info { opacity: 1; transform: translateY(0); }
        html:not(.trc-menu-open) .trc-menu-info { transition-delay: 0s; }
        .trc-menu-info_section { margin-bottom: 28px; }
        .trc-menu-info_label {
            font-family: "Maison Neue", -apple-system, "Helvetica Neue", helvetica, arial, sans-serif;
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 8px;
        }
        .trc-menu-info p, .trc-menu-info a {
            font-family: "Maison Neue", -apple-system, "Helvetica Neue", helvetica, arial, sans-serif;
            font-size: 14px;
            font-weight: 300;
            line-height: 1.7;
            color: #333;
            text-decoration: none;
            margin: 0;
            -webkit-font-smoothing: antialiased;
        }
        .trc-menu-info a:hover { color: #888; }
        .trc-menu-social { display: flex; gap: 20px; margin-top: 6px; }
        .trc-menu-social a {
            font-size: 12px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .trc-menu-lang {
            display: flex;
            gap: 16px;
            padding: 0 48px 32px;
            opacity: 0;
            transition: opacity 0.4s ease 0.3s;
        }
        html.trc-menu-open .trc-menu-lang { opacity: 1; }
        html:not(.trc-menu-open) .trc-menu-lang { transition-delay: 0s; }
        .trc-menu-lang a {
            font-family: "Maison Neue", -apple-system, "Helvetica Neue", helvetica, arial, sans-serif;
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #aaa;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .trc-menu-lang a.is-active { color: #1a1a1a; }
        .trc-menu-lang a:hover { color: #1a1a1a; }
        html.trc-menu-open { overflow: hidden; }

        @media (max-width: 768px) {
            .trc-menu-overlay { width: 85vw; max-width: none; }
            .trc-menu-content { padding: 72px 28px 28px; }
            .trc-menu-lang { padding: 0 28px 24px; }
            .trc-menu-btn { top: 20px; right: 20px; }
        }

        /* ── Page Layout ── */
        .trc-page-hero {
            position: relative;
            width: 100%;
            height: 70vh;
            min-height: 400px;
            overflow: hidden;
            background: #111;
        }
        .trc-page-hero img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }
        .trc-page-hero_overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.5) 100%);
            display: flex;
            align-items: flex-end;
            padding: 4rem 5vw;
        }
        .trc-page-hero_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(2rem, 4vw, 3.5rem);
            letter-spacing: 0.06em;
            color: #fff;
            margin: 0;
            -webkit-font-smoothing: antialiased;
        }
        .trc-page-hero_cats {
            display: flex;
            gap: 12px;
            margin-top: 1rem;
        }
        .trc-page-hero_cat {
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: rgba(255,255,255,0.8);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 4px 14px;
            border-radius: 2px;
        }

        /* ── Content Area ── */
        .trc-content {
            max-width: 860px;
            margin: 0 auto;
            padding: 4rem 5vw 3rem;
            font-size: 1rem;
            line-height: 1.85;
        }
        .trc-content h1, .trc-content h2, .trc-content h3, .trc-content h4 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            letter-spacing: 0.03em;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
        }
        .trc-content h1 { font-size: clamp(1.8rem, 3vw, 2.6rem); }
        .trc-content h2 { font-size: clamp(1.4rem, 2.5vw, 2rem); }
        .trc-content h3 { font-size: clamp(1.2rem, 2vw, 1.5rem); font-weight: 300; }
        .trc-content h4 { font-size: 1.1rem; font-weight: 300; }
        .trc-content p { margin-bottom: 1.5rem; }
        .trc-content a { text-decoration: underline; text-underline-offset: 3px; }
        .trc-content a:hover { opacity: 0.6; }
        .trc-content ul, .trc-content ol { padding-left: 1.5rem; margin-bottom: 1.5rem; }
        .trc-content li { margin-bottom: 0.5rem; }
        .trc-content img {
            border-radius: 2px;
            margin: 2rem 0;
        }
        .trc-content blockquote {
            border-left: 2px solid #ddd;
            margin: 2rem 0;
            padding: 1rem 2rem;
            font-style: italic;
            color: #555;
        }

        /* ── Image Gallery ── */
        .trc-gallery {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 5vw 5rem;
        }
        .trc-gallery h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: 1.4rem;
            letter-spacing: 0.06em;
            margin-bottom: 2rem;
            color: #999;
        }
        .trc-gallery_grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 12px;
        }
        .trc-gallery_item {
            overflow: hidden;
            border-radius: 2px;
            aspect-ratio: 4/3;
        }
        .trc-gallery_item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.16,1,0.3,1);
        }
        .trc-gallery_item:hover img {
            transform: scale(1.04);
        }

        /* ── Back Link ── */
        .trc-back {
            display: inline-flex;
            align-items: center;
            gap: 0.6em;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #999;
            text-decoration: none;
            padding: 2rem 5vw;
            transition: color 0.3s ease;
        }
        .trc-back:hover { color: #212122; }
        .trc-back svg {
            width: 16px; height: 16px;
            stroke: currentColor; stroke-width: 1.5; fill: none;
        }

        /* ── Article Meta ── */
        .trc-article-meta {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }
        .trc-article-date {
            font-size: 0.82rem;
            color: #999;
            letter-spacing: 0.04em;
        }
        .trc-article-cat {
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #666;
            border: 1px solid #ddd;
            padding: 3px 12px;
            border-radius: 2px;
            text-decoration: none !important;
        }

        /* ── Grid Listings ── */
        .trc-listing {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 5vw 5rem;
        }
        .trc-listing_grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 2rem;
        }
        .trc-listing_card {
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .trc-listing_card_img {
            overflow: hidden;
            border-radius: 2px;
            aspect-ratio: 16/10;
            background: #f0f0f0;
        }
        .trc-listing_card_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.16,1,0.3,1);
        }
        .trc-listing_card:hover .trc-listing_card_img img {
            transform: scale(1.04);
        }
        .trc-listing_card_body {
            padding: 1rem 0;
        }
        .trc-listing_card_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: 1.15rem;
            letter-spacing: 0.02em;
            margin: 0 0 0.5rem;
        }
        .trc-listing_card_excerpt {
            font-size: 0.85rem;
            line-height: 1.6;
            color: #777;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .trc-listing_card_date {
            font-size: 0.75rem;
            color: #aaa;
            margin-bottom: 0.3rem;
        }
        .trc-listing_card_cats {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 0.5rem;
        }
        .trc-listing_card_cats span {
            font-size: 9px;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #999;
        }

        /* ── Section Header ── */
        .trc-section-header {
            padding: 8rem 5vw 3rem;
            max-width: 1400px;
            margin: 0 auto;
        }
        .trc-section-header h1 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(2.2rem, 4vw, 3.5rem);
            letter-spacing: 0.06em;
            margin: 0 0 1rem;
            -webkit-font-smoothing: antialiased;
        }
        .trc-section-header p {
            font-size: 1rem;
            line-height: 1.7;
            color: #777;
            max-width: 560px;
        }

        /* ── Contact Page ── */
        .trc-contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            max-width: 1100px;
            margin: 0 auto;
            padding: 3rem 5vw 5rem;
        }
        .trc-contact-item h3 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: 1.3rem;
            letter-spacing: 0.04em;
            margin-bottom: 1rem;
        }
        .trc-contact-item p {
            font-size: 0.95rem;
            line-height: 1.8;
            color: #555;
        }
        .trc-contact-item a {
            text-decoration: none;
            border-bottom: 1px solid rgba(0,0,0,0.15);
            padding-bottom: 2px;
            transition: border-color 0.3s ease;
        }
        .trc-contact-item a:hover { border-color: rgba(0,0,0,0.6); }

        /* ── Related Posts ── */
        .trc-related {
            background: #f7f8f9;
            padding: 4rem 5vw;
            margin-top: 3rem;
        }
        .trc-related h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: 1.5rem;
            letter-spacing: 0.06em;
            margin-bottom: 2.5rem;
            text-align: center;
        }
        .trc-related_grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* ── Footer ── */
        .trc-footer {
            background: #111;
            color: #999;
            padding: 3rem 5vw 2rem;
            font-size: 0.82rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .trc-footer a { color: #ccc; text-decoration: none; }
        .trc-footer a:hover { color: #fff; }

        /* ── Services page specific ── */
        .trc-services-page {
            max-width: 1000px;
            margin: 0 auto;
            padding: 4rem 5vw 5rem;
        }

        @media (max-width: 768px) {
            .trc-page-hero { height: 50vh; min-height: 300px; }
            .trc-page-hero_overlay { padding: 2rem 5vw; }
            .trc-gallery_grid { grid-template-columns: 1fr; }
            .trc-listing_grid { grid-template-columns: 1fr; }
            .trc-contact-grid { grid-template-columns: 1fr; gap: 2rem; }
            .trc-section-header { padding-top: 5rem; }
        }
"""


# ── Menu HTML ──
def menu_html(prefix='', active=''):
    """Generate the menu button + overlay. prefix is '' for root or '../' for subdir."""
    return f'''
    <!-- Menu -->
    <button class="trc-menu-btn" id="trcMenuBtn" type="button" aria-label="Menu">
        <span class="trc-menu-btn_icon">
            <span></span><span></span><span></span>
        </span>
        Menu
    </button>
    <div class="trc-menu-backdrop" id="trcMenuBackdrop"></div>
    <div class="trc-menu-overlay" id="trcMenuOverlay">
        <div class="trc-menu-content">
            <nav>
                <ul class="trc-menu-nav">
                    <li><a href="{prefix}index.html">Projectos</a></li>
                    <li><a href="{prefix}sobre-nos.html">Sobre Nos</a></li>
                    <li><a href="{prefix}servicos.html">Servicos</a></li>
                    <li><a href="{prefix}noticias.html">Noticias</a></li>
                    <li><a href="{prefix}contactos.html">Contactos</a></li>
                </ul>
            </nav>
            <div class="trc-menu-divider"></div>
            <div class="trc-menu-info">
                <div class="trc-menu-info_section">
                    <div class="trc-menu-info_label">Contacto</div>
                    <p>
                        <a href="mailto:geral@tiagorcorreia.com">geral@tiagorcorreia.com</a><br>
                        <a href="tel:+351918660664">+351 918 660 664</a>
                    </p>
                </div>
                <div class="trc-menu-info_section">
                    <div class="trc-menu-info_label">Morada</div>
                    <p>R. dos Lagares d\'El-Rei 19A<br>1700-268 Lisboa</p>
                </div>
                <div class="trc-menu-info_section">
                    <div class="trc-menu-info_label">Redes</div>
                    <div class="trc-menu-social">
                        <a href="https://www.instagram.com/tiagorcorreia_arquitecto" target="_blank" rel="noopener">Instagram</a>
                        <a href="https://pt.linkedin.com/in/tiago-r-correia-15891528" target="_blank" rel="noopener">LinkedIn</a>
                        <a href="https://www.facebook.com/tiagorcorreia.arq/" target="_blank" rel="noopener">Facebook</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="trc-menu-lang">
            <a href="{prefix}projetos.html" class="is-active">PT</a>
            <a href="https://www.tiagorcorreia.com/en/">EN</a>
            <a href="https://www.tiagorcorreia.com/fr/">FR</a>
        </div>
    </div>
'''


MENU_JS = '''
    <script>
    (function() {
        var html = document.documentElement;
        var btn = document.getElementById('trcMenuBtn');
        var backdrop = document.getElementById('trcMenuBackdrop');
        var overlay = document.getElementById('trcMenuOverlay');
        if (!btn || !overlay) return;
        function closeMenu() { html.classList.remove('trc-menu-open'); }
        btn.addEventListener('click', function() { html.classList.toggle('trc-menu-open'); });
        if (backdrop) backdrop.addEventListener('click', closeMenu);
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && html.classList.contains('trc-menu-open')) closeMenu();
        });
    })();
    </script>
'''


def footer_html():
    return '''
    <footer class="trc-footer">
        <span>&copy; 2014&ndash;2026 Tiago R. Correia Arquitectos</span>
        <span>
            <a href="https://www.instagram.com/tiagorcorreia_arquitecto" target="_blank" rel="noopener">Instagram</a> &middot;
            <a href="https://pt.linkedin.com/in/tiago-r-correia-15891528" target="_blank" rel="noopener">LinkedIn</a> &middot;
            <a href="https://www.facebook.com/tiagorcorreia.arq/" target="_blank" rel="noopener">Facebook</a>
        </span>
    </footer>
'''


# ═══════════════════════════════════════════
#  1. PORTFOLIO ITEM PAGES
# ═══════════════════════════════════════════

def generate_portfolio_page(item):
    slug = item['slug']
    title = item['title']
    thumbnail = localize_thumbnail(item.get('thumbnail'))
    categories = item.get('categories', [])
    content = clean_content(item.get('content', ''))
    images = item.get('images', [])
    desc = excerpt_from_content(item.get('content', ''))

    cat_tags = ''.join(
        f'<span class="trc-page-hero_cat">{escape(c["name"])}</span>'
        for c in categories
    )

    gallery_items = ''
    for img_url in images:
        local_url = localize_thumbnail(img_url)
        gallery_items += f'''
                <div class="trc-gallery_item">
                    <img src="{local_url}" alt="{escape(title)}" loading="lazy">
                </div>'''

    gallery_section = ''
    if gallery_items:
        gallery_section = f'''
    <section class="trc-gallery">
        <h2>Galeria</h2>
        <div class="trc-gallery_grid">{gallery_items}
        </div>
    </section>'''

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>{escape(title)} &mdash; Tiago R. Correia Arquitectos</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape(title)} - Tiago R. Correia Arquitectos">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:image" content="{thumbnail}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html(prefix='')}

    <section class="trc-page-hero">
        <img src="{thumbnail}" alt="{escape(title)}">
        <div class="trc-page-hero_overlay">
            <div>
                <h1 class="trc-page-hero_title">{escape(title)}</h1>
                <div class="trc-page-hero_cats">{cat_tags}</div>
            </div>
        </div>
    </section>

    <a href="index.html" class="trc-back">
        <svg viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Voltar aos projectos
    </a>

    <article class="trc-content">
        {content}
    </article>
{gallery_section}
    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, f'{slug}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


# ═══════════════════════════════════════════
#  2. BLOG ARTICLE PAGES
# ═══════════════════════════════════════════

def generate_blog_page(post, all_posts):
    slug = post['slug']
    title = post['title']
    thumbnail = post.get('thumbnail', '')
    categories = post.get('categories', [])
    date_str = post.get('date', '')
    content = post.get('content', '')
    yoast_title = post.get('yoast_title', '') or f'{title} - Tiago R. Correia Arquitectos'
    yoast_desc = post.get('yoast_desc', '') or excerpt_from_content(content)

    # Clean content for subdir
    content = re.sub(r'\s*data-path-to-node="[^"]*"', '', content)
    content = re.sub(r'\s*data-index-in-node="[^"]*"', '', content)
    content = re.sub(r'\s*data-elementor-[a-z-]+="[^"]*"', '', content)
    content = localize_images_for_subdir(content)
    content = fix_internal_links(content, prefix='../')

    thumb_local = thumbnail.replace(
        'https://www.tiagorcorreia.com/wp-content/uploads/',
        '../assets/images/wp-content/uploads/'
    ) if thumbnail else '../assets/images/opengraph.png'

    cat_tags = ''.join(
        f'<span class="trc-article-cat">{escape(unescape(c["name"]))}</span>'
        for c in categories
    )

    formatted_date = format_date(date_str)

    # Related posts (same category, max 3)
    post_cats = {c['slug'] for c in categories}
    related = []
    for other in all_posts:
        if other['slug'] == slug:
            continue
        other_cats = {c['slug'] for c in other.get('categories', [])}
        if post_cats & other_cats:
            related.append(other)
        if len(related) >= 3:
            break
    # Fill with recent if needed
    if len(related) < 3:
        for other in all_posts:
            if other['slug'] == slug or other in related:
                continue
            related.append(other)
            if len(related) >= 3:
                break

    related_cards = ''
    for r in related:
        r_thumb = r.get('thumbnail', '')
        r_thumb_local = r_thumb.replace(
            'https://www.tiagorcorreia.com/wp-content/uploads/',
            '../assets/images/wp-content/uploads/'
        ) if r_thumb else '../assets/images/opengraph.png'
        r_excerpt = excerpt_from_content(r.get('content', ''), 100)
        related_cards += f'''
            <a class="trc-listing_card" href="{r['slug']}.html">
                <div class="trc-listing_card_img">
                    <img src="{r_thumb_local}" alt="{escape(r['title'])}" loading="lazy">
                </div>
                <div class="trc-listing_card_body">
                    <div class="trc-listing_card_date">{format_date_short(r.get('date',''))}</div>
                    <h3 class="trc-listing_card_title">{escape(r['title'])}</h3>
                    <p class="trc-listing_card_excerpt">{escape(r_excerpt)}</p>
                </div>
            </a>'''

    hero_section = ''
    if thumbnail:
        hero_section = f'''
    <section class="trc-page-hero">
        <img src="{thumb_local}" alt="{escape(title)}">
        <div class="trc-page-hero_overlay">
            <div>
                <h1 class="trc-page-hero_title">{escape(title)}</h1>
            </div>
        </div>
    </section>'''
    else:
        hero_section = f'''
    <div class="trc-section-header">
        <h1>{escape(title)}</h1>
    </div>'''

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>{escape(yoast_title)}</title>
    <meta name="description" content="{escape(yoast_desc)}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escape(yoast_title)}">
    <meta property="og:description" content="{escape(yoast_desc)}">
    <meta property="og:image" content="{thumb_local}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="../assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="../assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="../assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html(prefix='../')}
{hero_section}

    <a href="../noticias.html" class="trc-back">
        <svg viewBox="0 0 24 24"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Voltar as noticias
    </a>

    <article class="trc-content">
        <div class="trc-article-meta">
            <span class="trc-article-date">{formatted_date}</span>
            {cat_tags}
        </div>
        {content}
    </article>

    <section class="trc-related">
        <h2>Artigos Relacionados</h2>
        <div class="trc-related_grid">{related_cards}
        </div>
    </section>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    # Ensure noticias dir exists
    noticias_dir = os.path.join(BASE_DIR, 'noticias')
    os.makedirs(noticias_dir, exist_ok=True)

    filepath = os.path.join(noticias_dir, f'{slug}.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


# ═══════════════════════════════════════════
#  3. STATIC PAGES
# ═══════════════════════════════════════════

def generate_projetos_page():
    """Grid listing of all portfolio items."""
    cards = ''
    for item in portfolio_items:
        thumb = localize_thumbnail(item.get('thumbnail'))
        cats = item.get('categories', [])
        cat_spans = ''.join(f'<span>{escape(c["name"])}</span>' for c in cats)
        cards += f'''
            <a class="trc-listing_card" href="{item['slug']}.html">
                <div class="trc-listing_card_img">
                    <img src="{thumb}" alt="{escape(item['title'])}" loading="lazy">
                </div>
                <div class="trc-listing_card_body">
                    <h3 class="trc-listing_card_title">{escape(item['title'])}</h3>
                    <div class="trc-listing_card_cats">{cat_spans}</div>
                </div>
            </a>'''

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>Projectos &mdash; Tiago R. Correia Arquitectos</title>
    <meta name="description" content="Portfolio de projectos de arquitectura: condominios habitacionais, reabilitacao de edificios, moradias e turismo. Atelier Tiago R. Correia, Lisboa.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Projectos - Tiago R. Correia Arquitectos">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html()}

    <div class="trc-section-header">
        <h1>Projectos</h1>
        <p>Arquitectura residencial, reabilitacao urbana, condominios e espacos comerciais.</p>
    </div>

    <section class="trc-listing">
        <div class="trc-listing_grid">{cards}
        </div>
    </section>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, 'projetos.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_noticias_page():
    """Grid listing of all blog posts."""
    cards = ''
    for post in blog_posts:
        thumb = localize_thumbnail(post.get('thumbnail'))
        cats = post.get('categories', [])
        cat_spans = ''.join(f'<span>{escape(unescape(c["name"]))}</span>' for c in cats)
        excerpt = excerpt_from_content(post.get('content', ''), 120)
        cards += f'''
            <a class="trc-listing_card" href="noticias/{post['slug']}.html">
                <div class="trc-listing_card_img">
                    <img src="{thumb}" alt="{escape(post['title'])}" loading="lazy">
                </div>
                <div class="trc-listing_card_body">
                    <div class="trc-listing_card_date">{format_date_short(post.get('date',''))}</div>
                    <h3 class="trc-listing_card_title">{escape(post['title'])}</h3>
                    <p class="trc-listing_card_excerpt">{escape(excerpt)}</p>
                    <div class="trc-listing_card_cats">{cat_spans}</div>
                </div>
            </a>'''

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>Noticias &mdash; Tiago R. Correia Arquitectos</title>
    <meta name="description" content="Artigos tecnicos sobre arquitectura, licenciamento, investimento imobiliario e legislacao em Portugal. Blog do atelier Tiago R. Correia, Lisboa.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Noticias - Tiago R. Correia Arquitectos">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html()}

    <div class="trc-section-header">
        <h1>Noticias</h1>
        <p>Artigos sobre arquitectura, licenciamento, investimento imobiliario e legislacao em Portugal.</p>
    </div>

    <section class="trc-listing">
        <div class="trc-listing_grid">{cards}
        </div>
    </section>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, 'noticias.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_sobre_nos_page():
    """About page using WordPress page content."""
    page = pages_by_slug.get('sobre-nos', {})
    content = clean_content(page.get('content', ''))
    yoast_title = page.get('yoast_title', '') or 'Sobre Nos - Tiago R. Correia Arquitectos'
    yoast_desc = page.get('yoast_desc', '') or 'Tiago R. Correia, arquitecto desde 2014 em Lisboa.'

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>{escape(yoast_title)}</title>
    <meta name="description" content="{escape(yoast_desc)}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{escape(yoast_title)}">
    <meta property="og:description" content="{escape(yoast_desc)}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html()}

    <div class="trc-section-header">
        <h1>Sobre Nos</h1>
    </div>

    <article class="trc-content">
        {content}
    </article>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, 'sobre-nos.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_servicos_page():
    """Services page using WordPress page content."""
    page = pages_by_slug.get('servicos', {})
    content = clean_content(page.get('content', ''))
    yoast_title = page.get('yoast_title', '') or 'Servicos - Tiago R. Correia Arquitectos'
    yoast_desc = page.get('yoast_desc', '') or 'Servicos de arquitectura, licenciamento, BIM.'

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>{escape(yoast_title)}</title>
    <meta name="description" content="{escape(yoast_desc)}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{escape(yoast_title)}">
    <meta property="og:description" content="{escape(yoast_desc)}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html()}

    <div class="trc-section-header">
        <h1>Servicos</h1>
    </div>

    <article class="trc-content trc-services-page">
        {content}
    </article>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, 'servicos.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_contactos_page():
    """Contact page with info + WordPress content."""
    page = pages_by_slug.get('contactos', {})
    content = clean_content(page.get('content', ''))
    yoast_title = page.get('yoast_title', '') or 'Contactos - Tiago R. Correia Arquitectos'
    yoast_desc = page.get('yoast_desc', '') or 'Contacte o atelier Tiago R. Correia Arquitectos em Lisboa.'

    html = f'''<!doctype html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>{escape(yoast_title)}</title>
    <meta name="description" content="{escape(yoast_desc)}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{escape(yoast_title)}">
    <meta property="og:description" content="{escape(yoast_desc)}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="apple-touch-icon" sizes="180x180" href="assets/images/favicons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="assets/images/favicons/favicon-16x16.png">
    <link rel="stylesheet" href="assets/styles/main.css" media="all">
    <style>{INLINE_CSS}
    </style>
</head>
<body>
    {menu_html()}

    <div class="trc-section-header">
        <h1>Contactos</h1>
        <p>Marque uma reuniao connosco para discutir o seu projecto.</p>
    </div>

    <section class="trc-contact-grid">
        <div class="trc-contact-item">
            <h3>Morada</h3>
            <p>
                R. dos Lagares d'El-Rei 19A<br>
                1700-268 Lisboa, Portugal
            </p>
        </div>
        <div class="trc-contact-item">
            <h3>Telefone</h3>
            <p><a href="tel:+351918660664">+351 918 660 664</a></p>
        </div>
        <div class="trc-contact-item">
            <h3>Email</h3>
            <p><a href="mailto:geral@tiagorcorreia.com">geral@tiagorcorreia.com</a></p>
        </div>
        <div class="trc-contact-item">
            <h3>Redes Sociais</h3>
            <p>
                <a href="https://www.instagram.com/tiagorcorreia_arquitecto" target="_blank" rel="noopener">Instagram</a><br>
                <a href="https://pt.linkedin.com/in/tiago-r-correia-15891528" target="_blank" rel="noopener">LinkedIn</a><br>
                <a href="https://www.facebook.com/tiagorcorreia.arq/" target="_blank" rel="noopener">Facebook</a>
            </p>
        </div>
    </section>

    <article class="trc-content">
        {content}
    </article>

    <div style="width:100%;max-width:1400px;margin:0 auto;padding:0 5vw 4rem;">
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3111.2!2d-9.1369!3d38.7480!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd1933b1d719e28b%3A0x799c90fa4449b577!2sR.%20dos%20Lagares%20d&#39;El-Rei%2019A%2C%201700-270%20Lisboa!5e0!3m2!1spt-PT!2spt!4v1"
            width="100%" height="400" style="border:0;border-radius:2px;" allowfullscreen="" loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>

    {footer_html()}
    {MENU_JS}
</body>
</html>'''

    filepath = os.path.join(BASE_DIR, 'contactos.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


# ═══════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════

if __name__ == '__main__':
    generated = []
    errors = []

    print("=== Generating static site ===\n")

    # 1. Portfolio pages
    print(f"Generating {len(portfolio_items)} portfolio pages...")
    for item in portfolio_items:
        try:
            path = generate_portfolio_page(item)
            generated.append(path)
            print(f"  + {item['slug']}.html")
        except Exception as e:
            errors.append(f"Portfolio {item['slug']}: {e}")
            print(f"  ! ERROR {item['slug']}: {e}")

    # 2. Blog pages
    print(f"\nGenerating {len(blog_posts)} blog pages...")
    for post in blog_posts:
        try:
            path = generate_blog_page(post, blog_posts)
            generated.append(path)
            print(f"  + noticias/{post['slug']}.html")
        except Exception as e:
            errors.append(f"Blog {post['slug']}: {e}")
            print(f"  ! ERROR {post['slug']}: {e}")

    # 3. Static pages
    print("\nGenerating static pages...")
    for name, func in [
        ('projetos.html', generate_projetos_page),
        ('noticias.html', generate_noticias_page),
        ('sobre-nos.html', generate_sobre_nos_page),
        ('servicos.html', generate_servicos_page),
        ('contactos.html', generate_contactos_page),
    ]:
        try:
            path = func()
            generated.append(path)
            print(f"  + {name}")
        except Exception as e:
            errors.append(f"Page {name}: {e}")
            print(f"  ! ERROR {name}: {e}")

    # Summary
    print(f"\n=== Done ===")
    print(f"Generated: {len(generated)} files")
    if errors:
        print(f"Errors: {len(errors)}")
        for err in errors:
            print(f"  - {err}")
    else:
        print("No errors.")

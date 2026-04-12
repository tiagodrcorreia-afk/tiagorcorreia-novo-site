#!/usr/bin/env python3
"""
Fix the HTML structure of index.html to match the reference (projects.html).

Current (broken) structure:
  <div data-load-container>
    <popups>
    <scroll-container>
      <o-scroll>
        <hero>
        <c-projects-list>
          <c-projects-list_inner>
            <c-projects-filters>  ← WRONG: should be before scroll-container
            <c-grid>               ← WRONG: should be before scroll-container
            <list items>           ← correct
          </c-projects-list_inner>
        </c-projects-list>
      </o-scroll>
    </scroll-container>
    <c-credits>
  </div>

Target (correct) structure:
  <div data-load-container>
    <popups>
    <c-projects-filters>           ← moved here
    <c-grid>                       ← moved here
    <header class="c-header">      ← re-added (was deleted)
    <scroll-container>
      <o-scroll>
        <hero section>
        <c-projects-list>
          <c-projects-list_inner>
            <list items only>
          </c-projects-list_inner>
        </c-projects-list>
      </o-scroll>
    </scroll-container>
    <c-credits>
  </div>
"""
import re
from pathlib import Path

BASE = Path("/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2")

with open(BASE / "index.html", "r", encoding="utf-8") as f:
    content = f.read()

# ─── STEP 1: Extract filters block ─────────────────────────────
# Filters start at '<div class="c-projects-filters"' and end at '</div>    \n<div class="c-grid"'
filters_start_marker = '            <div class="c-projects-filters" data-module-filter>'
# The filters end just before the grid starts
grid_start_marker = '<div class="c-grid" data-module-grid'

filters_start = content.find(filters_start_marker)
grid_start = content.find(grid_start_marker)

if filters_start == -1 or grid_start == -1:
    print(f"ERROR: Can't find filters ({filters_start}) or grid ({grid_start})")
    exit(1)

# Filters block = from filters_start to just before grid
filters_block = content[filters_start:grid_start].rstrip() + "\n"
print(f"Extracted filters block: {len(filters_block)} chars")

# ─── STEP 2: Extract grid block ────────────────────────────────
# Grid ends with '</div>\n' before the first list item
first_list_item = '        <section class="c-projects-list_item"'
first_item_pos = content.find(first_list_item, grid_start)
if first_item_pos == -1:
    print("ERROR: Can't find first list item")
    exit(1)

grid_block = content[grid_start:first_item_pos].rstrip() + "\n"
print(f"Extracted grid block: {len(grid_block)} chars")

# ─── STEP 3: Remove filters+grid from their current position ──
# They sit between c-projects-list_inner opening and the first list item
# Current: <div class="c-projects-list_inner">\n\n    <div class="c-projects-filters"...>...<grid>...</div>\n    <section...
list_inner_marker = '    <div class="c-projects-list_inner">'
list_inner_pos = content.find(list_inner_marker)

# Replace: from after list_inner opening to before first list item, remove filters+grid
old_between = content[list_inner_pos + len(list_inner_marker):first_item_pos]
# New: just whitespace before first list item
new_between = "\n"

content = content[:list_inner_pos + len(list_inner_marker)] + new_between + content[first_item_pos:]

print(f"Removed filters+grid from c-projects-list_inner ({len(old_between)} chars)")

# ─── STEP 4: Insert filters+grid+header BEFORE scroll-container ─
scroll_container_marker = '        <div class="c-load-container_wrap" id="scroll-container">'
sc_pos = content.find(scroll_container_marker)
if sc_pos == -1:
    print("ERROR: Can't find scroll-container")
    exit(1)

# Build the site header (c-header) — this was lost during earlier fixes
site_header = """        <header class="c-header" id="header" data-module-theme="main">
            <a href="index.html" class="c-header_logo" aria-label="Tiago R. Correia Arquitectos">
                <svg role="img" class="c-header_logo_svg"><use href="assets/images/sprite.svg#logo"></use></svg>
            </a>
            <a href="index.html" class="c-header_name c-heading -h2">
                Tiago R. Correia Arquitectos
            </a>
            <button class="c-header_menu_button" data-module-nav-button type="button">
                <span class="c-header_menu_label">Menu</span>
            </button>
            <div class="c-header_popup_nav">
                <span class="c-header_popup_nav_background">
                    <a href="#" class="c-header_popup_nav_link" data-module-popup-back>
                        <svg role="img"><use href="assets/images/sprite.svg#arrow-left"></use></svg>
                    </a>
                </span>
            </div>
            <nav class="c-nav" role="navigation" data-nav="nav">
                <a href="index.html" class="c-nav_logo" aria-label="Tiago R. Correia Arquitectos">
                    <svg role="img"><use href="assets/images/sprite.svg#logo-shape"></use></svg>
                </a>
                <ul class="c-nav_list -menu">
                    <li class="c-nav_list_item is-current">
                        <a href="index.html">Projectos</a>
                    </li>
                    <li class="c-nav_list_item">
                        <a href="#">Sobre</a>
                    </li>
                    <li class="c-nav_list_item">
                        <a href="#">Contacto</a>
                    </li>
                </ul>
                <ul class="c-nav_list -lang">
                    <li class="c-nav_list_item -close">
                        <button data-nav="closeButton" type="button">Close</button>
                    </li>
                    <li class="c-nav_list_item -lang">
                        <a href="#">EN</a>
                    </li>
                    <li class="c-nav_list_item">
                        <a href="#">Política de Privacidade</a>
                    </li>
                </ul>
                <div class="c-nav_name">
                    <a href="index.html" class="c-heading -h2">
                        Tiago R. Correia Arquitectos
                    </a>
                </div>
            </nav>
        </header>

"""

# Build insertion block: filters + grid + header
insertion = "\n        " + filters_block.strip() + "\n\n" + grid_block.strip() + "\n\n" + site_header

content = content[:sc_pos] + insertion + content[sc_pos:]
print(f"Inserted filters+grid+header before scroll-container")

# ─── STEP 5: Verify the hero section has an anchor for homeHeader ─
# The reference has <span id="homeHeader"></span> before c-projects-list
# Our hero already uses id="homeHeader" on the header element, which is good

# ─── STEP 6: Fix og:title ─────────────────────────────────────
content = content.replace(
    '<meta property="og:title" content="Héloïse Thibodeau Architecte" />',
    '<meta property="og:title" content="Tiago R. Correia Arquitectos" />'
)

# Fix page title
content = content.replace(
    '<title>Héloïse Thibodeau Architecte — Architecture &amp; Design</title>',
    '<title>Tiago R. Correia Arquitectos — Arquitectura &amp; Design</title>'
)

# Fix meta description
content = content.replace(
    '<meta name="description" content="Héloïse Thibodeau Architecte is a Montreal-based architecture firm specializing in institutional, cultural, and residential projects." />',
    '<meta name="description" content="Tiago R. Correia Arquitectos — Atelier de arquitectura sediado em Lisboa, especializado em projectos residenciais, reabilitação urbana e espaços comerciais." />'
)

# ─── WRITE ────────────────────────────────────────────────────
with open(BASE / "index.html", "w", encoding="utf-8") as f:
    f.write(content)

# Verify structure
lines = content.split('\n')
print(f"\n✅ Structure fixed. Total lines: {len(lines)}")

# Check key markers and their order
markers = [
    ('c-popups_container', 'Popups'),
    ('c-projects-filters', 'Filters'),
    ('c-grid" data-module-grid', 'Grid'),
    ('c-header" id="header"', 'Site Header'),
    ('c-load-container_wrap" id="scroll-container"', 'Scroll Container'),
    ('c-home-header" id="homeHeader"', 'Hero'),
    ('c-projects-list" data-scroll-section', 'Projects List'),
    ('c-projects-list_item', 'First List Item'),
    ('c-credits', 'Credits'),
]

for marker, name in markers:
    pos = content.find(marker)
    if pos != -1:
        line_num = content[:pos].count('\n') + 1
        print(f"   Line {line_num:4d}: {name}")
    else:
        print(f"   MISSING: {name}")

# Check remaining HTA refs
hta_count = content.count('htarchitecte.com')
ht_count = content.count('Héloïse')
print(f"\n   htarchitecte.com refs: {hta_count}")
print(f"   Héloïse refs: {ht_count}")

#!/usr/bin/env python3
"""Redesign homepage: creative projects, enhanced services, editorial news."""

import re

FILE = '/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. UPDATE --gridSize
#    Old: hero(100vw) + 6 projects(~300vw) + CTA(20vw) + services(100vw) + news(200vw) + ctaFinal(60vw) = 780vw → was 620vw
#    New: hero(100vw) + 4 creative projects(~200vw) + CTA(20vw) + services(100vw) + news(140vw) + ctaFinal(60vw) = ~620vw
# ═══════════════════════════════════════════════════════════
html = html.replace('--gridSize: 620vw;', '--gridSize: 580vw;')

# ═══════════════════════════════════════════════════════════
# 2. REPLACE PROJECTS CSS + ADD NEW CREATIVE STYLES
# ═══════════════════════════════════════════════════════════

OLD_SERVICES_CSS = """        /* ── Services Section ── */
        .trc-services {
            flex-shrink: 0;
            width: 100vw;
            height: 100vh;
            background: #111;
            color: #f0f0f0;
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        .trc-services_inner {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 5vw;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }
        .trc-services_intro h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(2rem, 3.5vw, 3.2rem);
            letter-spacing: 0.06em;
            line-height: 1.2;
            margin-bottom: 1.5rem;
        }
        .trc-services_intro p {
            font-weight: 300;
            font-size: 0.95rem;
            line-height: 1.8;
            opacity: 0.7;
            max-width: 420px;
            margin-bottom: 2rem;
        }
        .trc-services_intro a.trc-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.6em;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.8rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #f0f0f0;
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.25);
            padding-bottom: 0.4em;
            transition: border-color 0.3s ease;
        }
        .trc-services_intro a.trc-btn:hover {
            border-color: rgba(255,255,255,0.8);
        }
        .trc-services_grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2.5rem 3rem;
        }
        .trc-services_item {
            position: relative;
        }
        .trc-services_item h3 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.95rem;
            letter-spacing: 0.04em;
            margin-bottom: 0.6rem;
        }
        .trc-services_item p {
            font-weight: 300;
            font-size: 0.78rem;
            line-height: 1.7;
            opacity: 0.5;
        }
        .trc-services_item::before {
            content: '';
            display: block;
            width: 24px;
            height: 1px;
            background: rgba(255,255,255,0.3);
            margin-bottom: 1rem;
        }"""

NEW_SERVICES_CSS = """        /* ── Services Section — Enhanced ── */
        .trc-services {
            flex-shrink: 0;
            width: 100vw;
            height: 100vh;
            background: #0a0a0a;
            color: #f0f0f0;
            display: flex;
            align-items: center;
            overflow: hidden;
            position: relative;
        }
        .trc-services::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse 80% 60% at 20% 50%, rgba(255,255,255,0.02) 0%, transparent 70%),
                radial-gradient(ellipse 60% 80% at 80% 60%, rgba(255,255,255,0.015) 0%, transparent 60%);
            pointer-events: none;
        }
        .trc-services_inner {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 4rem 5vw;
            display: flex;
            flex-direction: column;
            gap: 3.5rem;
            position: relative;
            z-index: 1;
        }
        .trc-services_top {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 3rem;
        }
        .trc-services_intro h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(2rem, 3.5vw, 3.2rem);
            letter-spacing: 0.06em;
            line-height: 1.2;
            margin-bottom: 0;
        }
        .trc-services_stats {
            display: flex;
            gap: 3.5rem;
            flex-shrink: 0;
        }
        .trc-services_stat {
            text-align: center;
        }
        .trc-services_stat_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: clamp(2.5rem, 4vw, 3.8rem);
            letter-spacing: -0.02em;
            line-height: 1;
            display: block;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }
        .trc-services_stat_number.is-visible {
            opacity: 1;
            transform: translateY(0);
        }
        .trc-services_stat_label {
            font-weight: 300;
            font-size: 0.65rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            opacity: 0.4;
            margin-top: 0.5rem;
            display: block;
        }
        .trc-services_divider {
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12) 20%, rgba(255,255,255,0.12) 80%, transparent);
        }
        .trc-services_grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0;
        }
        .trc-services_item {
            position: relative;
            padding: 2rem 2.5rem;
            border-right: 1px solid rgba(255,255,255,0.06);
            border-bottom: 1px solid rgba(255,255,255,0.06);
            transition: background 0.4s ease;
            cursor: default;
        }
        .trc-services_item:nth-child(3n) { border-right: none; }
        .trc-services_item:nth-child(n+4) { border-bottom: none; }
        .trc-services_item:hover {
            background: rgba(255,255,255,0.03);
        }
        .trc-services_item_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: 0.7rem;
            letter-spacing: 0.2em;
            opacity: 0.25;
            margin-bottom: 1.2rem;
            display: block;
        }
        .trc-services_item h3 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.95rem;
            letter-spacing: 0.04em;
            margin-bottom: 0.7rem;
            transition: color 0.3s ease;
        }
        .trc-services_item:hover h3 {
            color: #fff;
        }
        .trc-services_item p {
            font-weight: 300;
            font-size: 0.78rem;
            line-height: 1.7;
            opacity: 0.4;
            transition: opacity 0.3s ease;
        }
        .trc-services_item:hover p {
            opacity: 0.6;
        }
        .trc-services_item_line {
            position: absolute;
            bottom: 0;
            left: 2.5rem;
            width: 0;
            height: 1px;
            background: rgba(255,255,255,0.3);
            transition: width 0.5s ease;
        }
        .trc-services_item:hover .trc-services_item_line {
            width: calc(100% - 5rem);
        }
        .trc-services_bottom {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .trc-services_bottom p {
            font-weight: 300;
            font-size: 0.85rem;
            line-height: 1.7;
            opacity: 0.5;
            max-width: 460px;
        }
        .trc-services_bottom a.trc-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.6em;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.8rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #f0f0f0;
            text-decoration: none;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 0.8em 2em;
            transition: border-color 0.3s ease, background 0.3s ease;
            flex-shrink: 0;
        }
        .trc-services_bottom a.trc-btn:hover {
            border-color: rgba(255,255,255,0.6);
            background: rgba(255,255,255,0.04);
        }"""

html = html.replace(OLD_SERVICES_CSS, NEW_SERVICES_CSS)

# ═══════════════════════════════════════════════════════════
# 3. REPLACE NEWS CSS — Editorial asymmetric layout
# ═══════════════════════════════════════════════════════════

OLD_NEWS_CSS = """        /* ── News Section ── */
        .trc-news {
            flex-shrink: 0;
            width: 200vw;
            height: 100vh;
            background: #f7f8f9;
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        .trc-news_inner {
            width: 100%;
            padding: 4rem 5vw;
            display: flex;
            align-items: flex-start;
            gap: 4vw;
        }
        .trc-news_header {
            flex-shrink: 0;
            width: 16vw;
            min-width: 180px;
            padding-top: 1rem;
        }
        .trc-news_header h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.6rem, 2.5vw, 2.4rem);
            letter-spacing: 0.06em;
            line-height: 1.2;
            color: #212122;
            margin-bottom: 1rem;
        }
        .trc-news_header p {
            font-weight: 300;
            font-size: 0.82rem;
            line-height: 1.7;
            opacity: 0.5;
            color: #212122;
            margin-bottom: 1.5rem;
        }
        .trc-news_header a {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.75rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #212122;
            text-decoration: none;
            border-bottom: 1px solid rgba(0,0,0,0.2);
            padding-bottom: 0.3em;
            transition: border-color 0.3s ease;
        }
        .trc-news_header a:hover { border-color: rgba(0,0,0,0.8); }
        .trc-news_cards {
            display: flex;
            gap: 2.5vw;
            align-items: stretch;
        }
        .trc-news_card {
            flex-shrink: 0;
            width: 24vw;
            min-width: 260px;
            text-decoration: none;
            color: #212122;
            display: flex;
            flex-direction: column;
            transition: opacity 0.3s ease;
        }
        .trc-news_card:hover { opacity: 0.7; }
        .trc-news_card_img {
            width: 100%;
            aspect-ratio: 16/9;
            overflow: hidden;
            background: #e8e8e8;
            margin-bottom: 1rem;
        }
        .trc-news_card_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s ease;
        }
        .trc-news_card:hover .trc-news_card_img img {
            transform: scale(1.04);
        }
        .trc-news_card_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.65rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            opacity: 0.4;
            margin-bottom: 0.5rem;
        }
        .trc-news_card_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.92rem;
            letter-spacing: 0.02em;
            line-height: 1.5;
            margin-bottom: 0.5rem;
        }
        .trc-news_card_date {
            font-weight: 300;
            font-size: 0.72rem;
            opacity: 0.35;
            margin-top: auto;
        }"""

NEW_NEWS_CSS = """        /* ── News Section — Editorial Layout ── */
        .trc-news {
            flex-shrink: 0;
            width: 140vw;
            height: 100vh;
            background: #f7f8f9;
            display: flex;
            align-items: center;
            overflow: hidden;
        }
        .trc-news_inner {
            width: 100%;
            height: 80vh;
            padding: 0 5vw;
            display: flex;
            gap: 3vw;
            align-items: stretch;
        }
        /* Featured article — tall left column */
        .trc-news_featured {
            flex-shrink: 0;
            width: 36vw;
            display: flex;
            flex-direction: column;
            text-decoration: none;
            color: #212122;
            position: relative;
            overflow: hidden;
        }
        .trc-news_featured_img {
            flex: 1;
            overflow: hidden;
            position: relative;
        }
        .trc-news_featured_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);
        }
        .trc-news_featured:hover .trc-news_featured_img img {
            transform: scale(1.03);
        }
        .trc-news_featured_overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 3rem 2.5rem;
            background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 60%, transparent 100%);
            color: #fff;
        }
        .trc-news_featured_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.6rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            opacity: 0.7;
            margin-bottom: 0.8rem;
            display: block;
        }
        .trc-news_featured_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.2rem, 1.8vw, 1.6rem);
            letter-spacing: 0.02em;
            line-height: 1.4;
            margin-bottom: 0.6rem;
            display: block;
        }
        .trc-news_featured_date {
            font-weight: 300;
            font-size: 0.7rem;
            opacity: 0.5;
            display: block;
        }
        /* Right column — header + 3 stacked cards */
        .trc-news_right {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 2vh;
        }
        .trc-news_header {
            padding: 1rem 0 0 0;
        }
        .trc-news_header h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.6rem, 2.5vw, 2.4rem);
            letter-spacing: 0.06em;
            line-height: 1.2;
            color: #212122;
            margin-bottom: 0.5rem;
        }
        .trc-news_header_top {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
        }
        .trc-news_header a {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.72rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: #212122;
            text-decoration: none;
            border-bottom: 1px solid rgba(0,0,0,0.2);
            padding-bottom: 0.3em;
            transition: border-color 0.3s ease;
        }
        .trc-news_header a:hover { border-color: rgba(0,0,0,0.8); }
        .trc-news_card {
            display: flex;
            gap: 1.5vw;
            text-decoration: none;
            color: #212122;
            flex: 1;
            align-items: stretch;
            transition: opacity 0.3s ease;
        }
        .trc-news_card:hover { opacity: 0.7; }
        .trc-news_card_img {
            width: 18vw;
            min-width: 180px;
            flex-shrink: 0;
            overflow: hidden;
            background: #e8e8e8;
        }
        .trc-news_card_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s ease;
        }
        .trc-news_card:hover .trc-news_card_img img {
            transform: scale(1.04);
        }
        .trc-news_card_body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1rem 0;
        }
        .trc-news_card_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.6rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            opacity: 0.35;
            margin-bottom: 0.5rem;
        }
        .trc-news_card_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.88rem;
            letter-spacing: 0.02em;
            line-height: 1.5;
            margin-bottom: 0.4rem;
        }
        .trc-news_card_date {
            font-weight: 300;
            font-size: 0.68rem;
            opacity: 0.3;
            margin-top: auto;
        }
        .trc-news_card_divider {
            width: 100%;
            height: 1px;
            background: rgba(0,0,0,0.06);
        }"""

html = html.replace(OLD_NEWS_CSS, NEW_NEWS_CSS)

# ═══════════════════════════════════════════════════════════
# 4. ADD CREATIVE PROJECTS CSS (asymmetric layout)
# ═══════════════════════════════════════════════════════════

# Add new CSS for creative project grid after the projects-cta styles
PROJECTS_CTA_END = """        .trc-projects-cta a:hover svg { transform: translateX(4px); }"""

CREATIVE_PROJECTS_CSS = """        .trc-projects-cta a:hover svg { transform: translateX(4px); }

        /* ── Creative Asymmetric Projects ── */
        .trc-projects-creative {
            flex-shrink: 0;
            display: flex;
            align-items: center;
            height: 100vh;
            padding: 4vh 0;
            gap: 2.5vw;
        }
        .trc-project-card {
            position: relative;
            overflow: hidden;
            flex-shrink: 0;
            cursor: pointer;
        }
        .trc-project-card a {
            display: block;
            width: 100%;
            height: 100%;
            position: relative;
            text-decoration: none;
            color: #fff;
        }
        .trc-project-card_img {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        .trc-project-card_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.8s cubic-bezier(0.25,0.46,0.45,0.94);
        }
        .trc-project-card:hover .trc-project-card_img img {
            transform: scale(1.06);
        }
        .trc-project-card_overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 2rem 1.8rem;
            background: linear-gradient(0deg, rgba(0,0,0,0.65) 0%, rgba(0,0,0,0.2) 50%, transparent 100%);
            transform: translateY(calc(100% - 4rem));
            transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94);
        }
        .trc-project-card:hover .trc-project-card_overlay {
            transform: translateY(0);
        }
        .trc-project-card_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.58rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            opacity: 0.6;
            margin-bottom: 0.5rem;
            display: block;
        }
        .trc-project-card_name {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1rem, 1.4vw, 1.3rem);
            letter-spacing: 0.04em;
            line-height: 1.3;
            display: block;
        }
        /* Individual card sizes — creative asymmetry */
        .trc-project-card--tall {
            width: 28vw;
            height: 85vh;
        }
        .trc-project-card--wide {
            width: 40vw;
            height: 50vh;
        }
        .trc-project-card--square {
            width: 30vw;
            height: 65vh;
        }
        .trc-project-card--compact {
            width: 22vw;
            height: 72vh;
        }
        /* Stacked pair for 2 cards in a column */
        .trc-project-stack {
            display: flex;
            flex-direction: column;
            gap: 2.5vh;
            height: 85vh;
            flex-shrink: 0;
        }
        .trc-project-stack .trc-project-card {
            width: 30vw;
        }
        .trc-project-stack .trc-project-card:first-child {
            height: 55%;
        }
        .trc-project-stack .trc-project-card:last-child {
            height: calc(45% - 2.5vh);
        }"""

html = html.replace(PROJECTS_CTA_END, CREATIVE_PROJECTS_CSS)

# ═══════════════════════════════════════════════════════════
# 5. REPLACE PROJECTS HTML — Remove old 6 items, add 4 creative ones
# ═══════════════════════════════════════════════════════════

# Find and replace the entire projects section
OLD_PROJECTS_START = '    <div class="c-projects-list" data-scroll-section data-href="#projectsList" id="projectsList">'
OLD_PROJECTS_END = """        <!-- "Ver todos" CTA -->
        <div class="trc-projects-cta">
            <a href="projetos.html">
                Ver todos os projectos
                <svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
        </div>
    </div>
</div>"""

# Build the new creative projects HTML
NEW_PROJECTS_HTML = """    <div class="trc-projects-creative" data-scroll-section>

        <!-- Project 1: Tall card -->
        <div class="trc-project-card trc-project-card--tall">
            <a href="conversao-loja-apartamento-campo-de-ourique.html">
                <div class="trc-project-card_img">
                    <img src="assets/images/projetos/conversao-loja-apartamento-campo-de-ourique/thumb.jpg"
                         alt="Conversão Loja em Apartamento T1 Lisboa" width="2560" height="1440" loading="eager">
                </div>
                <div class="trc-project-card_overlay">
                    <span class="trc-project-card_cat">Reabilitação Urbana</span>
                    <span class="trc-project-card_name">Conversão Loja em<br>Apartamento T1 Lisboa</span>
                </div>
            </a>
        </div>

        <!-- Projects 2 & 3: Stacked pair -->
        <div class="trc-project-stack">
            <div class="trc-project-card">
                <a href="apart-praca-espanha.html">
                    <div class="trc-project-card_img">
                        <img src="assets/images/projetos/apart-praca-espanha/thumb.jpg"
                             alt="Apartamento Praça de Espanha" width="2560" height="1440" loading="eager">
                    </div>
                    <div class="trc-project-card_overlay">
                        <span class="trc-project-card_cat">Reabilitação Urbana</span>
                        <span class="trc-project-card_name">Apartamento<br>Praça de Espanha</span>
                    </div>
                </a>
            </div>
            <div class="trc-project-card">
                <a href="casa-cascais.html">
                    <div class="trc-project-card_img">
                        <img src="assets/images/projetos/casa-cascais/thumb.jpg"
                             alt="Casa Cascais" width="2560" height="1440" loading="eager">
                    </div>
                    <div class="trc-project-card_overlay">
                        <span class="trc-project-card_cat">Moradias</span>
                        <span class="trc-project-card_name">Casa Cascais</span>
                    </div>
                </a>
            </div>
        </div>

        <!-- Project 4: Compact tall card -->
        <div class="trc-project-card trc-project-card--compact">
            <a href="reabilitacao-miguel-bombarda-lisboa.html">
                <div class="trc-project-card_img">
                    <img src="assets/images/projetos/reabilitacao-miguel-bombarda-lisboa/thumb.jpg"
                         alt="Miguel Bombarda 54" width="1707" height="2560" loading="eager">
                </div>
                <div class="trc-project-card_overlay">
                    <span class="trc-project-card_cat">Reabilitação Urbana</span>
                    <span class="trc-project-card_name">Miguel Bombarda 54</span>
                </div>
            </a>
        </div>

        <!-- "Ver todos" CTA -->
        <div class="trc-projects-cta">
            <a href="projetos.html">
                Ver todos os projectos
                <svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
            </a>
        </div>
    </div>"""

# Find the old projects block from start to end and replace it
start_idx = html.find(OLD_PROJECTS_START)
end_idx = html.find(OLD_PROJECTS_END)
if start_idx != -1 and end_idx != -1:
    end_idx += len(OLD_PROJECTS_END)
    html = html[:start_idx] + NEW_PROJECTS_HTML + html[end_idx:]
    print(f"✅ Replaced projects HTML (chars {start_idx}-{end_idx})")
else:
    print(f"❌ Could not find projects HTML block. Start: {start_idx}, End: {end_idx}")

# ═══════════════════════════════════════════════════════════
# 6. REPLACE SERVICES HTML — Enhanced with stats + numbered grid
# ═══════════════════════════════════════════════════════════

OLD_SERVICES_HTML = """<section class="trc-services" data-scroll-section>
    <div class="trc-services_inner">
        <div class="trc-services_intro">
            <h2>Arquitectura de<br>excelência técnica</h2>
            <p>Aliamos criatividade conceptual à máxima precisão técnica. Projetamos em BIM, garantindo que cada edifício é construído virtualmente antes da obra começar.</p>
            <a href="servicos.html" class="trc-btn">Saber mais</a>
        </div>
        <div class="trc-services_grid">
            <div class="trc-services_item">
                <h3>Projectos de Arquitectura</h3>
                <p>Moradias, condomínios, reabilitação urbana e espaços comerciais com linguagem contemporânea.</p>
            </div>
            <div class="trc-services_item">
                <h3>Licenciamento</h3>
                <p>Instrução completa de processos junto das Câmaras Municipais, cumprindo PDM e regulamentos em vigor.</p>
            </div>
            <div class="trc-services_item">
                <h3>Coordenação de Especialidades</h3>
                <p>Compatibilização total entre arquitectura e engenharias — estrutural, hidráulica, eléctrica e térmica.</p>
            </div>
            <div class="trc-services_item">
                <h3>Design de Interiores</h3>
                <p>Ambientes que reflectem identidade. Foco no detalhe, materiais nobres e iluminação técnica.</p>
            </div>
            <div class="trc-services_item">
                <h3>LANDSCOPE</h3>
                <p>Análise de viabilidade em 5 dias úteis. Relatório completo para decisões imobiliárias seguras.</p>
            </div>
            <div class="trc-services_item">
                <h3>Tecnologia BIM</h3>
                <p>Modelação 3D integral. Detecção de conflitos, controlo de custos e simulação energética desde o primeiro traço.</p>
            </div>
        </div>
    </div>
</section>"""

NEW_SERVICES_HTML = """<section class="trc-services" data-scroll-section>
    <div class="trc-services_inner">
        <div class="trc-services_top">
            <div class="trc-services_intro">
                <h2>Arquitectura de<br>excelência técnica</h2>
            </div>
            <div class="trc-services_stats">
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="12">0</span>
                    <span class="trc-services_stat_label">Anos de experiência</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="180">0</span>
                    <span class="trc-services_stat_label">Projectos realizados</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="95">0%</span>
                    <span class="trc-services_stat_label">Taxa de aprovação</span>
                </div>
            </div>
        </div>
        <div class="trc-services_divider"></div>
        <div class="trc-services_grid">
            <div class="trc-services_item">
                <span class="trc-services_item_number">01</span>
                <h3>Projectos de Arquitectura</h3>
                <p>Moradias, condomínios, reabilitação urbana e espaços comerciais com linguagem contemporânea.</p>
                <div class="trc-services_item_line"></div>
            </div>
            <div class="trc-services_item">
                <span class="trc-services_item_number">02</span>
                <h3>Licenciamento</h3>
                <p>Instrução completa de processos junto das Câmaras Municipais, cumprindo PDM e regulamentos em vigor.</p>
                <div class="trc-services_item_line"></div>
            </div>
            <div class="trc-services_item">
                <span class="trc-services_item_number">03</span>
                <h3>Coordenação de Especialidades</h3>
                <p>Compatibilização total entre arquitectura e engenharias — estrutural, hidráulica, eléctrica e térmica.</p>
                <div class="trc-services_item_line"></div>
            </div>
            <div class="trc-services_item">
                <span class="trc-services_item_number">04</span>
                <h3>Design de Interiores</h3>
                <p>Ambientes que reflectem identidade. Foco no detalhe, materiais nobres e iluminação técnica.</p>
                <div class="trc-services_item_line"></div>
            </div>
            <div class="trc-services_item">
                <span class="trc-services_item_number">05</span>
                <h3>LANDSCOPE</h3>
                <p>Análise de viabilidade em 5 dias úteis. Relatório completo para decisões imobiliárias seguras.</p>
                <div class="trc-services_item_line"></div>
            </div>
            <div class="trc-services_item">
                <span class="trc-services_item_number">06</span>
                <h3>Tecnologia BIM</h3>
                <p>Modelação 3D integral. Detecção de conflitos, controlo de custos e simulação energética desde o primeiro traço.</p>
                <div class="trc-services_item_line"></div>
            </div>
        </div>
        <div class="trc-services_bottom">
            <p>Projetamos em BIM, garantindo que cada edifício é construído virtualmente antes da obra começar.</p>
            <a href="servicos.html" class="trc-btn">Descobrir serviços</a>
        </div>
    </div>
</section>"""

html = html.replace(OLD_SERVICES_HTML, NEW_SERVICES_HTML)

# ═══════════════════════════════════════════════════════════
# 7. REPLACE NEWS HTML — Featured + 3 horizontal cards
# ═══════════════════════════════════════════════════════════

OLD_NEWS_HTML = """<section class="trc-news" data-scroll-section>
    <div class="trc-news_inner">
        <div class="trc-news_header">
            <h2>Notícias &amp;<br>Insights</h2>
            <p>Artigos sobre investimento imobiliário, legislação e tendências do sector.</p>
            <a href="noticias.html">Ver todas as notícias</a>
        </div>
        <div class="trc-news_cards">
            <a href="noticias/como-criar-condominios-habitacao-investimento.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2024/09/Image7-min-1-768x432.png" alt="Condomínios de Habitação Lucrativos" width="768" height="432">
                </div>
                <span class="trc-news_card_cat">Investimento Imobiliário</span>
                <span class="trc-news_card_title">Guia Estratégico 2026: Como Criar Condomínios de Habitação Lucrativos</span>
                <span class="trc-news_card_date">3 Abril 2026</span>
            </a>
            <a href="noticias/tir-roi-promocao-imobiliaria-rentabilidade.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/04/IMG_3837-768x976.jpeg" alt="TIR e ROI Promoção Imobiliária" width="768" height="976">
                </div>
                <span class="trc-news_card_cat">Investimento Imobiliário</span>
                <span class="trc-news_card_title">TIR e ROI na Promoção Imobiliária: Como Calcular a Rentabilidade Real</span>
                <span class="trc-news_card_date">2 Abril 2026</span>
            </a>
            <a href="noticias/o-novo-rjue-as-5-alteracoes-estruturais-e-o-impacto-na-promocao-imobiliaria.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/03/rjue-2026-tiago-correia-768x432.jpg" alt="Novo RJUE 2026" width="768" height="432">
                </div>
                <span class="trc-news_card_cat">Legislação &amp; Licenciamento</span>
                <span class="trc-news_card_title">O Novo RJUE: As 5 Alterações Estruturais e o Impacto na Promoção Imobiliária</span>
                <span class="trc-news_card_date">31 Março 2026</span>
            </a>
            <a href="noticias/novas-regras-licenciamento-obras-2026.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/01/Gemini_Generated_Image_b9pxqbb9pxqbb9px-e1768636873676-768x708.png" alt="Licenciamento obras 2026" width="768" height="708">
                </div>
                <span class="trc-news_card_cat">Legislação &amp; Licenciamento</span>
                <span class="trc-news_card_title">As regras de licenciamento de obras mudaram em 2026: o que significa para si?</span>
                <span class="trc-news_card_date">17 Janeiro 2026</span>
            </a>
            <a href="noticias/quer-criar-o-empreendimento-turistico.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/01/unnamed-e1767533752578-768x709.jpg" alt="Empreendimento turístico" width="768" height="709">
                </div>
                <span class="trc-news_card_cat">Investimento Imobiliário</span>
                <span class="trc-news_card_title">Quer criar um empreendimento turístico? O guia para o seu investimento</span>
                <span class="trc-news_card_date">4 Janeiro 2026</span>
            </a>
            <a href="noticias/guia-sobre-o-iva-6-construcao-2026-portugal-oportunidades-e-estrategias.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2025/12/tiago-r-correia-iva-6-construcao-2025-portugal-2-768x401.png" alt="IVA 6% construção" width="768" height="401">
                </div>
                <span class="trc-news_card_cat">Legislação &amp; Licenciamento</span>
                <span class="trc-news_card_title">Guia sobre o IVA 6% construção 2026 Portugal: oportunidades e estratégias</span>
                <span class="trc-news_card_date">22 Dezembro 2025</span>
            </a>
        </div>
    </div>
</section>"""

NEW_NEWS_HTML = """<section class="trc-news" data-scroll-section>
    <div class="trc-news_inner">
        <!-- Featured article — large left -->
        <a href="noticias/como-criar-condominios-habitacao-investimento.html" class="trc-news_featured">
            <div class="trc-news_featured_img">
                <img loading="lazy" src="assets/images/wp-content/uploads/2024/09/Image7-min-1-768x432.png" alt="Condomínios de Habitação Lucrativos" width="768" height="432">
            </div>
            <div class="trc-news_featured_overlay">
                <span class="trc-news_featured_cat">Investimento Imobiliário</span>
                <span class="trc-news_featured_title">Guia Estratégico 2026: Como Criar Condomínios de Habitação Lucrativos</span>
                <span class="trc-news_featured_date">3 Abril 2026</span>
            </div>
        </a>
        <!-- Right column: header + 3 stacked cards -->
        <div class="trc-news_right">
            <div class="trc-news_header">
                <div class="trc-news_header_top">
                    <h2>Notícias &amp;<br>Insights</h2>
                    <a href="noticias.html">Ver todas</a>
                </div>
            </div>
            <a href="noticias/tir-roi-promocao-imobiliaria-rentabilidade.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/04/IMG_3837-768x976.jpeg" alt="TIR e ROI Promoção Imobiliária" width="768" height="976">
                </div>
                <div class="trc-news_card_body">
                    <span class="trc-news_card_cat">Investimento Imobiliário</span>
                    <span class="trc-news_card_title">TIR e ROI na Promoção Imobiliária: Como Calcular a Rentabilidade Real</span>
                    <span class="trc-news_card_date">2 Abril 2026</span>
                </div>
            </a>
            <div class="trc-news_card_divider"></div>
            <a href="noticias/o-novo-rjue-as-5-alteracoes-estruturais-e-o-impacto-na-promocao-imobiliaria.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/03/rjue-2026-tiago-correia-768x432.jpg" alt="Novo RJUE 2026" width="768" height="432">
                </div>
                <div class="trc-news_card_body">
                    <span class="trc-news_card_cat">Legislação &amp; Licenciamento</span>
                    <span class="trc-news_card_title">O Novo RJUE: As 5 Alterações Estruturais e o Impacto na Promoção Imobiliária</span>
                    <span class="trc-news_card_date">31 Março 2026</span>
                </div>
            </a>
            <div class="trc-news_card_divider"></div>
            <a href="noticias/novas-regras-licenciamento-obras-2026.html" class="trc-news_card">
                <div class="trc-news_card_img">
                    <img loading="lazy" src="assets/images/wp-content/uploads/2026/01/Gemini_Generated_Image_b9pxqbb9pxqbb9px-e1768636873676-768x708.png" alt="Licenciamento obras 2026" width="768" height="708">
                </div>
                <div class="trc-news_card_body">
                    <span class="trc-news_card_cat">Legislação &amp; Licenciamento</span>
                    <span class="trc-news_card_title">As regras de licenciamento de obras mudaram em 2026: o que significa para si?</span>
                    <span class="trc-news_card_date">17 Janeiro 2026</span>
                </div>
            </a>
        </div>
    </div>
</section>"""

html = html.replace(OLD_NEWS_HTML, NEW_NEWS_HTML)

# ═══════════════════════════════════════════════════════════
# 8. ADD ANIMATED COUNTER SCRIPT + scroll observer before closing </body>
# ═══════════════════════════════════════════════════════════

COUNTER_SCRIPT = """
<script>
/* ── Animated Counters ── */
(function() {
    function animateCounter(el) {
        const target = parseInt(el.dataset.count);
        const suffix = el.textContent.replace(/[0-9]/g, '');
        const duration = 1800;
        const start = performance.now();

        function tick(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.round(target * eased);
            el.textContent = current + suffix;
            if (progress < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    // Intersection Observer for stats + service items
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('trc-services_stat_number')) {
                    entry.target.classList.add('is-visible');
                    animateCounter(entry.target);
                }
                if (entry.target.classList.contains('trc-services_item')) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    // Observe counters
    document.querySelectorAll('.trc-services_stat_number').forEach(function(el) {
        observer.observe(el);
    });

    // Observe service items with stagger
    document.querySelectorAll('.trc-services_item').forEach(function(el, i) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease ' + (i * 0.1) + 's, transform 0.6s ease ' + (i * 0.1) + 's';
        observer.observe(el);
    });

    // For horizontal scroll, also trigger on scroll position
    var scrollContainer = document.getElementById('scroll-container');
    if (scrollContainer) {
        var triggered = false;
        scrollContainer.addEventListener('scroll', function() {
            if (triggered) return;
            var servicesEl = document.querySelector('.trc-services');
            if (!servicesEl) return;
            var rect = servicesEl.getBoundingClientRect();
            if (rect.left < window.innerWidth * 0.8) {
                triggered = true;
                document.querySelectorAll('.trc-services_stat_number').forEach(function(el) {
                    el.classList.add('is-visible');
                    animateCounter(el);
                });
                document.querySelectorAll('.trc-services_item').forEach(function(el) {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                });
            }
        });
    }
})();
</script>
"""

# Insert before closing </body>
html = html.replace('</body>', COUNTER_SCRIPT + '</body>')

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Homepage redesign complete!")
print(f"   Total file size: {len(html)} chars")

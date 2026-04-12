#!/usr/bin/env python3
"""Redesign v3: Vertical bars projects/news, blur services, impactful CTA."""

FILE = '/Users/tiagocorreia/Documents/Claude/website/novo-tema/previews/novo-site-v2/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════════════════════════
# 1. REPLACE PROJECTS CSS — 4 vertical bars full height
# ═══════════════════════════════════════════════════════════

OLD_PROJ_CSS = """        /* ── Creative Asymmetric Projects ── */
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

NEW_PROJ_CSS = """        /* ── Projects — 4 Vertical Bars ── */
        .trc-projects-creative {
            flex-shrink: 0;
            display: flex;
            align-items: stretch;
            height: 100vh;
            gap: 5px;
            padding: 0;
        }
        .trc-project-bar {
            position: relative;
            width: 22vw;
            height: 100vh;
            overflow: hidden;
            flex-shrink: 0;
            cursor: pointer;
        }
        .trc-project-bar a {
            display: block;
            width: 100%;
            height: 100%;
            position: relative;
            text-decoration: none;
            color: #fff;
        }
        .trc-project-bar_img {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        .trc-project-bar_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 1s cubic-bezier(0.25,0.46,0.45,0.94), filter 0.6s ease;
            filter: brightness(0.75);
        }
        .trc-project-bar:hover .trc-project-bar_img img {
            transform: scale(1.08);
            filter: brightness(1);
        }
        .trc-project-bar_overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            top: 0;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 3rem 2rem;
            background: linear-gradient(0deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.1) 40%, transparent 70%);
            transition: background 0.5s ease;
        }
        .trc-project-bar:hover .trc-project-bar_overlay {
            background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.15) 50%, transparent 70%);
        }
        .trc-project-bar_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: 5rem;
            letter-spacing: -0.04em;
            line-height: 1;
            opacity: 0.08;
            position: absolute;
            top: 2rem;
            left: 2rem;
        }
        .trc-project-bar_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.55rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            opacity: 0.5;
            margin-bottom: 0.6rem;
            display: block;
        }
        .trc-project-bar_name {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1rem, 1.3vw, 1.25rem);
            letter-spacing: 0.03em;
            line-height: 1.35;
            display: block;
            transform: translateY(8px);
            opacity: 0.85;
            transition: transform 0.4s ease, opacity 0.4s ease;
        }
        .trc-project-bar:hover .trc-project-bar_name {
            transform: translateY(0);
            opacity: 1;
        }
        .trc-project-bar_line {
            width: 30px;
            height: 1px;
            background: rgba(255,255,255,0.4);
            margin-top: 1rem;
            transition: width 0.5s ease;
        }
        .trc-project-bar:hover .trc-project-bar_line {
            width: 60px;
        }"""

html = html.replace(OLD_PROJ_CSS, NEW_PROJ_CSS)
print("✅ Projects CSS replaced")

# ═══════════════════════════════════════════════════════════
# 2. REPLACE SERVICES CSS — Blur background, aligned title, architectural
# ═══════════════════════════════════════════════════════════

OLD_SERV_CSS = """        /* ── Services Section — Enhanced ── */
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
            opacity: 1;
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

NEW_SERV_CSS = """        /* ── Services Section — Blur Background + Architectural ── */
        .trc-services {
            flex-shrink: 0;
            width: 100vw;
            height: 100vh;
            color: #f0f0f0;
            display: flex;
            align-items: center;
            overflow: hidden;
            position: relative;
        }
        .trc-services_bg {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
        }
        .trc-services_bg img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: blur(8px) brightness(0.25);
            transform: scale(1.05);
        }
        .trc-services_bg::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.45);
        }
        /* Thin architectural line accent */
        .trc-services_accent {
            position: absolute;
            top: 0;
            left: 5vw;
            width: 1px;
            height: 100%;
            background: linear-gradient(180deg, transparent, rgba(255,255,255,0.08) 20%, rgba(255,255,255,0.08) 80%, transparent);
            z-index: 1;
        }
        .trc-services_accent::after {
            content: 'TRC';
            position: absolute;
            top: 3rem;
            left: -0.5rem;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: 0.55rem;
            letter-spacing: 0.3em;
            opacity: 0.15;
            writing-mode: vertical-rl;
        }
        .trc-services_inner {
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 8vw;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
            position: relative;
            z-index: 2;
        }
        .trc-services_top {
            display: flex;
            align-items: flex-start;
            gap: 4rem;
        }
        .trc-services_intro {
            flex: 1;
        }
        .trc-services_intro h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.8rem, 3vw, 2.6rem);
            letter-spacing: 0.08em;
            line-height: 1.25;
            margin-bottom: 1rem;
            border-left: 2px solid rgba(255,255,255,0.15);
            padding-left: 1.5rem;
        }
        .trc-services_intro_desc {
            font-weight: 300;
            font-size: 0.85rem;
            line-height: 1.8;
            opacity: 0.55;
            max-width: 400px;
            padding-left: 1.5rem;
            border-left: 2px solid transparent;
        }
        .trc-services_stats {
            display: flex;
            gap: 3rem;
            flex-shrink: 0;
            padding-top: 0.5rem;
        }
        .trc-services_stat {
            text-align: center;
            position: relative;
        }
        .trc-services_stat::before {
            content: '';
            display: block;
            width: 20px;
            height: 1px;
            background: rgba(255,255,255,0.2);
            margin: 0 auto 0.8rem;
        }
        .trc-services_stat_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: clamp(2rem, 3.2vw, 3rem);
            letter-spacing: -0.02em;
            line-height: 1;
            display: block;
        }
        .trc-services_stat_label {
            font-weight: 300;
            font-size: 0.6rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            opacity: 0.35;
            margin-top: 0.4rem;
            display: block;
        }
        .trc-services_grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0;
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(2px);
            border: 1px solid rgba(255,255,255,0.06);
        }
        .trc-services_item {
            position: relative;
            padding: 1.8rem 2rem;
            border-right: 1px solid rgba(255,255,255,0.06);
            border-bottom: 1px solid rgba(255,255,255,0.06);
            transition: background 0.4s ease;
            cursor: default;
        }
        .trc-services_item:nth-child(3n) { border-right: none; }
        .trc-services_item:nth-child(n+4) { border-bottom: none; }
        .trc-services_item:hover {
            background: rgba(255,255,255,0.04);
        }
        .trc-services_item_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: 0.65rem;
            letter-spacing: 0.2em;
            opacity: 0.2;
            margin-bottom: 0.8rem;
            display: block;
        }
        .trc-services_item h3 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.9rem;
            letter-spacing: 0.04em;
            margin-bottom: 0.5rem;
            transition: color 0.3s ease;
        }
        .trc-services_item:hover h3 { color: #fff; }
        .trc-services_item p {
            font-weight: 300;
            font-size: 0.72rem;
            line-height: 1.7;
            opacity: 0.35;
            transition: opacity 0.3s ease;
        }
        .trc-services_item:hover p { opacity: 0.55; }
        .trc-services_item_line {
            position: absolute;
            bottom: 0;
            left: 2rem;
            width: 0;
            height: 1px;
            background: rgba(255,255,255,0.3);
            transition: width 0.5s ease;
        }
        .trc-services_item:hover .trc-services_item_line {
            width: calc(100% - 4rem);
        }
        .trc-services_bottom {
            display: flex;
            align-items: center;
            justify-content: flex-end;
        }
        .trc-services_bottom a.trc-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.6em;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.75rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #f0f0f0;
            text-decoration: none;
            border: 1px solid rgba(255,255,255,0.18);
            padding: 0.7em 2em;
            transition: border-color 0.3s ease, background 0.3s ease;
        }
        .trc-services_bottom a.trc-btn:hover {
            border-color: rgba(255,255,255,0.5);
            background: rgba(255,255,255,0.05);
        }"""

html = html.replace(OLD_SERV_CSS, NEW_SERV_CSS)
print("✅ Services CSS replaced")

# ═══════════════════════════════════════════════════════════
# 3. REPLACE NEWS CSS — 4 Vertical bars like projects
# ═══════════════════════════════════════════════════════════

OLD_NEWS_CSS = """        /* ── News Section — Editorial Layout ── */
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

NEW_NEWS_CSS = """        /* ── News Section — 4 Vertical Bars ── */
        .trc-news {
            flex-shrink: 0;
            height: 100vh;
            display: flex;
            align-items: stretch;
            overflow: hidden;
        }
        .trc-news_header-bar {
            flex-shrink: 0;
            width: 18vw;
            min-width: 200px;
            height: 100vh;
            background: #111;
            color: #f0f0f0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 4rem 2.5rem;
            position: relative;
        }
        .trc-news_header-bar::after {
            content: '';
            position: absolute;
            top: 15%;
            right: 0;
            width: 1px;
            height: 70%;
            background: linear-gradient(180deg, transparent, rgba(255,255,255,0.1) 30%, rgba(255,255,255,0.1) 70%, transparent);
        }
        .trc-news_header-bar h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.4rem, 2vw, 2rem);
            letter-spacing: 0.08em;
            line-height: 1.25;
            margin-bottom: 1.2rem;
        }
        .trc-news_header-bar p {
            font-weight: 300;
            font-size: 0.78rem;
            line-height: 1.8;
            opacity: 0.4;
            margin-bottom: 2rem;
        }
        .trc-news_header-bar a {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.68rem;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #f0f0f0;
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            padding-bottom: 0.3em;
            transition: border-color 0.3s ease;
            display: inline-block;
        }
        .trc-news_header-bar a:hover { border-color: rgba(255,255,255,0.7); }
        .trc-news_bars {
            display: flex;
            gap: 5px;
            height: 100vh;
        }
        .trc-news_bar {
            position: relative;
            width: 22vw;
            height: 100vh;
            overflow: hidden;
            flex-shrink: 0;
            text-decoration: none;
            color: #fff;
            display: block;
        }
        .trc-news_bar_img {
            width: 100%;
            height: 100%;
            overflow: hidden;
        }
        .trc-news_bar_img img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 1s cubic-bezier(0.25,0.46,0.45,0.94), filter 0.6s ease;
            filter: brightness(0.55) saturate(0.8);
        }
        .trc-news_bar:hover .trc-news_bar_img img {
            transform: scale(1.06);
            filter: brightness(0.7) saturate(1);
        }
        .trc-news_bar_overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 2.5rem 1.8rem;
            background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 50%, transparent 80%);
        }
        .trc-news_bar_cat {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.5rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            opacity: 0.5;
            margin-bottom: 0.5rem;
            display: block;
        }
        .trc-news_bar_title {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(0.85rem, 1.1vw, 1.05rem);
            letter-spacing: 0.02em;
            line-height: 1.45;
            display: block;
            margin-bottom: 0.5rem;
        }
        .trc-news_bar_date {
            font-weight: 300;
            font-size: 0.6rem;
            opacity: 0.35;
            display: block;
        }
        .trc-news_bar_line {
            width: 25px;
            height: 1px;
            background: rgba(255,255,255,0.35);
            margin-top: 0.8rem;
            transition: width 0.5s ease;
        }
        .trc-news_bar:hover .trc-news_bar_line {
            width: 50px;
        }"""

html = html.replace(OLD_NEWS_CSS, NEW_NEWS_CSS)
print("✅ News CSS replaced")

# ═══════════════════════════════════════════════════════════
# 4. REPLACE CTA FINAL CSS — More impactful, background image + blur
# ═══════════════════════════════════════════════════════════

OLD_CTA_CSS = """        /* ── CTA Final Section ── */
        .trc-cta-final {
            flex-shrink: 0;
            width: 60vw;
            height: 100vh;
            background: #111;
            color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .trc-cta-final_inner {
            max-width: 560px;
            padding: 3rem;
        }
        .trc-cta-final h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.8rem, 3vw, 2.8rem);
            letter-spacing: 0.06em;
            line-height: 1.3;
            margin-bottom: 1.2rem;
        }
        .trc-cta-final p {
            font-weight: 300;
            font-size: 0.88rem;
            line-height: 1.8;
            opacity: 0.6;
            margin-bottom: 2.5rem;
        }
        .trc-cta-final a.trc-btn-light {
            display: inline-block;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.78rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #111;
            background: #f0f0f0;
            padding: 1em 2.5em;
            text-decoration: none;
            transition: background 0.3s ease, color 0.3s ease;
        }
        .trc-cta-final a.trc-btn-light:hover {
            background: #fff;
        }"""

NEW_CTA_CSS = """        /* ── CTA Final Section — Impactful ── */
        .trc-cta-final {
            flex-shrink: 0;
            width: 60vw;
            height: 100vh;
            color: #f0f0f0;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .trc-cta-final_bg {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 0;
        }
        .trc-cta-final_bg img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: blur(4px) brightness(0.2);
            transform: scale(1.05);
        }
        .trc-cta-final_bg::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(135deg, rgba(0,0,0,0.6), rgba(0,0,0,0.3));
        }
        .trc-cta-final_inner {
            max-width: 560px;
            padding: 3rem;
            position: relative;
            z-index: 1;
        }
        .trc-cta-final_line {
            width: 40px;
            height: 1px;
            background: rgba(255,255,255,0.3);
            margin: 0 auto 2.5rem;
        }
        .trc-cta-final h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 200;
            font-size: clamp(1.8rem, 3vw, 2.8rem);
            letter-spacing: 0.08em;
            line-height: 1.3;
            margin-bottom: 1.2rem;
        }
        .trc-cta-final p {
            font-weight: 300;
            font-size: 0.85rem;
            line-height: 1.8;
            opacity: 0.55;
            margin-bottom: 2.5rem;
        }
        .trc-cta-final a.trc-btn-light {
            display: inline-block;
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.75rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: #fff;
            background: transparent;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 1.1em 3em;
            text-decoration: none;
            transition: background 0.4s ease, border-color 0.4s ease;
        }
        .trc-cta-final a.trc-btn-light:hover {
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.6);
        }
        .trc-cta-final_contact {
            margin-top: 2.5rem;
            font-weight: 300;
            font-size: 0.7rem;
            letter-spacing: 0.12em;
            opacity: 0.3;
        }
        .trc-cta-final_contact a {
            color: #f0f0f0;
            text-decoration: none;
            border-bottom: 1px solid rgba(255,255,255,0.15);
            transition: border-color 0.3s ease;
        }
        .trc-cta-final_contact a:hover { border-color: rgba(255,255,255,0.5); }"""

html = html.replace(OLD_CTA_CSS, NEW_CTA_CSS)
print("✅ CTA Final CSS replaced")

# ═══════════════════════════════════════════════════════════
# 5. REPLACE PROJECTS HTML — 4 vertical bars
# ═══════════════════════════════════════════════════════════

OLD_PROJ_HTML = """    <div class="trc-projects-creative" data-scroll-section>

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

NEW_PROJ_HTML = """    <div class="trc-projects-creative" data-scroll-section>

        <div class="trc-project-bar">
            <a href="conversao-loja-apartamento-campo-de-ourique.html">
                <span class="trc-project-bar_number">01</span>
                <div class="trc-project-bar_img">
                    <img src="assets/images/projetos/conversao-loja-apartamento-campo-de-ourique/thumb.jpg"
                         alt="Conversão Loja em Apartamento T1 Lisboa" width="2560" height="1440" loading="eager">
                </div>
                <div class="trc-project-bar_overlay">
                    <span class="trc-project-bar_cat">Reabilitação Urbana</span>
                    <span class="trc-project-bar_name">Conversão Loja em<br>Apartamento T1</span>
                    <div class="trc-project-bar_line"></div>
                </div>
            </a>
        </div>

        <div class="trc-project-bar">
            <a href="apart-praca-espanha.html">
                <span class="trc-project-bar_number">02</span>
                <div class="trc-project-bar_img">
                    <img src="assets/images/projetos/apart-praca-espanha/thumb.jpg"
                         alt="Apartamento Praça de Espanha" width="2560" height="1440" loading="eager">
                </div>
                <div class="trc-project-bar_overlay">
                    <span class="trc-project-bar_cat">Reabilitação Urbana</span>
                    <span class="trc-project-bar_name">Apartamento<br>Praça de Espanha</span>
                    <div class="trc-project-bar_line"></div>
                </div>
            </a>
        </div>

        <div class="trc-project-bar">
            <a href="casa-cascais.html">
                <span class="trc-project-bar_number">03</span>
                <div class="trc-project-bar_img">
                    <img src="assets/images/projetos/casa-cascais/thumb.jpg"
                         alt="Casa Cascais" width="2560" height="1440" loading="eager">
                </div>
                <div class="trc-project-bar_overlay">
                    <span class="trc-project-bar_cat">Moradias</span>
                    <span class="trc-project-bar_name">Casa Cascais</span>
                    <div class="trc-project-bar_line"></div>
                </div>
            </a>
        </div>

        <div class="trc-project-bar">
            <a href="reabilitacao-miguel-bombarda-lisboa.html">
                <span class="trc-project-bar_number">04</span>
                <div class="trc-project-bar_img">
                    <img src="assets/images/projetos/reabilitacao-miguel-bombarda-lisboa/thumb.jpg"
                         alt="Miguel Bombarda 54" width="1707" height="2560" loading="eager">
                </div>
                <div class="trc-project-bar_overlay">
                    <span class="trc-project-bar_cat">Reabilitação Urbana</span>
                    <span class="trc-project-bar_name">Miguel Bombarda 54</span>
                    <div class="trc-project-bar_line"></div>
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

html = html.replace(OLD_PROJ_HTML, NEW_PROJ_HTML)
print("✅ Projects HTML replaced")

# ═══════════════════════════════════════════════════════════
# 6. REPLACE SERVICES HTML — Add bg image + description + accent line
# ═══════════════════════════════════════════════════════════

OLD_SERV_HTML = """<section class="trc-services" data-scroll-section>
    <div class="trc-services_inner">
        <div class="trc-services_top">
            <div class="trc-services_intro">
                <h2>Arquitectura de<br>excelência técnica</h2>
            </div>
            <div class="trc-services_stats">"""

NEW_SERV_HTML = """<section class="trc-services" data-scroll-section>
    <div class="trc-services_bg">
        <img src="assets/images/projetos/casa-cascais/thumb.jpg" alt="" aria-hidden="true">
    </div>
    <div class="trc-services_accent"></div>
    <div class="trc-services_inner">
        <div class="trc-services_top">
            <div class="trc-services_intro">
                <h2>Arquitectura de<br>excelência técnica</h2>
                <p class="trc-services_intro_desc">Aliamos criatividade conceptual à máxima precisão técnica, com projectos desenvolvidos integralmente em BIM.</p>
            </div>
            <div class="trc-services_stats">"""

html = html.replace(OLD_SERV_HTML, NEW_SERV_HTML)
print("✅ Services HTML updated with bg + accent")

# Remove the old bottom paragraph (moved to intro)
html = html.replace(
    """        <div class="trc-services_bottom">
            <p>Projetamos em BIM, garantindo que cada edifício é construído virtualmente antes da obra começar.</p>
            <a href="servicos.html" class="trc-btn">Descobrir serviços</a>
        </div>""",
    """        <div class="trc-services_bottom">
            <a href="servicos.html" class="trc-btn">Descobrir serviços</a>
        </div>"""
)

# Remove the divider (design is cleaner without it now)
html = html.replace('        <div class="trc-services_divider"></div>\n', '')
print("✅ Services HTML cleaned up")

# ═══════════════════════════════════════════════════════════
# 7. REPLACE NEWS HTML — Header bar + 4 vertical bars
# ═══════════════════════════════════════════════════════════

OLD_NEWS_HTML = """<section class="trc-news" data-scroll-section>
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

NEW_NEWS_HTML = """<section class="trc-news" data-scroll-section>
    <div class="trc-news_header-bar">
        <h2>Notícias &amp;<br>Insights</h2>
        <p>Artigos sobre investimento imobiliário, legislação e tendências do sector.</p>
        <a href="noticias.html">Ver todas as notícias</a>
    </div>
    <div class="trc-news_bars">
        <a href="noticias/como-criar-condominios-habitacao-investimento.html" class="trc-news_bar">
            <div class="trc-news_bar_img">
                <img loading="lazy" src="assets/images/wp-content/uploads/2024/09/Image7-min-1-768x432.png" alt="Condomínios de Habitação Lucrativos" width="768" height="432">
            </div>
            <div class="trc-news_bar_overlay">
                <span class="trc-news_bar_cat">Investimento Imobiliário</span>
                <span class="trc-news_bar_title">Guia Estratégico 2026: Como Criar Condomínios de Habitação Lucrativos</span>
                <span class="trc-news_bar_date">3 Abril 2026</span>
                <div class="trc-news_bar_line"></div>
            </div>
        </a>
        <a href="noticias/tir-roi-promocao-imobiliaria-rentabilidade.html" class="trc-news_bar">
            <div class="trc-news_bar_img">
                <img loading="lazy" src="assets/images/wp-content/uploads/2026/04/IMG_3837-768x976.jpeg" alt="TIR e ROI Promoção Imobiliária" width="768" height="976">
            </div>
            <div class="trc-news_bar_overlay">
                <span class="trc-news_bar_cat">Investimento Imobiliário</span>
                <span class="trc-news_bar_title">TIR e ROI na Promoção Imobiliária: Rentabilidade Real</span>
                <span class="trc-news_bar_date">2 Abril 2026</span>
                <div class="trc-news_bar_line"></div>
            </div>
        </a>
        <a href="noticias/o-novo-rjue-as-5-alteracoes-estruturais-e-o-impacto-na-promocao-imobiliaria.html" class="trc-news_bar">
            <div class="trc-news_bar_img">
                <img loading="lazy" src="assets/images/wp-content/uploads/2026/03/rjue-2026-tiago-correia-768x432.jpg" alt="Novo RJUE 2026" width="768" height="432">
            </div>
            <div class="trc-news_bar_overlay">
                <span class="trc-news_bar_cat">Legislação &amp; Licenciamento</span>
                <span class="trc-news_bar_title">O Novo RJUE: As 5 Alterações Estruturais</span>
                <span class="trc-news_bar_date">31 Março 2026</span>
                <div class="trc-news_bar_line"></div>
            </div>
        </a>
        <a href="noticias/novas-regras-licenciamento-obras-2026.html" class="trc-news_bar">
            <div class="trc-news_bar_img">
                <img loading="lazy" src="assets/images/wp-content/uploads/2026/01/Gemini_Generated_Image_b9pxqbb9pxqbb9px-e1768636873676-768x708.png" alt="Licenciamento obras 2026" width="768" height="708">
            </div>
            <div class="trc-news_bar_overlay">
                <span class="trc-news_bar_cat">Legislação &amp; Licenciamento</span>
                <span class="trc-news_bar_title">Regras de Licenciamento 2026: O Que Mudou</span>
                <span class="trc-news_bar_date">17 Janeiro 2026</span>
                <div class="trc-news_bar_line"></div>
            </div>
        </a>
    </div>
</section>"""

html = html.replace(OLD_NEWS_HTML, NEW_NEWS_HTML)
print("✅ News HTML replaced")

# ═══════════════════════════════════════════════════════════
# 8. REPLACE CTA FINAL HTML — Add bg image + line + contact
# ═══════════════════════════════════════════════════════════

OLD_CTA_HTML = """<section class="trc-cta-final" data-scroll-section>
    <div class="trc-cta-final_inner">
        <h2>Pronto para dar vida ao seu projecto?</h2>
        <p>Transformamos ideias em espaços de excelência. Peça uma consulta para analisarmos a viabilidade do seu investimento.</p>
        <a href="contactos.html" class="trc-btn-light">Fale connosco</a>
    </div>
</section>"""

NEW_CTA_HTML = """<section class="trc-cta-final" data-scroll-section>
    <div class="trc-cta-final_bg">
        <img src="assets/images/projetos/apart-praca-espanha/thumb.jpg" alt="" aria-hidden="true">
    </div>
    <div class="trc-cta-final_inner">
        <div class="trc-cta-final_line"></div>
        <h2>Pronto para dar vida<br>ao seu projecto?</h2>
        <p>Transformamos ideias em espaços de excelência. Peça uma consulta para analisarmos a viabilidade do seu investimento.</p>
        <a href="contactos.html" class="trc-btn-light">Fale connosco</a>
        <div class="trc-cta-final_contact">
            <a href="tel:+351918660664">+351 918 660 664</a> &nbsp;&middot;&nbsp; <a href="mailto:geral@tiagorcorreia.com">geral@tiagorcorreia.com</a>
        </div>
    </div>
</section>"""

html = html.replace(OLD_CTA_HTML, NEW_CTA_HTML)
print("✅ CTA Final HTML replaced")

# ═══════════════════════════════════════════════════════════
# 9. UPDATE gridSize — projects(4x22vw+5px gaps+CTA 20vw=~110vw) + services(100vw) + news(18vw+4x22vw+5px=~108vw) + cta(60vw) + hero(100vw) = ~478vw
# ═══════════════════════════════════════════════════════════
html = html.replace('--gridSize: 580vw;', '--gridSize: 520vw;')
print("✅ gridSize updated")

# ═══════════════════════════════════════════════════════════
# WRITE
# ═══════════════════════════════════════════════════════════
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n🎉 Redesign v3 complete! File size: {len(html)} chars")

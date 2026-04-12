#!/usr/bin/env python3
"""
Fixes for redesign v3:
1. First bar spacing (projects & news) - equal gaps
2. Blur transitions on previous sections
3. Services "Arquitectura de excelência técnica" - horizontal, modern, dynamic
4. CTA "Pronto para dar vida" - same treatment, more impact
5. Menu text color changes based on background
"""

import re

file_path = "index.html"

with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

# ════════════════════════════════════════════
# 1. FIRST BAR SPACING — add padding-left: 5px
# ════════════════════════════════════════════
html = html.replace(
    """.trc-projects-creative {
            flex-shrink: 0;
            display: flex;
            align-items: stretch;
            height: 100vh;
            gap: 5px;
            padding: 0;
        }""",
    """.trc-projects-creative {
            flex-shrink: 0;
            display: flex;
            align-items: stretch;
            height: 100vh;
            gap: 5px;
            padding: 0 0 0 5px;
        }"""
)
print("✅ 1. Projects first bar spacing fixed")

html = html.replace(
    """.trc-news_bars {
            display: flex;
            gap: 5px;
            height: 100vh;
        }""",
    """.trc-news_bars {
            display: flex;
            gap: 5px;
            height: 100vh;
            padding-left: 5px;
        }"""
)
print("✅ 1. News first bar spacing fixed")


# ════════════════════════════════════════════
# 2. BLUR TRANSITIONS — blur fades on previous sections
# ════════════════════════════════════════════
# Add blur fade-out to right edge of projects-cta and last news bar
blur_transition_css = """
        /* ── Blur Transitions — fade into next section ── */
        .trc-projects-cta {
            position: relative;
        }
        .trc-projects-cta::after {
            content: '';
            position: absolute;
            top: 0;
            right: -1px;
            width: 80px;
            height: 100%;
            background: linear-gradient(90deg, transparent 0%, rgba(0,0,0,0.15) 60%, rgba(0,0,0,0.4) 100%);
            pointer-events: none;
            z-index: 2;
        }
        .trc-news_bar:last-child {
            position: relative;
        }
        .trc-news_bar:last-child::after {
            content: '';
            position: absolute;
            top: 0;
            right: -1px;
            width: 80px;
            height: 100%;
            background: linear-gradient(90deg, transparent 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0.5) 100%);
            pointer-events: none;
            z-index: 2;
        }
        /* Blur entry on services left edge */
        .trc-services::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 120px;
            height: 100%;
            background: linear-gradient(90deg, rgba(0,0,0,0.5) 0%, transparent 100%);
            z-index: 3;
            pointer-events: none;
        }
        /* Blur entry on CTA left edge */
        .trc-cta-final::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 120px;
            height: 100%;
            background: linear-gradient(90deg, rgba(0,0,0,0.5) 0%, transparent 100%);
            z-index: 3;
            pointer-events: none;
        }"""

# Insert before the Services section CSS
html = html.replace(
    "        /* ── Services Section — Blur Background + Architectural ── */",
    blur_transition_css + "\n\n        /* ── Services Section — Blur Background + Architectural ── */"
)
print("✅ 2. Blur transitions added")


# ════════════════════════════════════════════
# 3. SERVICES — Horizontal, modern, dynamic layout
# ════════════════════════════════════════════

old_services_css = """        .trc-services_top {
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
        }"""

new_services_css = """        /* ── Services Header — Horizontal Modern Layout ── */
        .trc-services_header {
            display: flex;
            align-items: stretch;
            width: 100%;
            margin-bottom: 2rem;
            position: relative;
        }
        .trc-services_header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12) 20%, rgba(255,255,255,0.12) 80%, transparent);
        }
        .trc-services_title-block {
            flex: 0 0 auto;
            padding-right: 3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
        }
        .trc-services_title-block::after {
            content: '';
            position: absolute;
            top: 10%;
            right: 0;
            width: 1px;
            height: 80%;
            background: rgba(255,255,255,0.1);
        }
        .trc-services_eyebrow {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.55rem;
            letter-spacing: 0.35em;
            text-transform: uppercase;
            opacity: 0.35;
            margin-bottom: 0.6rem;
        }
        .trc-services_title-block h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: clamp(2.2rem, 4vw, 3.4rem);
            letter-spacing: 0.06em;
            line-height: 1.1;
            white-space: nowrap;
        }
        .trc-services_title-block h2 em {
            font-style: normal;
            font-weight: 200;
            opacity: 0.5;
        }
        .trc-services_stats-row {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: space-around;
            padding-left: 3rem;
        }
        .trc-services_stat {
            text-align: center;
            position: relative;
            padding: 1rem 1.2rem;
        }
        .trc-services_stat_number {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: clamp(2.4rem, 3.8vw, 3.6rem);
            letter-spacing: -0.03em;
            line-height: 1;
            display: block;
        }
        .trc-services_stat_label {
            font-weight: 300;
            font-size: 0.55rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            opacity: 0.3;
            margin-top: 0.5rem;
            display: block;
        }
        .trc-services_desc-line {
            display: flex;
            align-items: center;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        .trc-services_desc-line p {
            font-weight: 300;
            font-size: 0.82rem;
            line-height: 1.75;
            opacity: 0.45;
            max-width: 480px;
        }
        .trc-services_desc-line::before {
            content: '';
            flex-shrink: 0;
            width: 40px;
            height: 1px;
            background: rgba(255,255,255,0.25);
        }"""

html = html.replace(old_services_css, new_services_css)
print("✅ 3a. Services header CSS updated — horizontal layout")

# Also update inner padding for wider layout
html = html.replace(
    """.trc-services_inner {
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 8vw;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
            position: relative;
            z-index: 2;
        }""",
    """.trc-services_inner {
            width: 100%;
            max-width: 1300px;
            margin: 0 auto;
            padding: 3rem 6vw;
            display: flex;
            flex-direction: column;
            gap: 0;
            position: relative;
            z-index: 2;
        }"""
)
print("✅ 3b. Services inner padding widened")

# Update Services HTML — header part
old_services_html = """    <div class="trc-services_inner">
        <div class="trc-services_top">
            <div class="trc-services_intro">
                <h2>Arquitectura de<br>excelência técnica</h2>
                <p class="trc-services_intro_desc">Aliamos criatividade conceptual à máxima precisão técnica, com projectos desenvolvidos integralmente em BIM.</p>
            </div>
            <div class="trc-services_stats">
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="12" data-suffix="">0</span>
                    <span class="trc-services_stat_label">Anos de experiência</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="180" data-suffix="+">0+</span>
                    <span class="trc-services_stat_label">Projectos realizados</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="95" data-suffix="%">0%</span>
                    <span class="trc-services_stat_label">Taxa de aprovação</span>
                </div>
            </div>
        </div>"""

new_services_html = """    <div class="trc-services_inner">
        <div class="trc-services_header">
            <div class="trc-services_title-block">
                <span class="trc-services_eyebrow">Serviços</span>
                <h2>Arquitectura <em>de</em> Excelência Técnica</h2>
            </div>
            <div class="trc-services_stats-row">
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="12" data-suffix="">0</span>
                    <span class="trc-services_stat_label">Anos de experiência</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="180" data-suffix="+">0+</span>
                    <span class="trc-services_stat_label">Projectos realizados</span>
                </div>
                <div class="trc-services_stat">
                    <span class="trc-services_stat_number" data-count="95" data-suffix="%">0%</span>
                    <span class="trc-services_stat_label">Taxa de aprovação</span>
                </div>
            </div>
        </div>
        <div class="trc-services_desc-line">
            <p>Aliamos criatividade conceptual à máxima precisão técnica, com projectos desenvolvidos integralmente em BIM.</p>
        </div>"""

html = html.replace(old_services_html, new_services_html)
print("✅ 3c. Services HTML updated — horizontal header")


# ════════════════════════════════════════════
# 4. CTA FINAL — Horizontal, more impact
# ════════════════════════════════════════════

old_cta_css = """        .trc-cta-final {
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

new_cta_css = """        .trc-cta-final {
            flex-shrink: 0;
            width: 60vw;
            height: 100vh;
            color: #f0f0f0;
            display: flex;
            align-items: center;
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
            background: linear-gradient(135deg, rgba(0,0,0,0.55), rgba(0,0,0,0.25));
        }
        .trc-cta-final_inner {
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 6vw;
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 5rem;
        }
        .trc-cta-final_left {
            flex: 1;
            position: relative;
        }
        .trc-cta-final_eyebrow {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 300;
            font-size: 0.55rem;
            letter-spacing: 0.35em;
            text-transform: uppercase;
            opacity: 0.35;
            margin-bottom: 1rem;
        }
        .trc-cta-final h2 {
            font-family: "Helvetica Neue", helvetica, arial, sans-serif;
            font-weight: 100;
            font-size: clamp(2.2rem, 4vw, 3.4rem);
            letter-spacing: 0.06em;
            line-height: 1.15;
            margin-bottom: 1.5rem;
        }
        .trc-cta-final h2 em {
            font-style: normal;
            font-weight: 200;
            opacity: 0.5;
        }
        .trc-cta-final_desc {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }
        .trc-cta-final_desc::before {
            content: '';
            flex-shrink: 0;
            width: 35px;
            height: 1px;
            background: rgba(255,255,255,0.3);
        }
        .trc-cta-final_desc p {
            font-weight: 300;
            font-size: 0.82rem;
            line-height: 1.8;
            opacity: 0.45;
            max-width: 380px;
        }
        .trc-cta-final_right {
            flex-shrink: 0;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 2rem;
            padding-left: 4rem;
            border-left: 1px solid rgba(255,255,255,0.08);
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
            padding: 1.2em 3.5em;
            text-decoration: none;
            transition: background 0.4s ease, border-color 0.4s ease;
        }
        .trc-cta-final a.trc-btn-light:hover {
            background: rgba(255,255,255,0.1);
            border-color: rgba(255,255,255,0.6);
        }
        .trc-cta-final_contact-block {
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }
        .trc-cta-final_contact-block a {
            color: #f0f0f0;
            text-decoration: none;
            font-weight: 300;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            opacity: 0.4;
            transition: opacity 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.6em;
        }
        .trc-cta-final_contact-block a:hover { opacity: 0.8; }
        .trc-cta-final_contact-block a svg {
            width: 14px;
            height: 14px;
            stroke: currentColor;
            stroke-width: 1.5;
            fill: none;
            flex-shrink: 0;
        }"""

html = html.replace(old_cta_css, new_cta_css)
print("✅ 4a. CTA CSS updated — horizontal split layout")

# Update CTA HTML
old_cta_html = """<section class="trc-cta-final" data-scroll-section>
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

new_cta_html = """<section class="trc-cta-final" data-scroll-section>
    <div class="trc-cta-final_bg">
        <img src="assets/images/projetos/apart-praca-espanha/thumb.jpg" alt="" aria-hidden="true">
    </div>
    <div class="trc-cta-final_inner">
        <div class="trc-cta-final_left">
            <div class="trc-cta-final_eyebrow">Próximo passo</div>
            <h2>Pronto <em>para</em> dar vida<br>ao seu projecto?</h2>
            <div class="trc-cta-final_desc">
                <p>Transformamos ideias em espaços de excelência. Peça uma consulta para analisarmos a viabilidade do seu investimento.</p>
            </div>
        </div>
        <div class="trc-cta-final_right">
            <a href="contactos.html" class="trc-btn-light">Fale connosco</a>
            <div class="trc-cta-final_contact-block">
                <a href="tel:+351918660664">
                    <svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
                    +351 918 660 664
                </a>
                <a href="mailto:geral@tiagorcorreia.com">
                    <svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    geral@tiagorcorreia.com
                </a>
            </div>
        </div>
    </div>
</section>"""

html = html.replace(old_cta_html, new_cta_html)
print("✅ 4b. CTA HTML updated — horizontal split layout")


# ════════════════════════════════════════════
# 5. MENU TEXT COLOR — JS detection based on scroll position
# ════════════════════════════════════════════
# The menu button (.trc-menu-btn) needs to change color based on what's behind it.
# Dark sections = white text, Light sections = dark text.
# We detect based on scrollLeft position which section is at the right edge (where menu is).

menu_color_js = """
    <!-- Menu color detection based on scroll position -->
    <script>
    (function() {
        var container = document.getElementById('scroll-container');
        var menuBtn = document.querySelector('.trc-menu-btn');
        var templateMenuLabel = document.querySelector('.c-header_menu_label');
        var templateMenuBtn = document.querySelector('.c-header_menu_button');
        if (!container || (!menuBtn && !templateMenuLabel)) return;

        // Build a map of section boundaries and their darkness
        function getSectionMap() {
            var sections = [];
            var scrollSections = document.querySelectorAll('[data-scroll-section]');
            scrollSections.forEach(function(sec) {
                var rect = sec.getBoundingClientRect();
                var scrollLeft = container.scrollLeft;
                var absLeft = rect.left + scrollLeft;
                var absRight = absLeft + rect.width;
                // Determine if section is dark or light
                var isDark = sec.classList.contains('trc-services') ||
                             sec.classList.contains('trc-news') ||
                             sec.classList.contains('trc-cta-final') ||
                             sec.classList.contains('c-home-header');
                // Projects creative is dark (images)
                var isProjects = sec.querySelector('.trc-projects-creative') !== null;
                // The home header section
                var isHome = sec.classList.contains('c-home-header');
                sections.push({
                    left: absLeft,
                    right: absRight,
                    dark: isDark || isHome
                });
            });
            // Also add the projects creative and projects-cta as separate zones
            var projCreative = document.querySelector('.trc-projects-creative');
            if (projCreative) {
                var pr = projCreative.getBoundingClientRect();
                var sl = container.scrollLeft;
                sections.push({ left: pr.left + sl, right: pr.right + sl, dark: true });
            }
            var projCta = document.querySelector('.trc-projects-cta');
            if (projCta) {
                var pcr = projCta.getBoundingClientRect();
                var sl2 = container.scrollLeft;
                sections.push({ left: pcr.left + sl2, right: pcr.right + sl2, dark: false });
            }
            return sections;
        }

        var cachedSections = null;
        var debounceTimer = null;

        function updateMenuColor() {
            if (!cachedSections) cachedSections = getSectionMap();
            // The menu button is at the right edge of viewport
            var menuX = container.scrollLeft + window.innerWidth - 80;
            var isDark = false;

            // Check which section the menu X falls into (prefer more specific matches)
            var best = null;
            cachedSections.forEach(function(s) {
                if (menuX >= s.left && menuX <= s.right) {
                    // Pick the narrower/more specific match
                    if (!best || (s.right - s.left) < (best.right - best.left)) {
                        best = s;
                    }
                }
            });
            isDark = best ? best.dark : true;

            if (menuBtn) {
                menuBtn.style.color = isDark ? '#fff' : '#1a1a1a';
            }
            if (templateMenuLabel) {
                var c = isDark ? '#fff' : '#1a1a1a';
                templateMenuLabel.style.color = c;
                templateMenuLabel.style.webkitTextFillColor = c;
            }
            if (templateMenuBtn) {
                // Also update hamburger icon color for template button
                var spans = templateMenuBtn.querySelectorAll('span');
                spans.forEach(function(sp) {
                    if (!sp.classList.contains('c-header_menu_label')) {
                        sp.style.color = isDark ? '#fff' : '#1a1a1a';
                    }
                });
            }
        }

        // Recalculate sections on resize
        window.addEventListener('resize', function() {
            cachedSections = null;
        });

        // Initial calculation after layout
        setTimeout(function() {
            cachedSections = getSectionMap();
            updateMenuColor();
        }, 500);

        // Poll scroll position (Lenis prevents scroll events)
        setInterval(function() {
            updateMenuColor();
        }, 150);
    })();
    </script>"""

# Insert before </body>
html = html.replace("</body>", menu_color_js + "\n</body>")
print("✅ 5. Menu color detection JS added")


# ════════════════════════════════════════════
# WRITE
# ════════════════════════════════════════════
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n🎉 All fixes applied! File size: {len(html)} chars")

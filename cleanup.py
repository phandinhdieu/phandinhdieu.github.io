#!/usr/bin/env python3
"""
Clean up Weebly legacy boilerplate from phandinhdieu.github.io HTML pages.
Keeps the same visual style; removes dead CDN links, empty CSS blocks,
Weebly JS, jQuery, and the Weebly footer attribution.
"""
import re, os

BASE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    'accueil.html',
    'index.html',
    'khoahoc-giaoduc.html',
    'vantho.html',
    'agrave-propos.html',
    'contact.html',
]

# ── patterns to remove entirely ──────────────────────────────────────────────

REMOVE_PATTERNS = [
    # Weebly CDN CSS links
    re.compile(r'<link[^>]*cdn2\.editmysite\.com[^>]*>\s*', re.DOTALL),
    # Weebly CDN JS scripts (including multi-line)
    re.compile(r'<script[^>]*cdn[12]\.editmysite\.com[^>]*>.*?</script>\s*', re.DOTALL),
    re.compile(r'<script[^>]*cdn[12]\.editmysite\.com[^>]*/>\s*', re.DOTALL),
    # Old jQuery from Google CDN
    re.compile(r"<script[^>]*ajax\.googleapis\.com/ajax/libs/jquery/1\.[^>]*></script>\s*", re.DOTALL),
    # var STATIC_BASE / ASSETS_BASE / STYLE_PREFIX block
    re.compile(r'<script>\s*var STATIC_BASE.*?</script>\s*', re.DOTALL),
    # initFlyouts / Weebly nav JS
    re.compile(r'<script type="text/javascript"><!--.*?//-->\s*</script>\s*', re.DOTALL),
    # _W.configDomain / _W.relinquish / _W.themePlugins / _W.recaptchaUrl inline scripts
    re.compile(r'<script[^>]*>\s*_W\.[^<]*</script>', re.DOTALL),
    re.compile(r'<script>\s*_W\.[^<]*</script>', re.DOTALL),
    # Weebly background image inline style block
    re.compile(r'<style>\s*\.wsite-background \{background-image:.*?</style>\s*', re.DOTALL),
    # The giant empty Weebly inline CSS block (starts with .wsite-elements selector)
    re.compile(
        r'<style type=[\'"]text/css[\'"]>\s*'
        r'\.wsite-elements\.wsite-not-footer.*?'
        r'@media screen and \(min-width: 767px\).*?'
        r'\}</style>\s*',
        re.DOTALL
    ),
    # Weebly footer attribution
    re.compile(
        r'<div id="footer-wrap">Create a.*?</div>\s*',
        re.DOTALL
    ),
    # Weebly section background classes (inline style on wsite-section divs)
    # We keep the div but strip the background-image inline style
    # (handled separately below)
]

# ── Fix HTTP fonts → HTTPS ────────────────────────────────────────────────────

def fix_fonts(html):
    return html.replace(
        "http://fonts.googleapis.com",
        "https://fonts.googleapis.com"
    )

# ── Fix logo link (href="" → href="accueil.html") ─────────────────────────────

def fix_logo_link(html):
    # Only fix the logo anchor, not all empty hrefs
    return re.sub(
        r'(<div id="logo">.*?<a)\s+href=""',
        r'\1 href="accueil.html"',
        html, count=1, flags=re.DOTALL
    )

# ── Remove wsite-background inline style from wsite-section divs ──────────────

def strip_section_bg(html):
    # Remove background-image/repeat/position/size/color inline styles
    # left over from Weebly that reference uploads/ or lost CDN images
    return re.sub(
        r'(<div[^>]*class="[^"]*wsite-section[^"]*"[^>]*?)\s+style="[^"]*background[^"]*"',
        r'\1',
        html
    )

# ── Replace old wsite-multicol tables with clean divs ────────────────────────

def clean_multicol(html):
    """Unwrap wsite-multicol table structures into simple divs."""
    # Remove the outer wrapper divs that only exist for Weebly layout
    html = re.sub(r'<div><div class="wsite-multicol"><div class="wsite-multicol-table-wrap"[^>]*>\s*', '', html)
    html = re.sub(r'</div></div></div>\s*(?=\s*(?:<div class="wsite-spacer"|<section|</div>))', '', html)
    # Remove multicol table/tbody/tr/td wrappers, flatten content
    html = re.sub(r'<table class="wsite-multicol-table">\s*<tbody class="wsite-multicol-tbody">\s*<tr class="wsite-multicol-tr">\s*', '', html)
    html = re.sub(r'<td class="wsite-multicol-col"[^>]*>\s*', '', html)
    html = re.sub(r'\s*</td>\s*', '\n', html)
    html = re.sub(r'\s*</tr>\s*</tbody>\s*</table>', '', html)
    return html

# ── Replace wsite-spacer with simple margin ───────────────────────────────────

def clean_spacers(html):
    return re.sub(
        r'<div(?:\s+class="wsite-spacer")?\s+style="height:\s*\d+px;">\s*</div>',
        '',
        html
    )

# ── Remove empty wsite-image wrapper divs ─────────────────────────────────────

def clean_wsite_image(html):
    # Keep the <img> but remove the outer wsite-image div wrappers
    html = re.sub(
        r'<div><div class="wsite-image[^"]*"[^>]*>\s*<a>\s*',
        '',
        html
    )
    html = re.sub(r'</a>\s*<div style="display:block;font-size:90%"></div>\s*</div></div>',
                  '',
                  html)
    return html

# ── Remove font tags ──────────────────────────────────────────────────────────

def clean_font_tags(html):
    html = re.sub(r'<font[^>]*>', '', html)
    html = html.replace('</font>', '')
    return html

# ── Add empty footer ──────────────────────────────────────────────────────────

CLEAN_FOOTER = '\t\t<div id="footer-wrap"></div>\n'

def ensure_clean_footer(html):
    # If footer-wrap was already removed, add a clean empty one
    if 'id="footer-wrap"' not in html:
        html = html.replace(
            '\n\t</div>\n\n\t<!-- JavaScript -->',
            f'\n{CLEAN_FOOTER}\n\t</div>\n\n\t<!-- JavaScript -->'
        )
    return html

# ── Main transform ────────────────────────────────────────────────────────────

def transform(html):
    for pat in REMOVE_PATTERNS:
        html = pat.sub('', html)
    html = fix_fonts(html)
    html = fix_logo_link(html)
    html = strip_section_bg(html)
    html = clean_spacers(html)
    html = clean_font_tags(html)
    html = ensure_clean_footer(html)
    # Collapse excessive blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html

# ── Run ───────────────────────────────────────────────────────────────────────

for page in PAGES:
    path = os.path.join(BASE, page)
    if not os.path.exists(path):
        print(f'[SKIP] {page} not found')
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    new_html = transform(html)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    orig_kb = len(html) // 1024
    new_kb  = len(new_html) // 1024
    print(f'[OK]  {page}  {orig_kb}KB → {new_kb}KB')

print('\nDone.')

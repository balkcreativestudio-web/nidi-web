#!/usr/bin/env python3
"""Builds the legal pages: nidi's frame, iubenda's text.

The documents live in iubenda. legal-src/*.html holds their "direct text
embedding" snippet for each one, which the script drops into the template
below; iubenda's own script then writes the document into the page when
someone opens it, so an edit in iubenda shows up here without anyone
copying words across.

Run from the repo root:  python3 scripts/build-legal.py
It writes privacy/, privacidad/, terms/ and terminos/.
"""

import os

DOCS = [
    # slug, lang, title, source file, the other language's slug, (sibling label, href)
    ('privacy', 'en', 'Privacy Policy', 'privacy-en', 'privacidad', ('Terms', '/terms/')),
    ('privacidad', 'es', 'Política de Privacidad', 'privacy-es', 'privacy', ('Términos', '/terminos/')),
    ('terms', 'en', 'Terms and Conditions', 'terms-en', 'terminos', ('Privacy', '/privacy/')),
    ('terminos', 'es', 'Términos y Condiciones', 'terms-es', 'terms', ('Privacidad', '/privacidad/')),
]

PAIRS = {'privacy': ('privacy', 'privacidad'), 'privacidad': ('privacy', 'privacidad'),
         'terms': ('terms', 'terminos'), 'terminos': ('terms', 'terminos')}

TEMPLATE = """<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} · nidi</title>
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://nidi.life/{slug}/" />
    <link rel="alternate" hreflang="{lang}" href="https://nidi.life/{slug}/" />
    <link rel="alternate" hreflang="{otherlang}" href="https://nidi.life/{otherslug}/" />
    <meta name="theme-color" content="#FFFDF9" />

    <style>
      /* The legal documents, in nidi's own clothes. The text itself is
         iubenda's: their script writes it into the page (direct text
         embedding), so it stays correct and current without anyone
         copying words across. Everything below is presentation, and
         the overrides are deliberately specific because iubenda ships
         its own stylesheet with the text. */
      :root {{
        --paper: #fffdf9;
        --ink: #2a241d;
        --ink2: #7a6f62;
        --muted: #b0a596;
        --line: #e7dfd2;
        --serif: Georgia, "Times New Roman", serif;
        --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial,
          sans-serif;
      }}

      * {{ box-sizing: border-box; }}

      html, body {{
        margin: 0;
        padding: 0;
        background: var(--paper);
        color: var(--ink);
      }}

      /* ── Lola's type hierarchy ─────────────────────────────────────
         Verbatim from the brand guidelines p. 26, and canonical in
         nidi-app/constants/brand.ts. Every size on this site is one of
         these rungs; when something needs a size that is not here, the
         answer is a different rung, not a new number.

           display            serif 44/48 regular
           headingPage        sans  40/42 light
           headingEditorial   serif 36/40 regular
           headingSection     sans  30/32 light
           contextualLarge    serif 28/30 italic
           headingPrompt      serif 22/24 regular
           contextualRegular  serif 20/22 italic
           bodyRegular        sans  18/24 light
           button             sans  18/20 medium
           eyebrow            sans  12/14 regular

         Before 2026-09-26 the site used 13, 14, 15, 16, 17, 19, 24, 26,
         32, 34 and 40, none of them from here. Maru read it as off-brand
         on the Why page and she was right about the whole site. */

      /* bodyRegular, read on a browser: 16/26, not the scale's 18/24.
         Lola's rungs are measured on a phone at arm's length; a page in
         a browser sits further away and its column is wider, so the
         same rung reads a size too big and the lines run long. Maru
         called it twice (2026-09-26, 2026-09-29). The leading goes the
         other way: reading text wants air an app screen does not. */
      body {{
        font-family: var(--sans);
        font-weight: 300;
        font-size: 16px;
        line-height: 26px;
        -webkit-font-smoothing: antialiased;
      }}

      /* At the page gutter, not in a centred box: index.html puts the
         wordmark 28px from the left edge, and Maru caught it jumping
         inwards when you moved between the home page and Why. The
         content below still centres; the chrome does not. */
      header {{
        padding: 24px 28px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        /* 24px of padding plus a 44pt tap target: the height the home
           page's header takes anyway, held on every page so the wordmark
           sits at the same y instead of riding 12px higher wherever the
           header has nothing beside it. box-sizing is border-box here,
           so this is the whole header, padding included. */
        min-height: 68px;
      }}

      .wordmark {{ display: block; height: 15px; width: auto; }}

      /* eyebrow. */
      .lang {{
        display: flex;
        align-items: center;
        font-size: 12px;
        line-height: 14px;
        letter-spacing: 0.06em;
      }}
      .lang a {{
        color: var(--ink2);
        text-decoration: none;
        font-weight: 500;
        min-height: 44px;
        min-width: 44px;
        padding: 0 8px;
        display: flex;
        align-items: center;
      }}
      .lang a[aria-current="page"] {{ color: var(--ink); font-weight: 600; }}
      .lang .bar {{ width: 1px; height: 14px; background: var(--line); }}

      main {{
        max-width: 960px;
        margin: 0 auto;
        padding: 32px 28px 64px;
      }}

      /* Read by a screen reader, not shown: iubenda's own heading is the
         visible title, and two titles saying the same thing is worse than
         none. */
      .sr-only {{
        position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
        overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
      }}

      /* headingEditorial. */
      h1.page-title {{
        font-family: var(--serif);
        font-weight: 400;
        font-size: 36px;
        line-height: 40px;
        letter-spacing: -0.02em;
        margin: 0 0 32px;
        text-wrap: balance;
      }}

      /* eyebrow. */
      footer {{
        padding: 0 28px 40px;
        font-size: 12px;
        line-height: 14px;
        color: var(--ink2);
      }}
      footer a {{
        color: var(--ink);
        text-decoration: none;
        /* No rule under them (Maru, 2026-09-26). */
      }}
      .sep {{ padding: 0 8px; }}

      /* Maru, 2026-09-26: EN | ES lives at the bottom right, on every
         page. Up top it was the only control competing with the first
         line of whatever the page had to say, and on the home page it
         had started sharing that corner with the Why link. */
      footer {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        text-align: left;
      }}
      footer .lang a {{ color: var(--ink2); }}

      /* EN | ES keeps its 44px tap target and gives back the space
         around it, so the switch sits on the links' own line and its S
         lands on the page gutter rather than 12px inside it. Without
         this the nav is a 44px block against a 14px line and reads as
         dropped (Maru, 2026-09-29). */
      footer .lang {{ margin: -15px -12px -15px 0; }}
      footer .lang a {{ min-width: 0; padding: 0 12px; }}

      /* On a phone the links plus the switch do not fit on one line, so
         the studio credit takes the second line and the switch stays
         beside the links at the right gutter. Stacking the switch under
         Privacy was the old answer, and it read as dropped and out of
         line. */
      @media (max-width: 520px) {{
        h1.page-title {{ font-size: 26px; line-height: 30px; margin-bottom: 22px; }}
        footer {{ align-items: flex-start; }}
        .foot-links .sep-studio {{ display: none; }}
        .foot-links .studio {{ display: block; margin-top: 6px; }}
      }}

      a:focus-visible {{ outline: 2px solid var(--ink); outline-offset: 2px; }}

      /* ── The embedded document ──────────────────────────────────── */
      .doc {{ font-size: 16px; color: var(--ink); }}

      /* iubenda's own container and headings, re-dressed. Their
         stylesheet loads after this one, so these carry !important:
         it is the one place in the site where that is the honest
         solution rather than a shortcut. */
      .doc .iub_container,
      .doc .iub_content {{
        max-width: none !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        border: 0 !important;
        font-family: var(--sans) !important;
        color: var(--ink) !important;
      }}

      /* html body in front of every one of these: iubenda's own
         stylesheet carries rules more specific than .doc h1, so the
         whole block below was losing silently. The Privacy title was
         36px type on a 24px line and the two lines sat on top of each
         other on a phone. */
      html body .doc h1, html body .doc h2, html body .doc h3,
      html body .doc .iub_header h1, html body .doc .iub_header h2 {{
        font-family: var(--serif) !important;
        font-weight: 400 !important;
        color: var(--ink) !important;
        letter-spacing: -0.01em;
        line-height: 1.25 !important;
      }}
      /* headingSection, headingPrompt, bodyRegular: the document's own
         three levels on the three rungs under the page title. */
      html body .doc h1 {{ font-size: 30px !important; line-height: 34px !important;
                 margin: 40px 0 16px !important; }}
      html body .doc h2 {{ font-size: 22px !important; line-height: 26px !important;
                 margin: 36px 0 12px !important; }}
      html body .doc h3 {{ font-size: 18px !important; line-height: 26px !important;
                 margin: 28px 0 10px !important; }}

      .doc p, .doc li, .doc td, .doc th, .doc div {{
        font-family: var(--sans) !important;
        font-weight: 300 !important;
        font-size: 16px !important;
        line-height: 26px !important;
        color: var(--ink) !important;
      }}

      .doc a {{ color: var(--ink) !important; text-decoration: underline; }}

      /* The Terms carry a fill-in-the-blank line of 45 underscores
         ("consumer(s):______"), which nothing will break: it made the
         whole document 482px wide inside a 375px phone and pushed the
         page sideways. anywhere, not break-word: only anywhere shrinks
         the element's min-content width, which is what is doing the
         pushing. */
      .doc p, .doc li, .doc td, .doc th {{ overflow-wrap: anywhere; }}

      /* iubenda lays its own page out in flex rows that do not wrap: an
         aside beside the document, and a credits block in its footer.
         On a phone they pushed the whole page sideways, our own header
         and footer with it. */
      html body .doc footer,
      html body .doc .footer__first-row {{ flex-wrap: wrap !important; gap: 12px !important;
        box-sizing: border-box !important; max-width: 100% !important;
        margin-left: 0 !important; margin-right: 0 !important;
        padding: 16px !important; }}
      html body .doc .footer__first-row > * {{ max-width: 100% !important; }}
      html body .doc .aside-main-wrapper {{ display: block !important; }}
      /* And the accordion summaries, which are flex rows carrying a
         block of text: at 320px their text spilled past the page. */
      html body .doc summary {{ flex-wrap: wrap !important; }}
      html body .doc summary > * {{ min-width: 0 !important; max-width: 100% !important; }}

      .doc ul, .doc ol {{ padding-left: 22px; }}
      .doc li {{ margin: 6px 0; }}

      /* Their boxes and rules, in nidi's neutrals. */
      .doc .iub_content .one_line_col,
      .doc .box_primary, .doc .box_10, .doc .simple_pp {{
        background: transparent !important;
        border-color: var(--line) !important;
        box-shadow: none !important;
      }}
      .doc hr {{ border: 0; border-top: 1px solid var(--line); margin: 32px 0; }}

      /* Anything wide (their tables) scrolls inside itself rather than
         pushing the page sideways on a phone. */
      .doc table {{ display: block; overflow-x: auto; width: 100%; }}

      /* While iubenda's script is still fetching, the link it replaces
         should not read as the whole page. */
      .doc > a.iubenda-embed {{ color: var(--ink2) !important;
        font-size: 12px !important; line-height: 14px !important; }}


      /* ── iubenda's own components (their "legalDoc" markup) ──────── */
      .doc .container {{
        max-width: none !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
      }}

      /* Their header is a three-column flex row that does not fold on a
         phone: its breakpoints assume iubenda's own page, not ours. One
         column, always, inside a paper card. */
      .doc .main-header {{
        display: block !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 24px !important;
      }}
      .doc .main-header > * + * {{ margin-top: 14px; }}
      .doc .main-header h1 {{
        margin: 0 !important;
        font-size: 36px !important;
      }}
      /* Their stylesheet paints this rule in their own green. */
      .doc .main-header {{ border-top-color: var(--line) !important; }}
      .doc .main-header__meta {{
        color: var(--ink2) !important;
        font-size: 12px !important;
      }}

      /* Their two columns: a table of contents beside the document. Left
         to itself the aside takes a third of the width and the text ends up
         in a 480px trench. Below 900px the aside goes and their own
         "Table of contents" button takes over. */
      .doc .aside-main-wrapper {{
        display: grid !important;
        grid-template-columns: 200px minmax(0, 1fr) !important;
        gap: 48px !important;
        align-items: start;
      }}
      .doc aside {{ position: sticky; top: 24px; }}
      .doc .table-of-content-list a {{ font-size: 12px !important; }}

      @media (max-width: 900px) {{
        .doc .aside-main-wrapper {{ grid-template-columns: minmax(0, 1fr) !important; }}
        .doc aside {{ display: none !important; }}
      }}

      /* Their cards, accordions and buttons: paper edges, no shadows. */
      .doc .summary__card,
      .doc .legalDoc__accordion,
      .doc .body__details-box,
      .doc .card-button,
      .doc .table-of-content-btn-wrapper,
      .doc .open-dialog,
      .doc .iub-manage-preferences-btn {{
        background: transparent !important;
        border-color: var(--line) !important;
        box-shadow: none !important;
        color: var(--ink) !important;
      }}
      .doc .pill {{
        background: transparent !important;
        border: 1px solid var(--line) !important;
        color: var(--ink) !important;
      }}
      .doc .main__section {{ margin-top: 40px; }}

      /* iubenda draws its section icons as green SVG backgrounds
         (#1CC691). They cannot be recoloured directly, so they are
         desaturated and darkened to nidi's ink tint. Text is never
         inside these pseudo-elements, so nothing legible is touched. */
      .doc h2::before,
      .doc summary::before,
      .doc .card-button::before,
      .doc .meta__keys::before,
      .doc .meta__company::before,
      .doc .meta__location::before,
      .doc .check-style-list li::before {{
        filter: grayscale(1) brightness(0.62) !important;
      }}
      .doc summary {{ filter: grayscale(1) brightness(0.62); }}
      .doc summary * {{ filter: none; }}

      /* Theirs, and ours: text for screen readers only. */
      .doc .sr-only {{
        position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
        overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
      }}

      @media (max-width: 600px) {{
        h1.page-title {{ font-size: 30px; line-height: 32px; }}
        .doc h1 {{ font-size: 22px !important; line-height: 24px !important; }}
        .doc h2 {{ font-size: 18px !important; line-height: 24px !important; }}
      }}
    </style>
  </head>

  <body>
    <header>
      <a href="/" aria-label="nidi">{svg}</a>
    </header>

    <main>
      <h1 class="sr-only">{title}</h1>
      <div class="doc">
        {embed}
      </div>
    </main>

    <footer>
      <div class="foot-links">
        <a href="{siblinghref}">{siblinglabel}</a>
        <span class="sep">·</span>
        <a href="/">{homelabel}</a>
        <span class="sep sep-studio">·</span>
        <span class="studio">BALK Creative Studio</span>
      </div>
      <nav class="lang" aria-label="{navlabel}">
        <a href="/{enslug}/" lang="en"{encurrent}>EN</a>
        <span class="bar" aria-hidden="true"></span>
        <a href="/{esslug}/" lang="es"{escurrent}>ES</a>
      </nav>
    </footer>
  </body>
</html>
"""


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    svg_source = open(os.path.join(root, 'index.html')).read()
    start = svg_source.index('<svg class="wordmark"')
    svg = svg_source[start:svg_source.index('</svg>', start) + len('</svg>')]

    for slug, lang, title, docfile, otherslug, (siblabel, sibhref) in DOCS:
        embed = open(os.path.join(root, 'legal-src', docfile + '.html')).read().strip()
        enslug, esslug = PAIRS[slug]
        page = TEMPLATE.format(
            lang=lang,
            otherlang='es' if lang == 'en' else 'en',
            slug=slug,
            otherslug=otherslug,
            title=title,
            svg=svg,
            embed=embed,
            navlabel='Language' if lang == 'en' else 'Idioma',
            enslug=enslug,
            esslug=esslug,
            encurrent=' aria-current="page"' if lang == 'en' else '',
            escurrent=' aria-current="page"' if lang == 'es' else '',
            siblinglabel=siblabel,
            siblinghref=sibhref,
            homelabel='Home' if lang == 'en' else 'Inicio',
        )
        os.makedirs(os.path.join(root, slug), exist_ok=True)
        with open(os.path.join(root, slug, 'index.html'), 'w') as f:
            f.write(page)
        print(slug)


if __name__ == '__main__':
    main()

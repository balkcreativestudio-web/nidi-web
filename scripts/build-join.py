#!/usr/bin/env python3
"""Builds join/index.html and join/es/index.html from 404.html (2026-11-16).

GitHub Pages serves 404.html for any path that does not exist, which is
how nidi.life/join/<code> got a page without a server, but with a 404
status, and WhatsApp draws no link preview for a 404. So since
2026-11-16 the app shares nidi.life/join/?c=<code> (English) or
nidi.life/join/es/?c=<code> (Spanish): two real pages that answer 200
and, until 2026-11-23, carried the home page's preview, the honey orb on
cream with phrase A in the inviter's language.

Since 2026-11-23 (Maru: "La genérica") both pages carry ONE preview that
reads the same whoever receives it: the wordmark alone on the honey orb
(assets/og-join.png), the title "Nidi" and one line in both languages.
The preview used to follow the inviter's language, and in 3 of 9 complete
families the other home used Nidi in the other language. The home pages
(/ and /es/) keep og-en.png and og-es.png with the phrase.

The page itself is 404.html, unchanged: its script reads the code from
?c= and the language from /join/es/. Edit 404.html, never the two copies,
then run from the repo root:  python3 scripts/build-join.py
"""

import os

ROOT = os.path.join(os.path.dirname(__file__), '..')

# One preview for everyone (2026-11-23). Only the page address and the
# locale differ: the page still greets in the language of its path.
TITLE = 'Nidi'
DESC = 'Para familias que viven lejos. For families who live far apart.'
IMAGE = 'https://nidi.life/assets/og-join.png'

PAGES = {
    'en': dict(
        path='join/index.html',
        url='https://nidi.life/join/',
        title=TITLE,
        desc=DESC,
        image=IMAGE,
        locale='en_GB',
    ),
    'es': dict(
        path='join/es/index.html',
        url='https://nidi.life/join/es/',
        title=TITLE,
        desc=DESC,
        image=IMAGE,
        locale='es_AR',
    ),
}

HEAD = '''<title>{title}</title>
    <!-- Built from 404.html by scripts/build-join.py. Do not edit here. -->
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Nidi" />
    <meta property="og:locale" content="{locale}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{image}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="{title}." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{image}" />'''


def build():
    src = open(os.path.join(ROOT, '404.html')).read()
    assert src.count('<title>nidi</title>') == 1
    for lang, p in PAGES.items():
        out = src.replace('<title>nidi</title>', HEAD.format(**p), 1)
        if lang == 'es':
            assert out.count('<html lang="en">') == 1
            out = out.replace('<html lang="en">', '<html lang="es">', 1)
        path = os.path.join(ROOT, p['path'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(out)
        print('wrote', p['path'])


if __name__ == '__main__':
    build()

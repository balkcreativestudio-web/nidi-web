#!/usr/bin/env python3
"""Builds the Why pages: /why/ (EN) and /por-que/ (ES).

Maru's own text, in her own first person, about why nidi exists. The
English and the Spanish are both hers; the Spanish is not a translation
of the English and the two are deliberately not word-for-word.

Nidi is capitalised in both languages here, and lowercase in the app's
own voice and in the wordmark: Maru's rule is that the app is lowercase
when it speaks as itself and capitalised when somebody speaks about it
from outside. This page is somebody speaking about it.

The frame (header, wordmark, language switch, footer, tokens) comes from
scripts/build-legal.py the same way scripts/build-support.py takes it,
so this does not look like a different website from the privacy policy.

Run from the repo root:  python3 scripts/build-why.py
"""

import os

FRAME = open(os.path.join(os.path.dirname(__file__), 'build-legal.py')).read()
# build-legal.py holds this block inside a str.format template, so its
# braces are doubled. Here it is inserted as a value rather than
# formatted, so they have to come back down to one.
CSS = (FRAME[FRAME.index('    <style>'):FRAME.index('      /* ── The embedded document ──')]
       .replace('{{', '{').replace('}}', '}'))
SVG_SRC = open(os.path.join(os.path.dirname(__file__), '..', 'index.html')).read()
_start = SVG_SRC.index('<svg class="wordmark"')
_end = SVG_SRC.index('</svg>', _start) + len('</svg>')
WORDMARK = SVG_SRC[_start:_end]

# Lola's type hierarchy, verbatim from the brand guidelines p. 26 and
# canonical in nidi-app/constants/brand.ts:
#
#   headingEditorial   serif 36/40 regular
#   bodyRegular        sans  18/24 light
#
# The first version of this page set the whole essay in serif at 20/32,
# which Maru read as off-brand before anybody looked up why. It was: the
# reading voice of nidi is Hanken Grotesk Light, and serif carries
# titles and short emotional lines, not paragraphs.
EXTRA_CSS = """
      main { max-width: 620px; }

      /* headingEditorial: serif 36/40. */
      h1.page-title {
        font-family: var(--serif);
        font-weight: 400;
        font-size: 36px;
        line-height: 40px;
        letter-spacing: -0.02em;
        margin: 0 0 32px;
        text-wrap: balance;
      }

      /* bodyRegular: sans light 18/24. */
      .why p {
        font-family: var(--sans);
        font-weight: 300;
        font-size: 18px;
        line-height: 24px;
        color: var(--ink);
        margin: 0 0 24px;
      }

      /* The last two lines are one paragraph with a hard break in the
         middle, the way Maru wrote it: the pause before "she knows her
         grandparents' voices" is the point of the ending. */
      .why p .turn { display: block; margin-top: 12px; }

      @media (max-width: 520px) {
        h1.page-title { font-size: 30px; line-height: 34px; margin-bottom: 24px; }
      }
"""

PAGE = """<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} · nidi</title>
    <meta name="description" content="{description}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="https://nidi.life/{slug}/" />
    <link rel="alternate" hreflang="en" href="https://nidi.life/why/" />
    <link rel="alternate" hreflang="es" href="https://nidi.life/por-que/" />
    <meta name="theme-color" content="#FFFDF9" />
{css}{extra}
    </style>
  </head>
  <body>
    <header>
      <a href="/" aria-label="nidi">{svg}</a>
    </header>

    <main>
      <h1 class="page-title">{title}</h1>
      <div class="why">
{body}
      </div>
    </main>

    <!-- No way home in here: the wordmark at the top left is it
         (Maru, 2026-09-26). -->
    <footer>
      <div class="foot-links">
        <a href="{privacy}">{privacylabel}</a>
        <span class="sep">·</span>
        <a href="{terms}">{termslabel}</a>
        <span class="sep">·</span>
        BALK Creative Studio
      </div>
      <nav class="lang" aria-label="{navlabel}">
        <a href="/why/" lang="en"{encurrent}>EN</a>
        <span class="bar" aria-hidden="true"></span>
        <a href="/por-que/" lang="es"{escurrent}>ES</a>
      </nav>
    </footer>
  </body>
</html>
"""

EN = dict(
    slug='why', lang='en', title='Why',
    description=(
        "Why I built Nidi: an Argentine mother in the Netherlands, "
        "grandparents 11,000 km away, and a daughter who knows their voices."
    ),
    navlabel='Language',
    privacy='/privacy/', privacylabel='Privacy',
    terms='/terms/', termslabel='Terms',
    paragraphs=[
        "I'm an Argentine mother in the Netherlands. When my daughter was "
        "born, my parents were 11,000 km away, and video calls with a baby "
        "don't work. I wanted her to grow up knowing her grandparents' "
        "voices, not just faces on a screen. So I built Nidi.",

        "Nidi connects two houses: the child's, and one far away. Every day "
        "it suggests small things to do, apart but together. A grandmother "
        "records a good morning in her voice. Both houses photograph the "
        "same sky, or cook the same recipe. The screen carries it; the "
        "moment happens off it. It all lands in Memory, an archive that "
        "stays with the family.",

        "Nidi is quiet on purpose. Voice, photo and text. A few things a "
        "day, chosen for the child's age, from the first months to six "
        "years old. Nothing to scroll, nothing to keep up with. Just what "
        "happened today, kept.",

        "Since we started testing, my parents have read my daughter bedtime "
        "stories, sung to her at breakfast, and left a good morning every "
        "day, recorded the night before in Buenos Aires."
        '<span class="turn">My daughter is not yet two. She knows her '
        "grandparents' voices.</span>",
    ],
)

ES = dict(
    slug='por-que', lang='es', title='Por qué',
    description=(
        'Por qué hice Nidi: una mamá argentina en Holanda, los abuelos a '
        '11.000 kilómetros, y una hija que conoce sus voces.'
    ),
    navlabel='Idioma',
    privacy='/privacidad/', privacylabel='Privacidad',
    terms='/terminos/', termslabel='Términos',
    paragraphs=[
        'Soy una mamá argentina que vive en Holanda. Cuando nació mi hija, '
        'mis papás estaban a 11.000 kilómetros, y las videollamadas con un '
        'bebé no funcionan. Yo quería que creciera conociendo la voz de sus '
        'abuelos, no solo caras en una pantalla. Entonces hice Nidi.',

        'Nidi une dos casas: la del niño, y una que está en otro lugar. '
        'Todos los días propone cosas chicas para hacer, cada uno en su casa '
        'y los dos juntos. Una abuela graba un buen día con su voz. Las dos '
        'casas sacan una foto del mismo cielo, o cocinan la misma receta. La '
        'pantalla lo lleva; el momento pasa afuera de ella. Todo queda en '
        'Recuerdos, un archivo que se queda con la familia.',

        'Nidi es silencioso a propósito. Voz, foto y texto. Algunas cosas '
        'por día, elegidas según la edad del niño, desde los primeros meses '
        'hasta los seis años. Nada para scrollear, nada que seguir. Solo lo '
        'que pasó hoy, guardado.',

        'Desde que empezamos a probarlo, mis papás le leyeron cuentos a mi '
        'hija antes de dormir, le cantaron en el desayuno, y le dejaron un '
        'buen día todos los días, grabado la noche anterior en Buenos Aires.'
        '<span class="turn">Mi hija todavía no cumplió dos. Conoce la voz de '
        'sus abuelos.</span>',
    ],
)


def render(doc: dict) -> str:
    body = '\n'.join(f'        <p>{p}</p>' for p in doc['paragraphs'])
    current = ' aria-current="page"'
    return PAGE.format(
        css=CSS, extra=EXTRA_CSS, svg=WORDMARK, body=body,
        encurrent=current if doc['lang'] == 'en' else '',
        escurrent=current if doc['lang'] == 'es' else '',
        **{k: v for k, v in doc.items() if k != 'paragraphs'},
    )


def main() -> None:
    root = os.path.join(os.path.dirname(__file__), '..')
    for doc in (EN, ES):
        out = os.path.join(root, doc['slug'])
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, 'index.html'), 'w') as f:
            f.write(render(doc))
        print('wrote', doc['slug'] + '/index.html')


if __name__ == '__main__':
    main()

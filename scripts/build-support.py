#!/usr/bin/env python3
"""Builds the support pages: /support/ (EN) and /soporte/ (ES).

Apple asks every app for a support URL, and the honest version of one is
a way to reach a person plus answers to the things people actually write
in about. Both are here.

The frame (header, wordmark, language switch, footer, tokens) is the
same one scripts/build-legal.py uses, so support does not look like a
different website from the privacy policy.

Run from the repo root:  python3 scripts/build-support.py
"""

import os
import re

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

EXTRA_CSS = """
      main { max-width: 720px; }

      h1.page-title {
        font-family: var(--serif);
        font-weight: 400;
        font-size: 40px;
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin: 0 0 12px;
        text-wrap: balance;
      }
      .lede {
        font-size: 17px;
        color: var(--ink2);
        margin: 0 0 40px;
        max-width: 34em;
      }

      .reach {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 24px;
        margin: 0 0 48px;
      }
      .reach p { margin: 0 0 8px; }
      .reach .mail {
        font-family: var(--serif);
        font-size: 24px;
        letter-spacing: -0.01em;
      }
      .reach .mail a { color: var(--ink); text-decoration: none;
                       border-bottom: 1px solid var(--line); }
      .reach .when { font-size: 14px; color: var(--ink2); margin: 12px 0 0; }

      h2 {
        font-family: var(--serif);
        font-weight: 400;
        font-size: 26px;
        letter-spacing: -0.01em;
        margin: 48px 0 20px;
      }

      .q { border-top: 1px solid var(--line); padding: 20px 0 4px; }
      .q h3 {
        font-family: var(--sans);
        font-weight: 600;
        font-size: 16px;
        margin: 0 0 6px;
      }
      .q p { margin: 0 0 12px; color: var(--ink2); }
      .q a { color: var(--ink); }

      @media (max-width: 520px) {
        h1.page-title { font-size: 32px; }
        .reach { padding: 20px; }
        .reach .mail { font-size: 20px; }
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
    <link rel="alternate" hreflang="en" href="https://nidi.life/support/" />
    <link rel="alternate" hreflang="es" href="https://nidi.life/soporte/" />
    <meta name="theme-color" content="#FFFDF9" />
{css}{extra}
    </style>
  </head>
  <body>
    <header>
      <a href="/" aria-label="nidi">{svg}</a>
      <nav class="lang" aria-label="{navlabel}">
        <a href="/support/" lang="en"{encurrent}>EN</a>
        <span class="bar" aria-hidden="true"></span>
        <a href="/soporte/" lang="es"{escurrent}>ES</a>
      </nav>
    </header>

    <main>
      <h1 class="page-title">{title}</h1>
      <p class="lede">{lede}</p>

      <div class="reach">
        <p>{reachlabel}</p>
        <p class="mail"><a href="mailto:hello@nidi.life">hello@nidi.life</a></p>
        <p class="when">{reachwhen}</p>
      </div>

      <h2>{faqtitle}</h2>
{faq}
    </main>

    <footer>
      <a href="{privacy}">{privacylabel}</a>
      <span class="sep">·</span>
      <a href="{terms}">{termslabel}</a>
      <span class="sep">·</span>
      <a href="/">{homelabel}</a>
      <span class="sep">·</span>
      BALK Creative Studio
    </footer>
  </body>
</html>
"""

EN = dict(
    slug='support', lang='en', title='Support',
    description='How to reach us about nidi, and answers to the questions people ask most.',
    lede='Something not working, or a question about your nidi? Write to us. A person reads every message.',
    reachlabel='Write to us',
    reachwhen='We answer in English and Spanish, usually within two working days.',
    faqtitle='The questions people ask',
    privacy='/privacy/', privacylabel='Privacy',
    terms='/terms/', termslabel='Terms',
    homelabel='nidi.life', navlabel='Language',
    faq=[
        ('How do I invite the other person?',
         'In the app, open You and then Your nidis, and send the invitation. '
         'It arrives as a link to nidi.life and a short code. Whoever opens '
         'the link gets the app and enters the code, and the two of you are '
         'connected.'),
        ('Someone sent me a code. What do I do with it?',
         'Download nidi, sign in with your email, and there is a place to '
         'enter the code on the first screen. You do not need an account '
         'anywhere else.'),
        ('What does nidi cost?',
         'The first exchanges are free. After that, one membership keeps a '
         'nidi going, and only one of the two people pays it. The other side '
         'never sees a payment screen.'),
        ('How do I cancel?',
         'Memberships are handled by Apple, not by us. On your iPhone open '
         'Settings, tap your name, then Subscriptions, and cancel there. It '
         'stays active until the end of the period you already paid for.'),
        ('What happens to our moments if the membership stops?',
         'Nothing is deleted. Everything you have already sent each other '
         'stays in Memory and can still be opened and listened to. What '
         'pauses is sending new ones, until someone starts the membership '
         'again.'),
        ('How do I delete my account?',
         'In the app, open You, scroll to the bottom and choose Delete '
         'account. We email you a code to make sure it is really you, and '
         'nothing is deleted until you enter it.'),
        ('Who can see what we send?',
         'Only the two adults in that nidi. Photos and voice notes are '
         'stored privately and are not public, not searchable, and not '
         'shown to anyone else. We do not sell anything to anyone.'),
        ('I am not getting notifications.',
         'Check that notifications are allowed for nidi in your iPhone '
         'settings, and that Quiet hours in the app are not covering the '
         'time you expect them. If it still happens, write to us.'),
        ('Can I use nidi in Spanish?',
         'Yes. nidi follows your phone. If your phone is in Spanish, so is '
         'nidi, and each of you reads in your own language even inside the '
         'same nidi.'),
        ('Something is broken.',
         'Write to us and say what you were doing when it happened. If you '
         'can, add a screenshot. It is the fastest way for us to find it.'),
    ],
)

ES = dict(
    slug='soporte', lang='es', title='Soporte',
    description='Cómo escribirnos por nidi, y las respuestas a lo que más nos preguntan.',
    lede='¿Algo no funciona, o tenés una duda sobre tu nidi? Escribinos. Los mensajes los lee una persona.',
    reachlabel='Escribinos',
    reachwhen='Respondemos en español y en inglés, normalmente dentro de los dos días hábiles.',
    faqtitle='Lo que más nos preguntan',
    privacy='/privacidad/', privacylabel='Privacidad',
    terms='/terminos/', termslabel='Términos',
    homelabel='nidi.life', navlabel='Idioma',
    faq=[
        ('¿Cómo invito a la otra persona?',
         'En la app, entrá a Vos y después a Tus nidis, y mandá la '
         'invitación. Llega como un link a nidi.life y un código corto. '
         'Quien abre el link baja la app, pone el código, y quedan '
         'conectados.'),
        ('Me mandaron un código. ¿Qué hago?',
         'Bajá nidi, entrá con tu correo, y en la primera pantalla hay un '
         'lugar para poner el código. No necesitás cuenta en ningún otro '
         'lado.'),
        ('¿Cuánto cuesta nidi?',
         'Los primeros intercambios son gratis. Después, una membresía '
         'mantiene el nidi andando, y la paga una sola de las dos personas. '
         'La otra nunca ve una pantalla de pago.'),
        ('¿Cómo doy de baja la membresía?',
         'Las membresías las maneja Apple, no nosotros. En tu iPhone entrá '
         'a Configuración, tocá tu nombre, después Suscripciones, y '
         'cancelá ahí. Sigue activa hasta que termine el período que ya '
         'pagaste.'),
        ('¿Qué pasa con nuestros momentos si se corta la membresía?',
         'No se borra nada. Todo lo que ya se mandaron queda en Memoria y '
         'se puede seguir abriendo y escuchando. Lo que se pausa es mandar '
         'cosas nuevas, hasta que alguien retome la membresía.'),
        ('¿Cómo borro mi cuenta?',
         'En la app, entrá a Vos, bajá hasta el final y elegí Borrar '
         'cuenta. Te mandamos un código por correo para confirmar que sos '
         'vos, y no se borra nada hasta que lo pongas.'),
        ('¿Quién puede ver lo que nos mandamos?',
         'Solo los dos adultos de ese nidi. Las fotos y los audios se '
         'guardan de forma privada: no son públicos, no aparecen en '
         'búsquedas y no se le muestran a nadie más. No le vendemos nada a '
         'nadie.'),
        ('No me llegan las notificaciones.',
         'Fijate que nidi tenga permitidas las notificaciones en la '
         'configuración del iPhone, y que las Horas de silencio de la app '
         'no estén tapando el horario en que las esperás. Si sigue '
         'pasando, escribinos.'),
        ('¿Puedo usar nidi en español?',
         'Sí. nidi sigue el idioma de tu teléfono. Si tu teléfono está en '
         'español, nidi también, y cada uno lee en su propio idioma aunque '
         'estén en el mismo nidi.'),
        ('Algo se rompió.',
         'Escribinos contando qué estabas haciendo cuando pasó. Si podés, '
         'sumá una captura de pantalla. Es la forma más rápida de que lo '
         'encontremos.'),
    ],
)


def render(doc: dict) -> str:
    faq = '\n'.join(
        f'      <div class="q">\n'
        f'        <h3>{q}</h3>\n'
        f'        <p>{a}</p>\n'
        f'      </div>'
        for q, a in doc['faq']
    )
    current = ' aria-current="page"'
    return PAGE.format(
        css=CSS, extra=EXTRA_CSS, svg=WORDMARK, faq=faq,
        encurrent=current if doc['lang'] == 'en' else '',
        escurrent=current if doc['lang'] == 'es' else '',
        **{k: v for k, v in doc.items() if k != 'faq'},
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

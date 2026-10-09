#!/usr/bin/env python3
"""Builds nidi.life: index.html (one long page, both languages) and the
two old Why URLs, which now point at its #why section.

Copy is written side by side as  [[ English ||| Español ]]  and expanded
into two spans with lang attributes; the page shows one of them. *word*
becomes the italic run Lola puts in every headline. Everything the app's
voice rules forbid (dashes, exclamation marks, urgency) is kept out of
the copy here, not filtered afterwards: read docs/voice.md in nidi-app.

Design source: Lola's guideline (Nidi_Guidelines.pdf) and the app's own
tokens; scratchpad notes in nidi-app/docs/design. The structure follows
how heare.app tells its story (hook, the moment, three steps, proof,
trust, the app, questions, one last ask), in Nidi's own voice.

APP_LIVE: False until Apple releases the app. While it is False, every
call to action is the email form; flip it and run this again and they
all become "Take a look" on the App Store.

Run from the repo root:  python3 scripts/build-home.py
"""

import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..')
APP_LIVE = False
APP_STORE_URL = 'https://apps.apple.com/app/id6774968835'

# The wordmark artwork lives in index.html (every build script reads it
# from there), so it is lifted from the page this overwrites.
_old = open(os.path.join(ROOT, 'index.html')).read()
_s = _old.index('<svg class="wordmark"')
WORDMARK = _old[_s:_old.index('</svg>', _s) + len('</svg>')]
WORDMARK_CTA = WORDMARK.replace('class="wordmark"', 'class="wordmark wordmark-cream" aria-hidden="true"', 1) \
                       .replace('role="img" aria-label="nidi" ', '')

TEMPLATE = r'''<!doctype html>
<html lang="en" data-l="en" data-live="@@LIVE@@">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Nidi. Grow close. From anywhere.</title>
    <meta name="description" content="Nidi connects two homes: the one where a child is growing up, and one far away. Voice, photo and text, a few small things a day, kept in Memory." />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Nidi. Grow close. From anywhere." />
    <meta property="og:description" content="Nidi connects two homes: the one where a child is growing up, and one far away." />
    <meta property="og:url" content="https://nidi.life" />
    <meta property="og:image" content="https://nidi.life/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="https://nidi.life/assets/og.png" />
    <link rel="canonical" href="https://nidi.life" />
    <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
    <meta name="theme-color" content="#F4EFE7" />
    <meta name="color-scheme" content="light" />
    <link rel="preload" href="/assets/fonts/Lora-Regular.ttf" as="font" type="font/ttf" crossorigin />
    <link rel="preload" href="/assets/fonts/HankenGrotesk-Light.ttf" as="font" type="font/ttf" crossorigin />
    <script>
      // Language is settled before first paint so the page never flashes
      // the wrong one. ?lang=es links straight to Spanish.
      (function () {
        var l = new URLSearchParams(location.search).get("lang");
        try { l = l || localStorage.getItem("nidi-lang"); } catch (e) {}
        l = l || ((navigator.language || "en").toLowerCase().indexOf("es") === 0 ? "es" : "en");
        l = l === "es" ? "es" : "en";
        document.documentElement.lang = l;
        document.documentElement.setAttribute("data-l", l);
      })();
    </script>
    <style>
      @font-face { font-family: "Lora"; src: url(/assets/fonts/Lora-Regular.ttf) format("truetype"); font-weight: 400; font-style: normal; font-display: swap; }
      @font-face { font-family: "Lora"; src: url(/assets/fonts/Lora-Italic.ttf) format("truetype"); font-weight: 400; font-style: italic; font-display: swap; }
      @font-face { font-family: "Hanken Grotesk"; src: url(/assets/fonts/HankenGrotesk-Light.ttf) format("truetype"); font-weight: 300; font-style: normal; font-display: swap; }
      @font-face { font-family: "Hanken Grotesk"; src: url(/assets/fonts/HankenGrotesk-Medium.ttf) format("truetype"); font-weight: 500; font-style: normal; font-display: swap; }

      :root {
        /* Lola's neutrals (guideline p.32) and the app's text tint. */
        --ink: #2a241d;
        --cream: #f4efe7;
        --paper: #fffef8;
        --ink2: #74695a;
        --line: rgba(42, 36, 29, 0.15);
        --hair: rgba(42, 36, 29, 0.09);
        /* Personal colours stand for people and nothing else (p.35):
           here they only ever colour an orb. Olive and lavender are the
           pair Lola chose to introduce the brand. */
        --olive: #87995b;
        --lavender: #9890b0;
        --honey: #e2a75a;
        --serif: "Lora", Georgia, "Times New Roman", serif;
        --sans: "Hanken Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        --gutter: max(24px, calc((100vw - 1160px) / 2));
        --ease-out: cubic-bezier(0, 0, 0.58, 1);
      }
      * { box-sizing: border-box; }
      html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }
      html[data-l="en"] [lang="es"]:not(html):not(button), html[data-l="es"] [lang="en"]:not(html):not(button) { display: none !important; }
      body {
        margin: 0;
        background: var(--paper);
        color: var(--ink);
        font-family: var(--sans);
        font-weight: 300;
        font-size: 18px;
        line-height: 1.55;
        -webkit-font-smoothing: antialiased;
        font-synthesis: none;
        overflow-x: hidden;
      }
      img, svg { display: block; max-width: 100%; }
      .hero-grid > *, .split > *, .row > *, .arrival-grid > *, .free-grid > * { min-width: 0; }
      a { color: inherit; }
      em { font-style: italic; }
      :focus-visible { outline: 2px solid var(--ink); outline-offset: 3px; border-radius: 4px; }
      .sr-only { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
      .skip { position: absolute; left: 16px; top: -60px; background: var(--ink); color: var(--paper); padding: 10px 16px; border-radius: 999px; z-index: 100; text-decoration: none; }
      .skip:focus { top: 12px; }
      .wrap { width: min(1160px, calc(100% - 48px)); margin-inline: auto; }

      /* ── Type (Lola p.26, scaled for a browser) ─────────────────── */
      h1, h2, h3, h4 { margin: 0; font-family: var(--serif); font-weight: 400; text-wrap: balance; }
      h1 { font-size: clamp(34px, 6.1vw, 84px); line-height: 1.06; letter-spacing: -0.012em; }
      h2 { font-size: clamp(34px, 4.7vw, 62px); line-height: 1.1; letter-spacing: -0.008em; }
      h3 { font-size: clamp(27px, 3.1vw, 40px); line-height: 1.15; }
      h4 { font-size: 22px; line-height: 1.25; }
      p { margin: 0; text-wrap: pretty; }
      .eyebrow { font-weight: 500; font-size: 12px; line-height: 14px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink2); margin-bottom: 20px; }
      .lead { font-size: clamp(19px, 2vw, 23px); line-height: 1.5; color: var(--ink); max-width: 34em; }
      .muted { color: var(--ink2); }
      section { position: relative; padding-block: clamp(76px, 10vw, 148px); }
      section[id], .scroll-anchor { scroll-margin-top: 72px; }
      .bg-cream { background: var(--cream); }
      .bg-paper { background: var(--paper); }
      .bg-ink { background: var(--ink); color: var(--cream); }
      .bg-ink .eyebrow, .bg-ink .muted { color: rgba(244, 239, 231, 0.62); }

      /* ── Buttons and the email form (same controls as the app) ──── */
      .btn { display: inline-flex; align-items: center; justify-content: center; min-height: 52px; padding: 0 28px; border: 0; border-radius: 999px; background: var(--ink); color: var(--paper); font-family: var(--sans); font-weight: 500; font-size: 17px; text-decoration: none; cursor: pointer; transition: transform 0.4s var(--ease-out), background 0.4s var(--ease-out); }
      .btn:hover { background: #3d352b; }
      .btn:active { transform: scale(0.985); }
      .btn:disabled { opacity: 0.55; cursor: default; }
      .btn { white-space: nowrap; }
      .btn-sm { min-height: 44px; padding: 0 20px; font-size: 15px; }
      .btn-light { background: var(--cream); color: var(--ink); }
      .btn-light:hover { background: #fff; }
      form.wl { display: flex; gap: 10px; max-width: 460px; }
      form.wl input[type="email"] { flex: 1; min-width: 0; min-height: 52px; font-family: var(--serif); font-size: 16px; line-height: 22px; color: var(--ink); background: var(--paper); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; }
      form.wl input[type="email"]::placeholder { color: #b0a596; }
      form.wl input[type="email"][aria-invalid="true"] { border-color: #cc644c; box-shadow: 0 0 0 1px #cc644c; }
      .wl-done, .wl-error { margin-top: 14px; font-size: 16px; }
      .wl-error { color: #a8442e; }
      .wl-note { margin-top: 14px; font-size: 14px; color: var(--ink2); }
      .bg-ink .wl-note { color: rgba(244, 239, 231, 0.62); }
      .live-only { display: none; }
      html[data-live="true"] .live-only { display: block; }
      html[data-live="true"] .soon-only { display: none; }
      html[data-live="true"] a.live-only.btn { display: inline-flex; }
      @media (max-width: 520px) { form.wl { flex-direction: column; } form.wl .btn { width: 100%; } }

      /* ── Header ───────────────────────────────────────────────────── */
      header.top { position: sticky; top: 0; z-index: 50; background: rgba(244, 239, 231, 0.88); backdrop-filter: saturate(1.2) blur(14px); -webkit-backdrop-filter: saturate(1.2) blur(14px); border-bottom: 1px solid transparent; transition: border-color 0.4s var(--ease-out); }
      header.top.scrolled { border-bottom-color: var(--hair); }
      .bar { display: flex; align-items: center; justify-content: space-between; gap: 20px; min-height: 68px; }
      .wordmark { height: 30px; width: auto; animation: appear 0.8s var(--ease-out) both; }
      .wordmark path { fill: currentColor; }
      .wordmark-cream { color: var(--cream); }
      nav.links { display: flex; gap: 6px; margin-left: auto; }
      nav.links a { font-size: 15px; font-weight: 500; text-decoration: none; color: var(--ink2); padding: 10px 14px; min-height: 44px; display: inline-flex; align-items: center; border-radius: 999px; transition: color 0.3s; }
      nav.links a:hover { color: var(--ink); }
      .lang { display: flex; align-items: center; font-size: 12px; letter-spacing: 0.06em; }
      .lang button { background: none; border: 0; font: inherit; font-weight: 500; color: var(--ink2); min-height: 44px; min-width: 40px; padding: 0 6px; cursor: pointer; }
      .lang button[aria-pressed="true"] { color: var(--ink); }
      .lang .sep { width: 1px; height: 14px; background: var(--line); }
      @media (max-width: 880px) { nav.links { display: none; } .bar { gap: 8px; } .bar .lang { margin-left: auto; } }
      @keyframes appear { from { opacity: 0; } to { opacity: 1; } }

      /* ── The orb: two nests, breathing ───────────────────────────── */
      /* Nine-stop falloff measured off Lola's Figma, flat for the inner
         third and gone into paper at the rim; a hairline ring or it
         reads as a smudge. It breathes 1.000 to 1.077 over 2.5s, and
         two orbs are never quite in step: they are near, not in sync. */
      .orb { --c: var(--olive); --bg: var(--paper); --size: 260px; width: var(--size); height: var(--size); border-radius: 50%; position: relative; border: 1.25px solid color-mix(in srgb, var(--c) 68%, var(--bg));
        background: radial-gradient(circle closest-side,
          var(--c) 0%, color-mix(in srgb, var(--bg) 1%, var(--c)) 36.2%, color-mix(in srgb, var(--bg) 5.5%, var(--c)) 51.5%,
          color-mix(in srgb, var(--bg) 13.2%, var(--c)) 62.9%, color-mix(in srgb, var(--bg) 24.8%, var(--c)) 72.3%,
          color-mix(in srgb, var(--bg) 39.6%, var(--c)) 80.6%, color-mix(in srgb, var(--bg) 57.5%, var(--c)) 88%,
          color-mix(in srgb, var(--bg) 78.4%, var(--c)) 94.6%, var(--bg) 100%); }
      .orb.on-cream { --bg: var(--cream); }
      .orb.lav { --c: var(--lavender); }
      .breathes { animation: breathe 2.5s ease-in-out infinite; }
      @keyframes breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.077); } }

      /* ── Hero ─────────────────────────────────────────────────────── */
      .hero { background: var(--cream); padding-block: clamp(40px, 6vw, 88px) clamp(72px, 9vw, 130px); overflow: hidden; }
      .hero-grid { display: grid; gap: 56px; align-items: center; }
      @media (min-width: 940px) { .hero-grid { grid-template-columns: 1.3fr 0.8fr; gap: 48px; } }
      .hero .lead { margin-top: 28px; }
      .hero .cta { margin-top: 36px; }
      /* A window's shadow drifting over paper: time passing in another house. */
      .light { position: absolute; inset: -20% -10%; pointer-events: none; background: linear-gradient(104deg, transparent 32%, rgba(255, 254, 248, 0.62) 46%, rgba(255, 254, 248, 0.0) 60%); animation: drift 16s ease-in-out infinite alternate; }
      @keyframes drift { from { transform: translateX(-14%); } to { transform: translateX(14%); } }
      .hero > .wrap { position: relative; }
      .homes { position: relative; min-height: clamp(360px, 38vw, 470px); }
      .home { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 20px; text-align: center; }
      .home p { font-size: clamp(14px, 1.2vw, 17px); line-height: 1.25; max-width: 10.5em; text-wrap: balance; letter-spacing: -0.01em; opacity: 0; animation: arrive 1.1s var(--ease-out) forwards; }
      .home-a { left: 4%; bottom: 0; }
      .home-a .orb { --size: clamp(170px, 19vw, 240px); }
      .home-a p { animation-delay: 0.9s; }
      .home-b { right: 2%; top: 0; }
      .home-b .orb { --size: clamp(92px, 10vw, 128px); }
      .home-b p { animation-delay: 1.9s; }
      .drifts-a { animation: float 11s ease-in-out infinite alternate; }
      .drifts-b { animation: float 13s ease-in-out -4s infinite alternate; }
      @keyframes float { from { transform: translate(0, 0); } to { transform: translate(8px, -12px); } }
      /* Words arrive from a third of their strength, never from nothing. */
      @keyframes arrive { from { opacity: 0.0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      @media (max-width: 939px) { .homes { min-height: 380px; } .home-a .orb { --size: 190px; } .home-b .orb { --size: 104px; } }

      /* ── Pillars ──────────────────────────────────────────────────── */
      .pillars { padding-block: 0; background: var(--paper); border-bottom: 1px solid var(--hair); }
      .pillar-grid { display: grid; }
      .pillar { padding: 34px 0; border-top: 1px solid var(--hair); }
      .pillar:first-child { border-top: 0; }
      .pillar .eyebrow { margin-bottom: 10px; color: var(--ink); }
      @media (min-width: 820px) { .pillar-grid { grid-template-columns: repeat(3, 1fr); } .pillar { border-top: 0; border-left: 1px solid var(--hair); padding: 44px 36px; } .pillar:first-child { border-left: 0; padding-left: 0; } }

      /* ── Her words, up where they are felt ───────────────────────── */
      .stand { padding-block: clamp(72px, 9vw, 128px); }
      .stand blockquote { margin: 0; max-width: 17em; font-family: var(--serif); font-style: italic; font-size: clamp(30px, 4.4vw, 54px); line-height: 1.18; text-wrap: balance; }
      .stand-by { margin-top: 32px; max-width: 34em; font-size: 17px; color: var(--ink2); }
      .stand-by a { color: var(--ink); text-underline-offset: 4px; text-decoration-thickness: 1px; white-space: nowrap; }
      /* ── The moment ───────────────────────────────────────────────── */
      .split { display: grid; gap: 48px; align-items: center; }
      @media (min-width: 900px) { .split { grid-template-columns: 1fr 1fr; gap: 88px; } .split.flip > :first-child { order: 2; } }
      .photo { border-radius: 4px; overflow: hidden; background: var(--cream); }
      .bg-ink .photo { background: #3a322a; }
      .photo img { width: 100%; height: auto; }
      .scenes { margin-top: 40px; display: grid; gap: 0; }
      .scene { padding: 22px 0; border-top: 1px solid var(--hair); }
      .scene .eyebrow { margin-bottom: 6px; }
      .scene p { font-family: var(--serif); font-size: 20px; line-height: 1.4; }
      .scene p.eyebrow { font-family: var(--sans); font-size: 12px; line-height: 14px; }
      .resolve { margin-top: 36px; font-size: 20px; max-width: 28em; }

      /* ── How it works ─────────────────────────────────────────────── */
      .steps { margin-top: 44px; display: grid; gap: 0; }
      .step { padding: 28px 0; border-top: 1px solid var(--line); display: grid; gap: 8px; }
      .step h3 { font-size: clamp(25px, 2.6vw, 32px); }
      .step p { color: var(--ink2); max-width: 30em; }
      .photo.tall { max-width: 460px; }

      /* ── Arrival: the orb, opened ────────────────────────────────── */
      .arrival { background: var(--cream); overflow: hidden; }
      .arrival-grid { display: grid; gap: 56px; align-items: center; }
      @media (min-width: 900px) { .arrival-grid { grid-template-columns: 1fr 380px; gap: 96px; } }
      .arrival .lead { margin-top: 24px; }
      .hint { margin-top: 28px; font-size: 14px; color: var(--ink2); letter-spacing: 0.02em; }
      .phone { position: relative; width: min(340px, 82vw); aspect-ratio: 9 / 18.4; border-radius: 46px; overflow: hidden; background: var(--paper); box-shadow: 0 30px 70px rgba(42, 36, 29, 0.16), 0 0 0 1px var(--hair); margin-inline: auto; isolation: isolate; }
      .p-idle { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: flex-start; padding: 0 24px; transition: opacity 0.7s var(--ease-out); }
      .p-status { position: absolute; left: 0; right: 0; top: 0; height: 52px; display: flex; align-items: center; padding: 6px 30px 0; font-weight: 500; font-size: 14px; }
      .p-status i { position: absolute; left: 50%; top: 12px; width: 92px; height: 27px; margin-left: -46px; border-radius: 99px; background: #0b0a09; }
      .p-greet { margin-top: 62px; display: flex; align-items: center; gap: 12px; }
      .av { width: 34px; height: 34px; border-radius: 50%; background: var(--honey); box-shadow: 0 0 0 2px var(--paper), 0 0 0 3px var(--honey); display: grid; place-items: center; color: var(--paper); font-size: 15px; font-weight: 500; flex: none; }
      .gr { font-family: var(--serif); font-style: italic; font-size: 14px; line-height: 1.2; max-width: 11em; }
      .p-tabs { position: absolute; left: 14px; right: 14px; bottom: 14px; height: 50px; border-radius: 999px; background: var(--paper); box-shadow: 0 6px 14px rgba(42, 36, 29, 0.08), 0 0 0 1px var(--hair); display: flex; align-items: center; justify-content: space-between; padding: 0 5px; font-size: 12px; font-weight: 500; }
      .p-tabs span { flex: 1; text-align: center; }
      .p-tabs b { flex: none; background: var(--ink); color: var(--paper); border-radius: 999px; padding: 0 16px; height: 40px; display: grid; place-items: center; font-weight: 500; }
      .p-whisper { margin-top: 26px; font-size: 28px; line-height: 1.08; letter-spacing: -0.045em; max-width: 9em; }
      .p-label { margin-top: 26px; font-weight: 500; font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink2); }
      .p-orb { position: absolute; left: 50%; top: 58%; width: 62%; aspect-ratio: 1; margin: -31% 0 0 -31%; border: 0; padding: 0; background: none; cursor: pointer; border-radius: 50%; }
      .p-orb .orb { --size: 100%; width: 100%; height: 100%; }
      .p-grow { position: absolute; left: 50%; top: 58%; width: 62%; aspect-ratio: 1; margin: -31% 0 0 -31%; transform: scale(0.0001); pointer-events: none; z-index: 1; }
      .p-grow .orb { --size: 100%; width: 100%; height: 100%; }
      .p-wash { position: absolute; inset: 0; z-index: 2; opacity: 0; pointer-events: none; background: linear-gradient(180deg, color-mix(in srgb, var(--olive) 100%, var(--paper)) 0%, color-mix(in srgb, var(--paper) 22%, var(--olive)) 38%, color-mix(in srgb, var(--paper) 78%, var(--olive)) 72%, var(--paper) 100%); transition: opacity 1.1s var(--ease-out) 0.35s; }
      .p-open { position: absolute; inset: 0; z-index: 3; padding: 66px 22px 22px; display: flex; flex-direction: column; opacity: 0; pointer-events: none; color: var(--paper); }
      .p-meta { font-weight: 500; font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase; opacity: 0; transition: opacity 0.8s var(--ease-out) 0.9s; }
      .p-quote { margin-top: 26px; padding: 20px 20px 18px; border-radius: 22px; background: rgba(255, 254, 248, 0.2); border: 1px solid rgba(255, 254, 248, 0.5); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); font-family: var(--serif); font-style: italic; font-size: 19px; line-height: 1.4; }
      .p-quote span { display: block; opacity: 0; transform: translateY(6px); transition: opacity 0.9s var(--ease-out), transform 0.9s var(--ease-out); }
      .p-play { margin: 22px 0 0 2px; width: 52px; height: 52px; border-radius: 50%; border: 1.5px solid rgba(255, 254, 248, 0.9); background: rgba(255, 254, 248, 0.2); display: grid; place-items: center; opacity: 0; transition: opacity 0.8s var(--ease-out) 1.0s; }
      .p-play i { width: 0; height: 0; border-left: 13px solid var(--paper); border-top: 8px solid transparent; border-bottom: 8px solid transparent; margin-left: 4px; }
      .p-reply { margin-top: auto; background: var(--paper); color: var(--ink); border-radius: 20px; padding: 16px 18px; display: flex; align-items: center; justify-content: space-between; gap: 12px; font-size: 15px; opacity: 0; transform: translateY(10px); transition: opacity 0.9s var(--ease-out), transform 0.9s var(--ease-out); }
      .p-reply b { width: 38px; height: 38px; border-radius: 50%; background: var(--ink); color: var(--paper); display: grid; place-items: center; font-weight: 300; font-size: 18px; }
      .p-close { position: absolute; top: 18px; right: 18px; z-index: 5; width: 44px; height: 44px; border: 0; border-radius: 50%; background: none; color: var(--paper); font-size: 24px; line-height: 1; cursor: pointer; opacity: 0; pointer-events: none; transition: opacity 0.6s var(--ease-out) 0.9s; }
      /* Opened */
      .phone[data-state="open"] .p-idle { opacity: 0; pointer-events: none; }
      .phone[data-state="open"] .p-grow { transform: scale(9); transition: transform 1.3s var(--ease-out); }
      .phone[data-state="open"] .p-wash { opacity: 1; }
      .phone[data-state="open"] .p-open { opacity: 1; pointer-events: auto; transition: opacity 0.4s 0.5s; }
      .phone[data-state="open"] .p-meta, .phone[data-state="open"] .p-play { opacity: 1; }
      .phone[data-state="open"] .p-close { opacity: 1; pointer-events: auto; }
      .phone[data-state="open"] .p-quote span { opacity: 1; transform: none; }
      .phone[data-state="open"] .p-quote span:nth-child(1) { transition-delay: 1.3s; }
      .phone[data-state="open"] .p-quote span:nth-child(2) { transition-delay: 2.5s; }
      .phone[data-state="open"] .p-quote span:nth-child(3) { transition-delay: 3.7s; }
      .phone[data-state="open"] .p-reply { opacity: 1; transform: none; transition-delay: 4.6s; }
      .phone[data-state="closing"] .p-grow { transition: transform 0.7s var(--ease-out); }
      .p-orb:focus-visible { outline-offset: 6px; }

      /* ── The app, one screen at a time ───────────────────────────── */
      .tour-head { max-width: 760px; }
      .rows { margin-top: clamp(56px, 8vw, 104px); display: grid; gap: clamp(72px, 10vw, 128px); }
      .row { display: grid; gap: 40px; align-items: center; }
      @media (min-width: 900px) { .row { grid-template-columns: 1fr 1fr; gap: 96px; } .row.flip .copy { order: 2; } }
      .row .copy p { margin-top: 20px; color: var(--ink2); max-width: 26em; font-size: 19px; }
      .screen { width: min(320px, 78vw); margin-inline: auto; border-radius: 44px; overflow: hidden; box-shadow: 0 26px 60px rgba(42, 36, 29, 0.16), 0 8px 18px rgba(42, 36, 29, 0.08), 0 0 0 1px var(--hair); background: var(--cream); }
      .screen img { width: 100%; height: auto; }


      /* ── Screens built in code from the app's own design ─────────── */
      .screen.mock { aspect-ratio: 1206 / 2622; position: relative; container-type: inline-size; background: var(--cream); }
      .m-status { position: absolute; left: 0; right: 0; top: 0; height: 16cqw; display: flex; align-items: center; padding: 2cqw 9cqw 0; font-weight: 500; font-size: 4.4cqw; }
      .m-status i { position: absolute; left: 50%; top: 3.8cqw; width: 28.6cqw; height: 8.4cqw; margin-left: -14.3cqw; border-radius: 99px; background: #0b0a09; }
      .m-eyebrow { position: absolute; left: 0; right: 0; top: 29cqw; text-align: center; font-weight: 500; font-size: 3.3cqw; letter-spacing: 0.12em; text-transform: uppercase; }
      .m-title { position: absolute; left: 8cqw; right: 8cqw; top: 38cqw; text-align: center; font-family: var(--serif); font-size: 8.1cqw; line-height: 1.12; text-wrap: balance; }
      .screen.compose { background: linear-gradient(180deg, #e2a75a 0%, #e8bb82 45%, #ebcc9f 100%); }
      .m-print { position: absolute; left: 14.5cqw; right: 14.5cqw; top: 76cqw; background: var(--paper); padding: 2.8cqw; border-radius: 1cqw; box-shadow: 0 2cqw 5cqw rgba(42, 36, 29, 0.14); }
      .m-print img { width: 100%; aspect-ratio: 1; object-fit: cover; }
      .m-field { position: absolute; left: 14.5cqw; right: 14.5cqw; top: 153cqw; padding: 3.3cqw 4cqw; text-align: center; border: 0.35cqw solid rgba(42, 36, 29, 0.75); border-radius: 2cqw; background: rgba(255, 254, 248, 0.36); font-family: var(--serif); font-style: italic; font-size: 4.2cqw; line-height: 1.25; text-wrap: balance; }
      .m-send { position: absolute; left: 25cqw; right: 25cqw; top: 177cqw; height: 13.4cqw; border-radius: 99px; background: var(--ink); color: var(--paper); display: grid; place-items: center; font-weight: 500; font-size: 5.2cqw; }
      .m-pick { position: absolute; left: 0; right: 0; top: 196cqw; text-align: center; font-weight: 500; font-size: 4cqw; }
      .screen.recv { background: linear-gradient(180deg, #87995b 0%, color-mix(in srgb, var(--paper) 22%, var(--olive)) 38%, color-mix(in srgb, var(--paper) 78%, var(--olive)) 72%, var(--paper) 100%); color: var(--ink); }
      .recv .m-status { color: var(--paper); }
      .m-x { position: absolute; right: 6.5cqw; top: 22cqw; color: var(--paper); font-size: 9cqw; line-height: 1; font-weight: 300; }
      .m-meta { position: absolute; left: 8cqw; right: 8cqw; top: 40cqw; color: var(--paper); font-weight: 500; font-size: 3.1cqw; letter-spacing: 0.12em; text-transform: uppercase; }
      .m-photo { position: absolute; left: 8cqw; right: 8cqw; top: 50cqw; border-radius: 3cqw; overflow: hidden; box-shadow: 0 2cqw 6cqw rgba(42, 36, 29, 0.18); }
      .m-photo img { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; }
      .m-line { position: absolute; left: 8cqw; right: 8cqw; top: 163cqw; font-family: var(--serif); font-style: italic; font-size: 5.4cqw; }
      .m-reply { position: absolute; left: 6cqw; right: 6cqw; bottom: 9cqw; height: 16cqw; border-radius: 5cqw; background: var(--paper); box-shadow: 0 1cqw 3cqw rgba(42, 36, 29, 0.08); display: flex; align-items: center; justify-content: space-between; padding: 0 3.5cqw 0 5cqw; font-size: 4.2cqw; }
      .m-reply b { width: 10cqw; height: 10cqw; border-radius: 50%; background: var(--ink); color: var(--paper); display: grid; place-items: center; font-weight: 300; font-size: 5cqw; }
      /* Memory's entry screen, to Lola's own canvas (440 wide): the same
         title, the same three slots and rotations, the same polaroid. */
      .mem { --u: calc(100cqw / 440); }
      .m-av { position: absolute; left: calc(var(--u) * 24); top: calc(var(--u) * 77); width: calc(var(--u) * 50); height: calc(var(--u) * 50); border-radius: 50%; background: var(--honey); box-shadow: 0 0 0 calc(var(--u) * 2) var(--cream), 0 0 0 calc(var(--u) * 4) var(--honey); display: grid; place-items: center; color: var(--paper); font-size: calc(var(--u) * 20); font-weight: 500; }
      .mem-title { left: calc(var(--u) * 24); right: calc(var(--u) * 24); top: calc(var(--u) * 170); font-size: calc(var(--u) * 38); line-height: 1.1; }
      .mem-sub { position: absolute; left: 0; right: 0; top: calc(var(--u) * 282); text-align: center; font-family: var(--serif); font-style: italic; font-size: calc(var(--u) * 19); padding: 0 calc(var(--u) * 24); }
      .print { position: absolute; width: calc(var(--u) * 231); padding: calc(var(--u) * 14) calc(var(--u) * 13) calc(var(--u) * 43); background: #e8eae7; border-radius: calc(var(--u) * 2); box-shadow: 0 calc(var(--u) * 8) calc(var(--u) * 20) rgba(42, 36, 29, 0.14), 0 calc(var(--u) * 1) calc(var(--u) * 3) rgba(42, 36, 29, 0.12); transform: rotate(var(--r)); }
      .print img { width: 100%; aspect-ratio: 1; object-fit: cover; }
      .p3 { --r: 5deg; left: calc(var(--u) * (295.7 - 115.5)); top: calc(var(--u) * (510.8 - 134.9)); }
      .p2 { --r: -5deg; left: calc(var(--u) * (147.3 - 115.5)); top: calc(var(--u) * (560.1 - 134.9)); }
      .p1 { --r: 0deg; left: calc(var(--u) * (218 - 115.5)); top: calc(var(--u) * (653.05 - 134.9)); }
      .js .mem .print { opacity: 0; translate: 0 -3cqw; transition: opacity 1s var(--ease-out), translate 1.1s var(--ease-out); }
      .js .mem.in .print { opacity: 1; translate: 0 0; }
      .js .mem.in .p2 { transition-delay: 0.45s; } .js .mem.in .p1 { transition-delay: 0.9s; }
      /* Sharing: the sky that arrived, and a photo going out with its line. */
      .pair { position: relative; width: min(430px, 90vw); aspect-ratio: 100 / 150; margin-inline: auto; }
      .pair .screen { position: absolute; width: 62%; margin: 0; }
      .pair .back { right: 0; top: 0; }
      .pair .front { left: 0; top: 14%; }
      .pair .screen { transform: none; }

      /* ── Things to do ─────────────────────────────────────────────── */
      .things-head { max-width: 720px; }
      .cards { margin-top: 56px; display: grid; gap: 16px; grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr)); }
      .card { background: var(--paper); border-radius: 14px; padding: 26px 26px 28px; display: flex; flex-direction: column; justify-content: space-between; gap: 34px; min-height: 176px; box-shadow: 0 6px 14px rgba(42, 36, 29, 0.07), 0 0 0 1px var(--hair); }
      .card .eyebrow { margin: 0; font-size: 10px; letter-spacing: 0.12em; }
      .card h4 { font-size: 24px; }
      .arrow { align-self: flex-end; margin-top: -8px; width: 40px; height: 40px; border-radius: 50%; background: var(--ink); color: var(--paper); display: grid; place-items: center; font-size: 17px; }
      .card-foot { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; }

      /* ── Quiet on purpose ─────────────────────────────────────────── */
      .quiet-grid { margin-top: 72px; display: grid; gap: 0; }
      .q { padding: 28px 0; border-top: 1px solid rgba(244, 239, 231, 0.16); }
      .q .eyebrow { color: var(--cream); margin-bottom: 10px; }
      .q p { color: rgba(244, 239, 231, 0.72); max-width: 22em; font-size: 17px; }
      @media (min-width: 900px) { .quiet-grid { grid-template-columns: repeat(4, 1fr); gap: 36px; } .q { border-top: 0; padding: 0; } }

      /* ── For whom ─────────────────────────────────────────────────── */
      .who-grid { margin-top: 56px; display: grid; gap: 0; }
      .who { padding: 0; }
      .who .photo { margin-bottom: 26px; }
      .who .photo img { aspect-ratio: 4 / 5; object-fit: cover; }
      .who h4 { margin-bottom: 10px; }
      .who p { color: var(--ink2); max-width: 24em; }
      @media (min-width: 900px) { .who-grid { grid-template-columns: repeat(3, 1fr); gap: 56px; } }

      /* ── Free to start ────────────────────────────────────────────── */
      .free-grid { display: grid; gap: 48px; }
      @media (min-width: 900px) { .free-grid { grid-template-columns: 5fr 7fr; gap: 96px; } }
      .free-list { display: grid; gap: 0; }
      .free-item { padding: 26px 0; border-top: 1px solid var(--line); }
      .free-item:first-child { border-top: 0; padding-top: 0; }
      .free-item h4 { margin-bottom: 8px; }
      .free-item p { color: var(--ink2); max-width: 32em; }

      /* ── Why ──────────────────────────────────────────────────────── */
      .why-body { max-width: 680px; margin-top: 44px; display: grid; gap: 22px; font-size: clamp(19px, 1.9vw, 22px); line-height: 1.6; }
      .why-turn { margin-top: 64px; position: relative; max-width: 820px; }
      .why-turn blockquote { margin: 0; font-family: var(--serif); font-style: italic; font-size: clamp(30px, 4.2vw, 52px); line-height: 1.2; text-wrap: balance; }
      .doodle { width: 74px; height: auto; opacity: 0.85; }
      .doodles { display: flex; gap: 26px; align-items: flex-end; margin-bottom: 28px; }
      .draws { clip-path: inset(0 100% 0 0); transition: clip-path 1.1s var(--ease-out); }
      .draws.in { clip-path: inset(0 0 0 0); }
      .why-photo { margin-top: 72px; border-radius: 4px; overflow: hidden; max-height: 460px; }
      .why-photo img { width: 100%; height: 460px; object-fit: cover; object-position: 50% 40%; }

      /* ── Questions ────────────────────────────────────────────────── */
      .faq { margin-top: 56px; max-width: 820px; }
      details { border-top: 1px solid var(--line); }
      details:last-child { border-bottom: 1px solid var(--line); }
      summary { list-style: none; cursor: pointer; padding: 24px 44px 24px 0; font-family: var(--serif); font-size: clamp(20px, 2.1vw, 24px); line-height: 1.3; position: relative; min-height: 44px; }
      summary::-webkit-details-marker { display: none; }
      summary::after { content: "+"; position: absolute; right: 4px; top: 50%; transform: translateY(-50%); font-family: var(--sans); font-weight: 300; font-size: 28px; color: var(--ink2); transition: transform 0.4s var(--ease-out); }
      details[open] summary::after { transform: translateY(-50%) rotate(45deg); }
      details > div { padding: 0 44px 28px 0; color: var(--ink2); max-width: 36em; }

      /* ── The last ask ─────────────────────────────────────────────── */
      .finale { text-align: center; padding-block: clamp(96px, 13vw, 180px); overflow: hidden; }
      .finale .wordmark { height: 44px; margin: 0 auto 48px; animation: none; }
      .finale h2 { max-width: 14em; margin-inline: auto; }
      .finale .cta { margin-top: 44px; display: flex; flex-direction: column; align-items: center; }
      .finale form.wl .btn { background: var(--cream); color: var(--ink); }
      .finale .orb-bg { position: absolute; border-radius: 50%; pointer-events: none; }

      /* ── Footer ───────────────────────────────────────────────────── */
      footer { background: var(--ink); color: rgba(244, 239, 231, 0.62); padding: 0 0 36px; font-size: 14px; }
      .foot { border-top: 1px solid rgba(244, 239, 231, 0.16); padding-top: 26px; display: flex; flex-wrap: wrap; gap: 8px 22px; align-items: center; justify-content: space-between; }
      .foot a { color: inherit; text-decoration: none; padding: 10px 0; display: inline-block; }
      .foot a:hover { color: var(--cream); }
      .foot .links2 { display: flex; flex-wrap: wrap; gap: 4px 22px; align-items: center; }
      footer .lang button { color: rgba(244, 239, 231, 0.62); }
      footer .lang button[aria-pressed="true"] { color: var(--cream); }
      footer .lang .sep { background: rgba(244, 239, 231, 0.2); }

      /* ── Reveal: a quiet settle, only for what is below the fold ── */
      .js .rv { opacity: 0; transform: translateY(18px); transition: opacity 0.9s var(--ease-out), transform 0.9s var(--ease-out); transition-delay: var(--d, 0s); }
      .js .rv.in { opacity: 1; transform: none; }
      
      @media (prefers-reduced-motion: reduce) {
        html { scroll-behavior: auto; }
        *, *::before, *::after { animation-duration: 0.001ms !important; animation-delay: 0s !important; animation-iteration-count: 1 !important; transition-duration: 0.001ms !important; transition-delay: 0s !important; }
        .home p { opacity: 1; }
        .light { display: none; }
      }
    </style>
  </head>
  <body>
    <a class="skip" href="#main">[[Skip to content ||| Saltar al contenido]]</a>

    <header class="top" id="top">
      <div class="wrap bar">
        <a href="/" id="home" aria-label="Nidi">@@WORDMARK@@</a>
        <nav class="links" aria-label="[[Sections ||| Secciones]]">
          <a href="#how">[[How it works ||| Cómo funciona]]</a>
          <a href="#who">[[Who it is for ||| Para quién]]</a>
          <a href="#why">[[Why ||| Por qué]]</a>
          <a href="#questions">[[Questions ||| Preguntas]]</a>
        </nav>
        <nav class="lang" aria-label="Language">
          <button type="button" data-lang="en" lang="en" aria-pressed="true">EN</button>
          <span class="sep" aria-hidden="true"></span>
          <button type="button" data-lang="es" lang="es" aria-pressed="false">ES</button>
        </nav>
        <a class="btn btn-sm soon-only" href="#start">[[Stay close. ||| Avisame.]]</a>
        <a class="btn btn-sm live-only" href="@@STORE@@">[[Take a look ||| Mirá cómo es]]</a>
      </div>
    </header>

    <main id="main">

      <!-- 1. HERO ───────────────────────────────────────────────── -->
      <section class="hero" id="start">
        <div class="light" aria-hidden="true"></div>
        <div class="wrap hero-grid">
          <div>
            <p class="eyebrow">[[A shared space for two homes ||| Un espacio compartido entre dos casas]]</p>
            <h1>[[Grow close. From&nbsp;*anywhere.* ||| Crecé cerca. Desde *donde&nbsp;estés.*]]</h1>
            <p class="lead">[[Nidi connects two homes: the one where a child is growing up, and one far away. Made for children from 0 to 6: a few small things a day, kept in one quiet place. ||| Nidi une dos casas: la donde crece un niño o una niña, y una que está lejos. Pensada para chicos de 0 a 6 años: algunas cosas chicas por día, guardadas en un solo lugar tranquilo.]]</p>
            <div class="cta">
              @@FORM:hero@@
            </div>
          </div>
          <div class="homes" aria-label="[[Two homes, two skies ||| Dos casas, dos cielos]]">
            <div class="home home-a drifts-a">
              <div class="orb on-cream breathes"></div>
              <p>[[Mid morning for Bea in Buenos&nbsp;Aires. ||| Media mañana para Bea en Buenos&nbsp;Aires.]]</p>
            </div>
            <div class="home home-b drifts-b">
              <p>[[Mid afternoon for Teo in Madrid. ||| Es media tarde para Teo en Madrid.]]</p>
              <div class="orb on-cream lav breathes" style="animation-delay: -1.1s"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. THREE PILLARS ──────────────────────────────────────── -->
      <section class="pillars" aria-label="[[What Nidi is ||| Qué es Nidi]]">
        <div class="wrap pillar-grid">
          <div class="pillar rv"><p class="eyebrow">[[Voice, photo and text ||| Voz, foto y texto]]</p><p>[[A few things a day. Nothing to scroll, nothing to keep up with. ||| Algunas cosas por día. Nada para scrollear, nada que seguir.]]</p></div>
          <div class="pillar rv" style="--d:.12s"><p class="eyebrow">[[Only your family ||| Solo tu familia]]</p><p>[[What you share is seen by the people in your nidi, and no one else. No ads. ||| Lo que compartís lo ven las personas de tu nidi, y nadie más. Sin publicidad.]]</p></div>
          <div class="pillar rv" style="--d:.24s"><p class="eyebrow">[[Free to start ||| Gratis para empezar]]</p><p>[[Two free weeks, no payment details needed. ||| Dos semanas gratis, sin necesidad de medio de pago.]]</p></div>
        </div>
      </section>

      <!-- 2b. HER WORDS ────────────────────────────────────────── -->
      <section class="bg-cream stand" id="words">
        <div class="wrap">
          <blockquote class="rv">[[Growing up far apart does not mean growing&nbsp;apart. ||| Crecer lejos no significa crecer&nbsp;distanciados.]]</blockquote>
        </div>
      </section>

      <!-- 3. THE MOMENT ─────────────────────────────────────────── -->
      <section class="bg-paper" id="moment">
        <div class="wrap split">
          <div class="photo rv"><img src="/assets/photos/hands-hold.jpg" width="1600" height="1067" loading="lazy" alt="" /></div>
          <div>
            <p class="eyebrow rv">[[The moment ||| El momento]]</p>
            <h2 class="rv">[[Video calls with a baby don't&nbsp;*work.* ||| Las videollamadas con un bebé no&nbsp;*funcionan.*]]</h2>
            <div class="scenes">
              <div class="scene rv"><p class="eyebrow">[[Far away ||| Lejos]]</p><p>[[A grandmother an ocean away, who still wants to say good morning. ||| Una abuela al otro lado del océano, que igual quiere dar los buenos días.]]</p></div>
              <div class="scene rv"><p class="eyebrow">[[Travelling ||| De viaje]]</p><p>[[A parent away for work, who wants to be part of today and not only call at the end of it. ||| Un papá o una mamá de viaje por trabajo, que quiere ser parte del día y no solo llamar al final.]]</p></div>
              <div class="scene rv"><p class="eyebrow">[[Another city ||| Otra ciudad]]</p><p>[[An aunt, an uncle, a godparent: someone who loves the child and lives somewhere else. ||| Una tía, un tío, un padrino: alguien que quiere al niño o a la niña y vive en otro lugar.]]</p></div>
            </div>
            <p class="resolve rv">[[Nidi gives them something small to do together, every day: apart, but together. ||| Nidi les da algo chico para hacer todos los días: cada uno en su casa, y juntos.]]</p>
          </div>
        </div>
      </section>

      <!-- 4. HOW IT WORKS ───────────────────────────────────────── -->
      <section class="bg-cream" id="how">
        <div class="wrap split flip">
          <div class="photo tall rv"><img src="/assets/photos/hands-flour.jpg" width="1000" height="1896" loading="lazy" alt="" /></div>
          <div>
            <p class="eyebrow rv">[[How it works ||| Cómo funciona]]</p>
            <h2 class="rv">[[Three steps, and then it's&nbsp;*every day.* ||| Tres pasos, y después es&nbsp;*todos los días.*]]</h2>
            <div class="steps">
              <div class="step rv"><p class="eyebrow">[[First ||| Primero]]</p><h3>[[Start your nidi ||| Empezá tu nidi]]</h3><p>[[Tell Nidi a little about yourself and the child, and pick the colour that will stand for you. ||| Contale a Nidi un poco sobre vos y sobre el niño o la niña, y elegí el color que va a ser tuyo.]]</p></div>
              <div class="step rv"><p class="eyebrow">[[Then ||| Después]]</p><h3>[[Invite the other home ||| Invitá a la otra casa]]</h3><p>[[Send an invitation to someone far away. They join free and never pay for it. ||| Mandá una invitación a alguien que está lejos. Entra gratis y nunca paga por esto.]]</p></div>
              <div class="step rv"><p class="eyebrow">[[Every day ||| Todos los días]]</p><h3>[[Do something small ||| Hagan algo chico]]</h3><p>[[A good morning in a grandmother's voice. The same sky, photographed in two places. A recipe cooked in both kitchens. ||| Un buen día con la voz de una abuela. El mismo cielo, fotografiado en dos lugares. Una receta cocinada en las dos cocinas.]]</p></div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5. ARRIVAL: the signature moment, playable ────────────── -->
      <section class="arrival" id="arrival">
        <div class="wrap arrival-grid">
          <div>
            <p class="eyebrow rv">[[When something arrives ||| Cuando algo llega]]</p>
            <h2 class="rv">[[It arrives quietly. *Whenever you're ready.* ||| Llega sin hacer ruido. *Cuando quieras.*]]</h2>
            <p class="lead rv">[[There is no badge, no feed, no pressure. A soft orb in the colour of the person who sent it breathes until you open it. Then their colour fills the room, and their words arrive. ||| Sin globitos rojos, sin feed, sin apuro. Una esfera suave, del color de quien la mandó, respira hasta que la abrís. Entonces su color llena la pantalla y llegan sus palabras.]]</p>
            <p class="hint rv">[[Try it: touch the orb. ||| Probalo: tocá la esfera.]]</p>
          </div>
          <div class="phone rv" id="phone" data-state="idle">
            <div class="p-idle">
              <div class="p-status" aria-hidden="true"><span>15:03</span><i></i></div>
              <div class="p-greet"><span class="av" aria-hidden="true">A</span><span class="gr">[[Good afternoon, Ana. ||| Buenas tardes, Ana.]]</span></div>
              <p class="p-whisper">[[Mid morning for Bea in Buenos Aires. ||| Media mañana para Bea en Buenos Aires.]]</p>
              <p class="p-label">[[Something arrived for you ||| Algo llegó para vos]]</p>
              <div class="p-tabs" aria-hidden="true"><b>[[Today ||| Hoy]]</b><span>[[Activities ||| Actividades]]</span><span>[[Memory ||| Recuerdos]]</span></div>
            </div>
            <div class="p-grow" aria-hidden="true"><div class="orb"></div></div>
            <button class="p-orb" id="orbBtn" type="button" aria-label="[[Open what Bea sent ||| Abrir lo que mandó Bea]]" aria-expanded="false"><div class="orb breathes"></div></button>
            <div class="p-wash" aria-hidden="true"></div>
            <div class="p-open" id="pOpen" aria-hidden="true">
              <p class="p-meta">[[From Bea · Today at 3:03 PM ||| De Bea · Hoy a las 15:03]]</p>
              <div class="p-quote" aria-live="polite">
                <span>[[Good morning, love. ||| Buen día, mi amor.]]</span>
                <span>[[The sun came out here, ||| Salió el sol acá,]]</span>
                <span>[[so I thought of you. ||| y me acordé de vos.]]</span>
              </div>
              <div class="p-play" aria-hidden="true"><i></i></div>
              <div class="p-reply"><span>[[Whenever you're ready, reply. ||| Cuando quieras, contestale.]]</span><b aria-hidden="true">→</b></div>
            </div>
            <button class="p-close" id="closeBtn" type="button" aria-label="[[Close ||| Cerrar]]" tabindex="-1">×</button>
          </div>
        </div>
      </section>

      <!-- 5b. LESS SCREEN ─────────────────────────────────────── -->
      <section class="bg-ink" id="less-screen">
        <div class="wrap split flip">
          <div class="photo rv"><img src="/assets/photos/child-garden.jpg" width="1400" height="934" loading="lazy" alt="" /></div>
          <div>
            <p class="eyebrow rv">[[Less screen, more together ||| Menos pantalla, más juntos]]</p>
            <h2 class="rv">[[Let children be&nbsp;*children.* ||| Dejemos que los chicos sean&nbsp;*chicos.*]]</h2>
            <p class="lead rv" style="margin-top: 28px; color: var(--cream)">[[We don't always have time for a call, and a baby or a toddler won't sit through one anyway. So Nidi asks for something else: do something small together, each in your own home, and share it afterwards. ||| No siempre hay tiempo para una llamada, y un bebé o un chiquito de dos años no se queda frente a una pantalla. Por eso Nidi propone otra cosa: hacer algo chico juntos, cada uno en su casa, y compartirlo después.]]</p>
            <p class="rv muted" style="margin-top: 22px; max-width: 30em">[[The screen carries it; the moment happens off it. Nidi is for the adults. The children keep doing what children do, with you, however far apart you are. ||| La pantalla lo lleva; el momento pasa afuera de ella. Nidi es para los adultos. Los chicos hacen lo que hacen los chicos, con vos, no importa la distancia.]]</p>
          </div>
        </div>
      </section>

      <!-- 6. THE APP ────────────────────────────────────────────── -->
      <section class="bg-paper" id="app">
        <div class="wrap">
          <div class="tour-head">
            <p class="eyebrow rv">[[Inside Nidi ||| Adentro de Nidi]]</p>
            <h2 class="rv">[[Calm, familiar, and made for the people who love the&nbsp;*same child.* ||| Tranquila, familiar, y hecha para quienes quieren al&nbsp;*mismo niño o niña.*]]</h2>
          </div>
          <div class="rows">
            <div class="row">
              <div class="copy"><p class="eyebrow rv">[[Today ||| Hoy]]</p><h3 class="rv">[[A line about the *other* home. ||| Una línea sobre la *otra* casa.]]</h3><p class="rv">[[Today opens with what it is like where they are: their time, their sky. Then, whenever you like, you send something from your day. ||| Hoy empieza con cómo es el día donde están ellos: su hora, su cielo. Y cuando quieras, mandás algo de tu día.]]</p></div>
              <div class="screen rv"><img lang="en" src="/assets/screens/en-ana-today-arrived.jpg" width="720" height="1566" loading="lazy" alt="Nidi's Today screen: a line about the other home, and a soft green orb waiting to be opened." /><img lang="es" src="/assets/screens/es-ana-today-arrived.jpg" width="720" height="1566" loading="lazy" alt="La pantalla Hoy de Nidi: una línea sobre la otra casa y una esfera verde esperando que la abras." /></div>
            </div>
            <div class="row flip">
              <div class="copy"><p class="eyebrow rv">[[Activities ||| Actividades]]</p><h3 class="rv">[[Small things, chosen for *their age.* ||| Cosas chicas, elegidas para *su edad.*]]</h3><p class="rv">[[From the first months to six years old. Some you do on your own, some are the same thing done in each home, and some are for your next call. ||| Desde los primeros meses hasta los seis años. Algunas son para hacer por tu cuenta, otras se hacen igual en cada casa y otras son para la próxima llamada.]]</p></div>
              <div class="screen rv"><img lang="en" src="/assets/screens/en-bea-activities.jpg" width="720" height="1566" loading="lazy" alt="Nidi's activities: cards such as Read the same page, with a label above each." /><img lang="es" src="/assets/screens/es-bea-activities.jpg" width="720" height="1566" loading="lazy" alt="Las actividades de Nidi: tarjetas como Leer la misma página, con una etiqueta arriba de cada una." /></div>
            </div>
            <div class="row">
              <div class="copy"><p class="eyebrow rv">[[Sharing ||| Compartir]]</p><h3 class="rv">[[A photo, a voice, or a few *words.* ||| Una foto, una voz o unas *palabras.*]]</h3><p class="rv">[[Voice notes in English or Spanish can arrive written out too, so the other home can read along. Whoever recorded sees the words before sending, and can correct them. ||| Los audios en español o en inglés pueden llegar también escritos, para que en la otra casa se puedan leer. Quien grabó ve las palabras antes de mandar y las puede corregir.]]</p></div>
              <div class="pair rv">
                <div class="screen mock recv back" role="img" aria-label="[[A photo from Bea of a sunny window with plants, with a line under it ||| Una foto de Bea de una ventana con sol y plantas, con una línea debajo]]">
                  <div class="m-status"><span>15:04</span><i></i></div>
                  <span class="m-x" aria-hidden="true">×</span>
                  <p class="m-meta">[[From Bea · Today at 3:03 PM ||| De Bea · Hoy a las 15:03]]</p>
                  <div class="m-photo"><img src="/assets/photos/recv-window.jpg" alt="" width="700" height="875" loading="lazy" /></div>
                  <p class="m-line">[[our window, this morning. ||| nuestra ventana, esta mañana.]]</p>
                  <div class="m-reply"><span>[[Whenever you're ready, reply. ||| Cuando quieras, contestale.]]</span><b aria-hidden="true">→</b></div>
                </div>
                <div class="screen mock compose front" role="img" aria-label="[[Sending a photo of a dog asleep in a sunny armchair, with a line written under it ||| Mandando la foto de una perra dormida en un sillón al sol, con una línea escrita debajo]]">
                  <div class="m-status"><span>15:24</span><i></i></div>
                  <p class="m-eyebrow">[[Anytime ||| Cuando quieras]]</p>
                  <p class="m-title">[[Anything you feel like sharing. ||| Lo que tengas ganas de compartir.]]</p>
                  <div class="m-print"><img src="/assets/photos/send-dog.jpg" alt="" width="520" height="520" loading="lazy" /></div>
                  <div class="m-field">[[Remy found the only sunny spot. ||| Remy encontró el único rincón con sol.]]</div>
                  <div class="m-send">[[Send ||| Enviar]]</div>
                  <p class="m-pick">[[Pick another ||| Elegir otra]]</p>
                </div>
              </div>
            </div>
            <div class="row flip">
              <div class="copy"><p class="eyebrow rv">[[Memory ||| Recuerdos]]</p><h3 class="rv">[[Everything lands in *Memory.* ||| Todo queda en *Recuerdos.*]]</h3><p class="rv">[[By date, from both homes: photos, voice notes and messages. Nothing gets deleted by accident, you can reply to any of it, and it stays with the family. ||| Por fecha, de las dos casas: fotos, audios y mensajes. Nada se borra sin querer, a todo le podés contestar, y se queda con la familia.]]</p></div>
              <div class="screen mock mem rv" role="img" aria-label="[[Memory: the moments worth keeping, three printed photos stacked one over another ||| Recuerdos: los momentos que vale la pena guardar, tres fotos impresas, una sobre otra]]">
                <div class="m-status"><span>15:21</span><i></i></div>
                <p class="m-title mem-title">[[The moments worth keeping ||| Los momentos que vale la pena guardar.]]</p>
                <p class="mem-sub">[[Take a look back at what you've shared ||| Lo que fueron guardando entre las dos casas.]]</p>
                <div class="m-av" aria-hidden="true">A</div>
                <div class="print p3"><img src="/assets/photos/mem-canal.jpg" alt="" width="520" height="780" loading="lazy" /></div>
                <div class="print p2"><img src="/assets/photos/mem-home.jpg" alt="" width="520" height="780" loading="lazy" /></div>
                <div class="print p1"><img src="/assets/photos/mem-sky.jpg" alt="" width="520" height="780" loading="lazy" /></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 8. QUIET ON PURPOSE (trust) ───────────────────────────── -->
      <section class="bg-ink" id="trust">
        <div class="wrap">
          <p class="eyebrow rv">[[Built for families ||| Hecha para familias]]</p>
          <h2 class="rv" style="max-width: 14em">[[Quiet on&nbsp;*purpose.* ||| Silenciosa a&nbsp;*propósito.*]]</h2>
          <div class="quiet-grid">
            <div class="q rv"><p class="eyebrow">[[Private ||| Privado]]</p><p>[[Photos and voice notes are stored privately: never public and never searchable. ||| Las fotos y los audios se guardan de forma privada: no son públicos ni aparecen en búsquedas.]]</p></div>
            <div class="q rv" style="--d:.1s"><p class="eyebrow">[[Calm ||| Tranquilo]]</p><p>[[No ads, no feed, no counting. A few things a day, and then it lets you go. ||| Sin publicidad, sin feed, sin contadores. Algunas cosas por día, y después te deja ir.]]</p></div>
            <div class="q rv" style="--d:.2s"><p class="eyebrow">[[Simple ||| Simple]]</p><p>[[You sign in with a code sent to your email. No password to remember. ||| Entrás con un código que te llega por email. Sin contraseña que recordar.]]</p></div>
            <div class="q rv" style="--d:.3s"><p class="eyebrow">[[Kept ||| Guardado]]</p><p>[[Everything you share is kept in Memory, by date, for the family. Nothing gets lost along the way. ||| Todo lo que compartís se guarda en Recuerdos, por fecha, para la familia. Nada se pierde en el camino.]]</p></div>
          </div>
        </div>
      </section>

      <!-- 9. WHO IT IS FOR ──────────────────────────────────────── -->
      <section class="bg-paper" id="who">
        <div class="wrap">
          <p class="eyebrow rv">[[Who it is for ||| Para quién es]]</p>
          <h2 class="rv" style="max-width: 15em">[[Two homes that love the same&nbsp;*child.* ||| Dos casas que quieren al mismo&nbsp;*niño o niña.*]]</h2>
          <div class="who-grid">
            <div class="who rv"><div class="photo"><img src="/assets/photos/who-home.jpg" width="900" height="1125" loading="lazy" alt="" /></div><h4>[[The home where they grow up ||| La casa donde crece]]</h4><p>[[Parents of children from 0 to 6 who want the people far away to be part of an ordinary day. Each home can have up to two adults. ||| Madres y padres de chicos de 0 a 6 años que quieren que quienes están lejos sean parte de un día cualquiera. En cada casa puede haber hasta dos personas adultas.]]</p></div>
            <div class="who rv" style="--d:.1s"><div class="photo"><img src="/assets/photos/who-far.jpg" width="900" height="1125" loading="lazy" alt="" /></div><h4>[[The home far away ||| La casa que está lejos]]</h4><p>[[Grandparents, aunts, uncles, godparents. Nothing to learn and nothing to keep up with: just a way to be there, in your own voice. ||| Abuelos, tíos, padrinos. Nada que aprender y nada que seguir: solo una forma de estar, con tu propia voz.]]</p></div>
            <div class="who rv" style="--d:.2s"><div class="photo"><img src="/assets/photos/who-many.jpg" width="900" height="1125" loading="lazy" alt="" /></div><h4>[[More than one nidi ||| Más de un nidi]]</h4><p>[[One person can be part of several nidis, say one with each side of the family. Everyone reads Nidi in their own language, English or Spanish. ||| Una misma persona puede tener más de un nidi, por ejemplo uno con cada lado de la familia. Cada persona usa Nidi en su idioma, español o inglés.]]</p></div>
          </div>
        </div>
      </section>

      <!-- 10. FREE TO START ─────────────────────────────────────── -->
      <section class="bg-cream" id="free">
        <div class="wrap free-grid">
          <div>
            <p class="eyebrow rv">[[Free to start ||| Gratis para empezar]]</p>
            <h2 class="rv">[[Try it for two weeks, with nothing to&nbsp;*set up.* ||| Probala dos semanas, sin nada que&nbsp;*configurar.*]]</h2>
          </div>
          <div class="free-list">
            <div class="free-item rv"><h4>[[Two free weeks ||| Dos semanas gratis]]</h4><p>[[Your first nidi comes with two weeks, counted from the day the other home joins. No payment details are needed, and nothing is charged when it ends. ||| El primer nidi que empezás tiene dos semanas de prueba, que se cuentan desde el día en que entra la otra casa. No hace falta ningún medio de pago, y cuando terminan no se cobra nada.]]</p></div>
            <div class="free-item rv"><h4>[[Then, a subscription ||| Después, una suscripción]]</h4><p>[[To keep sharing, the person who started the nidi chooses a monthly or a yearly subscription. One covers up to three nidis. The options and prices are shown in the app, before anything is charged. ||| Para seguir compartiendo, quien empezó el nidi elige una suscripción mensual o anual. Una cubre hasta tres nidis. Las opciones y los precios se ven en la app, antes de que se cobre nada.]]</p></div>
            <div class="free-item rv"><h4>[[Only one person pays ||| Paga una sola persona]]</h4><p>[[The people you invite join free and never pay for it. ||| Las personas que invitás entran gratis y nunca pagan por esto.]]</p></div>
          </div>
        </div>
      </section>

      <!-- 11. WHY (Maru's own words) ────────────────────────────── -->
      <section class="bg-paper" id="why">
        <div class="wrap">
          <p class="eyebrow rv">[[Why Nidi exists ||| Por qué existe Nidi]]</p>
          <h2 class="rv">[[Why I made&nbsp;*Nidi.* ||| Por qué hice&nbsp;*Nidi.*]]</h2>
          <div class="why-body">
            <p class="rv">[[I'm an Argentine mother in the Netherlands. When my daughter was born, my parents were 11,000 km away, and video calls with a baby don't work. I wanted her to grow up knowing her grandparents' voices, their stories, the small things they do every day. Not just faces on a screen. So I built Nidi. ||| Soy una mamá argentina que vive en Holanda. Cuando nació mi hija, mis papás estaban a 11.000 kilómetros, y las videollamadas con un bebé no funcionan. Yo quería que creciera conociendo la voz de sus abuelos, sus historias, las cosas chiquitas que hacen todos los días. No solo caras en una pantalla. Entonces hice Nidi.]]</p>
            <p class="rv">[[Nidi connects two houses: the child's, and one far away. Every day it suggests small things to do, apart but together. A grandmother records a good morning in her voice. Both houses photograph the same sky, or cook the same recipe. The screen carries it; the moment happens off it. It all lands in Memory, an archive that stays with the&nbsp;family. ||| Nidi une dos casas: la del niño, y una que está en otro lugar. Todos los días propone cosas chicas para hacer, cada uno en su casa y los dos juntos. Una abuela graba un buen día con su voz. Las dos casas sacan una foto del mismo cielo, o cocinan la misma receta. La pantalla lo lleva; el momento pasa afuera de ella. Todo queda en Recuerdos, un archivo que se queda con la&nbsp;familia.]]</p>
            <p class="rv">[[Since we started testing, my parents have read my daughter bedtime stories, sung to her at breakfast, and left a good morning every day, recorded the night before in Buenos Aires. ||| Desde que empezamos a probarlo, mis papás le leyeron cuentos a mi hija antes de dormir, le cantaron en el desayuno, y le dejaron un buen día todos los días, grabado la noche anterior en Buenos Aires.]]</p>
          </div>
          <div class="why-turn">
            <div class="doodles" aria-hidden="true">
              <img class="doodle draws" src="/assets/doodles/doodle-22-sun.png" alt="" width="74" height="72" loading="lazy" />
              <img class="doodle draws" style="transition-delay:.5s" src="/assets/doodles/doodle-33-moon-stars.png" alt="" width="74" height="73" loading="lazy" />
            </div>
            <blockquote class="rv">[[My daughter is not yet two. She knows her grandparents' voices. ||| Mi hija todavía no cumplió dos. Conoce la voz de sus abuelos.]]</blockquote>
          </div>
        </div>
      </section>

      <!-- 12. QUESTIONS ─────────────────────────────────────────── -->
      <section class="bg-cream" id="questions">
        <div class="wrap">
          <p class="eyebrow rv">[[Questions ||| Preguntas]]</p>
          <h2 class="rv">[[A few things you might be&nbsp;*wondering.* ||| Lo que quizás te estés&nbsp;*preguntando.*]]</h2>
          <div class="faq rv">
            <details><summary>[[Is Nidi free? ||| ¿Nidi es gratis?]]</summary><div>[[The first nidi you start comes with two free weeks, with no payment details. After that, to keep sharing, the person who started it chooses a monthly or yearly subscription. ||| El primer nidi que empezás tiene dos semanas gratis, sin medio de pago. Después, para seguir compartiendo, quien lo empezó elige una suscripción mensual o anual.]]</div></details>
            <details><summary>[[Who pays? ||| ¿Quién paga?]]</summary><div>[[Only the person who starts a nidi. The people they invite join free and never pay for it. One subscription covers up to three nidis. ||| Solo quien empieza un nidi. Las personas que invita entran gratis y nunca pagan por esto. Una suscripción cubre hasta tres nidis.]]</div></details>
            <details><summary>[[Does the other home need the app? ||| ¿La otra casa necesita la app?]]</summary><div>[[Yes. They install Nidi, sign in with a code sent to their email, and join with your invitation. It is free for them. ||| Sí. Instalan Nidi, entran con un código que les llega por email y se suman con tu invitación. Para ellos es gratis.]]</div></details>
            <details><summary>[[Who can see what we share? ||| ¿Quién ve lo que compartimos?]]</summary><div>[[Only the people in your nidi. Photos and voice notes are stored privately, never public and never searchable. ||| Solo las personas de tu nidi. Las fotos y los audios se guardan de forma privada: no son públicos ni aparecen en búsquedas.]]</div></details>
            <details><summary>[[What languages does it speak? ||| ¿En qué idiomas está?]]</summary><div>[[English and Spanish. Everyone reads Nidi in their own language, even inside the same nidi, and voice notes in either language can arrive written out. ||| En español y en inglés. Cada persona usa Nidi en su idioma, aunque estén en el mismo nidi, y los audios en cualquiera de los dos idiomas pueden llegar también escritos.]]</div></details>
            <details><summary>[[How old is the child? ||| ¿Qué edad tiene que tener el niño o la niña?]]</summary><div>[[Activities are chosen for the child's age, from the first months to six years old. Up to age three, the home where the child lives also has a place to keep their firsts. ||| Las actividades se eligen según la edad, desde los primeros meses hasta los seis años. Y hasta los tres años, la casa donde crece tiene un lugar para guardar las primeras veces.]]</div></details>
            <details><summary>[[What happens if we stop the subscription? ||| ¿Qué pasa si dejamos la suscripción?]]</summary><div>[[The nidi pauses for now, and nobody can add anything new. Everything already shared stays in Memory, and anyone in the nidi can still open it. You can manage or cancel a subscription at any time in your iPhone's Settings. ||| El nidi queda en pausa, por ahora, y nadie puede sumar nada nuevo. Todo lo que ya compartieron sigue en Recuerdos, y cualquiera del nidi puede abrirlo. La suscripción la manejás o la cancelás cuando quieras en Ajustes del iPhone.]]</div></details>
            <details><summary>[[Is there an Android version? ||| ¿Hay versión para Android?]]</summary><div>[[Not yet. Nidi comes first to iPhone, and Android is on its way. Leave your email and we will write when it is ready. ||| Todavía no. Nidi sale primero para iPhone, y Android viene en camino. Dejá tu email y te escribimos cuando esté listo.]]</div></details>
          </div>
        </div>
      </section>

      <!-- 13. THE LAST ASK ──────────────────────────────────────── -->
      <section class="bg-ink finale" id="join">
        <div class="wrap" style="position: relative">
          @@WORDMARK_CTA@@
          <h2 class="rv">[[Small moments can mean&nbsp;*everything.* ||| Los momentos chicos pueden ser&nbsp;*todo.*]]</h2>
          <div class="cta">
            @@FORM:end@@
          </div>
        </div>
      </section>
    </main>

    <footer>
      <div class="wrap foot">
        <div class="links2">
          <a id="privacy" href="/privacy/">[[Privacy ||| Privacidad]]</a>
          <a id="terms" href="/terms/">[[Terms ||| Términos]]</a>
          <a id="support" href="/support/">[[Support ||| Soporte]]</a>
          <span>BALK Creative Studio</span>
          <span>[[Photos via Unsplash and Pexels ||| Fotos de Unsplash y Pexels]]</span>
        </div>
        <nav class="lang" aria-label="Language">
          <button type="button" data-lang="en" lang="en" aria-pressed="true">EN</button>
          <span class="sep" aria-hidden="true"></span>
          <button type="button" data-lang="es" lang="es" aria-pressed="false">ES</button>
        </nav>
      </div>
    </footer>

    <script>
      // The endpoint is public by design: verify_jwt is false on the
      // function and its CORS is open, so no Supabase key is embedded.
      var ENDPOINT = "https://orqdnuikcdskmvorchly.supabase.co/functions/v1/path-c-waitlist";
      var T = {
        en: { title: "Nidi. Grow close. From anywhere.", placeholder: "Your email", invalid: "Check the email address.", failed: "We couldn't add you just now. Try again in a moment.", privacy: "/privacy/", terms: "/terms/", support: "/support/" },
        es: { title: "Nidi. Crecé cerca. Desde donde estés.", placeholder: "Tu email", invalid: "Revisá el email.", failed: "No pudimos anotarte ahora. Probá de nuevo en un momento.", privacy: "/privacidad/", terms: "/terminos/", support: "/soporte/" }
      };
      var lang = document.documentElement.getAttribute("data-l") === "es" ? "es" : "en";

      function setLang(next) {
        lang = next === "es" ? "es" : "en";
        var c = T[lang], d = document.documentElement;
        d.lang = lang; d.setAttribute("data-l", lang);
        document.title = c.title;
        document.querySelectorAll("form.wl input[type=email]").forEach(function (i) { i.placeholder = c.placeholder; });
        document.getElementById("privacy").href = c.privacy;
        document.getElementById("terms").href = c.terms;
        document.getElementById("support").href = c.support;
        document.querySelectorAll(".lang button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-lang") === lang ? "true" : "false"); });
        document.querySelectorAll(".wl-error[data-kind]").forEach(function (e) { e.textContent = c[e.dataset.kind]; });
        try { localStorage.setItem("nidi-lang", lang); } catch (e) {}
      }
      setLang(lang);
      document.querySelectorAll(".lang button").forEach(function (b) { b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); }); });

      // ── Email forms (hero and last ask) ───────────────────────────
      document.querySelectorAll("form.wl").forEach(function (form) {
        var wrap = form.parentElement, input = form.querySelector("input"), button = form.querySelector("button");
        var done = wrap.querySelector(".wl-done"), error = wrap.querySelector(".wl-error");
        function showError(kind) {
          error.dataset.kind = kind; error.textContent = T[lang][kind]; error.hidden = false;
          error.classList.toggle("sr-only", kind === "invalid");
          if (kind === "invalid") input.setAttribute("aria-invalid", "true");
        }
        form.addEventListener("submit", function (e) {
          e.preventDefault();
          var email = input.value.trim();
          if (!/^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[a-z]{2,}$/i.test(email)) { showError("invalid"); input.focus(); return; }
          error.hidden = true; input.removeAttribute("aria-invalid");
          button.disabled = true; input.disabled = true;
          fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: email, locale: lang, source: "landing" }) })
            .then(function (res) { if (!res.ok) throw new Error("http " + res.status); return res.json(); })
            .then(function (body) { if (!body || body.ok !== true) throw new Error("not ok"); form.hidden = true; done.hidden = false; })
            .catch(function () { button.disabled = false; input.disabled = false; showError("failed"); });
        });
        input.addEventListener("input", function () { if (input.getAttribute("aria-invalid") === "true") { input.removeAttribute("aria-invalid"); error.hidden = true; } });
      });

      // ── "Stay close." goes to the nearest email field ─────────────
      document.querySelectorAll('a.btn[href="#start"]').forEach(function (a) {
        a.addEventListener("click", function (e) {
          e.preventDefault();
          var nearTop = window.scrollY < window.innerHeight * 0.6;
          var input = document.getElementById(nearTop ? "email-hero" : "email-end");
          input.scrollIntoView({ behavior: "smooth", block: nearTop ? "center" : "center" });
          setTimeout(function () { input.focus({ preventScroll: true }); }, nearTop ? 50 : 650);
        });
      });

      // The logo goes to the very top, whatever the page is doing.
      document.getElementById("home").addEventListener("click", function (e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
        if (location.hash) history.replaceState(null, "", location.pathname + location.search);
      });

      // ── The orb, opened ───────────────────────────────────────────
      (function () {
        var phone = document.getElementById("phone"), orb = document.getElementById("orbBtn"),
            close = document.getElementById("closeBtn"), openPane = document.getElementById("pOpen");
        function set(state) {
          phone.setAttribute("data-state", state);
          var isOpen = state === "open";
          orb.setAttribute("aria-expanded", isOpen ? "true" : "false");
          openPane.setAttribute("aria-hidden", isOpen ? "false" : "true");
          close.tabIndex = isOpen ? 0 : -1;
        }
        orb.addEventListener("click", function () { set("open"); setTimeout(function () { close.focus({ preventScroll: true }); }, 600); });
        close.addEventListener("click", function () { set("closing"); setTimeout(function () { set("idle"); orb.focus({ preventScroll: true }); }, 50); });
      })();

      // ── Quiet reveals, only for what is below the fold ────────────
      (function () {
        var bar = document.querySelector("header.top");
        function onScroll() { bar.classList.toggle("scrolled", window.scrollY > 8); }
        window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
        if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
        var els = document.querySelectorAll(".rv, .draws");
        var h = window.innerHeight;
        document.documentElement.classList.add("js");
        els.forEach(function (el) { if (el.getBoundingClientRect().top < h * 0.92) el.classList.add("in"); });
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
        }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
        els.forEach(function (el) { if (!el.classList.contains("in")) io.observe(el); });
        // If the observer never fires (print, odd embeds), nothing stays hidden.
        setTimeout(function () { els.forEach(function (el) { el.classList.add("in"); }); }, 6000);
      })();
    </script>
    <!-- Arrivals: one count, no cookie, no identifier (2026-10-04). See
         the note on the previous version of this page in git history:
         the route and nothing else is sent, credentials are omitted so
         no vendor cookie is ever set, failures are swallowed. -->
    <script>
      (function () {
        try {
          var p = location.pathname;
          var body = JSON.stringify({ path: p.indexOf("/join/") === 0 ? "/join/:code" : p, referrer: document.referrer || null, lang: document.documentElement.lang === "es" ? "es" : "en" });
          fetch("https://orqdnuikcdskmvorchly.supabase.co/functions/v1/site-view", { method: "POST", headers: { "Content-Type": "application/json" }, body: body, credentials: "omit", keepalive: true, mode: "cors" }).catch(function () {});
        } catch (e) {}
      })();
    </script>
  </body>
</html>
'''

FORM = '''<div class="wl-wrap">
              <form class="wl soon-only" id="form-@@ID@@" novalidate>
                <label for="email-@@ID@@" class="sr-only">[[Your email ||| Tu email]]</label>
                <input id="email-@@ID@@" type="email" name="email" placeholder="Your email" autocomplete="email" inputmode="email" required />
                <button class="btn" type="submit">[[Stay close. ||| Avisame.]]</button>
              </form>
              <p class="wl-done" hidden role="status">[[You're in. We'll write when Nidi is ready. ||| Listo. Te escribimos cuando Nidi esté disponible.]]</p>
              <p class="wl-error" hidden role="alert"></p>
              <p class="wl-note soon-only">[[Coming soon to the App Store, for iPhone. Android is on its way. Free for two weeks. ||| Muy pronto en el App Store, para iPhone. Android viene en camino. Dos semanas gratis.]]</p>
              <a class="btn live-only" href="@@STORE@@">[[Take a look ||| Mirá cómo es]]</a>
              <p class="wl-note live-only">[[On the App Store, for iPhone. Free for two weeks. ||| En el App Store, para iPhone. Dos semanas gratis.]]</p>
            </div>'''

# Redirects: the old Why pages now live inside the home page.
REDIRECT = '''<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <title>Nidi</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="robots" content="noindex" />
    <link rel="canonical" href="https://nidi.life/" />
    <meta http-equiv="refresh" content="0; url=/?lang={lang}#why" />
    <script>location.replace("/?lang={lang}#why");</script>
  </head>
  <body style="background:#fffef8;font-family:sans-serif"><p><a href="/?lang={lang}#why">nidi.life</a></p></body>
</html>
'''


def pair(m):
    en, es = m.group(1).strip(), m.group(2).strip()
    return f'<span lang="en">{en}</span><span lang="es">{es}</span>'


def italics(s):
    return re.sub(r'\*(.+?)\*', r'<em>\1</em>', s)


def expand(html):
    # Attribute values cannot hold spans: those pairs are English-first
    # defaults the script swaps (aria-labels) or are written per language.
    def attr(m):
        return f'{m.group(1)}="{m.group(2).split("|||")[0].strip()}"'
    html = re.sub(r'((?:aria-label|alt))="\[\[(.*?)\]\]"', attr, html)
    html = re.sub(r'\[\[(.*?)\|\|\|(.*?)\]\]', lambda m: italics(pair(m)), html, flags=re.S)
    return html


def build():
    out = TEMPLATE
    for fid in ('hero', 'end'):
        out = out.replace(f'@@FORM:{fid}@@', FORM.replace('@@ID@@', fid))
    out = (out.replace('@@WORDMARK@@', WORDMARK)
              .replace('@@WORDMARK_CTA@@', WORDMARK_CTA)
              .replace('@@STORE@@', APP_STORE_URL)
              .replace('@@LIVE@@', 'true' if APP_LIVE else 'false'))
    out = expand(out)
    with open(os.path.join(ROOT, 'index.html'), 'w') as f:
        f.write(out)
    for folder, lang in (('why', 'en'), ('por-que', 'es')):
        with open(os.path.join(ROOT, folder, 'index.html'), 'w') as f:
            f.write(REDIRECT.format(lang=lang))
    print('wrote index.html', len(out), 'bytes; why and por-que now redirect')


if __name__ == '__main__':
    build()

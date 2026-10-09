# nidi-web

[nidi.life](https://nidi.life): one long page that tells the story of Nidi
(hero, the moment, how it works, a playable "something arrived", the app,
things to do, trust, who it is for, free to start, Maru's Why, questions,
the last ask). English and Spanish on the same URL; `?lang=es` links to one.

No framework and no build step on the server: `index.html` is generated.

    python3 scripts/build-home.py

Copy lives in that script, written side by side as `[[ English ||| Español ]]`.
`APP_LIVE = False` keeps every call to action as the email form
(`path-c-waitlist`, MailerLite). On launch day set it to `True`, run the
script, and every button becomes "Take a look" on the App Store.
`/why/` and `/por-que/` are generated redirects to `/#why`.

The privacy, terms and support pages come from `scripts/build-legal.py` and
`scripts/build-support.py` and still read the wordmark out of `index.html`.

Fonts are self-hosted (`assets/fonts`) so no visitor's address is sent to a
font service; the site sets no cookies and stores only the language choice.

Served by GitHub Pages from `main`.

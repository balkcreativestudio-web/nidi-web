# nidi-web

The pre-launch page for [nidi.life](https://www.nidi.life).

One `index.html`, no framework, no build step. It exists to capture
email addresses before launch and does nothing else.

The form POSTs to the `path-c-waitlist` Supabase Edge Function, which
forwards the address to MailerLite. That function has `verify_jwt =
false` and open CORS, so no Supabase key is embedded in this page.

Served by GitHub Pages from `main`.

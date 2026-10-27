# Zayvori Web — Claude Code Context

Static marketing and legal website for **Zayvori**, the Android to-do app where tasks link into visual workflows (app repo: `../workflow-app`). Plain HTML, CSS and vanilla JS — no build step, deployed as-is. Same approach as the Damson Kitchen site (`../recipe-web`), which is the reference for conventions.

## File map

| File | Role |
|------|------|
| `index.html` | Home: hero (with an HTML mock-up of the To do view and a reminder notification), features, the map band (an inline SVG workflow map in the app's dark theme), how it works, privacy, "coming soon" |
| `privacy.html` | Privacy Policy. **Google Play requires its URL** for the listing |
| `404.html` | GitHub Pages serves it for any missing URL, at any depth — so it uses absolute `/` paths |
| `styles.css` | All styles. Brand tokens at the top as CSS custom properties |
| `script.js` | Mobile menu, the nav border once scrolled, fade-ins. Stores nothing |
| `assets/favicon.svg` | The Zayvori mark on its gradient tile. Also used as the nav and footer logo |
| `assets/apple-touch-icon.png`, `assets/og-image.png` | Rendered from the mark (180px; 1200×630 link preview) |
| `assets/fonts/` | Self-hosted Space Grotesk (headings) and Inter (body), Latin-subset woff2, SIL Open Font License |
| `CNAME`, `robots.txt`, `sitemap.xml` | Custom domain; crawl rules; page list — update `lastmod` and add `<url>` entries when pages change |

## Brand

- **Tokens are the app's exact values** (`workflow-app/src/theme.ts`): violet `#6A4DFF` → magenta `#C34DFF` gradient, mint `#2BD99F` ticks, done `#0FA97A`, ink `#12121F`, background `#F4F4F9`, dark `#0B0B13`. Change the app, change these.
- **The mark** (a white Z-shaped route between two mint "done" ticks) is the same geometry as the app icon (`workflow-app/scripts/make-icons.js`) and in-app `BrandMark.tsx`. Change one, change all.
- **Type:** Space Grotesk for names, headings and numbers; Inter for body. Self-hosted — never load from `fonts.googleapis.com` (it would send visitors' IPs to Google and break the privacy policy's no-third-parties line).
- **Ration the colour**, as the app does: gradient on primary buttons and the one highlighted word, violet for eyebrows and links, everything else neutral. The faint doodle pattern (`.doodles`) echoes the app's background pattern.
- **Voice:** plain, upbeat, practical. UK English. Talk about getting things done and knowing what's next — not productivity jargon. Use the app's own words for concepts (Ready, Waiting, Not needed, "any one is enough", Finish) — see `workflow-app/src/labels.ts`.

## What the app does (keep copy aligned)

Workflows from Start to Finish; tasks branch, run side by side and merge; "finish all of them" or "any one is enough" before a step; unneeded tasks are set aside automatically; **To do** view (ready now / coming up / done) and **Map** view; one-tap complete with Undo; due dates; reminders (due soon, due now, morning summary) with **Mark complete / Dismiss** on the notification; progress "x of y"; confetti on finish; light/dark/system theme; background pattern. **Everything on the phone: no account, no server, no sync, no analytics.**

Not features (don't claim): accounts, sync/backup to a cloud, sharing or collaboration, templates, repeating/looping tasks, iOS.

## No cookies, no analytics, no third parties

The site makes no third-party requests, which is what lets the privacy policy be one short page with no consent banner. Adding any tracker, embed or externally hosted asset changes the privacy policy — weigh that first.

## Launch state and open items

- **Pre-launch.** The app isn't on Google Play yet: the CTA is "Coming soon" with an email link. When it launches, swap the nav button, hero CTA and download card for the Play link (`https://play.google.com/store/apps/details?id=com.zayvori.workflow`).
- **The mock-up and map are illustrations, not screenshots.** Swap in real screenshots once there's a tidy demo workflow to capture.
- **`hello@zayvori.com` must exist** before launch — it's the contact in the privacy policy and the CTA.
- **Privacy policy "Who we are"** assumes the same setup as Damson Kitchen: an independent UK developer trading as Zayvori, no company. Confirm before submitting to Play. Not reviewed by a lawyer.

## Deployment

Intended for **GitHub Pages** (free, handles the domain and TLS): enable Pages on `main` in the repo settings; `CNAME` sets `zayvori.com`.

**zayvori.com currently serves the finance research tool** (behind Cloudflare). Before this site can go live there, that tool moves off the domain and DNS points at GitHub Pages (four `A` records for the apex plus `www` CNAME to `brent-jenkins.github.io`). If Cloudflare stays in front as a proxy, add Cloudflare to the privacy policy's "This website" section — it then also processes visitors' IP addresses.

## Previewing locally

Any static server from this folder works, e.g. `npx serve .` then open http://localhost:3000.

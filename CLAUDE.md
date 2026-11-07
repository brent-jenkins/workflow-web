# Zayvori Web — Claude Code Context

Static marketing and legal website for **Zayvori**, the Android to-do app where tasks link into visual workflows (app repo: `../workflow-app`). Plain HTML, CSS and vanilla JS — no build step, deployed as-is. Same approach as the Damson Kitchen site (`../recipe-web`), which is the reference for conventions.

## File map

| File | Role |
|------|------|
| `index.html` | Home, in selling order: hero (outcome-first headline, real map screenshot, reminder notification), **the difference** (a plain list beside the To do view — the core pitch), the map band (dark-theme map screenshot), the tablet (`#tablet`: the 10" landscape capture, list, next steps and map side by side, `assets/screens/tablet-wide.png` from make-store-assets.js `--web`, in a `.tablet` frame), Today, templates, then the AI: Describe it leading into Zayvori Premium (after the free core, as a helper rather than the headline, matching the Play listing), the little things (a plain list), privacy and backup, "coming soon" |
| `assets/screens/` | Real app screenshots, made by `workflow-app/scripts/make-store-assets.js --web assets/screens` from the store captures. Retake there, re-export here |
| `help.html` | Help and guide: one page on the parts worth explaining (getting started, task states and All/Any, Today/To do/Map, dates and reminders, templates and sending, repeating, widget, backups). Linked from the nav, the footer and the app's Settings → Help and guide. Keep it in step with the app; use the app's own words (`workflow-app/src/labels.ts`) |
| `privacy.html` | Privacy Policy. **Google Play requires its URL** for the listing |
| `404.html` | GitHub Pages serves it for any missing URL, at any depth — so it uses absolute `/` paths |
| `styles.css` | All styles. Brand tokens at the top as CSS custom properties |
| `script.js` | Mobile menu and the nav border once scrolled. Stores nothing |
| `assets/favicon.svg` | The Zayvori mark on its gradient tile. Also used as the nav and footer logo |
| `assets/apple-touch-icon.png`, `assets/og-image.png` | Rendered from the mark (180px; 1200×630 link preview) |
| `assets/fonts/` | Self-hosted Space Grotesk (headings) and Inter (body), Latin-subset woff2, SIL Open Font License |
| `CNAME`, `robots.txt`, `sitemap.xml` | Custom domain; crawl rules; page list — update `lastmod` and add `<url>` entries when pages change |

## Brand

- **Tokens are the app's exact values** (`workflow-app/src/theme.ts`): violet `#6A4DFF` → magenta `#C34DFF` gradient, mint `#2BD99F` ticks, done `#0FA97A`, ink `#12121F`, background `#F4F4F9`, dark `#0B0B13`. Change the app, change these.
- **The mark** (a white Z-shaped route between two mint "done" ticks) is the same geometry as the app icon (`workflow-app/scripts/make-icons.js`) and in-app `BrandMark.tsx`. Change one, change all.
- **Type:** Space Grotesk for names, headings and numbers; Inter for body. Self-hosted — never load from `fonts.googleapis.com` (it would send visitors' IPs to Google and break the privacy policy's no-third-parties line).
- **Ration the color**, as the app does: gradient only on the logo tile and primary buttons; the highlighted word in the headline is solid violet (`.hl`), not gradient text; violet for links; everything else neutral. The faint doodle pattern (`.doodles`) is on the hero and the templates section only: it marks the templates out as their own band between Today and Describe it.
- **Don't look template-made** (November 2026: "it looks AI-generated"). Avoid the stock landing-page kit: a small uppercase label over every heading (only the hero's and Premium's remain), centered heading + subtitle + identical icon cards in every section (section heads are left-aligned; the smaller features are a plain two-column list, `.also`), scroll fade-ins are the exception (removed, then brought back by choice: gentle, and usual on sites now), a numbered "how it works" strip (removed), gradient text. Prefer specific, real examples (an AP exam, a move to Denver) over generic ones, and lively but plain headings. Still marketing: confident and concrete, not dull.
- **Voice:** plain, upbeat, practical. **US English**, matching the app and the Play listing, in words as well as spelling: check off (not tick), come around (not round), a move (not moving house). A workflow is called a **plan** everywhere people read it (the app's Plans tab, "New plan"), since November 2026. Talk about getting things done and knowing what's next — not productivity jargon. Use the app's own words for concepts (Ready, Waiting, Not needed, "any one is enough", Finish) — see `workflow-app/src/labels.ts`.

## What the app does (keep copy aligned)

Workflows from Start to Finish; tasks branch, run side by side and merge; "finish all of them" or "any one is enough" before a step; unneeded tasks are set aside automatically; **To do** view (next steps / coming up / done) and **Map** view; one-tap complete with Undo; **phones, tablets and foldables** (0.0.18: on a wide screen the list sits beside the chosen plan, and a wide plan shows To do and the Map side by side; tablets turn, phones stay portrait); due dates; reminders (due soon, due now, morning summary) with **Mark complete / Snooze 1 hour / Dismiss** on the notification; progress "x of y"; confetti on finish; light/dark/system theme; background pattern; **templates** (five starters, save any workflow as one, due dates follow the start date); duplicate / run again (a fresh copy, dates counted from today); **moving a date later offers to move the tasks it pushes too early**, keeping the gaps; the **Next steps home-screen widget** (Android; tick tasks off from it); the **Today tab** (overdue, due today and next steps across every workflow; a late tick offers to move later tasks); **repeating workflows** (weekly to yearly, the next round starts itself on a fixed schedule); **send a template** to someone as a file, opened in Zayvori; choose which tab the app **starts on**; **backup to a file** the user keeps anywhere, and restore. **Everything on the phone: no account, no server, no sync, no analytics.**

**Describe it**: type or say a plan and Claude drafts the workflow, by the day or by the hour (times of day and a tip per task), with holidays on the phone's country's date. What leaves the phone: the description, today's date, the phone's two-letter region setting and a random install id (privacy.html → Describe it). **Change with AI** (shipped with app 0.0.11) revises an existing workflow or template: the request plus that one plan (task names, notes, dates and times, order, which are done) is sent; every change is reviewed before Apply, with Undo; done tasks are never changed. Keep any privacy claim on the site consistent with that.

**Premium** (Google Play subscription, live since app 0.0.13): Describe it, Change with AI, timed plans and Calendar sync; $2.99 a month or $29.99 a year (yearly raised from $19.99 on 6 Nov 2026, before anyone subscribed), 14-day free trial with 25 AI requests, then up to 100 a month (fair use, enforced by the API); everything else free. The home page has a Premium section; never say the AI features are free, and never say nothing leaves the phone without naming the Premium AI features as the exception.

Not features (don't claim): accounts, automatic cloud sync, live sharing or collaboration (sending a template file is fine to claim), repeating single tasks (whole workflows repeat), iOS.

**Selling, not describing:** lead with the outcome (only what you can do today) and a recognizable situation (moving, remodeling, events); show the before/after; mechanism words ("branch", "merge") come after.

## No cookies, no analytics, no third parties

The site makes no third-party requests, which is what lets the privacy policy be one short page with no consent banner. Adding any tracker, embed or externally hosted asset changes the privacy policy — weigh that first.

## Launch state and open items

- **Pre-launch.** The app isn't on Google Play yet: the CTA is "Coming soon" with an email link. When it launches, swap the nav button, hero CTA and download card for the Play link (`https://play.google.com/store/apps/details?id=com.zayvori.workflow`).
- **`support@zayvori.com` must exist** — it's the contact in the privacy policy, the help page and the CTA. It replaced hello@zayvori.com, which stopped working, in November 2026.
- **Privacy policy "Who we are"** assumes the same setup as Damson Kitchen: an independent UK developer trading as Zayvori, no company. Confirm before submitting to Play. Not reviewed by a lawyer.

## Deployment

**GitHub Pages** (handles the domain and TLS), deploying `main` from the repo root; `CNAME` sets `zayvori.com`. Pages is free only for **public** repos (Damson Kitchen's `recipe-web` is public); a private repo needs GitHub Pro.

**History:** zayvori.com previously served a static page for the investment research project from the VM (`root@204.168.242.186`, Caddy, deployed by a webhook from the `investment-web` repo). That was **decommissioned on 2026-10-27**: the `zayvori.com` / `www.zayvori.com` Caddy blocks, `/var/www/zayvori.com`, `/root/zayvori-web` and `zayvori-web-webhook.service` were removed. Everything is backed up on the VM at `/root/zayvori-web-decommission-20261027.tar.gz`. The `investment-web` repo is now orphaned; its GitHub webhook will fail and can be deleted.

**cfd.zayvori.com stays on the VM, unchanged.** It has its own DNS record and its own Caddy-managed certificate; moving the apex doesn't touch it. Keep its Cloudflare record **proxied (orange cloud)**: the VM's firewall only accepts 80/443 from Cloudflare's ranges.

**DNS for this site (Cloudflare, zone zayvori.com):**
- Apex `zayvori.com`: four `A` records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (and optionally `AAAA` → `2606:50c0:8000::153` … `8003::153`).
- **The site lives at `zayvori.com` only** (the `CNAME` file and every canonical URL say so). `www` is optional: a `CNAME` → `brent-jenkins.github.io` makes GitHub redirect `www.zayvori.com` to `zayvori.com`; with no `www` record, `www` simply doesn't resolve.
- All of these **DNS only (grey cloud)**, so GitHub can issue the certificate and the privacy policy's "hosted on GitHub Pages" stays the whole story. If they're ever proxied, add Cloudflare to the privacy policy, since it then processes visitors' IP addresses.
- Then in the repo: Settings → Pages → custom domain `zayvori.com`, wait for the certificate, tick **Enforce HTTPS**.

## Previewing locally

Any static server from this folder works, e.g. `npx serve .` then open http://localhost:3000.

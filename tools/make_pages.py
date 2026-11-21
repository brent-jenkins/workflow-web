"""Builds the home page and the help page in every language, and the sitemap.

Run from the repo root:  python tools/make_pages.py

- home-src/<lang>.html is the home page's <main> content; help-src/<lang>.html
  is the help page's body (inside .legal__body). Edit those, never the
  generated index.html / help.html files (English at the root, the others in
  /<lang>/).
- This script adds the shared head (canonical, hreflang alternates for every
  language plus x-default, Open Graph, and on the home page the
  SoftwareApplication data), the header with the globe language menu, the
  footer and the scripts, and writes sitemap.xml.
- Section anchors (#why, #templates…, and the help's #getting-started, #dates…)
  are the same in every language and never translated: the app opens the help
  page in its own language and may link to a section. The script fails if a
  language's anchors differ from English's.
- English pages carry a small redirect: a visitor arriving from outside the
  site whose browser's first language is one of the others goes to that
  language's page, keeping the query (campaign tags) and the #section.
  ?lang=en stops it. It reads the browser's language and the referrer and
  stores nothing. Search engines crawl in English and aren't redirected.
- One Spanish (Latin America's) and one Portuguese (Brazil's), for every
  country, as in the app. hreflang "es" and "pt" so every search finds them.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAY = 'https://play.google.com/store/apps/details?id=com.zayvori.workflow'
SITE = 'https://zayvori.com'
TODAY = '2026-11-22'

# code, folder, html lang, hreflang, og:locale, name in itself, menu code
LANGS = [
    ('en', '', 'en', 'en', 'en_US', 'English', 'EN'),
    ('es', 'es', 'es-419', 'es', 'es_LA', 'Español', 'ES'),
    ('pt', 'pt', 'pt-BR', 'pt', 'pt_BR', 'Português (Brasil)', 'PT'),
    ('fr', 'fr', 'fr', 'fr', 'fr_FR', 'Français', 'FR'),
    ('de', 'de', 'de', 'de', 'de_DE', 'Deutsch', 'DE'),
    ('it', 'it', 'it', 'it', 'it_IT', 'Italiano', 'IT'),
    ('id', 'id', 'id', 'id', 'id_ID', 'Bahasa Indonesia', 'ID'),
]

C = {
    'en': dict(
        why='Why Zayvori', templates='Templates', describe='Describe it', premium='Premium', help='Help', download='Download',
        privacy='Privacy policy', terms='Terms of use', home='Zayvori — home', menu='Open menu', language='Language',
        home_title='Zayvori — big jobs, one next step at a time',
        home_desc='Moving, remodeling, planning an event: Zayvori knows which tasks wait for others, so you see what you can do today. No account, works offline, and your plans stay on your phone. Plan with AI in Zayvori Premium. Free on Google Play.',
        og_desc='A to-do app that knows which tasks wait on which, so you only see what you can do today. Free on Google Play.',
        ld_desc='A to-do app for big jobs: tasks that wait for others, run side by side or offer alternatives, so you only see the next steps you can do today. No account, works offline, and your plans stay on your phone.',
        help_title='Help and guide — Zayvori', help_desc='How Zayvori works: plans, Today, the map, due dates and reminders, templates, repeating plans, the widget and backups.',
        help_eyebrow='Help', help_h1='How Zayvori works', help_sub='A short guide to the parts worth knowing about.'),
    'es': dict(
        why='Por qué Zayvori', templates='Plantillas', describe='Descríbelo', premium='Premium', help='Ayuda', download='Descargar',
        privacy='Privacidad (en inglés)', terms='Términos (en inglés)', home='Zayvori — inicio', menu='Abrir menú', language='Idioma',
        home_title='Zayvori — grandes proyectos, un paso a la vez',
        home_desc='Una mudanza, una remodelación, organizar un evento: Zayvori sabe qué tareas esperan a otras, así que ves lo que puedes hacer hoy. Sin cuenta, funciona sin conexión y tus planes se quedan en tu teléfono. Planifica con IA en Zayvori Premium. Gratis en Google Play.',
        og_desc='Una app de tareas que sabe qué espera a qué, así que solo ves lo que puedes hacer hoy. Gratis en Google Play.',
        ld_desc='Una app de tareas para grandes proyectos: tareas que esperan a otras, van en paralelo u ofrecen alternativas, así que solo ves los próximos pasos que puedes hacer hoy. Sin cuenta, funciona sin conexión y tus planes se quedan en tu teléfono.',
        help_title='Ayuda y guía — Zayvori', help_desc='Cómo funciona Zayvori: planes, Hoy, el mapa, fechas límite y recordatorios, plantillas, planes que se repiten, el widget y las copias de seguridad.',
        help_eyebrow='Ayuda', help_h1='Cómo funciona Zayvori', help_sub='Una guía breve de lo que vale la pena saber.'),
    'pt': dict(
        why='Por que o Zayvori', templates='Modelos', describe='Descreva', premium='Premium', help='Ajuda', download='Baixar',
        privacy='Privacidade (em inglês)', terms='Termos (em inglês)', home='Zayvori — início', menu='Abrir menu', language='Idioma',
        home_title='Zayvori — grandes projetos, um passo de cada vez',
        home_desc='Mudança, reforma, um evento: o Zayvori sabe quais tarefas esperam por outras, então você vê o que dá para fazer hoje. Sem conta, funciona off-line e seus planos ficam no seu celular. Planeje com IA no Zayvori Premium. Grátis no Google Play.',
        og_desc='Um app de tarefas que sabe o que espera pelo quê, então você só vê o que dá para fazer hoje. Grátis no Google Play.',
        ld_desc='Um app de tarefas para grandes projetos: tarefas que esperam por outras, andam lado a lado ou oferecem alternativas, então você só vê os próximos passos que dá para fazer hoje. Sem conta, funciona off-line e seus planos ficam no seu celular.',
        help_title='Ajuda e guia — Zayvori', help_desc='Como o Zayvori funciona: planos, Hoje, o mapa, prazos e lembretes, modelos, planos que se repetem, o widget e os backups.',
        help_eyebrow='Ajuda', help_h1='Como o Zayvori funciona', help_sub='Um guia rápido do que vale a pena saber.'),
    'fr': dict(
        why='Pourquoi Zayvori', templates='Modèles', describe='Décrivez-le', premium='Premium', help='Aide', download='Télécharger',
        privacy='Confidentialité (en anglais)', terms='Conditions (en anglais)', home='Zayvori — accueil', menu='Ouvrir le menu', language='Langue',
        home_title='Zayvori — les grands projets, une étape à la fois',
        home_desc='Un déménagement, une rénovation, un événement : Zayvori sait quelles tâches en attendent d’autres, et vous montre ce que vous pouvez faire aujourd’hui. Sans compte, hors ligne, et vos plans restent sur votre téléphone. Planifiez avec l’IA dans Zayvori Premium. Gratuit sur Google Play.',
        og_desc='Une app de tâches qui sait ce qui attend quoi, pour ne vous montrer que ce que vous pouvez faire aujourd’hui. Gratuit sur Google Play.',
        ld_desc='Une app de tâches pour les grands projets : des tâches qui en attendent d’autres, avancent en parallèle ou offrent des alternatives, pour ne voir que vos prochaines étapes. Sans compte, hors ligne, et vos plans restent sur votre téléphone.',
        help_title='Aide et guide — Zayvori', help_desc='Comment fonctionne Zayvori : plans, Aujourd’hui, la carte, échéances et rappels, modèles, plans répétés, le widget et les sauvegardes.',
        help_eyebrow='Aide', help_h1='Comment fonctionne Zayvori', help_sub='Un petit guide de ce qui vaut la peine d’être connu.'),
    'de': dict(
        why='Warum Zayvori', templates='Vorlagen', describe='Beschreib es', premium='Premium', help='Hilfe', download='Herunterladen',
        privacy='Datenschutz (Englisch)', terms='Nutzungsbedingungen (Englisch)', home='Zayvori — Startseite', menu='Menü öffnen', language='Sprache',
        home_title='Zayvori — große Vorhaben, ein Schritt nach dem anderen',
        home_desc='Umzug, Renovierung, eine Feier: Zayvori weiß, welche Aufgaben auf andere warten, und zeigt dir, was du heute tun kannst. Kein Konto, funktioniert offline, und deine Pläne bleiben auf deinem Handy. Planen mit KI in Zayvori Premium. Kostenlos bei Google Play.',
        og_desc='Eine To-do-App, die weiß, was worauf wartet, und dir nur zeigt, was du heute tun kannst. Kostenlos bei Google Play.',
        ld_desc='Eine To-do-App für große Vorhaben: Aufgaben, die auf andere warten, parallel laufen oder Alternativen bieten, sodass du nur deine nächsten Schritte siehst. Kein Konto, funktioniert offline, und deine Pläne bleiben auf deinem Handy.',
        help_title='Hilfe und Anleitung — Zayvori', help_desc='So funktioniert Zayvori: Pläne, Heute, die Karte, Fälligkeiten und Erinnerungen, Vorlagen, wiederkehrende Pläne, das Widget und Sicherungen.',
        help_eyebrow='Hilfe', help_h1='So funktioniert Zayvori', help_sub='Eine kurze Anleitung zu allem, was wissenswert ist.'),
    'it': dict(
        why='Perché Zayvori', templates='Modelli', describe='Descrivilo', premium='Premium', help='Aiuto', download='Scarica',
        privacy='Privacy (in inglese)', terms='Condizioni (in inglese)', home='Zayvori — home', menu='Apri il menu', language='Lingua',
        home_title='Zayvori — grandi lavori, un passo alla volta',
        home_desc='Un trasloco, una ristrutturazione, un evento: Zayvori sa quali attività aspettano altre, così vedi cosa puoi fare oggi. Senza account, funziona offline e i tuoi piani restano sul telefono. Pianifica con l’IA in Zayvori Premium. Gratis su Google Play.',
        og_desc='Un’app di attività che sa cosa aspetta cosa, così vedi solo ciò che puoi fare oggi. Gratis su Google Play.',
        ld_desc='Un’app di attività per i grandi lavori: attività che aspettano altre, procedono in parallelo o offrono alternative, così vedi solo i prossimi passi che puoi fare oggi. Senza account, funziona offline e i tuoi piani restano sul telefono.',
        help_title='Aiuto e guida — Zayvori', help_desc='Come funziona Zayvori: piani, Oggi, la mappa, scadenze e promemoria, modelli, piani che si ripetono, il widget e i backup.',
        help_eyebrow='Aiuto', help_h1='Come funziona Zayvori', help_sub='Una breve guida a ciò che vale la pena sapere.'),
    'id': dict(
        why='Kenapa Zayvori', templates='Template', describe='Jelaskan', premium='Premium', help='Bantuan', download='Unduh',
        privacy='Privasi (bahasa Inggris)', terms='Ketentuan (bahasa Inggris)', home='Zayvori — beranda', menu='Buka menu', language='Bahasa',
        home_title='Zayvori — pekerjaan besar, satu langkah demi satu langkah',
        home_desc='Pindahan, renovasi, merencanakan acara: Zayvori tahu tugas mana yang menunggu tugas lain, jadi Anda melihat apa yang bisa dikerjakan hari ini. Tanpa akun, bisa offline, dan rencana Anda tetap di ponsel. Rencanakan dengan AI di Zayvori Premium. Gratis di Google Play.',
        og_desc='Aplikasi tugas yang tahu apa menunggu apa, jadi Anda hanya melihat yang bisa dikerjakan hari ini. Gratis di Google Play.',
        ld_desc='Aplikasi tugas untuk pekerjaan besar: tugas yang menunggu tugas lain, berjalan berdampingan, atau menawarkan alternatif, jadi Anda hanya melihat langkah berikutnya. Tanpa akun, bisa offline, dan rencana Anda tetap di ponsel.',
        help_title='Bantuan dan panduan — Zayvori', help_desc='Cara kerja Zayvori: rencana, Hari ini, peta, jatuh tempo dan pengingat, template, rencana berulang, widget, dan cadangan.',
        help_eyebrow='Bantuan', help_h1='Cara kerja Zayvori', help_sub='Panduan singkat tentang hal-hal yang perlu diketahui.'),
}

GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')
CARET = ('<svg class="nav__lang-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg>')

OTHERS = [l[0] for l in LANGS if l[0] != 'en']
REDIRECT = ('  <script>/* Visitors from outside the site whose browser prefers another of our languages go to it; ?lang=en stops this. Stores nothing (tools/make_pages.py). */'
            "(function(){try{var q=new URLSearchParams(location.search);if(q.get('lang')==='en')return;"
            "if(document.referrer&&new URL(document.referrer).host===location.host)return;"
            "var l=((navigator.languages&&navigator.languages[0])||navigator.language||'').toLowerCase().split('-')[0];if(l==='in')l='id';"
            f"if({OTHERS!r}.indexOf(l)<0)return;"
            "location.replace('/'+l+(location.pathname==='/index.html'?'/':location.pathname)+location.search+location.hash);}catch(e){}})();</script>\n")


def url(kind, folder):
    page = '' if kind == 'home' else 'help.html'
    return f'/{folder}/{page}' if folder else f'/{page}'


def read(kind, code):
    return io.open(os.path.join(ROOT, f'{kind}-src', f'{code}.html'), encoding='utf-8').read().rstrip()


def indent(s, n):
    return '\n'.join((' ' * n + l) if l.strip() else l for l in s.split('\n'))


def header(kind, code, folder, short):
    c = C[code]
    home = url('home', folder)
    menu = '\n'.join(
        f'          <li><a href="{url(kind, f)}" lang="{hl}" hreflang="{hr}"{" aria-current=\"true\"" if k == code else ""}>{name}</a></li>'
        for (k, f, hl, hr, _, name, _) in LANGS)
    extra = (f'''        <a href="{home}#describe">{c['describe']}</a>
        <a href="{home}#premium">{c['premium']}</a>
''' if kind == 'home' else '')
    current = ' aria-current="page"' if kind == 'help' else ''
    return f'''  <header class="nav">
    <div class="nav__inner container">
      <a href="{home}" class="nav__logo" aria-label="{c['home']}">
        <img class="brandmark" src="/assets/favicon.svg" alt="" width="34" height="34" />
        <span class="nav__logo-text">Zayvori</span>
      </a>
      <nav class="nav__links" aria-label="Main">
        <a href="{home}#why">{c['why']}</a>
        <a href="{home}#templates">{c['templates']}</a>
{extra}        <a href="{url('help', folder)}"{current}>{c['help']}</a>
        <a href="{PLAY}" class="btn btn--primary btn--sm" target="_blank" rel="noopener">{c['download']}</a>
      </nav>
      <details class="nav__lang">
        <summary aria-label="{c['language']}" title="{c['language']}">{GLOBE}<span>{short}</span>{CARET}</summary>
        <ul class="nav__lang-menu">
{menu}
        </ul>
      </details>
      <button class="nav__hamburger" aria-label="{c['menu']}" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>'''


def footer(kind, code, folder):
    c = C[code]
    home = url('home', folder)
    current = ' aria-current="page"' if kind == 'help' else ''
    return f'''  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <a href="{home}" class="nav__logo" aria-label="{c['home']}">
          <img class="brandmark" src="/assets/favicon.svg" alt="" width="34" height="34" />
          <span class="nav__logo-text">Zayvori</span>
        </a>
        <nav class="footer__links" aria-label="Footer">
          <a href="{home}#why">{c['why']}</a>
          <a href="{home}#templates">{c['templates']}</a>
          <a href="{url('help', folder)}"{current}>{c['help']}</a>
          <a href="/privacy.html">{c['privacy']}</a>
          <a href="/terms.html">{c['terms']}</a>
          <a href="mailto:support@zayvori.com">support@zayvori.com</a>
          <a href="https://x.com/zayvoriapp" class="footer__social" target="_blank" rel="noopener me" aria-label="Zayvori on X"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.2l-4.8-6.3L6.4 22H3.3l7.3-8.3L1 2h6.3l4.4 5.8zm-1.1 18h1.7L6.3 3.9H4.5z"/></svg></a>
          <a href="https://www.tiktok.com/@zayvoriapp" class="footer__social" target="_blank" rel="noopener me" aria-label="Zayvori on TikTok"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M16.6 2h-3.4v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.1a6.4 6.4 0 1 0 5.4 6.3V8.7a8 8 0 0 0 4.6 1.5V6.8a4.6 4.6 0 0 1-4.6-4.8z"/></svg></a>
        </nav>
      </div>
      <p class="footer__bottom">© 2026 Zayvori.</p>
    </div>
  </footer>

  <script src="/analytics.js" defer></script>
  <script src="/script.js" defer></script>
</body>
</html>
'''


def head(kind, code, folder, html_lang, og_locale):
    c = C[code]
    title, desc = (c['home_title'], c['home_desc']) if kind == 'home' else (c['help_title'], c['help_desc'])
    alternates = '\n'.join(f'  <link rel="alternate" hreflang="{hr}" href="{SITE}{url(kind, f)}" />' for (_, f, _, hr, _, _, _) in LANGS)
    alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{url(kind, "")}" />'
    og = ''
    if kind == 'home':
        others = '\n'.join(f'  <meta property="og:locale:alternate" content="{loc}" />' for (k, _, _, _, loc, _, _) in LANGS if k != code)
        og = f'''
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Zayvori" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{c['og_desc']}" />
  <meta property="og:url" content="{SITE}{url(kind, folder)}" />
  <meta property="og:image" content="{SITE}/assets/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:locale" content="{og_locale}" />
{others}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{SITE}/assets/og-image.png" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Zayvori",
    "description": "{c['ld_desc']}",
    "inLanguage": "{html_lang}",
    "url": "{SITE}{url(kind, folder)}",
    "installUrl": "{PLAY}",
    "downloadUrl": "{PLAY}",
    "applicationCategory": "ProductivityApplication",
    "operatingSystem": "Android",
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
    "sameAs": ["{PLAY}", "https://x.com/zayvoriapp", "https://www.tiktok.com/@zayvoriapp"],
    "screenshot": "{SITE}/assets/og-image.png",
    "image": "{SITE}/assets/favicon.svg"
  }}
  </script>'''
    font = '\n  <link rel="preload" href="/assets/fonts/space-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin />' if kind == 'home' else ''
    redirect = REDIRECT if code == 'en' else ''
    # Site ownership checks: inert meta tags, no requests. Pinterest reads the home page.
    verify = '  <meta name="p:domain_verify" content="114b1fce8092e500bb66a118ced883cd" />
' if (kind == 'home' and code == 'en') else ''
    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{redirect}  <title>{title}</title>
  <meta name="description" content="{desc}" />
{verify}  <link rel="canonical" href="{SITE}{url(kind, folder)}" />
{alternates}
  <meta name="theme-color" content="#6A4DFF" />{og}
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />{font}
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <!-- Generated by tools/make_pages.py from {kind}-src/{code}.html: edit that, then rerun. -->
'''


def page(kind, code, folder, html_lang, og_locale, short):
    c = C[code]
    top = head(kind, code, folder, html_lang, og_locale) + '\n' + header(kind, code, folder, short) + '\n\n'
    if kind == 'home':
        main = f'  <main>\n{indent(read("home", code), 4)}\n  </main>\n\n'
    else:
        main = f'''  <main>
    <section class="legal-hero doodles">
      <div class="container">
        <span class="eyebrow">{c['help_eyebrow']}</span>
        <h1>{c['help_h1']}</h1>
        <p>{c['help_sub']}</p>
      </div>
    </section>

    <section class="legal doodles">
      <div class="container">
        <div class="legal__body">
{indent(read("help", code), 10)}
        </div>
      </div>
    </section>
  </main>

'''
    return top + main + footer(kind, code, folder)


def sitemap():
    def entry(loc, alts):
        links = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{u}" />' for h, u in alts)
        return f'  <url>\n    <loc>{SITE}{loc}</loc><lastmod>{TODAY}</lastmod>{links}\n  </url>\n'
    out = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for kind in ('home', 'help'):
        alts = [(hr, url(kind, f)) for (_, f, _, hr, _, _, _) in LANGS] + [('x-default', url(kind, ''))]
        for (_, f, *_rest) in LANGS:
            out += entry(url(kind, f), alts)
    out += f'  <url><loc>{SITE}/privacy.html</loc><lastmod>2026-11-21</lastmod></url>\n'
    out += f'  <url><loc>{SITE}/terms.html</loc><lastmod>2026-11-09</lastmod></url>\n</urlset>\n'
    io.open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(out)


def main():
    for kind, filename in (('home', 'index.html'), ('help', 'help.html')):
        anchors = None
        for code, folder, html_lang, _, og_locale, _, short in LANGS:
            if not os.path.exists(os.path.join(ROOT, f'{kind}-src', f'{code}.html')):
                print(f'skipped {kind} {code}: no {kind}-src/{code}.html yet')
                continue
            html = page(kind, code, folder, html_lang, og_locale, short)
            ids = sorted(set(re.findall(r'\sid="([a-z0-9-]+)"', html)))
            anchors = anchors if anchors is not None else ids
            if ids != anchors:
                sys.exit(f'{kind} {code}: section anchors differ from English: {sorted(set(ids) ^ set(anchors))}')
            out = os.path.join(ROOT, folder, filename) if folder else os.path.join(ROOT, filename)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            io.open(out, 'w', encoding='utf-8', newline='\n').write(html)
            print('wrote', os.path.relpath(out, ROOT))
    sitemap()
    print('wrote sitemap.xml')


main()

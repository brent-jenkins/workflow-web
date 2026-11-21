"""Builds help.html in every language from help-src/<lang>.html.

Run from the repo root:  python tools/make_help.py

Each help-src/<lang>.html is the page's body (the part inside .legal__body):
edit those, never the generated help.html files. This script wraps each in
the shared header, language menu, footer and head (hreflang alternates for
every language), and writes /help.html (English) and /<folder>/help.html.

Section anchors (#getting-started, #dates…) must be the same in every
language and never translated: the app opens the help page in its own
language (Settings → Help and guide) and may link to a section.

Spanish is Latin America's (as in the app: one Spanish for every country),
and hreflang "es" so every Spanish search finds it; Portuguese is Brazil's,
hreflang "pt".
"""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAY = 'https://play.google.com/store/apps/details?id=com.zayvori.workflow'

# code: (folder, html lang, hreflang, name in itself, short code shown on the menu)
LANGS = [
    ('en', '', 'en', 'en', 'English', 'EN'),
    ('es', 'es', 'es-419', 'es', 'Español', 'ES'),
    ('pt', 'pt', 'pt-BR', 'pt', 'Português (Brasil)', 'PT'),
    ('fr', 'fr', 'fr', 'fr', 'Français', 'FR'),
    ('de', 'de', 'de', 'de', 'Deutsch', 'DE'),
    ('it', 'it', 'it', 'it', 'Italiano', 'IT'),
    ('id', 'id', 'id', 'id', 'Bahasa Indonesia', 'ID'),
]

CHROME = {
    'en': dict(title='Help and guide — Zayvori', desc='How Zayvori works: plans, Today, the map, due dates and reminders, templates, repeating plans, the widget and backups.',
               eyebrow='Help', h1='How Zayvori works', sub='A short guide to the parts worth knowing about.', why='Why Zayvori', templates='Templates',
               help='Help', download='Download', privacy='Privacy policy', terms='Terms of use', home='Zayvori — home', menu='Open menu', language='Language', legal_note=''),
    'es': dict(title='Ayuda y guía — Zayvori', desc='Cómo funciona Zayvori: planes, Hoy, el mapa, fechas límite y recordatorios, plantillas, planes que se repiten, el widget y las copias de seguridad.',
               eyebrow='Ayuda', h1='Cómo funciona Zayvori', sub='Una guía breve de lo que vale la pena saber.', why='Por qué Zayvori', templates='Plantillas',
               help='Ayuda', download='Descargar', privacy='Privacidad (en inglés)', terms='Términos (en inglés)', home='Zayvori — inicio', menu='Abrir menú', language='Idioma', legal_note=''),
    'pt': dict(title='Ajuda e guia — Zayvori', desc='Como o Zayvori funciona: planos, Hoje, o mapa, prazos e lembretes, modelos, planos que se repetem, o widget e os backups.',
               eyebrow='Ajuda', h1='Como o Zayvori funciona', sub='Um guia rápido do que vale a pena saber.', why='Por que o Zayvori', templates='Modelos',
               help='Ajuda', download='Baixar', privacy='Privacidade (em inglês)', terms='Termos (em inglês)', home='Zayvori — início', menu='Abrir menu', language='Idioma', legal_note=''),
    'fr': dict(title='Aide et guide — Zayvori', desc='Comment fonctionne Zayvori : plans, Aujourd’hui, la carte, échéances et rappels, modèles, plans répétés, le widget et les sauvegardes.',
               eyebrow='Aide', h1='Comment fonctionne Zayvori', sub='Un petit guide de ce qui vaut la peine d’être connu.', why='Pourquoi Zayvori', templates='Modèles',
               help='Aide', download='Télécharger', privacy='Confidentialité (en anglais)', terms='Conditions (en anglais)', home='Zayvori — accueil', menu='Ouvrir le menu', language='Langue', legal_note=''),
    'de': dict(title='Hilfe und Anleitung — Zayvori', desc='So funktioniert Zayvori: Pläne, Heute, die Karte, Fälligkeiten und Erinnerungen, Vorlagen, wiederkehrende Pläne, das Widget und Sicherungen.',
               eyebrow='Hilfe', h1='So funktioniert Zayvori', sub='Eine kurze Anleitung zu allem, was wissenswert ist.', why='Warum Zayvori', templates='Vorlagen',
               help='Hilfe', download='Herunterladen', privacy='Datenschutz (Englisch)', terms='Nutzungsbedingungen (Englisch)', home='Zayvori — Startseite', menu='Menü öffnen', language='Sprache', legal_note=''),
    'it': dict(title='Aiuto e guida — Zayvori', desc='Come funziona Zayvori: piani, Oggi, la mappa, scadenze e promemoria, modelli, piani che si ripetono, il widget e i backup.',
               eyebrow='Aiuto', h1='Come funziona Zayvori', sub='Una breve guida a ciò che vale la pena sapere.', why='Perché Zayvori', templates='Modelli',
               help='Aiuto', download='Scarica', privacy='Privacy (in inglese)', terms='Condizioni (in inglese)', home='Zayvori — home', menu='Apri il menu', language='Lingua', legal_note=''),
    'id': dict(title='Bantuan dan panduan — Zayvori', desc='Cara kerja Zayvori: rencana, Hari ini, peta, jatuh tempo dan pengingat, template, rencana berulang, widget, dan cadangan.',
               eyebrow='Bantuan', h1='Cara kerja Zayvori', sub='Panduan singkat tentang hal-hal yang perlu diketahui.', why='Kenapa Zayvori', templates='Template',
               help='Bantuan', download='Unduh', privacy='Privasi (bahasa Inggris)', terms='Ketentuan (bahasa Inggris)', home='Zayvori — beranda', menu='Buka menu', language='Bahasa', legal_note=''),
}


GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>')
CARET = ('<svg class="nav__lang-caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg>')


def url(folder):
    return f'/{folder}/help.html' if folder else '/help.html'


def body_for(code):
    return io.open(os.path.join(ROOT, 'help-src', f'{code}.html'), encoding='utf-8').read()


def page(code, folder, html_lang, short):
    c = CHROME[code]
    pre = '../' if folder else ''
    alternates = '\n'.join(
        f'  <link rel="alternate" hreflang="{hl}" href="https://zayvori.com{url(f)}" />' for (_, f, _, hl, _, _) in LANGS
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="https://zayvori.com/help.html" />'
    menu = '\n'.join(
        f'          <li><a href="{url(f)}" lang="{hl2}" hreflang="{hl}"{" aria-current=\"true\"" if k == code else ""}>{name}</a></li>'
        for (k, f, hl2, hl, name, _) in LANGS
    )
    body = '\n'.join(('          ' + l) if l.strip() else l for l in body_for(code).rstrip().split('\n'))
    return f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{c['title']}</title>
  <meta name="description" content="{c['desc']}" />
  <link rel="canonical" href="https://zayvori.com{url(folder)}" />
{alternates}
  <meta name="theme-color" content="#6A4DFF" />
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg" />
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
  <link rel="stylesheet" href="/styles.css" />
</head>
<body>
  <!-- Generated by tools/make_help.py from help-src/{code}.html: edit that, then rerun. -->

  <header class="nav">
    <div class="nav__inner container">
      <a href="/" class="nav__logo" aria-label="{c['home']}">
        <img class="brandmark" src="/assets/favicon.svg" alt="" width="34" height="34" />
        <span class="nav__logo-text">Zayvori</span>
      </a>
      <nav class="nav__links" aria-label="Main">
        <a href="/#why">{c['why']}</a>
        <a href="/#templates">{c['templates']}</a>
        <a href="{url(folder)}" aria-current="page">{c['help']}</a>
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
  </header>

  <main>
    <section class="legal-hero doodles">
      <div class="container">
        <span class="eyebrow">{c['eyebrow']}</span>
        <h1>{c['h1']}</h1>
        <p>{c['sub']}</p>
      </div>
    </section>

    <section class="legal doodles">
      <div class="container">
        <div class="legal__body">
{body}
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <a href="/" class="nav__logo" aria-label="{c['home']}">
          <img class="brandmark" src="/assets/favicon.svg" alt="" width="34" height="34" />
          <span class="nav__logo-text">Zayvori</span>
        </a>
        <nav class="footer__links" aria-label="Footer">
          <a href="/#why">{c['why']}</a>
          <a href="/#templates">{c['templates']}</a>
          <a href="{url(folder)}" aria-current="page">{c['help']}</a>
          <a href="/privacy.html">{c['privacy']}</a>
          <a href="/terms.html">{c['terms']}</a>
          <a href="mailto:support@zayvori.com">support@zayvori.com</a>
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


def main():
    anchors = None
    for code, folder, html_lang, _, _, short in LANGS:
        html = page(code, folder, html_lang, short)
        ids = sorted(set(__import__('re').findall(r'id="([a-z-]+)"', html)))
        anchors = anchors or ids
        if ids != anchors:
            sys.exit(f'{code}: section anchors differ from English: {set(ids) ^ set(anchors)}')
        out = os.path.join(ROOT, folder, 'help.html') if folder else os.path.join(ROOT, 'help.html')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        io.open(out, 'w', encoding='utf-8', newline='\n').write(html)
        print('wrote', os.path.relpath(out, ROOT))


main()

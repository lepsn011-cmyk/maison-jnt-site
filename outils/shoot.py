#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shoot.py — captures d'écran du site Maison JNT (CLAUDE.md §7).

    python3 outils/shoot.py --out /tmp/hero.png --width 375
    python3 outils/shoot.py --out /tmp/full.png --width 1440 --fullpage
    python3 outils/shoot.py --out /tmp/fiche.png --width 1440 --click ".entree"
    python3 outils/shoot.py --out /tmp/sec.png  --width 768 --section catalogue

Le binaire Chromium est pointé explicitement : playwright 1.62 réclame ici un
build que l'image ne fournit pas, et `playwright install` est interdit.
"""

import argparse
import functools
import os
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE = '/opt/pw-browsers/chromium'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--width', type=int, default=1440)
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--section', help="id d'une section à cadrer")
    ap.add_argument('--fullpage', action='store_true')
    ap.add_argument('--settle', type=int, default=700, help='ms avant capture')
    ap.add_argument('--click', help='sélecteur à cliquer avant la capture')
    ap.add_argument('--query', default='', help='query string, ex. "famille=chypree"')
    ap.add_argument('--reduced', action='store_true', help='prefers-reduced-motion: reduce')
    a = ap.parse_args()

    h = functools.partial(SimpleHTTPRequestHandler, directory=RACINE)
    h.log_message = lambda *x, **k: None
    srv = ThreadingHTTPServer(('127.0.0.1', 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    url = f'http://127.0.0.1:{port}/index.html' + (f'?{a.query}' if a.query else '')

    with sync_playwright() as pw:
        nav = pw.chromium.launch(headless=True, executable_path=EXE)
        ctx = nav.new_context(viewport={'width': a.width, 'height': a.height},
                              device_scale_factor=2, locale='fr-FR',
                              reduced_motion='reduce' if a.reduced else 'no-preference')
        page = ctx.new_page()
        page.goto(url, wait_until='networkidle')
        # On n'attend pas « au jugé » : on attend que les polices soient prêtes,
        # sinon la capture fige un rendu en police de repli.
        page.evaluate('() => document.fonts.ready')

        # Les images du catalogue sont en loading="lazy" : elles ne commencent à
        # charger qu'en entrant dans la zone visible. `networkidle` est donc atteint
        # AVANT elles, et une capture de section les fige en emplacement gris — ce
        # qui a fait passer quatre décors bien présents pour des trous. On force
        # donc le défilement, puis on attend le décodage RÉEL de chaque image.
        # Faire défiler pour « réveiller » le lazy-load est une heuristique qui
        # rate : la photo de boutique, créée en JS, ne démarrait toujours pas.
        # On bascule donc TOUTES les images en chargement immédiat et on relance
        # la requête pour celles qui n'ont rien commencé (currentSrc vide).
        page.evaluate('''() => {
            document.querySelectorAll('img').forEach(i => {
                i.loading = 'eager';
                if (!i.currentSrc && i.getAttribute('src')) {
                    const s = i.getAttribute('src');
                    i.setAttribute('src', '');
                    i.setAttribute('src', s);
                }
            });
        }''')
        page.wait_for_function(
            '''() => Array.from(document.images)
                 .every(i => i.complete && i.naturalWidth > 0)''',
            timeout=20000)
        # `complete` dit « octets reçus », pas « pixels décodés » : decode() attend
        # le bitmap réellement prêt à peindre.
        page.evaluate('() => Promise.all(Array.from(document.images).map('
                      'i => i.decode().catch(() => null)))')
        page.wait_for_timeout(a.settle)

        if a.click:
            page.click(a.click)
            page.wait_for_timeout(500)

        os.makedirs(os.path.dirname(os.path.abspath(a.out)) or '.', exist_ok=True)
        if a.section:
            page.locator(f'#{a.section}').screenshot(path=a.out)
        else:
            page.screenshot(path=a.out, full_page=a.fullpage)

        polices = page.evaluate(
            '() => Array.from(document.fonts).filter(f=>f.status==="loaded").map(f=>f.family)')
        n_img = page.evaluate('() => Array.from(document.images).filter(i => i.complete && i.naturalWidth > 0).length')
        n_tot = page.evaluate('() => document.images.length')
        print(f'{a.out}  {a.width}px  polices={sorted(set(polices))}  images={n_img}/{n_tot} peintes')
        nav.close()
    srv.shutdown()


if __name__ == '__main__':
    main()

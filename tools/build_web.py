"""Genera la versión web instalable (iPhone, Android, ordenador) en la carpeta site/.

- index.html con fuentes locales, manifest e iconos para «Añadir a pantalla de inicio».
- sw.js: guarda la app en el móvil para que funcione sin internet.
Uso: python3 tools/build_web.py [versión]
"""
import json, pathlib, re, shutil, sys

root = pathlib.Path(__file__).resolve().parent.parent
site = root / 'site'
version = sys.argv[1] if len(sys.argv) > 1 else 'dev'

if site.exists():
    shutil.rmtree(site)
(site / 'fonts').mkdir(parents=True)
(site / 'icons').mkdir()

for f in (root / 'app' / 'src' / 'main' / 'assets' / 'fonts').iterdir():
    shutil.copy(f, site / 'fonts' / f.name)
for f in (root / 'web' / 'icons').iterdir():
    shutil.copy(f, site / 'icons' / f.name)

src = (root / 'web' / 'punto-a-punto.html').read_text(encoding='utf-8')

fonts = '<style>\n' + '\n'.join(
    f'@font-face{{font-family:"{fam}";font-weight:{w};font-display:swap;src:url(fonts/{file}) format("woff2")}}'
    for fam, w, file in [
        ('Barlow', 400, 'barlow-latin-400-normal.woff2'),
        ('Barlow', 500, 'barlow-latin-500-normal.woff2'),
        ('Barlow', 600, 'barlow-latin-600-normal.woff2'),
        ('Barlow', 700, 'barlow-latin-700-normal.woff2'),
        ('Barlow Condensed', 600, 'barlow-condensed-latin-600-normal.woff2'),
        ('Barlow Condensed', 700, 'barlow-condensed-latin-700-normal.woff2'),
    ]) + '\n</style>'
src = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', fonts, src)
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')

head = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1b5a3d">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Punto a Punto">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<style>
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}
/* Franja de la barra de estado del iPhone, del color de la pista */
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:#1b5a3d;z-index:10}
html{-webkit-text-size-adjust:100%}
.install{position:fixed;left:0;right:0;bottom:0;z-index:20;background:#1b5a3d;color:#f2f7f1;font:15px/1.4 "Barlow",system-ui,sans-serif;
  padding:12px max(16px,env(safe-area-inset-right,0px)) calc(12px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));
  display:flex;gap:12px;align-items:center;box-shadow:0 -4px 16px rgba(0,0,0,.25)}
.install p{margin:0;flex:1;min-width:0;line-height:1.55}
.install b{color:#d6e64c}
.install button{flex:none;background:transparent;border:1.5px solid rgba(255,255,255,.5);color:inherit;border-radius:8px;padding:6px 10px;font:inherit;font-weight:600}
.share-ico{display:inline-block;width:12px;height:11px;vertical-align:-1px;border:2px solid currentColor;border-top:0;border-radius:0 0 3px 3px;position:relative;margin:0 2px}
.share-ico::before{content:"";position:absolute;left:50%;top:-6px;width:2px;height:10px;background:currentColor;transform:translateX(-50%)}
.share-ico::after{content:"";position:absolute;left:50%;top:-6px;width:5px;height:5px;border-left:2px solid currentColor;border-top:2px solid currentColor;transform:translateX(-50%) rotate(45deg)}
</style>
<script>window.PWA=true;</script>
"""

pwa_tail = """
<div class="install" id="installTip" hidden>
  <p>Para instalarla en tu iPhone: pulsa <b>Compartir</b> <span class="share-ico" aria-hidden="true"></span> y luego <b>«Añadir a pantalla de inicio»</b>. Usa siempre la app desde ese icono.</p>
  <button type="button" id="installClose">Cerrar</button>
</div>
<script>
(function(){
  var ios=/iphone|ipad|ipod/i.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
  var standalone=window.navigator.standalone===true||(window.matchMedia&&matchMedia('(display-mode: standalone)').matches);
  var closed=false;try{closed=localStorage.getItem('puntoapunto.installTip')==='1';}catch(e){}
  var tip=document.getElementById('installTip');
  if(ios&&!standalone&&!closed)tip.hidden=false;
  document.getElementById('installClose').addEventListener('click',function(){tip.hidden=true;try{localStorage.setItem('puntoapunto.installTip','1');}catch(e){}});
  // Pide al navegador que no borre los partidos guardados
  try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist();}catch(e){}
  if('serviceWorker' in navigator){window.addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){});});}
})();
</script>
"""

i = src.index('<div class="wrap">')
out = head + src[:i] + '</head>\n<body>\n' + src[i:] + pwa_tail + '</body>\n</html>\n'
(site / 'index.html').write_text(out, encoding='utf-8')

manifest = {
    "name": "Punto a Punto",
    "short_name": "Punto a Punto",
    "description": "Análisis de partidos de tenis punto a punto",
    "lang": "es",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#e8eee9",
    "theme_color": "#1b5a3d",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
(site / 'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

files = ['./', 'index.html', 'manifest.webmanifest'] + \
    [f'fonts/{p.name}' for p in sorted((site / 'fonts').iterdir()) if p.suffix == '.woff2'] + \
    [f'icons/{p.name}' for p in sorted((site / 'icons').iterdir())]
sw = """// Guarda la app en el dispositivo para que funcione sin internet.
const CACHE = 'puntoapunto-%s';
const FILES = %s;
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (req.mode === 'navigate') {
    // La página: primero la versión nueva si hay conexión; si no, la guardada.
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put('index.html', copy)); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req)));
});
""" % (version, json.dumps(files))
(site / 'sw.js').write_text(sw, encoding='utf-8')
(site / '.nojekyll').write_text('', encoding='utf-8')
print('ok', version, len(out))

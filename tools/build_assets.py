"""Genera app/src/main/assets/index.html a partir de web/punto-a-punto.html.
Añade la cabecera HTML completa y sustituye Google Fonts por las fuentes locales (funciona sin internet)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'web' / 'punto-a-punto.html').read_text(encoding='utf-8')
fonts = """<style>
@font-face{font-family:"Barlow";font-weight:400;font-display:swap;src:url(fonts/barlow-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow";font-weight:500;font-display:swap;src:url(fonts/barlow-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow";font-weight:600;font-display:swap;src:url(fonts/barlow-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow";font-weight:700;font-display:swap;src:url(fonts/barlow-latin-700-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow Condensed";font-weight:600;font-display:swap;src:url(fonts/barlow-condensed-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Barlow Condensed";font-weight:700;font-display:swap;src:url(fonts/barlow-condensed-latin-700-normal.woff2) format("woff2")}
</style>"""
src = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', fonts, src)
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
head = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
"""
i = src.index('<div class="wrap">')
out = head + src[:i] + '</head>\n<body>\n' + src[i:] + '\n</body>\n</html>\n'
(root / 'app' / 'src' / 'main' / 'assets' / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out))

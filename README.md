# Punto a Punto

App de Android para analizar partidos de tenis punto a punto, inspirada en la antigua app «Pasa la Red».

Cada punto se anota en cuatro pasos, para los dos jugadores:

1. **Saque**: ace, falta / doble falta, o saque dentro (1.º o 2.º).
2. **Cómo termina**: ganador, error forzado o error no forzado, y de qué jugador.
3. **Situación**: resto, ataque, defensa o peloteo.
4. **Golpe**: derecha, revés, dejadas, aproximaciones, voleas, remate o globos.

Con eso calcula estadísticas básicas (ganadores, errores, % de productividad), saque y resto, y un análisis táctico de rally, ataque y defensa. Los partidos se pueden exportar a Excel.

## Descargar

- **Android**: [PuntoAPunto.apk](https://github.com/raulpicogonzalez/punto-a-punto/releases/download/apk/PuntoAPunto.apk). Ábrelo en el móvil e instálalo (acepta «permitir apps de origen desconocido»).
- **iPhone** (y también Android u ordenador): abre **https://raulpicogonzalez.github.io/punto-a-punto/** en **Safari**, pulsa **Compartir** y luego **«Añadir a pantalla de inicio»**. Usa siempre la app desde ese icono: funciona sin internet y guarda ahí los partidos.

Las dos versiones se actualizan solas cada vez que cambia el código (pestaña *Actions*).

## Estructura

- `web/punto-a-punto.html`: la app (HTML + JavaScript, sin dependencias).
- `tools/build_assets.py`: copia la app a `app/src/main/assets/index.html` con las fuentes locales para que funcione sin internet.
- `app/`: proyecto Android (WebView) que muestra la app a pantalla completa.
- `tools/build_web.py`: genera la versión web instalable (`site/`), con icono, manifest y modo sin conexión, que se publica en GitHub Pages.

Fuentes: Barlow y Barlow Condensed (SIL Open Font License).

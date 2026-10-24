<h1 align="center">fravelz-tts</h1>

<p align="center">
  <img src="assets/readme-hero.jpg" alt="Banner navy y cian de la app de voz" width="100%">
</p>

<p align="center">Texto a voz en el escritorio. Hace ese trabajo y no es una pieza pública.</p>

App PySide6. Voces en línea con edge-tts y voces locales con Piper. La interfaz usa navy y cian `#00d4ff`. La salida cae en `~/Videos/recursos/tts/`.

<p align="center">
  <a href="https://skillicons.dev">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=py,linux&theme=dark&perline=6">
      <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=py,linux&theme=light&perline=6">
      <img alt="Python, Linux" src="https://skillicons.dev/icons?i=py,linux&perline=6">
    </picture>
  </a>
</p>

## Características

- Texto a voz en el escritorio, en línea y sin red.
- Instalador en `scripts/install.sh`.
- Pieza de uso propio, no un producto para enseñar.

> [!NOTE]
> Hace el trabajo de leer un guion en voz alta. No es una pieza de portafolio.

## Tecnologías

- **Python y PySide6** — la ventana.
- **edge-tts** — voces neurales, sin API key.
- **Piper** — dos voces en español, en local.

## Inicio rápido

```bash
bash scripts/install.sh
fravelz-tts
```

> [!IMPORTANT]
> Hace falta Python 3.11 o superior. La primera vez, Piper descarga voces y pide red.

## Uso

Pega el guion, elige en línea o local, y genera. El archivo queda en `~/Videos/recursos/tts/`.

También arranca con `.venv/bin/python -m fravelz_tts` desde la carpeta del repo.

> [!TIP]
> `bash scripts/install-voices.sh` baja solo las voces Piper si el entorno ya existe.

## Contribuir

Repositorio de [FraVelz](https://github.com/FraVelz). El remoto está en Fravelz-Setup.

## Licencia

Este repositorio no incluye un archivo de licencia. El uso previsto es personal.

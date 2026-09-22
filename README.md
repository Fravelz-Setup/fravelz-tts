# fravelz-tts

App de escritorio (PySide6) para **texto → voz** rápido.

- **Online:** voces neurales Microsoft vía `edge-tts` (gratis, sin API key) — español LatAm (CO, MX, AR, US).
- **Offline:** [Piper](https://github.com/rhasspy/piper) con 2 voces ES.
- UI paleta **Jarvis** (navy + cyan `#00d4ff`).
- Salida por defecto: `~/Videos/recursos/tts/`.

## Requisitos

- Python 3.11+
- Arch/Linux con PySide6 (se instala en el venv)
- Red para voces online y para la primera descarga de Piper

## Instalación

```bash
cd ~/Documentos/personal/fravelz-tts
bash scripts/install.sh
```

Eso crea `.venv`, instala dependencias, descarga Piper + voces ES, enlaza `~/.local/bin/fravelz-tts` y registra el `.desktop`.

Lanzar:

```bash
fravelz-tts
# o
cd ~/Documentos/personal/fravelz-tts && .venv/bin/python -m fravelz_tts
```

Solo voces Piper (si ya tienes el venv):

```bash
bash scripts/install-voices.sh
```

## Uso

1. Pega el guion.
2. Elige **Online** u **Offline** y una voz.
3. Ajusta velocidad % (solo Online).
4. **Generar** → guarda en `~/Videos/recursos/tts/` y reproduce.
5. **Guardar como…** / **Abrir carpeta** según necesites.

## Desarrollo

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python -m fravelz_tts
```

## Licencia

Uso personal.

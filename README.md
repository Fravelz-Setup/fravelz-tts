# fravelz-tts


Aplicación de escritorio para pasar texto a voz. En línea usa voces de edge-tts. Sin red usa Piper. La interfaz sigue la paleta del asistente Jarvis.

| | |
| --- | --- |
| Autor | [Fravelz](https://github.com/FraVelz) |
| Licencia | No hay archivo de licencia en el repositorio. |

## Tecnologías

- Python 3.11+
- PySide6
- edge-tts
- Piper (motor offline, fuera del paquete Python)

## Estructura base

Esqueleto del repositorio. El contenido interno cambia; estas piezas se mantienen.

```text
src/fravelz_tts/    aplicación
scripts/            instalación local
assets/             recursos de interfaz
```

## Puesta en marcha

```bash
bash scripts/install.sh
fravelz-tts
```

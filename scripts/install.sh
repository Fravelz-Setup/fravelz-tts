#!/usr/bin/env bash
# Install fravelz-tts for local use: venv, deps, Piper voices, PATH, .desktop
set -euo pipefail

SOURCE="${BASH_SOURCE[0]}"
while [[ -L "$SOURCE" ]]; do
  DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
ROOT="$(cd "$(dirname "$SOURCE")/.." && pwd)"
cd "$ROOT"

echo "==> venv"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -U pip
pip install -e .

echo "==> Piper + voces ES"
bash "$ROOT/scripts/install-voices.sh"

echo "==> salida de audio"
mkdir -p "$HOME/Videos/recursos/tts"

echo "==> launcher"
chmod +x "$ROOT/scripts/fravelz-tts"
mkdir -p "$HOME/.local/bin"
ln -sfn "$ROOT/scripts/fravelz-tts" "$HOME/.local/bin/fravelz-tts"

echo "==> .desktop"
mkdir -p "$HOME/.local/share/applications"
DESKTOP_SRC="$ROOT/assets/fravelz-tts.desktop"
DESKTOP_DST="$HOME/.local/share/applications/fravelz-tts.desktop"
sed "s|@EXEC@|$HOME/.local/bin/fravelz-tts|g; s|@ROOT@|$ROOT|g" "$DESKTOP_SRC" > "$DESKTOP_DST"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo ""
echo "Listo. Lanza: fravelz-tts"
echo "O desde el menú de aplicaciones: Fravelz TTS"
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo "Aviso: $HOME/.local/bin no está en PATH; añádelo a tu shell."
fi

#!/usr/bin/env bash
# Download Piper binary + Spanish ONNX voices into ~/.local/share/fravelz-tts/piper/
set -euo pipefail

SHARE="${XDG_DATA_HOME:-$HOME/.local/share}/fravelz-tts/piper"
mkdir -p "$SHARE"

ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) PIPER_ASSET="piper_linux_x86_64.tar.gz" ;;
  aarch64|arm64) PIPER_ASSET="piper_linux_aarch64.tar.gz" ;;
  *)
    echo "Arquitectura no soportada: $ARCH" >&2
    exit 1
    ;;
esac

PIPER_VER="2023.11.14-2"
PIPER_URL="https://github.com/rhasspy/piper/releases/download/${PIPER_VER}/${PIPER_ASSET}"

if [[ ! -x "$SHARE/piper" ]]; then
  echo "Descargando Piper (${PIPER_ASSET})…"
  TMP="$(mktemp -d)"
  trap 'rm -rf "$TMP"' EXIT
  curl -fsSL -o "$TMP/piper.tgz" "$PIPER_URL"
  tar -xzf "$TMP/piper.tgz" -C "$TMP"
  # Archive contains a top-level directory named "piper/"
  if [[ -x "$TMP/piper/piper" ]]; then
    # Move binary + libs into SHARE (flat)
    shopt -s dotglob
    mv "$TMP/piper"/* "$SHARE/"
    shopt -u dotglob
  else
    echo "Estructura de tarball inesperada" >&2
    find "$TMP" -maxdepth 3 >&2
    exit 1
  fi
  chmod +x "$SHARE/piper"
  rm -rf "$TMP"
  trap - EXIT
fi

if [[ ! -x "$SHARE/piper" ]]; then
  echo "No se encontró el binario piper en $SHARE" >&2
  ls -la "$SHARE" >&2 || true
  exit 1
fi

HF="https://huggingface.co/rhasspy/piper-voices/resolve/main"

download_voice() {
  local rel="$1"   # e.g. es/es_ES/davefx/medium/es_ES-davefx-medium
  local stem
  stem="$(basename "$rel")"
  if [[ -f "$SHARE/${stem}.onnx" && -f "$SHARE/${stem}.onnx.json" ]]; then
    echo "OK ${stem}"
    return 0
  fi
  echo "Descargando ${stem}…"
  curl -fsSL -o "$SHARE/${stem}.onnx" "${HF}/${rel}.onnx"
  curl -fsSL -o "$SHARE/${stem}.onnx.json" "${HF}/${rel}.onnx.json"
}

# Male ES + female-leaning ES (MLS)
download_voice "es/es_ES/davefx/medium/es_ES-davefx-medium"
download_voice "es/es_ES/mls_9972/low/es_ES-mls_9972-low"

echo "Piper listo en $SHARE"
# Libs live next to the binary; ensure runtime finds them
export LD_LIBRARY_PATH="$SHARE${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
"$SHARE/piper" --help 2>&1 | head -5 || true

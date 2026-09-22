"""Piper offline TTS via local binary + onnx models."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from fravelz_tts.paths import piper_binary, piper_dir


class PiperError(RuntimeError):
    pass


def is_available() -> bool:
    return piper_binary().is_file() and piper_binary().stat().st_size > 0


def model_path(model_stem: str) -> Path:
    return piper_dir() / f"{model_stem}.onnx"


def model_ready(model_stem: str) -> bool:
    onnx = model_path(model_stem)
    cfg = Path(str(onnx) + ".json")
    return onnx.is_file() and cfg.is_file()


def synthesize(text: str, model_stem: str, out: Path) -> Path:
    """Write WAV to ``out`` using Piper. Raises PiperError on failure."""
    binary = piper_binary()
    if not binary.is_file():
        raise PiperError(
            "Piper no instalado. Ejecuta scripts/install.sh o install-voices.sh."
        )
    onnx = model_path(model_stem)
    if not model_ready(model_stem):
        raise PiperError(
            f"Modelo ausente: {model_stem}. Ejecuta scripts/install-voices.sh."
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(binary),
        "--model",
        str(onnx),
        "--output_file",
        str(out),
    ]
    espeak = piper_dir() / "espeak-ng-data"
    if espeak.is_dir():
        cmd.extend(["--espeak_data", str(espeak)])

    env = os.environ.copy()
    lib_dir = str(piper_dir())
    prev = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = lib_dir if not prev else f"{lib_dir}:{prev}"

    try:
        proc = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            capture_output=True,
            check=False,
            timeout=120,
            env=env,
        )
    except FileNotFoundError as exc:
        raise PiperError(f"No se pudo ejecutar Piper: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise PiperError("Piper tardó demasiado.") from exc

    if proc.returncode != 0 or not out.is_file():
        err = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace")
        raise PiperError(err.strip() or f"Piper falló (code {proc.returncode})")

    return out


def which_piper() -> str | None:
    if is_available():
        return str(piper_binary())
    return shutil.which("piper")

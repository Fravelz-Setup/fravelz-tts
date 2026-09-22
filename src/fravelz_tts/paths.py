"""Data and output directories."""

from __future__ import annotations

from pathlib import Path


def home() -> Path:
    return Path.home()


def data_dir() -> Path:
    p = home() / ".local" / "share" / "fravelz-tts"
    p.mkdir(parents=True, exist_ok=True)
    return p


def piper_dir() -> Path:
    p = data_dir() / "piper"
    p.mkdir(parents=True, exist_ok=True)
    return p


def default_output_dir() -> Path:
    p = home() / "Videos" / "recursos" / "tts"
    p.mkdir(parents=True, exist_ok=True)
    return p


def piper_binary() -> Path:
    return piper_dir() / "piper"

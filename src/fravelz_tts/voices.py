"""Curated Spanish LatAm voices (online edge-tts + offline Piper)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EngineKind(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"


@dataclass(frozen=True)
class Voice:
    id: str
    label: str
    gender: str  # "H" | "M"
    engine: EngineKind
    # Piper: relative model stem under piper_dir (without .onnx)
    piper_model: str | None = None


ONLINE_VOICES: tuple[Voice, ...] = (
    Voice("es-CO-GonzaloNeural", "Colombia · Gonzalo (H)", "H", EngineKind.ONLINE),
    Voice("es-CO-SalomeNeural", "Colombia · Salomé (M)", "M", EngineKind.ONLINE),
    Voice("es-MX-JorgeNeural", "México · Jorge (H)", "H", EngineKind.ONLINE),
    Voice("es-MX-DaliaNeural", "México · Dalia (M)", "M", EngineKind.ONLINE),
    Voice("es-AR-TomasNeural", "Argentina · Tomás (H)", "H", EngineKind.ONLINE),
    Voice("es-AR-ElenaNeural", "Argentina · Elena (M)", "M", EngineKind.ONLINE),
    Voice("es-US-AlonsoNeural", "EE.UU. · Alonso (H)", "H", EngineKind.ONLINE),
    Voice("es-US-PalomaNeural", "EE.UU. · Paloma (M)", "M", EngineKind.ONLINE),
)

# Piper: davefx = male ES; mls_9972 = female-leaning ES (MLS)
OFFLINE_VOICES: tuple[Voice, ...] = (
    Voice(
        "piper-davefx",
        "Offline · Dave (H, ES)",
        "H",
        EngineKind.OFFLINE,
        piper_model="es_ES-davefx-medium",
    ),
    Voice(
        "piper-mls9972",
        "Offline · MLS 9972 (M, ES)",
        "M",
        EngineKind.OFFLINE,
        piper_model="es_ES-mls_9972-low",
    ),
)


def voices_for(engine: EngineKind) -> tuple[Voice, ...]:
    if engine is EngineKind.ONLINE:
        return ONLINE_VOICES
    return OFFLINE_VOICES


def find_voice(voice_id: str) -> Voice | None:
    for v in (*ONLINE_VOICES, *OFFLINE_VOICES):
        if v.id == voice_id:
            return v
    return None

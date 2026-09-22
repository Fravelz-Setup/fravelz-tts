"""edge-tts online synthesis."""

from __future__ import annotations

import asyncio
from pathlib import Path


def _rate_string(percent: int) -> str:
    """Map UI percent (50–200, 100=normal) to edge-tts rate like '+0%' / '-20%'."""
    delta = percent - 100
    if delta >= 0:
        return f"+{delta}%"
    return f"{delta}%"


async def _synthesize_async(text: str, voice: str, out: Path, rate_percent: int) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=_rate_string(rate_percent))
    await communicate.save(str(out))


def synthesize(text: str, voice: str, out: Path, rate_percent: int = 100) -> Path:
    """Write MP3 to ``out``. Raises on network/API failure."""
    out.parent.mkdir(parents=True, exist_ok=True)
    asyncio.run(_synthesize_async(text, voice, out, rate_percent))
    return out

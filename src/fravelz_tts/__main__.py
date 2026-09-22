"""CLI entry: python -m fravelz_tts"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    src = Path(__file__).resolve().parents[1]
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def main() -> None:
    _ensure_src_on_path()
    from fravelz_tts.app import run

    raise SystemExit(run())


if __name__ == "__main__":
    main()

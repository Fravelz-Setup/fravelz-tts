"""Main fravelz-tts window."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from fravelz_tts.engines import edge as edge_engine
from fravelz_tts.engines import piper as piper_engine
from fravelz_tts.paths import default_output_dir
from fravelz_tts.player import AudioPlayer
from fravelz_tts.theme import WINDOW_HEIGHT, WINDOW_WIDTH, apply_appearance
from fravelz_tts.voices import EngineKind, Voice, voices_for


class SynthWorker(QThread):
    done = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        text: str,
        voice: Voice,
        out: Path,
        rate_percent: int,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._text = text
        self._voice = voice
        self._out = out
        self._rate = rate_percent

    def run(self) -> None:
        try:
            if self._voice.engine is EngineKind.ONLINE:
                edge_engine.synthesize(
                    self._text, self._voice.id, self._out, self._rate
                )
            else:
                assert self._voice.piper_model
                piper_engine.synthesize(
                    self._text, self._voice.piper_model, self._out
                )
            self.done.emit(str(self._out))
        except Exception as exc:  # noqa: BLE001 — surface to UI
            self.failed.emit(str(exc))


def _slug(text: str, max_len: int = 40) -> str:
    s = re.sub(r"\s+", "-", text.strip().lower())
    s = re.sub(r"[^a-z0-9áéíóúñ\-]", "", s)
    s = s.strip("-")[:max_len] or "tts"
    return s


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("root")
        self.setWindowTitle("fravelz-tts")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._last_file: Path | None = None
        self._worker: SynthWorker | None = None
        self._player = AudioPlayer(self)
        self._player.error.connect(lambda m: self._set_status(m, error=True))

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 16)
        root.setSpacing(12)

        title = QLabel("FRAVELZ TTS")
        title.setObjectName("title")
        root.addWidget(title)

        sub = QLabel("Texto → voz · online (edge) / offline (Piper) · español LatAm")
        sub.setObjectName("subtitle")
        root.addWidget(sub)

        self.script = QTextEdit()
        self.script.setObjectName("script")
        self.script.setPlaceholderText("Pega aquí el guion…")
        root.addWidget(self.script, stretch=1)

        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        tb = QVBoxLayout(toolbar)
        tb.setSpacing(10)

        row_engine = QHBoxLayout()
        row_engine.addWidget(QLabel("Motor:"))
        self.radio_online = QRadioButton("Online")
        self.radio_offline = QRadioButton("Offline")
        self.radio_online.setChecked(True)
        self._engine_group = QButtonGroup(self)
        self._engine_group.addButton(self.radio_online)
        self._engine_group.addButton(self.radio_offline)
        row_engine.addWidget(self.radio_online)
        row_engine.addWidget(self.radio_offline)
        row_engine.addStretch()
        tb.addLayout(row_engine)

        row_voice = QHBoxLayout()
        row_voice.addWidget(QLabel("Voz:"))
        self.voice_combo = QComboBox()
        row_voice.addWidget(self.voice_combo, stretch=1)
        tb.addLayout(row_voice)

        row_rate = QHBoxLayout()
        row_rate.addWidget(QLabel("Velocidad %:"))
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 200)
        self.rate_spin.setValue(100)
        self.rate_spin.setSingleStep(5)
        self.rate_spin.setToolTip("Solo afecta motor Online (edge-tts)")
        row_rate.addWidget(self.rate_spin)
        row_rate.addStretch()
        tb.addLayout(row_rate)

        row_btn = QHBoxLayout()
        self.btn_generate = QPushButton("Generar")
        self.btn_generate.setObjectName("primary")
        self.btn_play = QPushButton("Play")
        self.btn_stop = QPushButton("Stop")
        self.btn_save = QPushButton("Guardar como…")
        self.btn_folder = QPushButton("Abrir carpeta")
        row_btn.addWidget(self.btn_generate)
        row_btn.addWidget(self.btn_play)
        row_btn.addWidget(self.btn_stop)
        row_btn.addWidget(self.btn_save)
        row_btn.addWidget(self.btn_folder)
        tb.addLayout(row_btn)

        root.addWidget(toolbar)

        self.status = QLabel("Listo")
        self.status.setObjectName("status")
        root.addWidget(self.status)

        self.radio_online.toggled.connect(self._refresh_voices)
        self.btn_generate.clicked.connect(self._on_generate)
        self.btn_play.clicked.connect(self._on_play)
        self.btn_stop.clicked.connect(lambda: self._player.stop())
        self.btn_save.clicked.connect(self._on_save_as)
        self.btn_folder.clicked.connect(self._on_open_folder)

        self._refresh_voices()
        self._set_status("Listo · salida: " + str(default_output_dir()))

    def _engine(self) -> EngineKind:
        return EngineKind.ONLINE if self.radio_online.isChecked() else EngineKind.OFFLINE

    def _refresh_voices(self) -> None:
        self.voice_combo.clear()
        for v in voices_for(self._engine()):
            self.voice_combo.addItem(v.label, v)
        offline = self._engine() is EngineKind.OFFLINE
        self.rate_spin.setEnabled(not offline)
        if offline and not piper_engine.is_available():
            self._set_status(
                "Piper no instalado — ejecuta scripts/install.sh",
                error=True,
            )

    def _current_voice(self) -> Voice:
        return self.voice_combo.currentData()

    def _set_status(self, msg: str, *, ok: bool = False, error: bool = False) -> None:
        self.status.setText(msg)
        self.status.setProperty("ok", "true" if ok else "false")
        self.status.setProperty("error", "true" if error else "false")
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def _on_generate(self) -> None:
        text = self.script.toPlainText().strip()
        if not text:
            self._set_status("Escribe o pega texto primero", error=True)
            return
        voice = self._current_voice()
        if voice is None:
            self._set_status("Selecciona una voz", error=True)
            return

        if voice.engine is EngineKind.OFFLINE:
            if not piper_engine.is_available():
                self._set_status(
                    "Piper no instalado. Usa Online o scripts/install.sh",
                    error=True,
                )
                return
            assert voice.piper_model
            if not piper_engine.model_ready(voice.piper_model):
                self._set_status(
                    f"Falta modelo {voice.piper_model}. Ejecuta install-voices.sh",
                    error=True,
                )
                return

        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        ext = ".mp3" if voice.engine is EngineKind.ONLINE else ".wav"
        name = f"{stamp}-{_slug(text)}{ext}"
        out = default_output_dir() / name

        self.btn_generate.setEnabled(False)
        self._set_status("Generando…")
        self._worker = SynthWorker(text, voice, out, self.rate_spin.value(), self)
        self._worker.done.connect(self._on_synth_done)
        self._worker.failed.connect(self._on_synth_fail)
        self._worker.finished.connect(lambda: self.btn_generate.setEnabled(True))
        self._worker.start()

    def _on_synth_done(self, path_str: str) -> None:
        self._last_file = Path(path_str)
        self._set_status(f"Listo · {self._last_file.name}", ok=True)
        self._player.play(self._last_file)

    def _on_synth_fail(self, msg: str) -> None:
        hint = msg
        if self._engine() is EngineKind.ONLINE and (
            "network" in msg.lower()
            or "connect" in msg.lower()
            or "timeout" in msg.lower()
            or "Temporary failure" in msg
        ):
            hint = f"{msg} — prueba Offline si no hay red"
        self._set_status(hint, error=True)

    def _on_play(self) -> None:
        if not self._last_file or not self._last_file.is_file():
            self._set_status("No hay audio generado aún", error=True)
            return
        self._player.play(self._last_file)

    def _on_save_as(self) -> None:
        if not self._last_file or not self._last_file.is_file():
            self._set_status("Genera audio primero", error=True)
            return
        dest, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar audio",
            str(default_output_dir() / self._last_file.name),
            "Audio (*.mp3 *.wav);;Todos (*)",
        )
        if not dest:
            return
        shutil.copy2(self._last_file, dest)
        self._set_status(f"Guardado · {dest}", ok=True)

    def _on_open_folder(self) -> None:
        folder = default_output_dir()
        if shutil.which("xdg-open"):
            subprocess.Popen(["xdg-open", str(folder)])  # noqa: S603
        else:
            QMessageBox.information(self, "Carpeta", str(folder))


def run() -> int:
    os.environ.setdefault("QT_NO_SYNTHESIZED_BOLD", "1")
    app = QApplication.instance() or QApplication([])
    font = QFont("Noto Sans", 13)
    app.setFont(font)
    apply_appearance(app)
    win = MainWindow()
    win.show()
    return app.exec()

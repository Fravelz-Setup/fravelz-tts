"""Jarvis navy + cyan palette (from fravelz-jarvis)."""

from __future__ import annotations

BG = "#050a14"
BG_ELEV = "#0a1220"
BG_PANEL = "#0e1a2e"
BG_CARD = "#122038"
FG = "#e8f4ff"
FG_DIM = "#8aa4c0"
FG_MUTED = "#5a7390"
ACCENT = "#00d4ff"
ACCENT_BRIGHT = "#5cefff"
ACCENT_SOFT = "#0d2a3d"
BORDER = "#1a3050"
BORDER_SUBTLE = "#243d5c"
ON_PRIMARY = "#031018"
DANGER = "#e05a6a"
OK = "#3d9a7a"

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 640
FONT_FAMILY = "JetBrains Mono Nerd Font"
FONT_FALLBACK = "JetBrains Mono"
FONT_UI = "Noto Sans"


def apply_appearance(app) -> None:
    """Fusion + palette so QSS text colors win over the desktop theme."""
    from PySide6.QtGui import QColor, QPalette

    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(BG))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(FG))
    pal.setColor(QPalette.ColorRole.Base, QColor(BG_PANEL))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor(BG_CARD))
    pal.setColor(QPalette.ColorRole.Text, QColor(FG))
    pal.setColor(QPalette.ColorRole.Button, QColor(BG_CARD))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(FG))
    pal.setColor(QPalette.ColorRole.BrightText, QColor(ACCENT_BRIGHT))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor(ON_PRIMARY))
    pal.setColor(QPalette.ColorRole.PlaceholderText, QColor(FG_MUTED))
    pal.setColor(QPalette.ColorRole.ToolTipBase, QColor(BG_CARD))
    pal.setColor(QPalette.ColorRole.ToolTipText, QColor(FG))
    pal.setColor(QPalette.ColorRole.Link, QColor(ACCENT))
    app.setPalette(pal)
    app.setStyleSheet(stylesheet())


def stylesheet() -> str:
    return f"""
    QWidget {{
        color: {FG};
        font-family: "{FONT_UI}", sans-serif;
        font-size: 13px;
    }}
    QWidget#root {{
        background-color: {BG};
        color: {FG};
    }}
    QLabel {{
        color: {FG};
        background-color: transparent;
    }}
    QLabel#title {{
        color: {ACCENT};
        font-family: "{FONT_FAMILY}", "{FONT_FALLBACK}", monospace;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 0.6px;
    }}
    QLabel#subtitle, QLabel#hint {{
        color: {FG_DIM};
        font-size: 12px;
    }}
    QLabel#status {{
        color: {FG_DIM};
        font-size: 12px;
        padding: 6px 2px;
    }}
    QLabel#status[ok="true"] {{
        color: {OK};
    }}
    QLabel#status[error="true"] {{
        color: {DANGER};
    }}
    QTextEdit#script {{
        background-color: {BG_PANEL};
        color: {FG};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 12px;
        selection-background-color: {ACCENT};
        selection-color: {ON_PRIMARY};
        font-size: 14px;
    }}
    QComboBox, QSpinBox {{
        background-color: {BG_CARD};
        color: {FG};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 6px 10px;
        min-height: 28px;
    }}
    QComboBox:hover, QSpinBox:hover {{
        border-color: {ACCENT};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {BG_PANEL};
        color: {FG};
        border: 1px solid {BORDER};
        selection-background-color: {ACCENT};
        selection-color: {ON_PRIMARY};
    }}
    QRadioButton {{
        color: {FG};
        spacing: 8px;
    }}
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid {BORDER_SUBTLE};
        background: {BG_ELEV};
    }}
    QRadioButton::indicator:checked {{
        border-color: {ACCENT};
        background: {ACCENT};
    }}
    QPushButton {{
        background-color: {ACCENT_SOFT};
        color: {ACCENT_BRIGHT};
        border: 1px solid {ACCENT};
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        min-height: 32px;
    }}
    QPushButton:hover {{
        background-color: {ACCENT};
        color: {ON_PRIMARY};
    }}
    QPushButton:pressed {{
        background-color: {BG_CARD};
        color: {ACCENT};
    }}
    QPushButton:disabled {{
        background-color: {BG_ELEV};
        color: {FG_MUTED};
        border-color: {BORDER};
    }}
    QPushButton#primary {{
        background-color: {ACCENT};
        color: {ON_PRIMARY};
        border: none;
        font-weight: 600;
    }}
    QPushButton#primary:hover {{
        background-color: {ACCENT_BRIGHT};
    }}
    QPushButton#primary:disabled {{
        background-color: {BORDER};
        color: {FG_MUTED};
    }}
    QFrame#toolbar {{
        background-color: {BG_ELEV};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 8px;
    }}
    """

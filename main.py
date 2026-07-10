"""Lispr Flow's lightweight PySide6 visual prototype.

The app intentionally does not record audio, persist API keys, authenticate users,
or open a billing portal yet. It is the native desktop foundation for those features.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


APP_NAME = "Lispr Flow"
BRAND_MARK = "lispr flow"
GITHUB_URL = "https://github.com/prshv1/Lispr"

# Colors that hold constant across both themes — the lime accent and the
# record panel, which is meant to read like a fixed "stage" element regardless
# of light/dark mode.
LIME = "#D5F06F"
BUTTON_INK = "#14130F"
BLUE = "#5B8CFF"
CLAY = "#E2775A"
RECORD_BG = "#0F0F0B"
RECORD_BORDER = "#2A2A22"
RECORD_INK = "#F2EEE1"
RECORD_MUTED = "#8B8677"
RECORD_ACCENT = "#9CB35B"

# Everything else swaps per theme.
THEMES = {
    "dark": {
        "BG": "#0A0A08",
        "PANEL": "#131310",
        "PANEL_ALT": "#181812",
        "INK": "#F2EEE1",
        "INK_SOFT": "#B8B29C",
        "MUTED": "#726C5C",
        "BORDER": "#242419",
        "BORDER_STRONG": "#3A3A2C",
        "ACCENT_TEXT": "#9CB35B",
        "DANGER_HOVER": "#241512",
    },
    "light": {
        "BG": "#F4F1EA",
        "PANEL": "#FFFDF6",
        "PANEL_ALT": "#F2ECDC",
        "INK": "#14130F",
        "INK_SOFT": "#39362E",
        "MUTED": "#706B5E",
        "BORDER": "#E7DFCC",
        "BORDER_STRONG": "#D8CFBC",
        "ACCENT_TEXT": "#5C6B34",
        "DANGER_HOVER": "#FBE5DD",
    },
}


def font_family(preferred: str, fallback: str) -> str:
    """Use bundled design fonts when available, with an Ubuntu-safe fallback."""
    return preferred if preferred in QFontDatabase().families() else fallback


class LisprFlow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 760)
        self.setMinimumSize(980, 660)
        self.recording = False
        self.recording_seconds = 0
        self.light_mode = False
        self.active_setting = "General"
        self.recordings = [
            ("today, 11:42", "I need to turn the project notes into a small next-steps list: finish the history view, test it on Ubuntu, and decide which transcription provider to start with."),
            ("yesterday, 17:16", "The Linux version should feel native and stay light. I want the first release to support Ubuntu well, while keeping the code portable to other distributions."),
            ("yesterday, 10:08", "Quick stand-up: the layout is in place, invite links work, and the next thing to prototype is showing the full text from each recording."),
            ("monday, 15:29", "Ideas to revisit later: a global shortcut, microphone selection, and a simple way to export or copy a transcript."),
        ]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick_recording)

        self._configure_window()
        self._build_shell()
        for button in self.findChildren(QPushButton):
            button.setFocusPolicy(Qt.NoFocus)
        self._show_page("home")

    def _configure_window(self) -> None:
        self.display_font = font_family("Fraunces", "DejaVu Serif")
        self.body_font = font_family("Afacad", "Noto Sans")
        self.mono_font = font_family("IBM Plex Mono", "DejaVu Sans Mono")
        QApplication.instance().setStyleSheet(self._build_stylesheet(THEMES["dark"]))

    def _build_stylesheet(self, p: dict) -> str:
        display, body, mono = self.display_font, self.body_font, self.mono_font
        return f"""
            * {{ font-family: '{body}'; color: {p['INK']}; }}
            QMainWindow, QWidget#app {{ background: {p['BG']}; }}
            QFrame#sidebar {{ background: {p['BG']}; border-right: 1px solid {p['BORDER']}; }}
            QFrame#content {{ background: {p['BG']}; }}
            QLabel#eyebrow {{ font-family: '{mono}'; color: {p['MUTED']}; font-size: 11px; font-weight: 500; letter-spacing: 1.6px; }}
            QLabel#pageTitle {{ font-family: '{display}'; color: {p['INK']}; font-size: 40px; font-weight: 500; font-style: italic; letter-spacing: -0.5px; }}
            QLabel#sectionTitle {{ font-family: '{display}'; color: {p['INK']}; font-size: 22px; font-weight: 500; }}
            QLabel#muted {{ color: {p['MUTED']}; font-size: 14px; }}
            QLabel#smallMuted {{ font-family: '{mono}'; color: {p['MUTED']}; font-size: 11px; }}
            QLabel#timer {{ font-family: '{mono}'; color: {LIME}; font-size: 18px; font-weight: 700; }}
            QLabel#statNumber {{ font-family: '{display}'; color: {p['INK']}; font-size: 30px; font-weight: 500; }}
            QLabel#statLabel {{ font-family: '{mono}'; color: {p['INK_SOFT']}; font-size: 11px; font-weight: 500; letter-spacing: 0.6px; }}
            QLabel#brandName {{ font-family: '{display}'; color: {p['INK']}; font-size: 20px; font-weight: 500; font-style: italic; }}
            QLabel#brandMark {{ background: {LIME}; color: {BUTTON_INK}; border-radius: 3px; font-family: '{mono}'; font-weight: 800; font-size: 15px; }}
            QLabel#previewBadge {{ font-family: '{mono}'; color: {p['ACCENT_TEXT']}; border: 1px solid {p['BORDER_STRONG']}; padding: 4px 8px; border-radius: 2px; font-size: 10px; font-weight: 500; letter-spacing: 0.6px; }}
            QLabel#noteTitle {{ font-family: '{mono}'; color: {p['INK_SOFT']}; font-weight: 600; font-size: 12px; }}
            QLabel#fieldLabel {{ font-family: '{mono}'; color: {p['INK_SOFT']}; font-size: 12px; font-weight: 600; letter-spacing: 0.4px; }}
            QLabel#liveLabel {{ font-family: '{mono}'; color: {RECORD_ACCENT}; font-size: 11px; font-weight: 500; letter-spacing: 0.8px; }}
            QLabel#recordStatus {{ color: {RECORD_INK}; font-family: '{display}'; font-size: 22px; font-weight: 500; font-style: italic; }}
            QLabel#shortcutHint {{ font-family: '{mono}'; color: {RECORD_MUTED}; font-size: 12px; }}
            QFrame#panel {{ background: {p['PANEL']}; border: 1px solid {p['BORDER']}; border-radius: 3px; }}
            QFrame#recordPanel {{ background: {RECORD_BG}; border: 1px solid {RECORD_BORDER}; border-radius: 3px; }}
            QFrame#notice {{ background: transparent; border: 1px dashed {p['BORDER_STRONG']}; border-radius: 3px; }}
            QFrame#divider {{ color: {p['BORDER']}; }}
            QPushButton {{ border: 0; background: transparent; padding: 9px 10px; text-align: left; border-radius: 2px; font-family: '{mono}'; font-size: 13px; color: {p['INK_SOFT']}; outline: none; }}
            QPushButton:hover {{ color: {p['INK']}; background: {p['PANEL_ALT']}; }}
            QPushButton#navButton {{ border-left: 2px solid transparent; padding-left: 12px; }}
            QPushButton#navButton:checked {{ background: transparent; color: {p['ACCENT_TEXT']}; font-weight: 700; border-left: 2px solid {LIME}; }}
            QPushButton#navButton:checked:hover {{ background: {p['PANEL_ALT']}; }}
            QPushButton#settingButton {{ border-left: 2px solid transparent; padding-left: 12px; }}
            QPushButton#settingButton:checked {{ background: transparent; color: {p['ACCENT_TEXT']}; font-weight: 700; border-left: 2px solid {LIME}; }}
            QPushButton#primaryButton {{ background: {LIME}; color: {BUTTON_INK}; font-weight: 700; padding: 11px 16px; border-radius: 2px; }}
            QPushButton#primaryButton:hover {{ background: #E4FA95; }}
            QPushButton#secondaryButton {{ background: transparent; border: 1px solid {p['BORDER_STRONG']}; color: {p['INK_SOFT']}; font-weight: 500; padding: 9px 14px; border-radius: 2px; }}
            QPushButton#secondaryButton:hover {{ border-color: {LIME}; color: {p['INK']}; background: {p['PANEL_ALT']}; }}
            QPushButton#secondaryButton[danger='true'] {{ color: {CLAY}; border-color: {CLAY}; }}
            QPushButton#secondaryButton[danger='true']:hover {{ background: {p['DANGER_HOVER']}; }}
            QPushButton#recordButton {{ background: {LIME}; color: {BUTTON_INK}; font-family: '{mono}'; font-size: 14px; font-weight: 700; padding: 13px 18px; border-radius: 2px; }}
            QPushButton#recordButton[recording='true'] {{ background: {RECORD_BG}; color: {CLAY}; border: 1px solid {CLAY}; }}
            QPushButton#themeToggle {{ border: 1px solid {p['BORDER_STRONG']}; border-radius: 16px; padding: 8px 16px; font-family: '{mono}'; font-size: 12px; font-weight: 600; color: {p['INK_SOFT']}; text-align: center; }}
            QPushButton#themeToggle:hover {{ background: {p['PANEL_ALT']}; color: {p['INK']}; }}
            QPushButton#themeToggle[active='true'] {{ background: {LIME}; color: {BUTTON_INK}; border-color: {LIME}; }}
            QPushButton#themeToggle[active='true']:hover {{ background: #E4FA95; }}
            QLineEdit, QComboBox {{ font-family: '{mono}'; font-size: 13px; background: {p['PANEL']}; color: {p['INK']}; border: 1px solid {p['BORDER_STRONG']}; border-radius: 2px; padding: 10px 12px; min-height: 21px; }}
            QLineEdit:focus, QComboBox:focus {{ border: 1px solid {LIME}; }}
            QComboBox::drop-down {{ border: 0; width: 28px; }}
            QComboBox QAbstractItemView {{ font-family: '{mono}'; font-size: 13px; background: {p['PANEL']}; color: {p['INK']}; border: 1px solid {p['BORDER_STRONG']}; outline: 0; selection-background-color: {p['PANEL_ALT']}; selection-color: {p['INK']}; padding: 4px; }}
            QComboBox QAbstractItemView::item {{ padding: 8px 10px; border: 0; min-height: 22px; }}
            QComboBox QAbstractItemView::item:hover {{ background: {p['PANEL_ALT']}; }}
            QComboBox QAbstractItemView::item:selected {{ background: {LIME}; color: {BUTTON_INK}; }}
            QListWidget {{ background: transparent; border: 0; outline: 0; }}
            QListWidget::item {{ background: {p['PANEL']}; border: 1px solid {p['BORDER']}; border-radius: 2px; margin: 0 0 8px 0; padding: 13px; color: {p['INK_SOFT']}; }}
            QListWidget::item:selected {{ background: {p['PANEL_ALT']}; border: 1px solid {LIME}; color: {p['INK']}; }}
            QScrollArea#panelScroll, QScrollArea#panelScroll > QWidget > QWidget {{ background: transparent; border: 0; }}
            QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}
            QScrollBar::handle:vertical {{ background: {p['BORDER_STRONG']}; border-radius: 4px; min-height: 28px; }}
            QScrollBar::handle:vertical:hover {{ background: {LIME}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; border: 0; background: transparent; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
            QMessageBox {{ background: {p['PANEL']}; }}
            QMessageBox QLabel {{ background: transparent; color: {p['INK']}; font-family: '{body}'; font-size: 13px; }}
            QMessageBox QPushButton {{ background: {p['PANEL_ALT']}; color: {p['INK']}; border: 1px solid {p['BORDER_STRONG']}; text-align: center; padding: 7px 18px; border-radius: 2px; min-width: 64px; outline: none; }}
            QMessageBox QPushButton:hover {{ border-color: {LIME}; color: {p['INK']}; }}
            QMessageBox QPushButton:default {{ background: {LIME}; color: {BUTTON_INK}; border-color: {LIME}; font-weight: 700; }}
        """

    def _apply_theme(self, theme_name: str) -> None:
        QApplication.instance().setStyleSheet(self._build_stylesheet(THEMES[theme_name]))
        for widget in (self.theme_toggle, self.record_button, self.delete_button):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def _toggle_theme(self) -> None:
        self.light_mode = not self.light_mode
        self.theme_toggle.setText("☀  light mode" if self.light_mode else "☾  dark mode")
        self.theme_toggle.setProperty("active", self.light_mode)
        self._apply_theme("light" if self.light_mode else "dark")

    def _build_shell(self) -> None:
        app = QWidget(objectName="app")
        self.setCentralWidget(app)
        root = QHBoxLayout(app)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame(objectName="sidebar")
        sidebar.setFixedWidth(244)
        root.addWidget(sidebar)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(20, 24, 20, 20)
        side.setSpacing(5)

        mark = QLabel("L")
        mark.setObjectName("brandMark")
        mark.setAlignment(Qt.AlignCenter)
        mark.setFixedSize(30, 30)
        brand_name = QLabel(BRAND_MARK)
        brand_name.setObjectName("brandName")
        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)
        brand_row.addWidget(mark)
        brand_row.addWidget(brand_name)
        brand_row.addStretch()
        side.addLayout(brand_row)
        side.addSpacing(48)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.home_nav = self._nav_button("01 · home", "home")
        self.settings_nav = self._nav_button("02 · settings", "settings")
        side.addWidget(self.home_nav)
        side.addWidget(self.settings_nav)
        side.addStretch()

        invite = QPushButton("→ invite a friend")
        invite.setObjectName("secondaryButton")
        invite.setToolTip("Copy the Lispr Flow project link")
        invite.clicked.connect(self._copy_invite_link)
        side.addWidget(invite)
        footer = QLabel("// a quiet tool for linux voices")
        footer.setObjectName("smallMuted")
        footer.setWordWrap(True)
        side.addWidget(footer)

        content_frame = QFrame(objectName="content")
        root.addWidget(content_frame, 1)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(46, 38, 46, 38)
        self.pages = QStackedWidget()
        content_layout.addWidget(self.pages)
        self.home_page = self._build_home_page()
        self.settings_page = self._build_settings_page()
        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.settings_page)

    def _nav_button(self, text: str, page: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self._show_page(page))
        self.nav_group.addButton(button)
        return button

    def _build_home_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QHBoxLayout()
        header.setSpacing(24)
        title_block = QVBoxLayout()
        eyebrow = QLabel("lispr flow / desktop preview")
        eyebrow.setObjectName("eyebrow")
        title_block.addWidget(eyebrow)
        title = QLabel("Speak. Keep moving.")
        title.setObjectName("pageTitle")
        title_block.addWidget(title)
        subtitle = QLabel("Your words, captured without making your desktop feel busy.")
        subtitle.setObjectName("muted")
        title_block.addWidget(subtitle)
        header.addLayout(title_block)
        header.addStretch()
        self.record_button = QPushButton("start dictation →")
        self.record_button.setObjectName("recordButton")
        self.record_button.setCursor(Qt.PointingHandCursor)
        self.record_button.clicked.connect(self._toggle_recording)
        header.addWidget(self.record_button, alignment=Qt.AlignBottom)
        layout.addLayout(header)
        layout.addSpacing(30)

        record_panel = QFrame(objectName="recordPanel")
        record_layout = QHBoxLayout(record_panel)
        record_layout.setContentsMargins(25, 22, 25, 22)
        live = QVBoxLayout()
        live_label = QLabel("// ready when you are")
        live_label.setObjectName("liveLabel")
        live.addWidget(live_label)
        self.record_status = QLabel("Press the shortcut and say what you mean.")
        self.record_status.setObjectName("recordStatus")
        live.addWidget(self.record_status)
        self.shortcut_hint = QLabel("super + space  ·  default microphone")
        self.shortcut_hint.setObjectName("shortcutHint")
        live.addWidget(self.shortcut_hint)
        record_layout.addLayout(live)
        record_layout.addStretch()
        self.record_timer = QLabel("00:00")
        self.record_timer.setObjectName("timer")
        record_layout.addWidget(self.record_timer, alignment=Qt.AlignCenter)
        layout.addWidget(record_panel)
        layout.addSpacing(28)

        content = QHBoxLayout()
        content.setSpacing(22)
        history = QFrame(objectName="panel")
        history_layout = QVBoxLayout(history)
        history_layout.setContentsMargins(22, 20, 22, 20)
        history_header = QHBoxLayout()
        history_title = QLabel("Recent words")
        history_title.setObjectName("sectionTitle")
        history_header.addWidget(history_title)
        history_header.addStretch()
        preview = QLabel("local preview")
        preview.setObjectName("previewBadge")
        history_header.addWidget(preview)
        history_layout.addLayout(history_header)
        history_description = QLabel("Select an entry to copy it or remove it from this visual history.")
        history_description.setObjectName("muted")
        history_layout.addWidget(history_description)
        history_layout.addSpacing(12)
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.SingleSelection)
        self.history_list.itemSelectionChanged.connect(self._sync_history_actions)
        history_layout.addWidget(self.history_list, 1)
        actions = QHBoxLayout()
        self.copy_button = QPushButton("copy selected")
        self.copy_button.setObjectName("secondaryButton")
        self.copy_button.clicked.connect(self._copy_selected)
        self.delete_button = QPushButton("remove")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.setProperty("danger", True)
        self.delete_button.clicked.connect(self._delete_selected)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.delete_button)
        actions.addStretch()
        history_layout.addLayout(actions)
        content.addWidget(history, 3)

        stats = QVBoxLayout()
        stats.setSpacing(12)
        stats.addWidget(self._stat_card("1,204", "words spoken", "all time"))
        stats.addWidget(self._stat_card("386", "words this week", "+18% from last week"))
        stats.addWidget(self._stat_card("142", "words per minute", "based on recent speech"))
        note = QFrame(objectName="notice")
        note_layout = QVBoxLayout(note)
        note_layout.setContentsMargins(16, 15, 16, 15)
        note_title = QLabel("// local-first foundation")
        note_title.setObjectName("noteTitle")
        note_text = QLabel("Audio capture and transcription will arrive after this desktop foundation is solid.")
        note_text.setObjectName("muted")
        note_text.setWordWrap(True)
        note_layout.addWidget(note_title)
        note_layout.addWidget(note_text)
        stats.addWidget(note)
        stats.addStretch()
        stats_widget = QWidget()
        stats_widget.setLayout(stats)
        stats_widget.setFixedWidth(235)
        content.addWidget(stats_widget)
        layout.addLayout(content, 1)
        self._render_history()
        return page

    def _stat_card(self, value: str, label: str, detail: str) -> QFrame:
        card = QFrame(objectName="panel")
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(17, 16, 17, 16)
        number = QLabel(value)
        number.setObjectName("statNumber")
        stat_label = QLabel(label)
        stat_label.setObjectName("statLabel")
        stat_detail = QLabel(detail)
        stat_detail.setObjectName("smallMuted")
        layout.addWidget(number)
        layout.addWidget(stat_label)
        layout.addWidget(stat_detail)
        return card

    def _build_settings_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        eyebrow = QLabel("control sheet")
        eyebrow.setObjectName("eyebrow")
        outer.addWidget(eyebrow)
        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        outer.addWidget(title)
        sub = QLabel("Keep Lispr Flow out of the way, but tuned to how you work.")
        sub.setObjectName("muted")
        outer.addWidget(sub)
        outer.addSpacing(28)

        layout = QHBoxLayout()
        layout.setSpacing(18)
        nav = QFrame(objectName="panel")
        nav.setFixedWidth(208)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(5)
        self.settings_group = QButtonGroup(self)
        self.settings_group.setExclusive(True)
        for name, label in (("General", "general"), ("Account", "account")):
            button = QPushButton(label)
            button.setObjectName("settingButton")
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, setting=name: self._show_setting(setting))
            self.settings_group.addButton(button)
            nav_layout.addWidget(button)
            if name == "General":
                button.setChecked(True)
        nav_layout.addStretch()
        nav_note = QLabel("// changes stay local until the real settings service exists")
        nav_note.setObjectName("smallMuted")
        nav_note.setWordWrap(True)
        nav_layout.addWidget(nav_note)
        layout.addWidget(nav)

        self.settings_stack = QStackedWidget()
        self.general_settings = self._build_general_settings()
        self.account_settings = self._build_account_settings()
        self.general_settings_page = self._scrollable(self.general_settings)
        self.account_settings_page = self._scrollable(self.account_settings)
        self.settings_stack.addWidget(self.general_settings_page)
        self.settings_stack.addWidget(self.account_settings_page)
        layout.addWidget(self.settings_stack, 1)
        outer.addLayout(layout, 1)
        return page

    def _scrollable(self, widget: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setObjectName("panelScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(widget)
        return scroll

    def _settings_panel(self) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame(objectName="panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(32, 29, 32, 29)
        layout.setSpacing(0)
        return panel, layout

    def _build_general_settings(self) -> QWidget:
        panel, layout = self._settings_panel()
        self._settings_title(layout, "General", "The few controls that matter before you start speaking.")
        self._field_label(layout, "start dictation shortcut")
        shortcut = QComboBox()
        shortcut.addItems(["Super + Space", "Ctrl + Shift + Space", "Alt + Space"])
        layout.addWidget(shortcut)
        layout.addSpacing(21)
        self._field_label(layout, "microphone")
        microphone = QComboBox()
        microphone.addItems(["Default microphone", "Built-in audio", "USB microphone"])
        layout.addWidget(microphone)
        layout.addSpacing(21)
        self._field_label(layout, "appearance")
        appearance_row = QHBoxLayout()
        appearance_label = QLabel("switch to light mode")
        appearance_label.setObjectName("muted")
        appearance_row.addWidget(appearance_label)
        appearance_row.addStretch()
        self.theme_toggle = QPushButton("☾  dark mode")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.setCursor(Qt.PointingHandCursor)
        self.theme_toggle.clicked.connect(self._toggle_theme)
        appearance_row.addWidget(self.theme_toggle)
        layout.addLayout(appearance_row)
        layout.addStretch()
        note = QFrame(objectName="notice")
        note_layout = QVBoxLayout(note)
        note_layout.setContentsMargins(16, 14, 16, 14)
        note_title = QLabel("shortcut & mic are visual for now")
        note_title.setObjectName("noteTitle")
        note_layout.addWidget(note_title)
        detail = QLabel("They define the interface contract, not a recording setting yet — appearance actually works.")
        detail.setObjectName("muted")
        detail.setWordWrap(True)
        note_layout.addWidget(detail)
        layout.addWidget(note)
        return panel

    def _build_account_settings(self) -> QWidget:
        panel, layout = self._settings_panel()
        self._settings_title(layout, "Account", "Bring your own transcription provider, or manage the Lispr Flow plan later.")
        self._field_label(layout, "account")
        account = QPushButton("manage account details")
        account.setObjectName("secondaryButton")
        account.clicked.connect(lambda: self._notice("Account management will open in your browser soon."))
        layout.addWidget(account, alignment=Qt.AlignLeft)
        helper = QLabel("Account changes will live on a dedicated web page in a future release.")
        helper.setObjectName("muted")
        layout.addWidget(helper)
        layout.addSpacing(24)
        self._field_label(layout, "transcription provider api key")
        api_key = QLineEdit()
        api_key.setEchoMode(QLineEdit.Password)
        api_key.setPlaceholderText("paste a key when provider support is ready")
        layout.addWidget(api_key)
        layout.addSpacing(12)
        save = QPushButton("save api key")
        save.setObjectName("primaryButton")
        save.clicked.connect(lambda: self._notice("API key saved for this preview."))
        layout.addWidget(save, alignment=Qt.AlignLeft)
        layout.addSpacing(26)
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setObjectName("divider")
        layout.addWidget(divider)
        layout.addSpacing(20)
        billing_title = QLabel("Billing")
        billing_title.setObjectName("sectionTitle")
        layout.addWidget(billing_title)
        billing_text = QLabel("Subscription controls will live on the billing page.")
        billing_text.setObjectName("muted")
        layout.addWidget(billing_text)
        layout.addSpacing(11)
        billing = QPushButton("go to billing page")
        billing.setObjectName("secondaryButton")
        billing.clicked.connect(lambda: self._notice("Billing page is coming soon."))
        layout.addWidget(billing, alignment=Qt.AlignLeft)
        layout.addSpacing(24)
        sign_out = QPushButton("sign out")
        sign_out.setObjectName("secondaryButton")
        sign_out.clicked.connect(lambda: self._notice("You are signed out in this preview."))
        layout.addWidget(sign_out, alignment=Qt.AlignLeft)
        layout.addStretch()
        return panel

    def _settings_title(self, layout: QVBoxLayout, title: str, description: str) -> None:
        heading = QLabel(title)
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)
        copy = QLabel(description)
        copy.setObjectName("muted")
        copy.setWordWrap(True)
        layout.addWidget(copy)
        layout.addSpacing(28)

    def _field_label(self, layout: QVBoxLayout, text: str) -> None:
        label = QLabel(text)
        label.setObjectName("fieldLabel")
        layout.addWidget(label)
        layout.addSpacing(7)

    def _show_page(self, page: str) -> None:
        is_home = page == "home"
        self.home_nav.setChecked(is_home)
        self.settings_nav.setChecked(not is_home)
        self.pages.setCurrentWidget(self.home_page if is_home else self.settings_page)

    def _show_setting(self, setting: str) -> None:
        self.active_setting = setting
        self.settings_stack.setCurrentWidget(self.general_settings_page if setting == "General" else self.account_settings_page)

    def _render_history(self) -> None:
        self.history_list.clear()
        for timestamp, transcript in self.recordings:
            excerpt = transcript if len(transcript) <= 108 else f"{transcript[:105]}…"
            item = QListWidgetItem(f"{excerpt}\n{timestamp}")
            item.setData(Qt.UserRole, transcript)
            self.history_list.addItem(item)
        if self.recordings:
            self.history_list.setCurrentRow(0)
        self._sync_history_actions()

    def _sync_history_actions(self) -> None:
        has_selection = self.history_list.currentItem() is not None
        self.copy_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def _copy_selected(self) -> None:
        item = self.history_list.currentItem()
        if item:
            QGuiApplication.clipboard().setText(item.data(Qt.UserRole))
            self._notice("Transcript copied to your clipboard.")

    def _delete_selected(self) -> None:
        row = self.history_list.currentRow()
        if row >= 0:
            self.recordings.pop(row)
            self._render_history()
            self._notice("Transcript removed from this preview.")

    def _copy_invite_link(self) -> None:
        QGuiApplication.clipboard().setText(GITHUB_URL)
        self._notice("Project link copied to your clipboard.")

    def _toggle_recording(self) -> None:
        self.recording = not self.recording
        self.record_button.setProperty("recording", self.recording)
        self.record_button.style().unpolish(self.record_button)
        self.record_button.style().polish(self.record_button)
        if self.recording:
            self.recording_seconds = 0
            self.record_button.setText("stop dictation ■")
            self.record_status.setText("Listening. Say it plainly.")
            self.shortcut_hint.setText("recording preview  ·  nothing is being sent yet")
            self.timer.start(1000)
        else:
            self.timer.stop()
            self.record_button.setText("start dictation →")
            self.record_status.setText("Press the shortcut and say what you mean.")
            self.shortcut_hint.setText("super + space  ·  default microphone")
            self._notice("Recording stopped. Audio capture is not connected in this preview.")

    def _tick_recording(self) -> None:
        self.recording_seconds += 1
        minutes, seconds = divmod(self.recording_seconds, 60)
        self.record_timer.setText(f"{minutes:02}:{seconds:02}")

    def _notice(self, message: str) -> None:
        QMessageBox.information(self, APP_NAME, message)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setFont(QFont(font_family("Afacad", "Noto Sans"), 11))
    window = LisprFlow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
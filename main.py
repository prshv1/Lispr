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
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


APP_NAME = "Lispr Flow"
GITHUB_URL = "https://github.com/prshv1/Lispr"

PAPER = "#F4F1EA"
SURFACE = "#FFFDF6"
SURFACE_SOFT = "#F2ECDC"
SURFACE_MUTED = "#E7DFCC"
INK = "#14130F"
INK_SOFT = "#39362E"
MUTED = "#706B5E"
FAINT = "#D8CFBC"
LIME = "#D5F06F"
MOSS = "#49614B"
BLUE = "#2F6FED"
CLAY = "#D65A31"


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
        self.active_setting = "General"
        self.recordings = [
            ("Today, 11:42", "I need to turn the project notes into a small next-steps list: finish the history view, test it on Ubuntu, and decide which transcription provider to start with."),
            ("Yesterday, 17:16", "The Linux version should feel native and stay light. I want the first release to support Ubuntu well, while keeping the code portable to other distributions."),
            ("Yesterday, 10:08", "Quick stand-up: the layout is in place, invite links work, and the next thing to prototype is showing the full text from each recording."),
            ("Monday, 15:29", "Ideas to revisit later: a global shortcut, microphone selection, and a simple way to export or copy a transcript."),
        ]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick_recording)

        self._configure_window()
        self._build_shell()
        self._show_page("home")

    def _configure_window(self) -> None:
        display = font_family("Fraunces", "DejaVu Serif")
        body = font_family("Afacad", "Noto Sans")
        mono = font_family("IBM Plex Mono", "DejaVu Sans Mono")
        self.display_font = display
        self.body_font = body
        self.mono_font = mono
        self.setStyleSheet(f"""
            * {{ font-family: '{body}'; color: {INK}; }}
            QMainWindow, QWidget#app {{ background: {PAPER}; }}
            QFrame#sidebar {{ background: {SURFACE_SOFT}; border-right: 1px solid {FAINT}; }}
            QFrame#content {{ background: {PAPER}; }}
            QLabel#eyebrow {{ color: {MOSS}; font-size: 11px; font-weight: 700; letter-spacing: 1.2px; }}
            QLabel#pageTitle {{ font-family: '{display}'; font-size: 38px; font-weight: 600; letter-spacing: -0.5px; }}
            QLabel#sectionTitle {{ font-family: '{display}'; font-size: 25px; font-weight: 600; }}
            QLabel#muted {{ color: {MUTED}; font-size: 14px; }}
            QLabel#smallMuted {{ color: {MUTED}; font-size: 12px; }}
            QLabel#timer {{ font-family: '{mono}'; color: {MOSS}; font-size: 12px; font-weight: 700; }}
            QLabel#statNumber {{ font-family: '{display}'; font-size: 30px; font-weight: 600; }}
            QLabel#statLabel {{ color: {INK_SOFT}; font-size: 13px; font-weight: 700; }}
            QFrame#panel {{ background: {SURFACE}; border: 1px solid {FAINT}; border-radius: 12px; }}
            QFrame#recordPanel {{ background: {INK}; border-radius: 12px; }}
            QFrame#notice {{ background: {SURFACE_MUTED}; border-radius: 8px; }}
            QPushButton {{ border: 0; background: transparent; padding: 10px 12px; text-align: left; border-radius: 7px; font-size: 14px; }}
            QPushButton:hover {{ background: {SURFACE_MUTED}; }}
            QPushButton:focus {{ outline: 3px solid {BLUE}; }}
            QPushButton#navButton:checked {{ background: {INK}; color: {SURFACE}; font-weight: 700; }}
            QPushButton#navButton:checked:hover {{ background: {INK}; }}
            QPushButton#settingButton:checked {{ background: {SURFACE_MUTED}; color: {INK}; font-weight: 700; }}
            QPushButton#primaryButton {{ background: {LIME}; color: {INK}; font-weight: 800; padding: 12px 16px; }}
            QPushButton#primaryButton:hover {{ background: #E2F58F; }}
            QPushButton#secondaryButton {{ background: {SURFACE}; border: 1px solid {INK}; color: {INK}; font-weight: 700; padding: 10px 14px; }}
            QPushButton#secondaryButton:hover {{ background: {SURFACE_MUTED}; }}
            QPushButton#recordButton {{ background: {LIME}; color: {INK}; font-size: 15px; font-weight: 800; padding: 13px 18px; }}
            QPushButton#recordButton[recording='true'] {{ background: #F7C7B8; color: #6C2112; }}
            QLineEdit, QComboBox {{ background: {SURFACE}; border: 1px solid {FAINT}; border-radius: 7px; padding: 10px 12px; min-height: 21px; }}
            QLineEdit:focus, QComboBox:focus {{ border: 2px solid {BLUE}; }}
            QComboBox::drop-down {{ border: 0; width: 28px; }}
            QListWidget {{ background: transparent; border: 0; outline: 0; }}
            QListWidget::item {{ background: {SURFACE}; border: 1px solid {FAINT}; border-radius: 8px; margin: 0 0 8px 0; padding: 13px; }}
            QListWidget::item:selected {{ background: {SURFACE_MUTED}; border: 1px solid {MOSS}; }}
        """)

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
        mark.setAlignment(Qt.AlignCenter)
        mark.setFixedSize(32, 32)
        mark.setStyleSheet(f"background: {LIME}; color: {INK}; border-radius: 6px; font-weight: 900; font-size: 16px;")
        brand_name = QLabel(APP_NAME)
        brand_name.setStyleSheet(f"font-family: '{self.display_font}'; font-size: 22px; font-weight: 600;")
        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)
        brand_row.addWidget(mark)
        brand_row.addWidget(brand_name)
        brand_row.addStretch()
        side.addLayout(brand_row)
        side.addSpacing(44)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        self.home_nav = self._nav_button("⌂   Home", "home")
        self.settings_nav = self._nav_button("⚙   Settings", "settings")
        side.addWidget(self.home_nav)
        side.addWidget(self.settings_nav)
        side.addStretch()

        invite = QPushButton("↗   Invite a friend")
        invite.setObjectName("secondaryButton")
        invite.setToolTip("Copy the Lispr Flow project link")
        invite.clicked.connect(self._copy_invite_link)
        side.addWidget(invite)
        footer = QLabel("A quiet tool for Linux voices")
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
        eyebrow = QLabel("LISPR FLOW / DESKTOP PREVIEW")
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
        self.record_button = QPushButton("●  Start dictation")
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
        live_label = QLabel("READY WHEN YOU ARE")
        live_label.setStyleSheet(f"color: {LIME}; font-size: 11px; font-weight: 800; letter-spacing: 1.2px;")
        live.addWidget(live_label)
        self.record_status = QLabel("Press the shortcut and say what you mean.")
        self.record_status.setStyleSheet(f"color: {SURFACE}; font-family: '{self.display_font}'; font-size: 23px; font-weight: 600;")
        live.addWidget(self.record_status)
        self.shortcut_hint = QLabel("Super + Space  ·  Default microphone")
        self.shortcut_hint.setStyleSheet(f"color: #C9C1B2; font-size: 13px;")
        live.addWidget(self.shortcut_hint)
        record_layout.addLayout(live)
        record_layout.addStretch()
        self.record_timer = QLabel("00:00")
        self.record_timer.setObjectName("timer")
        self.record_timer.setStyleSheet(f"font-family: '{self.mono_font}'; color: {LIME}; font-size: 18px; font-weight: 700;")
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
        preview = QLabel("LOCAL PREVIEW")
        preview.setStyleSheet(f"color: {MOSS}; background: {SURFACE_MUTED}; padding: 5px 7px; border-radius: 4px; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        history_header.addWidget(preview)
        history_layout.addLayout(history_header)
        history_description = QLabel("Select an entry to copy it or remove it from this visual history.")
        history_description.setObjectName("smallMuted")
        history_layout.addWidget(history_description)
        history_layout.addSpacing(12)
        self.history_list = QListWidget()
        self.history_list.setSelectionMode(QListWidget.SingleSelection)
        self.history_list.itemSelectionChanged.connect(self._sync_history_actions)
        history_layout.addWidget(self.history_list, 1)
        actions = QHBoxLayout()
        self.copy_button = QPushButton("Copy selected")
        self.copy_button.setObjectName("secondaryButton")
        self.copy_button.clicked.connect(self._copy_selected)
        self.delete_button = QPushButton("Remove")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.setStyleSheet(f"QPushButton#secondaryButton {{ color: {CLAY}; border-color: {CLAY}; }} QPushButton#secondaryButton:hover {{ background: #FBE5DD; }}")
        self.delete_button.clicked.connect(self._delete_selected)
        actions.addWidget(self.copy_button)
        actions.addWidget(self.delete_button)
        actions.addStretch()
        history_layout.addLayout(actions)
        content.addWidget(history, 3)

        stats = QVBoxLayout()
        stats.setSpacing(12)
        stats.addWidget(self._stat_card("1,204", "words spoken", "All time"))
        stats.addWidget(self._stat_card("386", "words this week", "+18% from last week"))
        stats.addWidget(self._stat_card("142", "words per minute", "Based on recent speech"))
        note = QFrame(objectName="notice")
        note_layout = QVBoxLayout(note)
        note_layout.setContentsMargins(16, 15, 16, 15)
        note_title = QLabel("Local-first foundation")
        note_title.setStyleSheet("font-weight: 800; font-size: 13px;")
        note_text = QLabel("Audio capture and transcription will arrive after this desktop foundation is solid.")
        note_text.setObjectName("smallMuted")
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
        eyebrow = QLabel("CONTROL SHEET")
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
        for name in ("General", "Account"):
            button = QPushButton(name)
            button.setObjectName("settingButton")
            button.setCheckable(True)
            button.clicked.connect(lambda _checked=False, setting=name: self._show_setting(setting))
            self.settings_group.addButton(button)
            nav_layout.addWidget(button)
            if name == "General":
                button.setChecked(True)
        nav_layout.addStretch()
        nav_note = QLabel("Changes stay local until the real settings service exists.")
        nav_note.setObjectName("smallMuted")
        nav_note.setWordWrap(True)
        nav_layout.addWidget(nav_note)
        layout.addWidget(nav)

        self.settings_stack = QStackedWidget()
        self.general_settings = self._build_general_settings()
        self.account_settings = self._build_account_settings()
        self.settings_stack.addWidget(self.general_settings)
        self.settings_stack.addWidget(self.account_settings)
        layout.addWidget(self.settings_stack, 1)
        outer.addLayout(layout, 1)
        return page

    def _settings_panel(self) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame(objectName="panel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(32, 29, 32, 29)
        layout.setSpacing(0)
        return panel, layout

    def _build_general_settings(self) -> QWidget:
        panel, layout = self._settings_panel()
        self._settings_title(layout, "General", "The few controls that matter before you start speaking.")
        self._field_label(layout, "Start dictation shortcut")
        shortcut = QComboBox()
        shortcut.addItems(["Super + Space", "Ctrl + Shift + Space", "Alt + Space"])
        layout.addWidget(shortcut)
        layout.addSpacing(21)
        self._field_label(layout, "Microphone")
        microphone = QComboBox()
        microphone.addItems(["Default microphone", "Built-in audio", "USB microphone"])
        layout.addWidget(microphone)
        layout.addStretch()
        note = QFrame(objectName="notice")
        note_layout = QVBoxLayout(note)
        note_layout.setContentsMargins(16, 14, 16, 14)
        note_layout.addWidget(QLabel("These controls are visual for now."))
        detail = QLabel("They define the interface contract, not a recording setting yet.")
        detail.setObjectName("smallMuted")
        note_layout.addWidget(detail)
        layout.addWidget(note)
        return panel

    def _build_account_settings(self) -> QWidget:
        panel, layout = self._settings_panel()
        self._settings_title(layout, "Account", "Bring your own transcription provider, or manage the Lispr Flow plan later.")
        self._field_label(layout, "Account")
        account = QPushButton("Manage account details")
        account.setObjectName("secondaryButton")
        account.clicked.connect(lambda: self._notice("Account management will open in your browser soon."))
        layout.addWidget(account, alignment=Qt.AlignLeft)
        helper = QLabel("Account changes will live on a dedicated web page in a future release.")
        helper.setObjectName("smallMuted")
        layout.addWidget(helper)
        layout.addSpacing(24)
        self._field_label(layout, "Transcription provider API key")
        api_key = QLineEdit()
        api_key.setEchoMode(QLineEdit.Password)
        api_key.setPlaceholderText("Paste a key when provider support is ready")
        layout.addWidget(api_key)
        layout.addSpacing(12)
        save = QPushButton("Save API key")
        save.setObjectName("primaryButton")
        save.clicked.connect(lambda: self._notice("API key saved for this preview."))
        layout.addWidget(save, alignment=Qt.AlignLeft)
        layout.addSpacing(26)
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"color: {FAINT};")
        layout.addWidget(divider)
        layout.addSpacing(20)
        billing_title = QLabel("Billing")
        billing_title.setObjectName("sectionTitle")
        layout.addWidget(billing_title)
        billing_text = QLabel("Subscription controls will live on the billing page.")
        billing_text.setObjectName("smallMuted")
        layout.addWidget(billing_text)
        layout.addSpacing(11)
        billing = QPushButton("Go to billing page")
        billing.setObjectName("secondaryButton")
        billing.clicked.connect(lambda: self._notice("Billing page is coming soon."))
        layout.addWidget(billing, alignment=Qt.AlignLeft)
        layout.addSpacing(24)
        sign_out = QPushButton("Sign out")
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
        label.setStyleSheet("font-size: 13px; font-weight: 800;")
        layout.addWidget(label)
        layout.addSpacing(7)

    def _show_page(self, page: str) -> None:
        is_home = page == "home"
        self.home_nav.setChecked(is_home)
        self.settings_nav.setChecked(not is_home)
        self.pages.setCurrentWidget(self.home_page if is_home else self.settings_page)

    def _show_setting(self, setting: str) -> None:
        self.active_setting = setting
        self.settings_stack.setCurrentWidget(self.general_settings if setting == "General" else self.account_settings)

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
            self.record_button.setText("■  Stop dictation")
            self.record_status.setText("Listening. Say it plainly.")
            self.shortcut_hint.setText("Recording preview  ·  Nothing is being sent yet")
            self.timer.start(1000)
        else:
            self.timer.stop()
            self.record_button.setText("●  Start dictation")
            self.record_status.setText("Press the shortcut and say what you mean.")
            self.shortcut_hint.setText("Super + Space  ·  Default microphone")
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

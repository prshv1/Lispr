"""Lispr Flow Day 0 UI prototype.

This intentionally contains no audio, account, API, billing, or persistence logic.
It is a lightweight native window for checking the initial product layout.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


APP_NAME = "Lispr Flow"
GITHUB_URL = "https://github.com/prshv1/Lispr"

BG = "#101112"
PANEL = "#17191b"
PANEL_HOVER = "#212427"
SIDEBAR = "#141618"
LINE = "#2a2d30"
TEXT = "#f1f3f5"
MUTED = "#a2a8ae"
ACCENT = "#86efac"
ACCENT_DARK = "#193323"
FIELD = "#202326"


class LisprFlow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1280x760")
        self.minsize(960, 640)
        self.configure(bg=BG)
        self.active_page = "home"
        self.active_setting = "General"

        self._configure_styles()
        self._build_shell()
        self.show_home()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Dark.TCombobox",
            fieldbackground=FIELD,
            background=FIELD,
            foreground=TEXT,
            arrowcolor=MUTED,
            bordercolor=LINE,
            lightcolor=FIELD,
            darkcolor=FIELD,
            padding=(10, 8),
        )
        style.map("Dark.TCombobox", fieldbackground=[("readonly", FIELD)])

    def _build_shell(self) -> None:
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=232)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=20, pady=(24, 34))
        tk.Label(
            brand,
            text="L",
            bg=ACCENT,
            fg="#102114",
            font=("Arial", 13, "bold"),
            width=2,
            height=1,
        ).pack(side="left")
        tk.Label(
            brand,
            text="Lispr Flow",
            bg=SIDEBAR,
            fg=TEXT,
            font=("Arial", 15, "bold"),
        ).pack(side="left", padx=(10, 0))

        self.nav = tk.Frame(self.sidebar, bg=SIDEBAR)
        self.nav.pack(fill="x", padx=12)
        self.home_button = self._nav_button("⌂", "Home", self.show_home)

        tk.Frame(self.sidebar, bg=SIDEBAR).pack(fill="both", expand=True)

        bottom_nav = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom_nav.pack(fill="x", padx=12, pady=(0, 20))
        self.invite_button = self._nav_button("↗", "Invite friends", self.show_invite, bottom_nav)
        self.settings_button = self._nav_button("⚙", "Settings", self.show_settings, bottom_nav)

        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

    def _nav_button(self, icon: str, label: str, command, parent: tk.Frame | None = None) -> tk.Button:
        button = tk.Button(
            parent or self.nav,
            text=f"  {icon}    {label}",
            command=command,
            anchor="w",
            borderwidth=0,
            relief="flat",
            padx=10,
            pady=11,
            bg=SIDEBAR,
            fg=MUTED,
            activebackground=PANEL_HOVER,
            activeforeground=TEXT,
            font=("Arial", 11),
            cursor="hand2",
        )
        button.pack(fill="x", pady=2)
        return button

    def _clear_content(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()

    def _select_page(self, page: str) -> None:
        self.active_page = page
        for button, name in ((self.home_button, "home"), (self.settings_button, "settings")):
            selected = name == page
            button.configure(bg=ACCENT_DARK if selected else SIDEBAR, fg=ACCENT if selected else MUTED)

    def show_home(self) -> None:
        self._select_page("home")
        self._clear_content()

        container = tk.Frame(self.content, bg=BG)
        container.pack(fill="both", expand=True, padx=46, pady=38)

        header = tk.Frame(container, bg=BG)
        header.pack(fill="x", pady=(0, 28))
        tk.Label(header, text="Home", bg=BG, fg=TEXT, font=("Arial", 26, "bold")).pack(anchor="w")
        tk.Label(
            header,
            text="Your recent recordings and speaking activity.",
            bg=BG,
            fg=MUTED,
            font=("Arial", 11),
        ).pack(anchor="w", pady=(7, 0))

        layout = tk.Frame(container, bg=BG)
        layout.pack(fill="both", expand=True)
        layout.columnconfigure(0, weight=3, minsize=520)
        layout.columnconfigure(1, weight=1, minsize=250)
        layout.rowconfigure(0, weight=1)

        history = tk.Frame(layout, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        history.grid(row=0, column=0, sticky="nsew", padx=(0, 22))
        history_header = tk.Frame(history, bg=PANEL)
        history_header.pack(fill="x", padx=24, pady=(23, 18))
        tk.Label(history_header, text="Recording history", bg=PANEL, fg=TEXT, font=("Arial", 15, "bold")).pack(side="left")
        tk.Label(history_header, text="Day 0 preview", bg=ACCENT_DARK, fg=ACCENT, font=("Arial", 9, "bold"), padx=8, pady=4).pack(side="right")

        records = tk.Frame(history, bg=PANEL)
        records.pack(fill="both", expand=True, padx=24)
        for title, time, words in [
            ("Project notes and next steps", "Today, 11:42 AM", "184 words"),
            ("A thought about the Linux version", "Yesterday, 5:16 PM", "76 words"),
            ("Quick stand-up update", "Yesterday, 10:08 AM", "132 words"),
            ("Ideas to revisit", "Monday, 3:29 PM", "58 words"),
        ]:
            self._history_item(records, title, time, words)

        tk.Label(
            history,
            text="Recordings will show up here once voice capture is added.",
            bg=PANEL,
            fg=MUTED,
            font=("Arial", 10),
        ).pack(anchor="w", padx=24, pady=22)

        summary = tk.Frame(layout, bg=BG)
        summary.grid(row=0, column=1, sticky="nsew")
        tk.Label(summary, text="Your summary", bg=BG, fg=TEXT, font=("Arial", 15, "bold")).pack(anchor="w", pady=(2, 13))
        self._stat_card(summary, "1,204", "Total words spoken", "All time")
        self._stat_card(summary, "386", "Words this week", "+18% from last week")
        self._stat_card(summary, "142", "Rough words per minute", "Based on recent recordings")

    def _history_item(self, parent: tk.Frame, title: str, time: str, words: str) -> None:
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=1)
        row.configure(highlightbackground=LINE, highlightthickness=1)
        icon = tk.Label(row, text="✦", bg="#22302a", fg=ACCENT, font=("Arial", 11), width=3, pady=13)
        icon.pack(side="left", padx=(12, 12), pady=8)
        text = tk.Frame(row, bg=PANEL)
        text.pack(side="left", fill="x", expand=True, pady=12)
        tk.Label(text, text=title, bg=PANEL, fg=TEXT, font=("Arial", 11, "bold")).pack(anchor="w")
        tk.Label(text, text=time, bg=PANEL, fg=MUTED, font=("Arial", 9)).pack(anchor="w", pady=(4, 0))
        tk.Label(row, text=words, bg=PANEL, fg=MUTED, font=("Arial", 9)).pack(side="right", padx=16)

    def _stat_card(self, parent: tk.Frame, value: str, label: str, detail: str) -> None:
        card = tk.Frame(parent, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        card.pack(fill="x", pady=(0, 12))
        tk.Label(card, text=value, bg=PANEL, fg=TEXT, font=("Arial", 23, "bold")).pack(anchor="w", padx=18, pady=(17, 4))
        tk.Label(card, text=label, bg=PANEL, fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", padx=18)
        tk.Label(card, text=detail, bg=PANEL, fg=MUTED, font=("Arial", 9)).pack(anchor="w", padx=18, pady=(5, 17))

    def show_settings(self) -> None:
        self._select_page("settings")
        self._clear_content()

        container = tk.Frame(self.content, bg=BG)
        container.pack(fill="both", expand=True, padx=46, pady=38)
        tk.Label(container, text="Settings", bg=BG, fg=TEXT, font=("Arial", 26, "bold")).pack(anchor="w")
        tk.Label(container, text="Set up Lispr Flow your way. These controls are visual for now.", bg=BG, fg=MUTED, font=("Arial", 11)).pack(anchor="w", pady=(7, 28))

        layout = tk.Frame(container, bg=BG)
        layout.pack(fill="both", expand=True)
        settings_nav = tk.Frame(layout, bg=PANEL, width=205, highlightbackground=LINE, highlightthickness=1)
        settings_nav.pack(side="left", fill="y")
        settings_nav.pack_propagate(False)
        self.setting_buttons: dict[str, tk.Button] = {}
        for label in ("General", "Auth", "Add account", "In account", "Sign out"):
            button = tk.Button(
                settings_nav,
                text=f"  {label}",
                command=lambda item=label: self.show_setting(item),
                anchor="w",
                borderwidth=0,
                padx=12,
                pady=11,
                bg=PANEL,
                fg=MUTED,
                activebackground=PANEL_HOVER,
                activeforeground=TEXT,
                font=("Arial", 10),
                cursor="hand2",
            )
            button.pack(fill="x", padx=10, pady=(12 if label == "General" else 2, 0))
            self.setting_buttons[label] = button

        divider = tk.Frame(layout, bg=BG, width=22)
        divider.pack(side="left", fill="y")
        self.settings_detail = tk.Frame(layout, bg=PANEL, highlightbackground=LINE, highlightthickness=1)
        self.settings_detail.pack(side="left", fill="both", expand=True)
        self.show_setting(self.active_setting)

    def show_setting(self, setting: str) -> None:
        self.active_setting = setting
        for name, button in self.setting_buttons.items():
            selected = name == setting
            button.configure(bg=ACCENT_DARK if selected else PANEL, fg=ACCENT if selected else MUTED)
        for child in self.settings_detail.winfo_children():
            child.destroy()

        detail = tk.Frame(self.settings_detail, bg=PANEL)
        detail.pack(fill="both", expand=True, padx=32, pady=30)

        if setting == "General":
            self._detail_title(detail, "General", "Choose the shortcut and microphone Lispr Flow will use later.")
            self._field_label(detail, "Start recording shortcut")
            shortcut = ttk.Combobox(detail, style="Dark.TCombobox", values=["Super + Space", "Ctrl + Shift + Space", "Alt + Space"], state="readonly")
            shortcut.set("Super + Space")
            shortcut.pack(fill="x", pady=(0, 23))
            self._field_label(detail, "Microphone input")
            microphone = ttk.Combobox(detail, style="Dark.TCombobox", values=["Default microphone", "Built-in audio", "USB microphone"], state="readonly")
            microphone.set("Default microphone")
            microphone.pack(fill="x")
        elif setting == "Auth":
            self._detail_title(detail, "Auth", "Add your own transcription provider API key. It will not be used yet.")
            self._field_label(detail, "API key")
            api_key = tk.Entry(detail, bg=FIELD, fg=TEXT, insertbackground=TEXT, relief="flat", highlightthickness=1, highlightbackground=LINE, font=("Arial", 11), show="•")
            api_key.pack(fill="x", ipady=10, pady=(0, 16))
            self._primary_button(detail, "Save API key", lambda: self._notice(detail, "API key saved for this preview."))
        elif setting == "Add account":
            self._detail_title(detail, "Add account", "Connect another account in a future release.")
            self._primary_button(detail, "Add account", lambda: self._notice(detail, "Account connection is coming soon."))
        elif setting == "In account":
            self._detail_title(detail, "In account", "You are currently viewing the local Day 0 preview.")
            self._primary_button(detail, "Manage account", lambda: self._notice(detail, "Account management is coming soon."))
        elif setting == "Sign out":
            self._detail_title(detail, "Sign out", "Sign-out is included in the layout but does not have account logic yet.")
            self._secondary_button(detail, "Sign out", lambda: self._notice(detail, "You are signed out in this preview."))

        billing = tk.Frame(detail, bg=PANEL)
        billing.pack(side="bottom", fill="x", pady=(40, 0))
        tk.Frame(billing, bg=LINE, height=1).pack(fill="x", pady=(0, 18))
        tk.Label(billing, text="Billing", bg=PANEL, fg=TEXT, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(billing, text="Subscription controls will live on the billing page.", bg=PANEL, fg=MUTED, font=("Arial", 9)).pack(anchor="w", pady=(4, 12))
        self._secondary_button(billing, "Go to billing page", lambda: self._notice(detail, "Billing page is coming soon."))

    def _detail_title(self, parent: tk.Frame, title: str, description: str) -> None:
        tk.Label(parent, text=title, bg=PANEL, fg=TEXT, font=("Arial", 19, "bold")).pack(anchor="w")
        tk.Label(parent, text=description, bg=PANEL, fg=MUTED, font=("Arial", 10), wraplength=570, justify="left").pack(anchor="w", pady=(7, 28))

    def _field_label(self, parent: tk.Frame, text: str) -> None:
        tk.Label(parent, text=text, bg=PANEL, fg=TEXT, font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 8))

    def _primary_button(self, parent: tk.Frame, text: str, command) -> tk.Button:
        button = tk.Button(parent, text=text, command=command, bg=ACCENT, fg="#102114", activebackground="#b0f7c6", activeforeground="#102114", borderwidth=0, padx=16, pady=10, font=("Arial", 10, "bold"), cursor="hand2")
        button.pack(anchor="w")
        return button

    def _secondary_button(self, parent: tk.Frame, text: str, command) -> tk.Button:
        button = tk.Button(parent, text=text, command=command, bg=FIELD, fg=TEXT, activebackground=PANEL_HOVER, activeforeground=TEXT, borderwidth=0, padx=16, pady=10, font=("Arial", 10, "bold"), cursor="hand2")
        button.pack(anchor="w")
        return button

    def _notice(self, parent: tk.Frame, message: str) -> None:
        notice = tk.Label(parent, text=message, bg=PANEL, fg=ACCENT, font=("Arial", 9))
        notice.pack(anchor="w", pady=(12, 0))
        self.after(2400, notice.destroy)

    def show_invite(self) -> None:
        popup = tk.Toplevel(self)
        popup.title("Invite friends")
        popup.configure(bg=PANEL)
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()
        popup.geometry("480x270")
        popup.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 480) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 270) // 2
        popup.geometry(f"+{x}+{y}")

        content = tk.Frame(popup, bg=PANEL)
        content.pack(fill="both", expand=True, padx=28, pady=26)
        tk.Label(content, text="Send this to your friends", bg=PANEL, fg=TEXT, font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(content, text="Help make Lispr Flow useful for more Linux users.", bg=PANEL, fg=MUTED, font=("Arial", 10)).pack(anchor="w", pady=(7, 20))
        link_row = tk.Frame(content, bg=FIELD, highlightbackground=LINE, highlightthickness=1)
        link_row.pack(fill="x")
        tk.Label(link_row, text=GITHUB_URL, bg=FIELD, fg=TEXT, font=("Arial", 10), anchor="w").pack(side="left", fill="x", expand=True, padx=12, pady=11)

        def copy_link() -> None:
            self.clipboard_clear()
            self.clipboard_append(GITHUB_URL)
            copy.configure(text="Copied!")
            popup.after(1800, lambda: copy.configure(text="Copy link"))

        actions = tk.Frame(content, bg=PANEL)
        actions.pack(fill="x", pady=(18, 0))
        tk.Button(actions, text="Close", command=popup.destroy, bg=FIELD, fg=TEXT, activebackground=PANEL_HOVER, activeforeground=TEXT, borderwidth=0, padx=15, pady=9, font=("Arial", 10, "bold"), cursor="hand2").pack(side="right")
        copy = tk.Button(actions, text="Copy link", command=copy_link, bg=ACCENT, fg="#102114", activebackground="#b0f7c6", activeforeground="#102114", borderwidth=0, padx=15, pady=9, font=("Arial", 10, "bold"), cursor="hand2")
        copy.pack(side="right", padx=(0, 9))


if __name__ == "__main__":
    LisprFlow().mainloop()

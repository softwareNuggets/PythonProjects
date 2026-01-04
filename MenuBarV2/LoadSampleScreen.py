# LoadSampleScreen.py
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class LoadSampleScreen(ttk.Frame):
    """
    A simple "page" that can be embedded into the app's main content area.

    on_cancel:
        Callback invoked when the user clicks Cancel so the host app can
        remove/destroy this screen.
    """

    def __init__(self, parent: tk.Misc, on_cancel: Callable[[], None]) -> None:
        super().__init__(parent, padding=16)

        self._on_cancel = on_cancel

        ttk.Label(self, text="LoadSampleScreen(ttk.Frame): goes here", font=("Segoe UI", 16)).pack(
            anchor="w", pady=(0, 10)
        )

        # Spacer that grows so the Cancel button stays at the bottom
        ttk.Frame(self).pack(fill="both", expand=True)

        ttk.Button(self, text="Cancel", command=self._on_cancel).pack(anchor="e")

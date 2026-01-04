#lets you use class names in type hints before the class is fully defined
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk



# MenuCommand is used for menu action callbacks.
# Callable[[], None] means: a function with no parameters that returns nothing.
# Example: def save_file() -> None:     (no parameters, no return value "None")
MenuCommand = Callable[[], None]




# ----------------------------
# Menu Items
# ----------------------------

class MenuSpecBuilder:
    """
    Definitions:
    - Menu bar: top-level container (the root menubar)
    - Top-level menu: a "cascade" added to the menubar (File/Edit/View/Help)
    - Menu item: a "command" entry (New, Save, Exit)
    - Submenu: a "cascade" within a menu (Export -> {CSV, PDF})
    - Separator/divider: a "separator"
    - Accelerator: displayed shortcut text (e.g., Ctrl+S)
    - Key binding: the actual Tk event binding (e.g., <Control-s>)
    - Icon: image shown next to menu item (compound=left)
    - Disabled item: state="disabled"
    - Check / radio items exist in Tk, but omitted here for clarity; can be added easily.
    """

    @staticmethod
    def default_spec() -> list[dict[str, Any]]:
        return [
            {
                "label": "File",
                "items": [
                    {
                        "label": "New File",
                        "action": "new_file",
                        "icon_key": "new",
                        "accelerator": "Ctrl+N",
                        "bind": "<Control-n>",
                    },
                    {"kind": "separator"},
                    {
                        "kind": "cascade",
                        "label": "Export",
                        "items": [
                            {"label": "Export as CSV", "action": "export_csv"},
                            {"label": "Export as PDF", "action": "export_pdf"},
                            {
                                "kind": "cascade",
                                "label": "Image Options",
                                "items": [
                                    {"label": "Resize Image", "action": "resize_image"},
                                    {"label": "Convert to B/W", "action": "convert_bw"},
                                ],
                                "icon_key": "gear",
                            },
                        ],
                        "icon_key": "export",
                    },
                    {"kind": "separator"},
                    {"label": "Load Sample Screen",
                     "action": "load_sample_screen",
                     "icon_key": "question_mark"
                    },
                    {"kind": "separator"},
                    {
                        "label": "Save",
                        "action": "save",
                        "icon_key": "save",
                        "accelerator": "Ctrl+S",
                        "bind": "<Control-s>",
                    },
                    {"kind": "separator"},
                    {"label": "Exit", "action": "exit_app", "icon_key": "exit"},
                ],
            },
            {
                "label": "Edit",
                "items": [
                    {"label": "Bold", "action": "bold_selection", "accelerator": "Ctrl+B", "bind": "<Control-b>"},
                ],
            },
            {
                "label": "Help",
                "items": [
                    {"label": "About", "action": "about"},
                ],
            },
        ]


# ----------------------------
# Actions (menu item callbacks)
# ----------------------------

class MenuActions:
    """
    Put your menu-click handlers here.
    These handlers receive the controller so they can access:
      - controller.root
      - controller.show_status(...)
      - controller.open_window(...)
    """

    def __init__(self, controller: "MenuController") -> None:
        self.controller = controller

    # ---- Example actions ----

    def new_file(self) -> None:
        self.controller.show_status("New File clicked")
        messagebox.showinfo("New File", "Create a new document here.")

    def export_csv(self) -> None:
        self.controller.show_status("Export as CSV clicked")
        messagebox.showinfo("Export", "Export CSV logic goes here.")

    def export_pdf(self) -> None:
        self.controller.show_status("Export as PDF clicked")
        messagebox.showinfo("Export", "Export PDF logic goes here.")

    def resize_image(self) -> None:
        self.controller.show_status("Resize Image clicked")
        messagebox.showinfo("Image", "Resize logic goes here.")

    def convert_bw(self) -> None:
        self.controller.show_status("Convert to B/W clicked")
        messagebox.showinfo("Image", "Convert to B/W logic goes here.")

    def save(self) -> None:
        self.controller.show_status("Save clicked")
        messagebox.showinfo("Save", "Save logic goes here.")

    def exit_app(self) -> None:
        self.controller.show_status("Exit clicked")
        self.controller.safe_quit()

    def about(self) -> None:
        self.controller.show_status("Viewing: About")

        messagebox.showinfo(
            "About",
            "Youtube: Software Nuggets\n\n"
            "A Python TkInter App -- Menu System\n\n"
            "Python 3.12"
        )

        # Dialog is closed, reset statusbar
        self.controller.show_status("Ready")

    def bold_selection(self) -> None:
        # Example: this would be wired to your editor widget in a real app
        self.controller.show_status("Bold clicked")
        messagebox.showinfo("Format", "Bold selection (hook into your text widget).")

    def load_sample_screen(self) -> None:
        # Status should describe the current view, not the click event
        self.controller.show_status("Viewing: Sample Screen")

        if self.controller.content_host is None:
            messagebox.showerror("UI Error", "No content host configured for screens.")
            self.controller.show_status("Ready")
            return

        # Clear existing content BEFORE creating the new screen (prevents Tk path errors)
        self.controller.clear_screen()

        from LoadSampleScreen import LoadSampleScreen

        def _cancel() -> None:
            # Remove the screen and reset the status so it doesn't mislead the user
            self.controller.clear_screen()
            self.controller.show_status("Ready")

        screen = LoadSampleScreen(
            parent=self.controller.content_host,
            on_cancel=_cancel,
        )
        self.controller.set_screen(screen)


# ----------------------------
# Styling configuration (as far as Tk menus allow)
# (frozen=True) = Once you create it, you cannot change its attributes
# ----------------------------

@dataclass(frozen=True)
class MenuStyle:
    font_family: str = "Segoe UI"
    font_size: int = 10
    fg: str = "#1f2937"            # slate-ish
    bg: str = "#ffffff"            # white
    active_fg: str = "#111827"
    active_bg: str = "#e5e7eb"     # light gray
    tearoff: bool = False          # keep professional look

    def make_font(self) -> tkfont.Font:
        return tkfont.Font(family=self.font_family, size=self.font_size)

# ----------------------------
# MenuController (builds menus + provides app hooks)
# ----------------------------

class MenuController:
    def __init__(
        self,
        root: tk.Tk,
        style: Optional[MenuStyle] = None,
        content_host: Optional[tk.Misc] = None,
    ) -> None:
    
        self.root = root
        self.style = style or MenuStyle()

        # Content area support
        self.content_host = content_host
        self.current_screen: Optional[tk.Widget] = None

        self.actions = MenuActions(self)
        self.menu_images: dict[str, tk.PhotoImage] = {}

        # Optional status bar (nice UX)
        self.status_var = tk.StringVar(value="Ready")
        self.status = ttk.Label(self.root, textvariable=self.status_var, anchor="w")
        self.status.pack(side="bottom", fill="x")

    def show_status(self, text: str) -> None:
        self.status_var.set(text)

    def safe_quit(self) -> None:
        self.root.destroy()

    def open_window(self, title: str, message: str) -> None:
        win = tk.Toplevel(self.root)
        win.title(title)
        ttk.Label(win, text=message, padding=12).pack()
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 12))

    # ---- Menu build API ----

    def build_menu_bar(self, spec: list[dict[str, Any]]) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        for top in spec:
            label = top["label"]
            submenu_items = top.get("items", [])
            menu = self.create_menu(menubar)
            self.populate_menu(menu, submenu_items)
            menubar.add_cascade(label=label, menu=menu)

        # Example: bind keyboard shortcuts that you also display as accelerators.
        # Tk menus show "accelerator" text, but the actual binding must be done by you.
        self.bind_accelerators(spec)

    def create_menu(self, parent: tk.Misc) -> tk.Menu:
        fnt = self.style.make_font()
        return tk.Menu(
            parent,
            tearoff=self.style.tearoff,
            font=fnt,
            foreground=self.style.fg,
            background=self.style.bg,
            activeforeground=self.style.active_fg,
            activebackground=self.style.active_bg,
        )

    def populate_menu(self, menu: tk.Menu, items: list[dict[str, Any]]) -> None:
        for item in items:
            kind = item.get("kind", "command")

            if kind == "separator":
                menu.add_separator()
                continue

            if kind == "cascade":
                submenu = self.create_menu(menu)
                self.populate_menu(submenu, item.get("items", []))
                menu.add_cascade(label=item["label"], menu=submenu)
                continue

            # Default: command item
            label = item["label"]
            action = item.get("action")  # can be callable OR string name on MenuActions
            state = item.get("state", "normal")
            accelerator = item.get("accelerator")  # display text only (binding done elsewhere)
            icon_key = item.get("icon_key")         # optional key to load icon image

            cmd = self.resolve_action(action)
            kwargs: dict[str, Any] = {
                "label": label,
                "command": cmd,
                "state": state,
            }
            if accelerator:
                kwargs["accelerator"] = accelerator

            if icon_key:
                img = self.get_icon(icon_key)
                if img is not None:
                    kwargs["image"] = img
                    kwargs["compound"] = "left"  # icon + text

            menu.add_command(**kwargs)

    def resolve_action(self, action: Any) -> MenuCommand:
        if action is None:
            return lambda: self.show_status("No action assigned")

        if callable(action):
            return action

        if isinstance(action, str):
            fn = getattr(self.actions, action, None)
            if fn is None or not callable(fn):
                return lambda: messagebox.showerror("Menu Error", f"Unknown action: {action}")
            return fn

        return lambda: messagebox.showerror("Menu Error", f"Invalid action type: {type(action)}")
        
    # helper methods to show/clear screens
    def set_screen(self, widget: tk.Widget) -> None:
        """Show a new 'page' inside the content area."""
        self.current_screen = widget
        widget.pack(fill="both", expand=True)

    def clear_screen(self) -> None:
        """Remove everything from the content area."""
        if self.content_host is None:
            return

        for child in self.content_host.winfo_children():
            child.destroy()

        self.current_screen = None

    def reset_status(self) -> None:
        """Reset the status bar to its default state."""
        self.status_var.set("Ready")

    # ---- Icons ----

    def get_icon(self, icon_key: str) -> Optional[tk.PhotoImage]:
        """
        Tkinter menu icons:
        - Use tk.PhotoImage (PNG/GIF supported).
        - Keep a reference to prevent garbage collection.
        - Some platforms/menus may not show icons consistently.
        """
        if icon_key in self.menu_images:
            return self.menu_images[icon_key]

        # Handle custom PNG files
        if icon_key == "question_mark":
            try:
                img = tk.PhotoImage(file="videos/question_mark.png")
                self.menu_images[icon_key] = img
                return img
            except Exception as e:
                print(f"Error loading question_mark icon: {e}")
                return None



        # Minimal built-in placeholder icons using tiny pixel art (no external files needed).
        # For real apps, replace with PhotoImage(file="path/to/icon.png")
        builtins = {
            "new": self.pixel_icon("#2563eb"),     # blue
            "save": self.pixel_icon("#111827"),    # near-black
            "exit": self.pixel_icon("#ef4444"),    # red
            "export": self.pixel_icon("#10b981"),  # green
            "gear": self.pixel_icon("#6b7280"),    # gray
        }

        img = builtins.get(icon_key)
        if img is not None:
            self.menu_images[icon_key] = img
        return img

    def pixel_icon(self, color: str) -> tk.PhotoImage:
        """
        Creates a simple square icon (12x12). Replace with real icons for a polished app.
        """
        size = 12
        img = tk.PhotoImage(width=size, height=size)
        img.put(color, to=(0, 0, size, size))
        # Add a tiny inner highlight to look less flat
        img.put("#ffffff", to=(2, 2, size - 2, size - 2))
        img.put(color, to=(3, 3, size - 3, size - 3))
        return img

    # ---- Keyboard accelerators (bindings) ----

    def bind_accelerators(self, spec: list[dict[str, Any]]) -> None:
        """
        Menus show accelerator text, but Tkinter requires you to bind keystrokes.
        We walk the spec, find accelerator bindings, and attach them to root.
        """
        for item in self.walk_items(spec):
            accel = item.get("bind")  # actual Tk binding string, e.g. "<Control-s>"
            action = item.get("action")
            if accel:
                cmd = self.resolve_action(action)
                self.root.bind_all(accel, lambda _evt, c=cmd: c())

    def walk_items(self, spec: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Flattens all menu items recursively for accelerator binding.
        """
        out: list[dict[str, Any]] = []
        for top in spec:
            for item in top.get("items", []):
                out.extend(self.walk_item(item))
        return out

    def walk_item(self, item: dict[str, Any]) -> list[dict[str, Any]]:
        out = [item]
        if item.get("kind") == "cascade":
            for child in item.get("items", []):
                out.extend(self.walk_item(child))
        return out


# ----------------------------
# Optional demo entry point (safe to delete in your project)
# ----------------------------

def main() -> None:
    root = tk.Tk()
    root.title("Beautiful Tkinter Menu System (Python 3.12)")
    root.geometry("900x550")

    # ttk theme - clam, alt, classic, vista, xpnative, aqua (macos)
    #  you'll only see theme changes on widgets like ttk.Button, ttk.Entry, ttk.Treeview, etc.
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass

    # Example content area
    frame = ttk.Frame(root, padding=0)
    frame.pack(fill="both", expand=True)

    content_host = ttk.Frame(frame, padding=16)
    content_host.pack(fill="both", expand=True)

    # Initial content
    ttk.Label(content_host, text="Your app content goes here.", font=("Segoe UI", 16)).pack(anchor="w")
    ttk.Label(content_host, text="Use the menus above. Status appears at the bottom.").pack(anchor="w", pady=(6, 0))

    ttk.Button(content_host, text="Button").pack(pady=6)
    ttk.Entry(content_host).pack(pady=6)
    ttk.Combobox(content_host, values=["A", "B", "C"]).pack(pady=6)
    ttk.Treeview(content_host, columns=("x",), show="headings").pack(pady=6)


    appMenuStyle = MenuStyle(
        font_family="Segoe UI",
        font_size=10,
        fg="#0f172a",
        bg="#ffffff",
        active_fg="#0f172a",
        active_bg="#e2e8f0",
        tearoff=False,
    )
    controller = MenuController(root=root, style=appMenuStyle, content_host=content_host)
    controller.build_menu_bar(MenuSpecBuilder.default_spec())

    root.mainloop()


if __name__ == "__main__":
    main()

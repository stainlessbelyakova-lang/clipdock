import customtkinter as ctk
from .config import APP_NAME, WINDOW_SIZE, POLL_INTERVAL
from .storage import load_clips, save_clips, create_clip
from .clipboard import get_clipboard, set_clipboard


class ClipDockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.minsize(850, 550)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.clips = load_clips()
        self.current_clip_id = None
        self.last_clipboard = ""
        self.search_text = ctk.StringVar()

        self.build_ui()
        self.refresh_list()
        self.poll_clipboard()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="ClipDock",
            font=("Arial", 24, "bold")
        )
        self.logo.grid(row=0, column=0, padx=15, pady=(20, 10), sticky="w")

        self.search_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Search clips...",
            textvariable=self.search_text
        )
        self.search_entry.grid(row=1, column=0, padx=15, pady=8, sticky="ew")
        self.search_text.trace_add("write", lambda *_: self.refresh_list())

        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear History",
            command=self.clear_history
        )
        self.clear_button.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        self.list_frame = ctk.CTkScrollableFrame(self.sidebar)
        self.list_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.viewer = ctk.CTkFrame(self, corner_radius=0)
        self.viewer.grid(row=0, column=1, sticky="nsew")
        self.viewer.grid_columnconfigure(0, weight=1)
        self.viewer.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self.viewer,
            text="Clipboard Viewer",
            font=("Arial", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.textbox = ctk.CTkTextbox(
            self.viewer,
            font=("Arial", 16),
            wrap="word"
        )
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox.configure(state="disabled")

        self.bottom_bar = ctk.CTkFrame(self.viewer, fg_color="transparent")
        self.bottom_bar.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.pin_button = ctk.CTkButton(
            self.bottom_bar,
            text="Pin",
            width=100,
            command=self.toggle_pin
        )
        self.pin_button.pack(side="left")

        self.copy_button = ctk.CTkButton(
            self.bottom_bar,
            text="Copy Back",
            width=120,
            command=self.copy_back
        )
        self.copy_button.pack(side="right")

    def poll_clipboard(self):
        text = get_clipboard()

        if text and text != self.last_clipboard:
            self.last_clipboard = text

            if not any(c["text"] == text for c in self.clips):
                self.clips.insert(0, create_clip(text))
                save_clips(self.clips)
                self.refresh_list()

        self.after(POLL_INTERVAL, self.poll_clipboard)

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        query = self.search_text.get().lower().strip()

        filtered = []
        for clip in self.clips:
            if query in clip["text"].lower():
                filtered.append(clip)

        filtered.sort(key=lambda c: (not c["pinned"], c["created_at"]))

        for clip in filtered:
            preview = clip["text"][:40].replace("\n", " ")
            if len(clip["text"]) > 40:
                preview += "..."

            if clip["pinned"]:
                preview = "📌 " + preview

            button = ctk.CTkButton(
                self.list_frame,
                text=preview,
                anchor="w",
                fg_color="#2b2b2b" if clip["id"] != self.current_clip_id else "#1f6aa5",
                command=lambda clip_id=clip["id"]: self.open_clip(clip_id)
            )
            button.pack(fill="x", padx=5, pady=4)

    def open_clip(self, clip_id):
        self.current_clip_id = clip_id
        clip = self.get_current_clip()

        if not clip:
            return

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", clip["text"])
        self.textbox.configure(state="disabled")

        self.pin_button.configure(text="Unpin" if clip["pinned"] else "Pin")
        self.refresh_list()

    def get_current_clip(self):
        for clip in self.clips:
            if clip["id"] == self.current_clip_id:
                return clip
        return None

    def toggle_pin(self):
        clip = self.get_current_clip()

        if not clip:
            return

        clip["pinned"] = not clip["pinned"]
        save_clips(self.clips)
        self.open_clip(clip["id"])

    def copy_back(self):
        clip = self.get_current_clip()

        if clip:
            set_clipboard(clip["text"])

    def clear_history(self):
        self.clips = [clip for clip in self.clips if clip["pinned"]]
        save_clips(self.clips)
        self.current_clip_id = None

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")

        self.refresh_list()
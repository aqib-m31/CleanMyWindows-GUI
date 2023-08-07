import customtkinter as ctk
from components import LabelFrame, ContainerFrame
import time

import clean_my_windows


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clean My Windows")
        self.geometry("1080x700")
        self.resizable(width=False, height=False)
        ctk.set_appearance_mode("dark")

        self.columnconfigure((0, 1), weight=1)

        self.lbl_title = ctk.CTkLabel(
            self,
            text="CLEAN MY WINDOWS",
            fg_color="dark slate gray",
            text_color="gray90",
            font=("Courier New", 32),
            anchor="center",
            pady=25,
        )
        self.lbl_title.grid(row=0, column=0, sticky="ew", columnspan=2)

        self.frm_container = ContainerFrame(self)
        self.frm_container.grid(row=1, column=0, sticky="ew", columnspan=2, pady=20)

        self.btn_scan = ctk.CTkButton(
            self,
            text="Scan Junk",
            border_spacing=10,
            command=self.handle_scan,
            font=("Arial", 20),
            fg_color="SeaGreen",
            hover_color="dark slate gray",
            text_color_disabled="gray80",
        )
        self.btn_scan.grid(row=2, column=0, columnspan=2, pady=20)

    def handle_scan(self):
        self.btn_scan.configure(state="disabled")
        self.frm_container.add_stat("Scanning for junk...")
        self.frm_container.add_stat("Searching for cache directories...")
        local_cache_dirs = clean_my_windows.get_cache_dirs(clean_my_windows.LOCAL_DIR)

        cache_dirs = local_cache_dirs + [
            clean_my_windows.USER_TEMP_DIR,
            clean_my_windows.SYSTEM_TEMP_DIR,
            clean_my_windows.PREFETCH_DIR,
        ]

        self.frm_container.add_stat(f"Scan Results")
        self.display_sizes(
            {
                "User Temp": clean_my_windows.USER_TEMP_DIR,
                "System Temp": clean_my_windows.SYSTEM_TEMP_DIR,
                "Prefetch": clean_my_windows.PREFETCH_DIR,
                "Local Cache Dirs": clean_my_windows.LOCAL_DIR,
            },
            multiples={"Local Cache Dirs": local_cache_dirs},
        )

    def display_sizes(self, paths, multiples={}):
        total_size = 0
        for label, path in paths.items():
            if label in multiples:
                size = clean_my_windows.get_dirs_size(multiples[label])
            else:
                size = clean_my_windows.get_dir_size(path)
            total_size += size
            self.frm_container.add_stat(
                f"{label} Size: {clean_my_windows.get_formatted_size(size)}"
            )

        self.frm_container.add_stat(
            f"Total Size: {clean_my_windows.get_formatted_size(total_size)}"
        )


app = App()
app.mainloop()

import customtkinter as ctk
from PIL import Image
from components import DirStat
from utils import get_formatted_size
from paths import (
    USER_TEMP_DIR,
    SYSTEM_TEMP_DIR,
    PREFETCH_DIR,
    LOCAL_DIR,
)
import re
from utils import get_dir_size, get_dirs_size, get_formatted_size, get_cache_dirs


class App(ctk.CTk):
    MAX_COL = 8
    CURRENT_ROW = 0
    CURRENT_COL = 0

    def __init__(self):
        # Set Window Configuration
        super().__init__()
        self.iconbitmap("..\\cmw.ico")
        self.geometry("1080x700")
        self.resizable(width=False, height=False)
        self.title("Clean My Windows")
        ctk.set_appearance_mode("light")

        self.columnconfigure(0, weight=1)
        # Title Label
        self.lbl_title = ctk.CTkLabel(
            self, text="Clean My Windows", font=("Calibri", 35)
        )
        self.lbl_title.grid(row=0, column=0, pady=20)

        # Main Frame to display stats
        self.frm_main = ctk.CTkFrame(self, height=400, fg_color="gray94")
        self.frm_main.grid(
            row=1, column=0, padx=50, pady=20, sticky="nsew", columnspan=2
        )

        # Scan Button
        self.btn_scan = ctk.CTkButton(
            self,
            text="Scan Junk",
            font=ctk.CTkFont("Calibri", 20, weight="bold"),
            border_width=1,
            border_spacing=15,
            corner_radius=30,
            border_color="dark slate gray",
            fg_color="transparent",
            text_color="dark slate gray",
            hover_color="lemon chiffon",
            text_color_disabled="gray1",
            command=self.handle_scan,
        )
        self.btn_scan.grid(row=2, column=0, pady=20)

    def add_stat(
        self, name: str, dir_path: str, dir_size: str, row: int, column: int
    ) -> None:
        self.folder = DirStat(self.frm_main, name, dir_size, dir_path)
        self.folder.grid(row=row, column=column, ipadx=30, ipady=10, padx=10, pady=10)

    def handle_scan(self):
        self.btn_scan.configure(state="disabled", text="Scanning...")
        for name, dir_path in get_cache_dirs():
            size = get_formatted_size(get_dir_size(dir_path))
            if App.CURRENT_COL == App.MAX_COL:
                App.CURRENT_ROW += 1
                App.CURRENT_COL = 0
            self.add_stat(
                name=name,
                dir_path=dir_path,
                dir_size=size,
                row=App.CURRENT_ROW,
                column=App.CURRENT_COL,
            )
            App.CURRENT_COL += 1
            self.frm_main.update()
        self.display_options()

    def display_options(self):
        self.btn_scan.configure(state="normal", text="Clean", command=self.clean)
        self.btn_scan.grid(padx=10, sticky="e")
        self.btn_exit = ctk.CTkButton(
            self,
            text="Exit",
            font=ctk.CTkFont("Calibri", 20, weight="bold"),
            border_width=1,
            border_spacing=15,
            corner_radius=30,
            border_color="dark slate gray",
            fg_color="transparent",
            text_color="dark slate gray",
            hover_color="lemon chiffon",
            text_color_disabled="gray1",
            command=self.destroy,
        )
        self.columnconfigure((0, 1), weight=1)
        self.btn_exit.grid(row=2, column=1, pady=20, padx=10, sticky="w")

    def clean(self):
        print("Cleaning")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

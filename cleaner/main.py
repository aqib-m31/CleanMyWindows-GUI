import customtkinter as ctk
from components import MainFrame
from utils import get_formatted_size
from utils import (
    get_dir_size,
    get_formatted_size,
    get_cache_dirs,
    clean_dir,
)


class App(ctk.CTk):
    MAX_COL = 8
    CURRENT_ROW = 0
    CURRENT_COL = 0

    def __init__(self):
        # Set Window Configuration
        super().__init__()
        self.iconbitmap("images\\cmw.ico")
        self.geometry("1080x700")
        self.resizable(width=False, height=False)
        self.title("Clean My Windows")
        ctk.set_appearance_mode("light")
        self.columnconfigure(0, weight=1)

        # Title Label
        self.lbl_title = ctk.CTkLabel(
            self, text="CLEAN MY WINDOWS", font=ctk.CTkFont("Calibri", 38, "bold")
        )
        self.lbl_title.grid(row=0, column=0, pady=20, columnspan=2, sticky="new")

        # Main Frame to display stats
        self.frm_main = MainFrame(self)
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

    def handle_scan(self):
        self.btn_scan.configure(state="disabled", text="Scanning...")
        for name, dir_path in get_cache_dirs():
            size = get_dir_size(dir_path)
            self.frm_main.add_stat(
                name=name,
                dir_path=dir_path,
                dir_size=size,
            )
            self.frm_main.update()
        self.total_size = self.frm_main.display_total_size()
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
        self.prgbar = ctk.CTkProgressBar(self, progress_color="green")
        self.prgbar.grid(row=3, column=0, columnspan=2, padx=50, pady=15, sticky="ew")
        self.lbl_prgbar = ctk.CTkLabel(self, text="", font=("Calibri", 20))
        self.lbl_prgbar.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        self.btn_scan.configure(state="disabled", text="Cleaning")
        self.btn_exit.configure(state="disabled")

        total_cleaned_size = 0
        for dir in self.frm_main.get_dirs():
            cleaned_size = clean_dir(dir.path)
            total_cleaned_size += cleaned_size

            if cleaned_size < 0:
                dir.state = "error"
            else:
                dir.state = "cleaned"

            self.prgbar.set(total_cleaned_size / self.total_size)
            self.lbl_prgbar.configure(
                text=f"Cleaned: {get_formatted_size(total_cleaned_size)}"
            )
        self.btn_scan.configure(text="Cleaned")
        self.btn_exit.configure(state="normal")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

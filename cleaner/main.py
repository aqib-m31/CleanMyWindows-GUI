import customtkinter as ctk
from .components import MainFrame, CButton
from .utils import (
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
        super().__init__(fg_color="gray100")
        self.iconbitmap("cleaner\\images\\cmw.ico")
        self.geometry("1080x700")
        self.resizable(width=False, height=False)
        self.title("Clean My Windows")
        self.columnconfigure(0, weight=1)

        # Title Label
        self.lbl_title = ctk.CTkLabel(
            self,
            text="CLEAN MY WINDOWS",
            font=ctk.CTkFont("Calibri", 38, "bold"),
            fg_color="light sea green",
            text_color="white",
        )
        self.lbl_title.grid(
            row=0, column=0, ipady=20, pady=(0, 20), columnspan=2, sticky="new"
        )

        # Main Frame to display stats
        self.frm_main = MainFrame(self)
        self.frm_main.grid(
            row=1, column=0, padx=50, pady=20, sticky="nsew", columnspan=2
        )

        # Scan Button
        self.btn_scan = CButton(
            self,
            text="SCAN JUNK",
            command=self.handle_scan,
        )
        self.btn_scan.grid(row=2, column=0, pady=20)

    def handle_scan(self):
        """Handle scanning process."""
        self.btn_scan.configure(state="disabled", text="SCANNING")

        # Get name and path of cache directory and add dir stat to main frame
        for name, dir_path in get_cache_dirs():
            size = get_dir_size(dir_path)
            self.frm_main.add_stat(
                name=name,
                dir_path=dir_path,
                dir_size=size,
            )
            self.frm_main.update()

        # Display total size of cache dirs and display option for cleaning
        self.total_size = self.display_total_size()
        self.display_options()

    def display_options(self):
        """Display option for cleaning cache and exit."""
        self.btn_scan.destroy()
        self.btn_clean = CButton(self, text="CLEAN", command=self.clean)
        self.btn_clean.grid(row=2, column=0, pady=20, padx=10, sticky="e")

        self.btn_exit = CButton(self, text="EXIT", command=self.destroy)
        self.columnconfigure((0, 1), weight=1)
        self.btn_exit.grid(row=2, column=1, pady=20, padx=10, sticky="w")

    def clean(self):
        """Clean the cache directories."""
        self.lbl_total_size.destroy()

        # Display progress bar
        self.prgbar = ctk.CTkProgressBar(self, progress_color="light sea green")
        self.prgbar.set(0)
        self.prgbar.grid(row=3, column=0, columnspan=2, padx=50, pady=10, sticky="ew")
        self.lbl_prgbar = ctk.CTkLabel(
            self, text="", font=self.btn_exit.cget("font"), text_color="light sea green"
        )
        self.lbl_prgbar.grid(row=4, column=0, columnspan=2, pady=(0, 5), sticky="ew")

        # Disable clean button and exit button till cleaning finishes
        self.btn_clean.configure(state="disabled", text="CLEANING")
        self.btn_exit.configure(state="disabled")

        total_cleaned_size = 0
        for dir in self.frm_main.get_dirs():
            # Clean dir and keep track of cleaned size
            cleaned_size = clean_dir(dir.path)
            total_cleaned_size += cleaned_size

            # Update the state (check mark on folder)
            if cleaned_size < 0:
                dir.state = "error"
            else:
                dir.state = "cleaned"

            # Update the progress bar
            self.prgbar.set(total_cleaned_size / self.total_size)
            self.lbl_prgbar.configure(
                text=f"Cleaned: {get_formatted_size(total_cleaned_size)}"
            )

        if self.prgbar.get() != 1:
            self.lbl_msg = ctk.CTkLabel(self, text="[ACCESS DENIED] TO SOME FILES", font=ctk.CTkFont("Calibri", 15, "bold"), text_color="red")
            self.lbl_msg.grid(row=5, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        # Update Clean button text and restore state of exit button
        self.btn_clean.configure(text="CLEANED")
        self.btn_exit.configure(state="normal")

    def display_total_size(self):
        """Display the total size of the cache dirs."""
        dirs = self.frm_main.winfo_children()
        size = 0

        for dir in dirs:
            size += dir.dir_size

        self.lbl_total_size = ctk.CTkLabel(
            self,
            text=f"Total Size: {get_formatted_size(size)}",
            font=ctk.CTkFont("Calibri", 24, "bold"),
            text_color="light sea green",
        )
        self.lbl_total_size.grid(row=3, column=0, pady=10, columnspan=2, sticky="ew")

        return size


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

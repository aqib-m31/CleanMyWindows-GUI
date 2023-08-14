import customtkinter as ctk
from .components import MainFrame, CButton, CCheckBox
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
        self.width = self.winfo_screenwidth() - 100
        self.height = self.winfo_screenheight() - 100
        self.geometry(f"{self.width}x{self.height}+50+0")
        self.resizable(width=True, height=False)
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
        self.lbl_title.grid(row=0, column=0, ipady=20, sticky="new")

        # Frame to hold all content
        self.frame = ctk.CTkScrollableFrame(
            master=self,
            fg_color="white",
            height=(self.height - 2 * self.lbl_title.winfo_reqheight()),
        )
        self.frame.grid(row=1, column=0, sticky="nsew")
        self.frame.columnconfigure((0, 1), weight=1)

        # Main Frame to display stats
        self.frm_main = MainFrame(self.frame)
        self.frm_main.grid(
            row=0, column=0, padx=50, pady=20, sticky="nsew", columnspan=2
        )
        self.frm_main.bind("<Configure>", self.frm_main.align_items)

        # Scan Button
        self.btn_scan = CButton(
            self.frame,
            text="SCAN JUNK",
            command=self.handle_scan,
        )
        self.btn_scan.grid(row=1, column=0, pady=20, columnspan=2)

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
        self.btn_clean = CButton(self.frame, text="CLEAN", command=self.clean)
        self.btn_clean.grid(row=1, column=0, pady=20, padx=10, sticky="e")

        self.btn_exit = CButton(self.frame, text="EXIT", command=self.destroy)
        self.btn_exit.grid(row=1, column=1, pady=20, padx=10, sticky="w")

        self.checkbox_select_all = CCheckBox(
            self.frame, "Select All", command=self.select_all
        )
        self.checkbox_select_all.grid(row=1, column=1, sticky="e", padx=(0, 60))

    def clean(self):
        """Clean the cache directories."""
        self.lbl_total_size.destroy()

        # Disable select all option and select option on dirs
        self.checkbox_select_all.configure(state="disabled")
        self.frm_main.disable_all()

        # Display progress bar
        self.prgbar = ctk.CTkProgressBar(self.frame, progress_color="light sea green")
        self.prgbar.set(0)
        self.prgbar.grid(row=2, column=0, columnspan=2, padx=50, pady=10, sticky="ew")
        self.lbl_prgbar = ctk.CTkLabel(
            self.frame,
            text="",
            font=self.btn_exit.cget("font"),
            text_color="light sea green",
        )
        self.lbl_prgbar.grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky="ew")

        # Disable clean button and exit button till cleaning finishes
        self.btn_clean.configure(state="disabled", text="CLEANING")
        self.btn_exit.configure(state="disabled")

        total_cleaned_size = 0
        access_denied_files = 0
        for dir in self.frm_main.get_dirs():
            # Clean dir and keep track of cleaned size
            cleaned_size, access_denied_f = clean_dir(dir.path)
            total_cleaned_size += cleaned_size
            access_denied_files += access_denied_f

            # Update the state (check mark on folder)
            if cleaned_size < 1:
                dir.state = "error"
            else:
                dir.state = "cleaned"

            # Update the progress bar
            self.prgbar.set(total_cleaned_size / self.total_size)
            self.lbl_prgbar.configure(
                text=f"Cleaned: {get_formatted_size(total_cleaned_size)}"
            )

        if access_denied_files != 0:
            self.lbl_msg = ctk.CTkLabel(
                self.frame,
                text=f"[ACCESS DENIED] TO {access_denied_files} FILES",
                font=("Calibri", 15),
                text_color="red",
            )
            self.lbl_msg.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="ew")

        # Update Clean button text and restore state of exit button
        if total_cleaned_size == 0:
            self.btn_clean.configure(text="Nothing to Clean")
        else:
            self.btn_clean.configure(text="CLEANED")
        self.btn_exit.configure(state="normal")

    def display_total_size(self):
        """Display the total size of the cache dirs."""
        dirs = self.frm_main.winfo_children()
        size = 0

        for dir in dirs:
            size += dir.dir_size

        self.lbl_total_size = ctk.CTkLabel(
            self.frame,
            text=f"Total Size: {get_formatted_size(size)}",
            font=ctk.CTkFont("Calibri", 24, "bold"),
            text_color="light sea green",
        )
        self.lbl_total_size.grid(row=2, column=0, pady=10, columnspan=2, sticky="ew")

        return size

    def select_all(self):
        """Checks or unchecks all the folders."""
        if self.checkbox_select_all.get():
            self.frm_main.set_all(1)
        elif not self.checkbox_select_all.get():
            self.frm_main.set_all(0)


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

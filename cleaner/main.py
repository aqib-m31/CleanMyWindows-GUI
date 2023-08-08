import customtkinter as ctk
from .components import ContainerFrame
import os
from shutil import rmtree
from time import time

from .paths import (
    USER_TEMP_DIR,
    SYSTEM_TEMP_DIR,
    PREFETCH_DIR,
    LOCAL_DIR,
)

from .utils import get_dir_size, get_dirs_size, get_formatted_size, get_cache_dirs


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=("azure", "gray14"))
        # Setup window configuration
        self.title("Clean My Windows")
        self.geometry("1080x700")
        self.minsize(width=640, height=700)
        ctk.set_appearance_mode("light")
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        # Top Label
        self.lbl_title = ctk.CTkLabel(
            self,
            text="CLEAN MY WINDOWS",
            fg_color=("sky blue", "dark slate gray"),
            text_color=("gray1", "gray100"),
            font=("Calibri", 32),
            anchor="center",
            pady=25,
        )
        self.lbl_title.grid(row=0, column=0, sticky="new", columnspan=2)

        # Appearance switch (Dark/Light)
        self.mode = ctk.StringVar(value="off")
        self.switch_mode = ctk.CTkSwitch(
            self.lbl_title,
            text="Dark Mode",
            command=self.switch_appearance,
            variable=self.mode,
            onvalue="dark",
            offvalue="light",
        )
        self.switch_mode.grid(row=0, column=0, sticky="e", padx=(0, 20))

        # Container Frame (logs and stats)
        self.frm_container = ContainerFrame(self)
        self.frm_container.grid(
            row=1, column=0, sticky="ew", columnspan=2, pady=20, padx=20
        )

        # Scan Button
        self.btn_scan = ctk.CTkButton(
            self,
            text="Scan Junk",
            border_spacing=10,
            command=self.handle_scan,
            font=("Calibri", 20),
            fg_color=("cadetblue1", "SeaGreen"),
            hover_color=("SkyBlue1", "dark slate gray"),
            text_color_disabled=("gray40", "gray80"),
            text_color=("gray1", "gray100"),
        )
        self.btn_scan.grid(row=2, column=0, columnspan=2, pady=(0, 20))

    def handle_scan(self):
        """Handle scanning process."""
        # Prevent user from running scan process many times
        self.btn_scan.configure(state="disabled")

        # Add stats text
        self.frm_container.add_stat("Scanning for junk...\n")
        self.frm_container.add_stat("Searching for cache directories...\n")

        # Get all junk directories
        local_cache_dirs = get_cache_dirs(LOCAL_DIR)
        self.cache_dirs = local_cache_dirs + [
            USER_TEMP_DIR,
            SYSTEM_TEMP_DIR,
            PREFETCH_DIR,
        ]

        # Display scan results
        self.display_sizes(
            {
                "User Temp": USER_TEMP_DIR,
                "System Temp": SYSTEM_TEMP_DIR,
                "Prefetch": PREFETCH_DIR,
                "Local Cache Dirs": LOCAL_DIR,
            },
            multiples={"Local Cache Dirs": local_cache_dirs},
        )

    def display_sizes(self, paths, multiples={}):
        """Display the scan results."""
        self.frm_container.add_stat(f"Scan Results\n")

        total_size = 0
        for label, path in paths.items():
            if label in multiples:
                size = get_dirs_size(multiples[label])
            else:
                size = get_dir_size(path)
            total_size += size
            self.frm_container.add_stat(f"{label} Size: {get_formatted_size(size)}\n")

        self.frm_container.add_stat(f"Total Size: {get_formatted_size(total_size)}\n")

        # Destroy the scan button and display options.
        self.btn_scan.destroy()
        self.display_options()

    def display_options(self):
        """Display Clean Button and Exit Button"""
        self.btn_clean = ctk.CTkButton(
            self,
            text="Clean",
            border_spacing=10,
            command=self.handle_clean,
            font=("Calibri", 20),
            fg_color=("cadetblue1", "SeaGreen"),
            hover_color=("SkyBlue1", "dark slate gray"),
            text_color_disabled=("gray40", "gray80"),
            text_color=("gray1", "gray100"),
        )
        self.btn_clean.grid(
            row=2, column=0, columnspan=1, pady=(0, 20), padx=(0, 10), sticky="e"
        )

        self.btn_exit = ctk.CTkButton(
            self,
            text="Exit",
            border_spacing=10,
            command=self.handle_exit,
            font=("Calibri", 20),
            fg_color=("salmon", "red"),
            hover_color=("light coral", "indian red"),
            text_color_disabled="gray80",
            text_color=("gray1", "gray100"),
        )
        self.btn_exit.grid(
            row=2, column=1, columnspan=1, pady=(0, 20), padx=(10, 0), sticky="w"
        )

    def handle_clean(self):
        """Handle cleaning process."""

        # Disable clean and exit button
        self.btn_clean.configure(state="disabled")
        self.btn_exit.configure(state="disabled")

        self.frm_container.add_stat("Cleaning in progress...\n")

        # Start cleaning and keep track of cleaned size and update the stats frame
        start_time = time()
        cleaned_size = self.clean_dirs(self.cache_dirs)
        end_time = time()
        self.frm_container.add_stat(
            f"Total Space Freed: {get_formatted_size(cleaned_size)}\n"
        )
        self.frm_container.add_stat(
            f"Time Elapsed: {((end_time - start_time) * 1000):.2f}ms\n"
        )

        # Destroy clean button and restore the state of exit button
        self.btn_clean.destroy()
        self.btn_exit.grid(column=0, columnspan=2, sticky="")
        self.btn_exit.configure(state="normal")

    def clean_dirs(self, dirs: list) -> int:
        """
        Clean the list of directories

        :param dirs: List of directories to be cleaned
        :type dirs: list
        :return: Cleaned size
        :rtype: int
        """

        cleaned_size = 0

        for dir in dirs:
            try:
                files = os.listdir(dir)

                if not files:
                    self.frm_container.add_log(f"Nothing to clean in {dir}\n")
                    continue

                for file in files:
                    path = os.path.join(dir, file)

                    try:
                        if not os.path.isdir(path):
                            file_size = os.path.getsize(path)
                            self.frm_container.add_log(f"--> Removing {path}\n")
                            os.remove(path)
                        else:
                            file_size = get_dir_size(path)
                            self.frm_container.add_log(f"--> Removing {path}\n")
                            rmtree(path)
                    except PermissionError:
                        self.frm_container.add_log(
                            f"--> [ACCESS DENIED] Couldn't clean {path}\n"
                        )
                    except FileNotFoundError:
                        self.frm_container.add_log(f"--> [FILE NOT FOUND] {path}\n")
                    else:
                        cleaned_size += file_size
            except PermissionError:
                self.frm_container.add_log(
                    f"--> [ACCESS DENIED] Couldn't Clean {dir}\n"
                )
            except FileNotFoundError:
                self.frm_container.add_log(f"--> [DIRECTORY NOT FOUND] {dir}\n")

        return cleaned_size

    def handle_exit(self):
        """Exit the window."""
        self.destroy()

    def switch_appearance(self):
        """Switch appearance. Dark or Light"""
        self.iconify()
        ctk.set_appearance_mode(self.switch_mode.get())
        self.deiconify()


if __name__ == "__main__":
    app = App()
    app.mainloop()

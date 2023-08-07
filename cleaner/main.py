import customtkinter as ctk
from .components import ContainerFrame
import os
import shutil
import time
from cleaner import clean_my_windows


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
        self.btn_scan.destroy()

        self.frm_container.add_stat("Scanning for junk...")
        self.frm_container.add_stat("Searching for cache directories...")
        local_cache_dirs = clean_my_windows.get_cache_dirs(clean_my_windows.LOCAL_DIR)

        self.cache_dirs = local_cache_dirs + [
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

        self.display_options()

    def display_options(self):
        self.btn_clean = ctk.CTkButton(
            self,
            text="Clean",
            border_spacing=10,
            command=self.handle_clean,
            font=("Arial", 20),
            fg_color="SeaGreen",
            hover_color="dark slate gray",
            text_color_disabled="gray80",
        )
        self.btn_clean.grid(row=2, column=0, columnspan=1, pady=20, padx=(0, 10), sticky="e")

        self.btn_exit = ctk.CTkButton(
            self,
            text="Exit",
            border_spacing=10,
            command=self.handle_exit,
            font=("Arial", 20),
            fg_color="indian red",
            hover_color="salmon",
            text_color_disabled="gray80",
        )
        self.btn_exit.grid(row=2, column=1, columnspan=1, pady=20, padx=(10, 0), sticky="w")

    def handle_clean(self):
        self.btn_clean.configure(state="disabled")
        self.btn_exit.configure(state="disabled")

        self.frm_container.add_stat("Cleaning in progress...")
        start_time = time.time()
        cleaned_size = self.clean_dirs(self.cache_dirs)
        end_time = time.time()
        self.frm_container.add_stat(f"Total Space Freed: {clean_my_windows.get_formatted_size(cleaned_size)}")
        self.frm_container.add_stat(f"Time Elapsed: {((end_time - start_time) * 1000):.2f}ms")
        self.btn_clean.destroy()
        self.btn_exit.grid(column=0, columnspan=2, sticky="")
        self.btn_exit.configure(state="normal")

    def clean_dirs(self, dirs):
        cleaned_size = 0
        for dir in dirs:
            try:
                files = os.listdir(dir)
                if not files:
                    self.frm_container.add_log(f"Nothing to clean in {dir}")
                    continue
                
                for file in files:
                    path = os.path.join(dir, file)

                    try:
                        if not os.path.isdir(path):
                            file_size = os.path.getsize(path)
                            self.frm_container.add_log(f"--> Removing {path}")
                            os.remove(path)
                        else:
                            file_size = clean_my_windows.get_dir_size(path)
                            self.frm_container.add_log(f"--> Removing {path}")
                            shutil.rmtree(path)
                    except PermissionError:
                        self.frm_container.add_log(f"[ACCESS DENIED] Couldn't clean {path}")
                    else:
                        cleaned_size += file_size
            except PermissionError:
                self.frm_container.add_log(f"[ACCESS DENIED] Couldn't Clean {dir}")    

        return cleaned_size
    
    def handle_exit(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

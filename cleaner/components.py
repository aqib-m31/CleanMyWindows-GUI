import customtkinter as ctk
from PIL import Image
from utils import get_formatted_size


class DirStat(ctk.CTkFrame):
    states = {
        "cleaned": ctk.CTkImage(Image.open("done.png"), size=(25, 25)),
        "error": ctk.CTkImage(Image.open("error.png"), size=(25, 25)),
    }

    def __init__(self, master, name, dir_size, path):
        super().__init__(master, fg_color="transparent")
        self.name = name
        self.dir_size = dir_size
        self.path = path
        self.columnconfigure(0, weight=1)

        self.dir_icon = ctk.CTkImage(Image.open("folder.png"), size=(60, 60))
        self.lbl_dir_icon = ctk.CTkLabel(self, image=self.dir_icon, text="")
        self.lbl_dir_icon.grid(row=0, column=0, pady=(5, 5), padx=(5, 5))

        self.lbl_name = ctk.CTkLabel(self, text=self.name)
        self.lbl_name.grid(row=1, column=0)

        self.lbl_size = ctk.CTkLabel(self, text=get_formatted_size(self.dir_size))
        self.lbl_size.grid(row=2, column=0)

        self.state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: str):
        if hasattr(self, "lbl_state_img"):
            if self.lbl_state_img:
                self.lbl_state_img.destroy()

        if not value:
            self._state = None
            return

        value = value.lower()
        if value not in DirStat.states:
            raise ValueError("State must be in ['cleaned', 'error', None]")

        if value == "error":
            self.bell()
        self._state = value
        self.lbl_state_img = ctk.CTkLabel(self, image=DirStat.states[value], text="")
        self.lbl_state_img.grid(row=3, column=0)
        self.update()


class MainFrame(ctk.CTkScrollableFrame):
    CURRENT_ROW = 0
    CURRENT_COL = 0
    MAX_COL = 7

    def __init__(self, master):
        super().__init__(master=master, fg_color="gray94", height=370)

    def add_stat(self, name: str, dir_path: str, dir_size: str) -> None:
        self.folder = DirStat(self, name, dir_size, dir_path)
        if MainFrame.CURRENT_COL > MainFrame.MAX_COL:
            MainFrame.CURRENT_COL = 0
            MainFrame.CURRENT_ROW += 1
        self.folder.grid(
            row=MainFrame.CURRENT_ROW,
            column=MainFrame.CURRENT_COL,
            ipadx=30,
            ipady=10,
            padx=10,
            pady=10,
        )
        MainFrame.CURRENT_COL += 1

    def display_total_size(self):
        dirs = self.winfo_children()
        size = 0
        for dir in dirs:
            size += dir.dir_size

        self.lbl_total_size = ctk.CTkLabel(
            self,
            text=f"Total Size: {get_formatted_size(size)}",
            font=ctk.CTkFont("Calibri", 24, "bold"),
            text_color="sea green",
        )
        self.lbl_total_size.grid(
            row=MainFrame.CURRENT_ROW + 1, column=0, pady=20, sticky="ew", columnspan=8
        )
        self.columnconfigure(tuple(range(8)), weight=1)
        return size

    def get_dirs(self):
        for dir in self.winfo_children():
            if isinstance(dir, DirStat):
                yield dir

import customtkinter as ctk
from PIL import Image


class DirStat(ctk.CTkFrame):
    states = {
        "cleaned": ctk.CTkImage(Image.open("done.png"), size=(25, 25)),
        "error": ctk.CTkImage(Image.open("error.png"), size=(25, 25)),
    }

    def __init__(self, master, name, dir_size, path):
        super().__init__(master, height=200, width=300, fg_color="transparent")
        self.name = name
        self.dir_size = dir_size
        self.path = path
        self.columnconfigure(0, weight=1)

        self.dir_icon = ctk.CTkImage(Image.open("folder.png"), size=(60, 60))
        self.lbl_dir_icon = ctk.CTkLabel(self, image=self.dir_icon, text="")
        self.lbl_dir_icon.grid(row=0, column=0, pady=(5, 5), padx=(5, 5))

        self.lbl_name = ctk.CTkLabel(self, text=self.name)
        self.lbl_name.grid(row=1, column=0)

        self.lbl_size = ctk.CTkLabel(self, text=self.dir_size)
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

        self._state = value
        self.lbl_state_img = ctk.CTkLabel(self, image=DirStat.states[value], text="")
        self.lbl_state_img.grid(row=3, column=0)

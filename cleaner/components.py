import customtkinter as ctk
from PIL import Image
from utils import get_formatted_size


class DirStat(ctk.CTkFrame):
    # Dict of states with respective images as their values
    states = {
        "cleaned": ctk.CTkImage(Image.open("images\\done.png"), size=(25, 25)),
        "error": ctk.CTkImage(Image.open("images\\error.png"), size=(25, 25)),
    }

    def __init__(self, master, name, dir_size, path):
        super().__init__(master, fg_color="transparent")

        # Configure attributes
        self.name = name
        self.dir_size = dir_size
        self.path = path
        self.columnconfigure(0, weight=1)

        # Directory icon
        self.dir_icon = ctk.CTkImage(Image.open("images\\folder.png"), size=(60, 60))
        self.lbl_dir_icon = ctk.CTkLabel(self, image=self.dir_icon, text="")
        self.lbl_dir_icon.grid(row=0, column=0, pady=(5, 5), padx=(5, 5))

        # Name of dir
        self.lbl_name = ctk.CTkLabel(self, text=self.name)
        self.lbl_name.grid(row=1, column=0)

        # Size of dir
        self.lbl_size = ctk.CTkLabel(self, text=get_formatted_size(self.dir_size))
        self.lbl_size.grid(row=2, column=0)

        self.state = None

    @property
    def state(self) -> str | None:
        """Return the state of dir."""
        return self._state

    @state.setter
    def state(self, value: str | None) -> None:
        """
        Set the state of dir.
        :param value: State of dir (cleaned, error or None)
        :type value: str | None
        """
        # Make sure the object has lbl_state_img attribute
        if hasattr(self, "lbl_state_img"):
            # Make sure lbl_state_img is not None and destroy the previous Label object
            if self.lbl_state_img:
                self.lbl_state_img.destroy()

        # Update State if value is None
        if not value:
            self._state = None
            return

        # Make sure value is a valid state
        value = value.lower()
        if value not in DirStat.states:
            raise ValueError("State must be in ['cleaned', 'error', None]")

        # Make sound if state is error
        if value == "error":
            self.bell()

        # Update state and view
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
        self.folder = None

    def add_stat(self, name: str, dir_path: str, dir_size: int) -> None:
        """
        Add cache dir stat to main frame.
        :param name: Name of the dir
        :type name: str
        :param dir_path: Path of the dir
        :type dir_path: str
        :param dir_size: Size of the dir in bytes
        :type dir_size: int
        """
        self.folder = DirStat(self, name, dir_size, dir_path)

        # Make sure icon appears on next line when there's no space
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

    def get_dirs(self):
        """Yield DirStat objects in main frame."""
        for dir in self.winfo_children():
            if isinstance(dir, DirStat):
                yield dir

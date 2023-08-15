import customtkinter as ctk
from .components import Frame


class App(ctk.CTk):
    """
    Represents the main application class.

    This class extends the ctk.CTk class and sets up the main application window.

    Methods:
        __init__: Initializes the App instance.
    """

    def __init__(self):
        """
        Initialize the main application window.

        Set up window configuration, title, labels, and the main content frame.
        """
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
        self.frame = Frame(
            self,
            height=(self.height - 2 * self.lbl_title.winfo_reqheight()),
            fg_color="white",
        )
        self.frame.grid(row=1, column=0, sticky="nsew")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()

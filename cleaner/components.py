"""
components.py

This module contains classes that define custom components for the Clean My Windows application.
These components are used to create the user interface elements displayed in the application's GUI.

Classes:
- DirStat: Represents statistics about a directory.
- MainFrame: Represents the main frame of the application.
- CButton: Represents a custom button.
- CCheckBox: Represents a custom checkbox.
- Frame: Represents a scrollable frame for containing UI elements.
"""


import customtkinter as ctk
from PIL import Image
from .utils import (
    get_dir_size,
    get_formatted_size,
    get_cache_dirs,
    clean_dir,
)


class DirStat(ctk.CTkFrame):
    """
    Represents statistics about a directory.

    This class defines a custom frame that displays information about a directory,
    including its name, size, and state. It also provides methods for updating the
    state of the directory and handling user interactions.

    Attributes:
        name (str): The name of the directory.
        dir_size (int): The size of the directory in bytes.
        path (str): The path to the directory.
        state (str | None): The state of the directory (cleaned, error, or None).

    Methods:
        __init__(self, master, name, dir_size, path):
            Initializes a new DirStat instance.
        state:
            Getter and setter property for the state of the directory.
        check_select_all:
            Checks the "Select All" checkbox if all directories are selected,
            or unchecks it if any directory checkbox is unchecked.

    The `DirStat` class encapsulates the visual representation of directory statistics
    in the Clean My Windows application. It manages the display of directory names,
    sizes, and states, and facilitates interactions with user checkboxes.
    """

    # Dict of states with respective images as their values
    states = {
        "cleaned": ctk.CTkImage(Image.open("cleaner\\images\\done.png"), size=(25, 25)),
        "error": ctk.CTkImage(Image.open("cleaner\\images\\error.png"), size=(25, 25)),
    }

    def __init__(self, master, name, dir_size, path):
        super().__init__(master, fg_color="transparent")
        self.master = master

        # Configure attributes
        self.name = name
        self.dir_size = dir_size
        self.path = path
        self.columnconfigure(0, weight=1)

        # Directory icon
        self.dir_icon = ctk.CTkImage(
            Image.open("cleaner\\images\\folder.png"), size=(60, 60)
        )
        self.lbl_dir_icon = ctk.CTkLabel(self, image=self.dir_icon, text="")
        self.lbl_dir_icon.grid(row=0, column=0, pady=(5, 5), padx=(5, 0), sticky="new")

        # Checkbox for selecting the directory
        self.checkbox = ctk.CTkCheckBox(
            self,
            width=20,
            height=20,
            text="",
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            border_color="light sea green",
            fg_color="light sea green",
            command=self.check_select_all,
        )
        self.checkbox.grid(row=0, column=0, sticky="ne")

        # Name of the directory
        self.lbl_name = ctk.CTkLabel(self, text=self.name, text_color="gray1")
        self.lbl_name.grid(row=1, column=0, sticky="new")

        # Size of the directory
        self.lbl_size = ctk.CTkLabel(
            self, text=get_formatted_size(self.dir_size), text_color="gray1"
        )
        self.lbl_size.grid(row=2, column=0, sticky="new")

        self.state = None

    @property
    def state(self) -> str | None:
        """Return the state of the directory."""
        return self._state

    @state.setter
    def state(self, value: str | None) -> None:
        """
        Set the state of the directory.
        :param value: State of the directory (cleaned, error, or None)
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

    def check_select_all(self):
        """
        Check the "Select All" checkbox if all checkboxes are selected,
        or uncheck it if any of the checkboxes is unchecked.
        """
        total_dirs = len(MainFrame.dirs)
        checked_dirs = 0

        for directory in MainFrame.dirs:
            if directory.checkbox.get():
                checked_dirs += 1

        # Determine whether to set the "Select All" checkbox as checked or unchecked
        if checked_dirs == total_dirs:
            MainFrame.selected_all = True
        else:
            MainFrame.selected_all = False

        # Update the "Select All" checkbox in the master frame
        self.master.check_select_all()


class MainFrame(ctk.CTkScrollableFrame):
    """
    Represents the main frame that displays directory statistics.

    This class defines a custom scrollable frame that holds and manages the display
    of directory statistics. It provides methods for adding statistics, selecting
    directories, and aligning items within the frame.

    Attributes:
        CURRENT_ROW (int): Current row index for grid placement.
        CURRENT_COL (int): Current column index for grid placement.
        MAX_COL (int): Maximum number of columns for layout.
        dirs (List[DirStat]): List of DirStat instances for displayed directories.
        selected_all (bool): Flag indicating whether all directories are selected.

    Methods:
        __init__: Initializes the MainFrame instance.
        add_stat: Adds a new directory statistics widget to the main frame.
        get_dirs: Yields selected DirStat objects in the main frame.
        set_all: Sets the value of all directory checkboxes.
        disable_all: Disables checkboxes of all DirStat instances.
        align_items: Aligns directory widgets within the frame.
        check_select_all: Checks or unchecks the "Select All" checkbox based on selection status.
    """

    CURRENT_ROW = 0
    CURRENT_COL = 0
    MAX_COL = 7
    dirs = []
    selected_all = False

    def __init__(self, master, select_all):
        """
        Initialize the MainFrame instance.

        :param master: The parent widget.
        :param select_all: Ref. to "Select All" checkbox widget.
        """
        super().__init__(master=master, fg_color="gray97", height=370)
        self.master = master
        self.folder = None
        self.select_all = select_all

    def add_stat(self, name: str, dir_path: str, dir_size: int) -> None:
        """
        Add cache directory stat to main frame.

        :param name: Name of the directory.
        :param dir_path: Path of the directory.
        :param dir_size: Size of the directory in bytes.
        """
        # Create a new DirStat instance for the given directory
        self.folder = DirStat(self, name, dir_size, dir_path)

        # Calculate the maximum number of columns based on available space
        MainFrame.MAX_COL = self.winfo_width() // (self.folder.winfo_reqwidth() + 130)

        # Check if the current column exceeds the maximum, then move to the next row
        if MainFrame.CURRENT_COL > MainFrame.MAX_COL:
            MainFrame.CURRENT_COL = 0
            MainFrame.CURRENT_ROW += 1

        # Place the DirStat widget in the grid
        self.folder.grid(
            row=MainFrame.CURRENT_ROW,
            column=MainFrame.CURRENT_COL,
            ipadx=30,
            ipady=10,
            padx=10,
            pady=10,
            sticky="n",
        )

        # Increment the column index and store the added folder in the list
        MainFrame.CURRENT_COL += 1
        MainFrame.dirs.append(self.folder)

    def get_dirs(self):
        """
        Yield selected DirStat objects in the main frame.
        """
        for directory in MainFrame.dirs:
            if directory.checkbox.get():
                yield directory

    def set_all(self, value: int) -> None:
        """
        Sets the value of all the checkboxes.

        :param value: Value to be set (0 or 1)
        :type value: int
        """
        for directory in MainFrame.dirs:
            if not value:
                directory.checkbox.deselect()
            elif value == 1:
                directory.checkbox.select()
        if value == 1:
            MainFrame.selected_all = True
        elif value == 0:
            MainFrame.selected_all = False

    def disable_all(self):
        """
        Disables all the checkboxes of DirStat instances.
        """
        for directory in MainFrame.dirs:
            directory.checkbox.configure(state="disabled")

    def align_items(self, event):
        """
        Aligns directory widgets within the frame based on available space.
        """
        if not len(MainFrame.dirs):
            return

        max_cols = self.winfo_width() // (self.folder.winfo_reqwidth() + 130)

        if MainFrame.MAX_COL == max_cols:
            return

        MainFrame.MAX_COL = max_cols
        MainFrame.CURRENT_COL = 0
        MainFrame.CURRENT_ROW = 0
        for directory in MainFrame.dirs:
            if MainFrame.CURRENT_COL > MainFrame.MAX_COL:
                MainFrame.CURRENT_COL = 0
                MainFrame.CURRENT_ROW += 1

            directory.grid(row=MainFrame.CURRENT_ROW, column=MainFrame.CURRENT_COL)

            MainFrame.CURRENT_COL += 1

        self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all"))

    def check_select_all(self):
        """
        Checks the "Select All" checkbox if all checkboxes are selected,
        or unchecks it if any of the checkboxes is unchecked.
        """
        if MainFrame.selected_all:
            self.select_all.select()
        else:
            self.select_all.deselect()


class CButton(ctk.CTkButton):
    """
    Represents a custom button with enhanced visual styling.

    This class extends the ctk.CTkButton class to provide a custom button with
    enhanced visual styling, including font settings, border styles, and color options.

    Attributes:
        master: The parent widget.
        text (str): The text to display on the button.
        command: The function to be called when the button is clicked.

    Methods:
        __init__: Initializes the CButton instance with custom styles.
    """

    def __init__(self, master, text, command):
        super().__init__(master=master, text=text, command=command)

        # Configure the button's visual properties
        self.configure(
            font=ctk.CTkFont("Calibri", 20, weight="bold"),
            border_width=1,
            border_spacing=15,
            corner_radius=15,
            border_color="light sea green",
            fg_color="transparent",
            text_color="light sea green",
            hover_color="alice blue",
            text_color_disabled="gray50",
        )


class CCheckBox(ctk.CTkCheckBox):
    """
    Represents a custom checkbox with enhanced visual styling.

    This class extends the ctk.CTkCheckBox class to provide a custom checkbox with
    enhanced visual styling, including size, border styles, and color options.

    Attributes:
        master: The parent widget.
        text (str): The label to display next to the checkbox.
        command: The function to be called when the checkbox is clicked.

    Methods:
        __init__: Initializes the CCheckBox instance with custom styles.
    """

    def __init__(self, master, text, command):
        super().__init__(master=master, text=text, command=command)

        # Configure the checkbox's visual properties
        self.configure(
            width=20,
            height=20,
            checkbox_width=20,
            checkbox_height=20,
            border_width=2,
            border_color="light sea green",
            fg_color="light sea green",
        )


class Frame(ctk.CTkScrollableFrame):
    """
    Represents a custom frame for displaying cache directory statistics and actions.

    This class extends the ctk.CTkScrollableFrame class to create a custom frame
    for displaying cache directory statistics, providing actions like scanning,
    cleaning, and exiting.

    Attributes:
        master: The parent widget.
        height: The height of the frame.
        fg_color: The foreground color of the frame.

    Methods:
        select_all: Checks or unchecks all the folders.
        handle_scan: Handles the scanning process.
        display_options: Displays options for cleaning and exiting.
        clean: Cleans the cache directories.
        display_total_size: Displays the total size of the cache dirs.
    """

    def __init__(self, master, height, fg_color):
        super().__init__(master=master, height=height, fg_color=fg_color)
        self.columnconfigure((0, 1), weight=1)
        self.master = master

        # Create a "Select All" checkbox
        self.checkbox_select_all = CCheckBox(
            self, "Select All", command=self.select_all
        )

        # Main Frame to display stats
        self.frm_main = MainFrame(self, self.checkbox_select_all)
        self.frm_main.grid(
            row=0, column=0, padx=50, pady=20, sticky="nsew", columnspan=2
        )
        self.frm_main.bind("<Configure>", self.frm_main.align_items)

        # Create a "Scan" Button
        self.btn_scan = CButton(
            self,
            text="SCAN JUNK",
            command=self.handle_scan,
        )
        self.btn_scan.grid(row=1, column=0, pady=20, columnspan=2)

    def select_all(self):
        """Checks or unchecks all the folders."""
        if self.checkbox_select_all.get():
            self.frm_main.set_all(1)
        elif not self.checkbox_select_all.get():
            self.frm_main.set_all(0)

    def handle_scan(self):
        """Handle scanning process."""
        self.btn_scan.configure(state="disabled", text="SCANNING")

        # Get name and path of cache directory and add directory stat to main frame
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
        self.btn_clean.grid(row=1, column=0, pady=20, padx=10, sticky="e")

        self.btn_exit = CButton(self, text="EXIT", command=self.master.destroy)
        self.btn_exit.grid(row=1, column=1, pady=20, padx=10, sticky="w")

        self.checkbox_select_all.grid(row=1, column=1, sticky="e", padx=(0, 60))

    def clean(self):
        """Clean the cache directories."""
        self.lbl_total_size.destroy()

        # Disable select all option and select option on dirs
        self.checkbox_select_all.configure(state="disabled")
        self.frm_main.disable_all()

        # Display progress bar
        self.prgbar = ctk.CTkProgressBar(self, progress_color="light sea green")
        self.prgbar.set(0)
        self.prgbar.grid(row=2, column=0, columnspan=2, padx=50, pady=10, sticky="ew")
        self.lbl_prgbar = ctk.CTkLabel(
            self,
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
        for directory in self.frm_main.get_dirs():
            # Clean directory and keep track of cleaned size
            cleaned_size, access_denied_f = clean_dir(directory.path)
            total_cleaned_size += cleaned_size
            access_denied_files += access_denied_f

            # Update the state (check mark on folder)
            if cleaned_size < 1:
                directory.state = "error"
            else:
                directory.state = "cleaned"

            # Update the progress bar
            self.prgbar.set(total_cleaned_size / self.total_size)
            self.lbl_prgbar.configure(
                text=f"Cleaned: {get_formatted_size(total_cleaned_size)}"
            )

        if access_denied_files != 0:
            self.lbl_msg = ctk.CTkLabel(
                self,
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

        for directory in dirs:
            size += directory.dir_size

        self.lbl_total_size = ctk.CTkLabel(
            self,
            text=f"Total Size: {get_formatted_size(size)}",
            font=ctk.CTkFont("Calibri", 24, "bold"),
            text_color="light sea green",
        )
        self.lbl_total_size.grid(row=2, column=0, pady=10, columnspan=2, sticky="ew")

        return size

import customtkinter as ctk


class ContainerFrame(ctk.CTkFrame):
    # Track current line number in stats frame and log frame
    stat_line = 1
    log_line = 1

    def __init__(self, master):
        super().__init__(master, width=450, fg_color=("azure2", "gray17"))
        self.columnconfigure((0, 1), weight=1)

        # Log Frame
        self.frm_log = ctk.CTkFrame(
            master=self, height=450, width=400, fg_color=("azure3", "gray20")
        )
        self.frm_log.columnconfigure(0, weight=1)

        # Log Label
        self.lbl_log = ctk.CTkLabel(
            self.frm_log,
            text="Log",
            text_color=("gray1", "gray100"),
            font=("Calibri", 20),
            anchor="center",
            corner_radius=5,
            fg_color=("azure", "gray24"),
        )
        self.lbl_log.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        # Log Text box
        self.txt_log = ctk.CTkTextbox(
            self.frm_log,
            height=400,
            fg_color=("azure", "gray22"),
            text_color=("gray1", "gray100"),
            state="disabled",
            wrap="none",
            padx=10,
            pady=10,
            spacing1=5,
        )
        self.txt_log.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.frm_log.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        # Stats Frame
        self.frm_stat = ctk.CTkFrame(
            master=self, height=400, width=400, fg_color=("azure3", "gray20")
        )
        self.frm_stat.columnconfigure(0, weight=1)

        # Stats Label
        self.lbl_stats = ctk.CTkLabel(
            self.frm_stat,
            text="Stats",
            text_color=("gray1", "gray100"),
            font=("Calibri", 20),
            anchor="center",
            corner_radius=5,
            fg_color=("azure", "gray24"),
        )
        self.lbl_stats.grid(row=0, column=0, sticky="ew", pady=10, padx=10, ipadx=20)

        # Stats Textbox
        self.txt_stats = ctk.CTkTextbox(
            self.frm_stat,
            height=400,
            fg_color=("azure", "gray22"),
            text_color=("gray1", "gray100"),
            state="disabled",
            font=("Calibri", 18),
            padx=10,
            pady=10,
            spacing1=5,
        )
        self.txt_stats.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.frm_stat.grid(row=0, column=1, sticky="ew", padx=20)

    def add_stat(self, stat: str) -> None:
        """Handle inserting stats in Stats Frame"""
        self.txt_stats.configure(state="normal")
        self.txt_stats.insert(f"{ContainerFrame.stat_line}.0", stat)
        self.txt_stats.configure(state="disabled")
        self.frm_stat.update()
        self.txt_stats.see(ctk.END)
        ContainerFrame.stat_line += 1

    def add_log(self, log: str) -> None:
        """Handle inserting logs in Log Frame"""
        self.txt_log.configure(state="normal")
        self.txt_log.insert(f"{ContainerFrame.log_line}.0", log)
        self.txt_log.configure(state="disabled")
        self.frm_stat.update()
        self.txt_log.see(ctk.END)
        ContainerFrame.log_line += 1

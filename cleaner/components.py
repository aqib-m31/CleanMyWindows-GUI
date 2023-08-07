import customtkinter as ctk


class LabelFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure((0, 1), weight=1)
        self.lbl_log = ctk.CTkLabel(
            self,
            text="Log",
            text_color="gray100",
            font=("Times", 30),
            anchor="center",
            corner_radius=6,
        )
        self.lbl_log.grid(row=0, column=0, sticky="ew", pady=20)
        self.lbl_stats = ctk.CTkLabel(
            self,
            text="Stats",
            text_color="gray100",
            font=("Times", 30),
            anchor="center",
        )
        self.lbl_stats.grid(row=0, column=1, sticky="ew", pady=20)


class ContainerFrame(ctk.CTkFrame):
    stat_row = 0
    log_row = 0

    def __init__(self, master):
        super().__init__(master, width=450)
        self.columnconfigure((0, 1), weight=1)
        self.frm_log = ctk.CTkScrollableFrame(
            master=self,
            height=400,
            width=400,
            label_text="Log",
            label_anchor="center",
            label_font=("", 20),
        )
        self.frm_log.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.frm_stat = ctk.CTkScrollableFrame(
            master=self,
            height=400,
            width=400,
            label_text="Stats",
            label_anchor="center",
            label_font=("", 20),
        )
        self.frm_stat.grid(row=0, column=1, sticky="ew", padx=20)
        self.frm_stat.columnconfigure(0, weight=1)

    def add_stat(self, value):
        label = ctk.CTkLabel(self.frm_stat, text=value)
        label.grid(row=ContainerFrame.stat_row, column=0, padx=(10, 0), sticky="w")
        self.frm_stat.update()
        ContainerFrame.stat_row += 1

    def add_log(self, value):
        label = ctk.CTkLabel(self.frm_log, text=value)
        label.grid(row=ContainerFrame.log_row, column=0, padx=(10, 0), sticky="w")
        self.frm_log.update()
        ContainerFrame.log_row += 1

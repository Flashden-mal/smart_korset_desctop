import customtkinter as ctk

class PatientRegistrationView(ctk.CTkFrame):
    def __init__(self, master, on_proceed, on_cancel):
        super().__init__(master, fg_color="transparent")
        self.on_proceed = on_proceed
        self.container = ctk.CTkFrame(self, width=600, height=750, corner_radius=50, fg_color="#FFFFFF", border_width=1, border_color="#E5E5E7")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        self.container.pack_propagate(False)

        ctk.CTkLabel(self.container, text="НОВЫЙ ПАЦИЕНТ", font=("Segoe UI Variable Display", 36, "bold")).pack(pady=(70, 10))
        ctk.CTkLabel(self.container, text="Создание учетной записи пациента", font=("Segoe UI Variable Display", 14), text_color="gray").pack(pady=(0, 60))

        self.n_e = ctk.CTkEntry(self.container, placeholder_text="Фамилия Имя Отчество", width=470, height=65, corner_radius=20, fg_color="#F5F5F7", border_width=0, font=("Segoe UI Variable", 17))
        self.n_e.pack(pady=20)

        r = ctk.CTkFrame(self.container, fg_color="transparent"); r.pack(fill="x", padx=65)
        self.g = ctk.CTkOptionMenu(r, values=["Мужской", "Женский"], width=160, height=55, corner_radius=15, fg_color="#F5F5F7", text_color="black", button_color="#E5E5E7")
        self.g.pack(side="left")
        
        d_f = ctk.CTkFrame(r, fg_color="transparent"); d_f.pack(side="right")
        e_cfg = {"height": 55, "corner_radius": 15, "border_width": 0, "fg_color": "#F5F5F7", "justify": "center", "font": ("Segoe UI Variable", 17)}
        self.d, self.m, self.y = ctk.CTkEntry(d_f, placeholder_text="ДД", width=60, **e_cfg), ctk.CTkEntry(d_f, placeholder_text="ММ", width=60, **e_cfg), ctk.CTkEntry(d_f, placeholder_text="ГГГГ", width=95, **e_cfg)
        for e in [self.d, self.m, self.y]: e.pack(side="left", padx=2)

        self.d.bind("<KeyRelease>", lambda e: self._tab(self.d, self.m, 2))
        self.m.bind("<KeyRelease>", lambda e: self._tab(self.m, self.y, 2))
        self.y.bind("<KeyRelease>", lambda e: self._tab(self.y, None, 4))

        ctk.CTkFrame(self.container, fg_color="transparent").pack(expand=True, fill="both")
        ctk.CTkButton(self.container, text="ПРОДОЛЖИТЬ", width=470, height=75, corner_radius=37, font=("Segoe UI Variable Display", 18, "bold"), fg_color="#007AFF", command=self.submit).pack(pady=(0, 20))
        ctk.CTkButton(self.container, text="Отмена", fg_color="transparent", text_color="gray", command=on_cancel).pack(pady=(0, 40))

    def _tab(self, c, n, l):
        if len(c.get()) > l: c.delete(l, 'end')
        if len(c.get()) == l and n: n.focus()

    def submit(self):
        self.on_proceed(self.n_e.get(), {"day": self.d.get(), "month": self.m.get(), "year": self.y.get()})
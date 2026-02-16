import customtkinter as ctk

class InitialExamView(ctk.CTkFrame):
    def __init__(self, master, p_id, p_name, code, age, on_save_callback):
        super().__init__(master, fg_color="transparent")
        self.p_id, self.p_name, self.code = p_id, p_name, code
        self.on_save = on_save_callback 

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0)
        self.scroll.pack(fill="both", expand=True, padx=60, pady=20)

        title_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        title_f.pack(fill="x", pady=(0, 40))
        ctk.CTkLabel(title_f, text="Первичный протокол осмотра", font=("Segoe UI Variable Display", 36, "bold"), text_color="#1D1D1F").pack(side="left")
        
        banner = ctk.CTkFrame(title_f, fg_color="#007AFF", corner_radius=15)
        banner.pack(side="right")
        ctk.CTkLabel(banner, text=f"ИНВАЙТ: {code}", font=("Segoe UI Variable Display", 14, "bold"), text_color="white", padx=20, pady=8).pack()

        self.inputs = {}
        self.add_section("1. Физикальные данные", [("Рост (см)", "height"), ("Вес (кг)", "weight"), ("Возраст", "age")], age)
        self.add_section("2. Диагностика деформации", [("Угол Кобба (TH)°", "cobb_th"), ("Угол Кобба (L)°", "cobb_l"), ("Тест Адамса (ATR)°", "atr"), ("Тест Риссера (0-5)", "risser")])
        self.add_section("3. Визуальные маркеры", [("Асимметрия плеч (см)", "shoulders"), ("Перекос таза (см)", "pelvis"), ("Шкала боли (0-10)", "pain")])

        ctk.CTkLabel(self.scroll, text="4. Заключение и назначения", font=("Segoe UI Variable", 18, "bold")).pack(anchor="w", padx=10, pady=(30, 10))
        self.notes = ctk.CTkTextbox(self.scroll, height=200, corner_radius=30, border_width=1, border_color="#E5E5E7", fg_color="#FFFFFF", font=("Segoe UI Variable", 16))
        self.notes.pack(fill="x", padx=5, pady=10)
        self.notes.insert("0.0", "Рекомендации: ")

        ctk.CTkButton(self.scroll, text="ЗАНЕСТИ ДАННЫЕ И СФОРМИРОВАТЬ КОД", 
                      height=80, corner_radius=40, font=("Segoe UI Variable Display", 20, "bold"),
                      fg_color="#34C759", hover_color="#28A745", command=self.save_and_redirect).pack(fill="x", pady=60)

    def add_section(self, title, fields, auto_age=None):
        ctk.CTkLabel(self.scroll, text=title, font=("Segoe UI Variable", 18, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        card = ctk.CTkFrame(self.scroll, corner_radius=30, fg_color="#FFFFFF", border_width=1, border_color="#E5E5E7")
        card.pack(fill="x", padx=5, pady=5)
        grid = ctk.CTkFrame(card, fg_color="transparent"); grid.pack(padx=30, pady=30, fill="x")
        for i, (label, key) in enumerate(fields):
            f = ctk.CTkFrame(grid, fg_color="transparent"); f.grid(row=0, column=i, padx=20)
            ctk.CTkLabel(f, text=label, font=("Segoe UI Variable", 13), text_color="gray").pack()
            e = ctk.CTkEntry(f, width=140, height=45, corner_radius=12, border_width=0, fg_color="#F5F5F7", font=("Segoe UI Variable", 16, "bold"), justify="center")
            if key == "age" and auto_age: e.insert(0, str(auto_age))
            e.pack(pady=5); self.inputs[key] = e

    def save_and_redirect(self):
        from api_service import APIService
        data = {k: v.get() for k, v in self.inputs.items()}
        data['notes'] = self.notes.get("0.0", "end")
        APIService.save_exam(self.p_id, data)
        # ПЕРЕХОД К QR ЭКРАНУ
        self.on_save(self.p_id, self.p_name, self.code)
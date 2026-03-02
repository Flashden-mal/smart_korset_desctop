import customtkinter as ctk

class MedicalReportView(ctk.CTkFrame):
    def __init__(self, master, patient, ex, on_back):
        super().__init__(master, fg_color="#F5F5F7")
        
        ctk.CTkButton(self, text="← Назад в карту", command=on_back, corner_radius=15, 
                      fg_color="#1D1D1F", text_color="white", width=160, height=40, font=("Segoe UI Variable", 13, "bold")).place(x=50, y=40)

        self.doc = ctk.CTkFrame(self, width=850, height=1050, corner_radius=0, fg_color="white", border_width=1, border_color="#E5E5E7")
        self.doc.place(relx=0.5, rely=0.52, anchor="center")
        self.doc.pack_propagate(False)

        header = ctk.CTkFrame(self.doc, fg_color="transparent")
        header.pack(fill="x", padx=80, pady=(80, 40))
        ctk.CTkLabel(header, text="МЕДИЦИНСКОЕ ЗАКЛЮЧЕНИЕ", font=("Segoe UI Variable", 12, "bold"), text_color="#86868B").pack(anchor="w")
        ctk.CTkLabel(header, text="Smart Korset System", font=("Segoe UI Variable Display", 42, "bold"), text_color="#1D1D1F").pack(anchor="w")

        info_grid = ctk.CTkFrame(self.doc, fg_color="transparent")
        info_grid.pack(fill="x", padx=80, pady=20)
        
        self.add_info(info_grid, "Пациент", patient['username'])
        self.add_info(info_grid, "Дата осмотра", ex['date'])
        self.add_info(info_grid, "Диагноз", ex.get('diagnosis', 'Плановый'))

        metrics_frame = ctk.CTkFrame(self.doc, fg_color="#FBFBFD", corner_radius=30, border_width=1, border_color="#E5E5E7")
        metrics_frame.pack(fill="x", padx=80, pady=40)
        
        # МАППИНГ ДАННЫХ ИЗ ОБЪЕКТА EX
        m_list = [
            ("Рост", f"{ex.get('h', '-')} см"),
            ("Вес", f"{ex.get('w', '-')} кг"),
            ("Угол Кобба", f"{ex.get('cobb', '-')}°"),
            ("Тест Адамса", f"{ex.get('atr', '-')}°")
        ]

        for i, (m, v) in enumerate(m_list):
            box = ctk.CTkFrame(metrics_frame, fg_color="transparent")
            box.grid(row=i//2, column=i%2, padx=60, pady=35)
            ctk.CTkLabel(box, text=m, font=("Segoe UI Variable", 14), text_color="#86868B").pack()
            ctk.CTkLabel(box, text=v, font=("Segoe UI Variable Display", 36, "bold"), text_color="#007AFF").pack()

        ctk.CTkLabel(self.doc, text="ПОДРОБНЫЕ ЗАМЕТКИ ВРАЧА", font=("Segoe UI Variable", 11, "bold"), text_color="gray").pack(anchor="w", padx=80)
        notes_box = ctk.CTkFrame(self.doc, fg_color="#F5F5F7", corner_radius=20)
        notes_box.pack(fill="both", expand=True, padx=80, pady=(10, 100))
        
        ctk.CTkLabel(notes_box, text=ex.get('notes', 'Дополнительных записей нет.'), 
                     font=("Segoe UI Variable", 16), wraplength=650, justify="left", padx=30, pady=30, text_color="#1D1D1F").pack(anchor="nw")

        ctk.CTkLabel(self.doc, text="Электронная подпись подтверждена системой Smart Korset AI", font=("Segoe UI Variable", 11), text_color="gray").pack(side="bottom", pady=40)

    def add_info(self, master, label, val):
        f = ctk.CTkFrame(master, fg_color="transparent"); f.pack(side="left", padx=(0, 50))
        ctk.CTkLabel(f, text=label, font=("Segoe UI Variable", 13), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(f, text=val, font=("Segoe UI Variable", 18, "bold"), text_color="#1D1D1F").pack(anchor="w")
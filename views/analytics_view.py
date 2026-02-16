import customtkinter as ctk

class PatientAnalyticsView(ctk.CTkFrame):
    def __init__(self, master, patient_name, on_back):
        super().__init__(master, fg_color="transparent")

        # HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkButton(header, text="← Назад", width=100, height=35, corner_radius=15,
                      fg_color="#F2F2F7", text_color="#1D1D1F", hover_color="#E5E5E7",
                      font=("Segoe UI Variable", 13, "bold"), command=on_back).pack(side="left")
        
        ctk.CTkLabel(header, text=f"Анализ пациента: {patient_name}", 
                     font=("Segoe UI Variable Display", 28, "bold"), text_color="#1D1D1F").pack(side="left", padx=30)

        # SCROLL AREA
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0)
        self.scroll.pack(fill="both", expand=True, padx=40)

        # --- AI INSIGHTS CARD (APPLE INTELLIGENCE STYLE) ---
        ai_card = ctk.CTkFrame(self.scroll, corner_radius=35, fg_color="#F5F5F7", border_width=2, border_color="#007AFF")
        ai_card.pack(fill="x", pady=10)
        
        ctk.CTkLabel(ai_card, text="✨ Резюме медицинского ИИ", font=("Segoe UI Variable Display", 20, "bold"), 
                     text_color="#007AFF").pack(anchor="w", padx=30, pady=(25, 10))
        
        insight_text = (
            "У пациента наблюдается стабильный завал корпуса влево (средний угол 16°). "
            "Критический наклон вперед зафиксирован 3 раза за последние 24 часа. "
            "Рекомендовано: Назначить курс укрепления мышц спины (уровень 2) и снизить порог вибрации до 15°."
        )
        ctk.CTkLabel(ai_card, text=insight_text, font=("Segoe UI Variable", 16), text_color="#1D1D1F",
                     wraplength=800, justify="left").pack(anchor="w", padx=30, pady=(0, 30))

        # --- STATS ROW ---
        stats_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)

        # Средний угол
        self.create_stat_card(stats_frame, "Средний угол", "22°", "Норма до 15°", "#FF9500")
        # Тренировки
        self.create_stat_card(stats_frame, "Тренировки", "85%", "12/15 выполнено", "#34C759")
        # Падения/Риски
        self.create_stat_card(stats_frame, "Риск сколиоза", "Высокий", "Степень 1", "#FF3B30")

        # --- PLACEHOLDER FOR CHART ---
        chart_mock = ctk.CTkFrame(self.scroll, height=300, corner_radius=30, fg_color="#FFFFFF", border_width=1, border_color="#EBEBEB")
        chart_mock.pack(fill="x", pady=20)
        ctk.CTkLabel(chart_mock, text="[ Здесь будет график телеметрии Matplotlib ]", 
                     font=("Segoe UI Variable", 16), text_color="#86868B").place(relx=0.5, rely=0.5, anchor="center")

    def create_stat_card(self, master, title, value, sub, color):
        card = ctk.CTkFrame(master, width=280, height=150, corner_radius=30, fg_color="#FFFFFF", border_width=1, border_color="#EBEBEB")
        card.pack(side="left", padx=10, expand=True, fill="both")
        card.pack_propagate(False)
        
        ctk.CTkLabel(card, text=title, font=("Segoe UI Variable", 14, "bold"), text_color="#86868B").pack(pady=(25, 0))
        ctk.CTkLabel(card, text=value, font=("Segoe UI Variable Display", 36, "bold"), text_color=color).pack()
        ctk.CTkLabel(card, text=sub, font=("Segoe UI Variable", 12), text_color="#86868B").pack()
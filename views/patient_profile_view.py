import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from api_service import APIService

class PatientProfileView(ctk.CTkFrame):
    def __init__(self, master, patient, on_back):
        super().__init__(master, fg_color="#FFFFFF")
        self.patient = patient
        self.on_back_to_list = on_back
        self.current_period = "День"

        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=60, pady=(40, 20))
        ctk.CTkButton(nav, text="← Список пациентов", command=self.on_back_to_list, width=150, height=42, corner_radius=15, fg_color="#F2F2F7", text_color="#007AFF", font=("Segoe UI Variable", 13, "bold")).pack(side="left")
        ctk.CTkButton(nav, text="+ ПРОВЕСТИ ОСМОТР", command=self.open_new_exam, width=200, height=45, corner_radius=22, fg_color="#34C759", hover_color="#28A745", font=("Segoe UI Variable", 14, "bold")).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0)
        self.scroll.pack(fill="both", expand=True, padx=60)

        # Полное имя
        ctk.CTkLabel(self.scroll, text=patient['username'], font=("Segoe UI Variable Display", 48, "bold"), text_color="#1D1D1F").pack(anchor="w")
        
        # Периоды
        self.p_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.p_frame.pack(fill="x", pady=25)
        self.p_btns = {}
        for p in ["Час", "День", "Неделя", "Месяц"]:
            btn = ctk.CTkButton(self.p_frame, text=p, width=110, height=38, corner_radius=12,
                                fg_color="#F2F2F7" if p != self.current_period else "#007AFF",
                                text_color="#1D1D1F" if p != self.current_period else "#FFFFFF",
                                font=("Segoe UI Variable", 14, "bold"),
                                command=lambda x=p: self.change_period(x))
            btn.pack(side="left", padx=6)
            self.p_btns[p] = btn

        self.chart_container = ctk.CTkFrame(self.scroll, corner_radius=40, fg_color="#FBFBFD", border_width=1, border_color="#E5E5E7")
        self.chart_container.pack(fill="x", pady=10)
        
        self.ai_card = ctk.CTkFrame(self.scroll, corner_radius=30, fg_color="#F0F7FF", border_width=1, border_color="#007AFF")
        self.ai_card.pack(fill="x", pady=35)
        ctk.CTkLabel(self.ai_card, text="✨ AI CLINICAL INSIGHT", font=("Segoe UI Variable", 11, "bold"), text_color="#007AFF").pack(anchor="w", padx=35, pady=(25,5))
        self.ai_label = ctk.CTkLabel(self.ai_card, text="Загрузка...", font=("Segoe UI Variable", 17), text_color="#1D1D1F", wraplength=1000, justify="left")
        self.ai_label.pack(padx=35, pady=(0,30), anchor="w")

        ctk.CTkLabel(self.scroll, text="История осмотров", font=("Segoe UI Variable Display", 28, "bold"), text_color="#1D1D1F").pack(anchor="w", pady=25)
        self.history_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.history_f.pack(fill="x")

        self.refresh_view()

    def change_period(self, period):
        self.current_period = period
        self.refresh_view()

    def refresh_view(self):
        for w in self.chart_container.winfo_children(): w.destroy()
        for w in self.history_f.winfo_children(): w.destroy()
        for p, btn in self.p_btns.items():
            btn.configure(fg_color="#F2F2F7" if p != self.current_period else "#007AFF", text_color="#1D1D1F" if p != self.current_period else "#FFFFFF")

        data = APIService.get_patient_analytics(self.patient['user_id'], self.current_period)
        self.draw_chart(data)
        self.ai_label.configure(text=data.get("ai", "Нет данных"))

        exams = APIService.get_patient_exams(self.patient['user_id'])
        if not exams:
            ctk.CTkLabel(self.history_f, text="Записей не найдено", font=("Segoe UI", 16), text_color="gray").pack(pady=30)
        else:
            for ex in exams:
                self.add_history_row(ex)

    def draw_chart(self, d):
        plt.close('all')
        fig, ax = plt.subplots(figsize=(12, 4.5), dpi=100)
        fig.patch.set_facecolor('#FBFBFD'); ax.set_facecolor('#FBFBFD')
        
        # Если данных мало, matplotlib может рисовать криво, добавим проверку
        if d.get("x") and d.get("y"):
            ax.plot(d["x"], d["y"], color='#007AFF', marker='o', linewidth=4, markersize=8, markerfacecolor='white', markeredgewidth=3)
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        
        FigureCanvasTkAgg(fig, master=self.chart_container).get_tk_widget().pack(fill="both", expand=True, padx=35, pady=35)

    def add_history_row(self, ex):
        card = ctk.CTkFrame(self.history_f, corner_radius=25, fg_color="#FBFBFD", border_width=1, border_color="#E5E5E7")
        card.pack(fill="x", pady=8)
        row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(fill="x", padx=30, pady=25)
        ctk.CTkLabel(row, text=f"📅 {ex['date']}", font=("Segoe UI Variable", 17, "bold")).pack(side="left")
        ctk.CTkLabel(row, text=ex.get('diagnosis', 'Осмотр'), font=("Segoe UI Variable", 17), text_color="#424245").pack(side="left", padx=40)
        ctk.CTkButton(row, text="Открыть справку", width=140, height=35, corner_radius=10, fg_color="#F2F2F7", text_color="#007AFF", 
                      command=lambda: self.open_report(ex)).pack(side="right")

    def open_report(self, ex):
        for w in self.master.master.content.winfo_children(): w.destroy()
        from views.medical_report_view import MedicalReportView
        # ВАЖНО: on_back теперь вызывает open_profile, что гарантирует возврат в карту
        MedicalReportView(self.master.master.content, self.patient, ex, 
                          on_back=lambda: self.master.master.open_profile(self.patient)).pack(fill="both", expand=True)

    def open_new_exam(self):
        for w in self.master.master.content.winfo_children(): w.destroy()
        from views.followup_exam_view import FollowupExamView
        FollowupExamView(self.master.master.content, self.patient, 
                         on_save=lambda: self.master.master.open_profile(self.patient)).pack(fill="both", expand=True)
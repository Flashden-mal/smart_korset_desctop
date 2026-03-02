import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from api_service import APIService
import tkinter.messagebox as messagebox

class PatientProfileView(ctk.CTkFrame):
    def __init__(self, master, patient, on_back):
        super().__init__(master, fg_color="#FFFFFF")
        self.patient, self.on_back_to_list = patient, on_back
        self.current_period = "День"

        # --- HEADER ---
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=60, pady=(40, 20))
        
        ctk.CTkButton(nav, text="← Список пациентов", command=on_back, 
                      width=150, height=42, corner_radius=15, 
                      fg_color="#F2F2F7", text_color="#007AFF", 
                      font=("Segoe UI Variable", 13, "bold")).pack(side="left")
        
        ctk.CTkButton(nav, text="+ ПРОВЕСТИ ОСМОТР", command=self.open_new_exam, 
                      width=200, height=45, corner_radius=22, 
                      fg_color="#34C759", font=("Segoe UI Variable", 14, "bold")).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0)
        self.scroll.pack(fill="both", expand=True, padx=60)

        # ЗАГОЛОВОК
        ctk.CTkLabel(self.scroll, text=patient['username'], 
                     font=("Segoe UI Variable Display", 52, "bold"), 
                     text_color="#1D1D1F").pack(anchor="w", pady=(0, 20))
        
        # КНОПКИ ПЕРИОДА
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

        # КОНТЕЙНЕР ГРАФИКА
        self.chart_container = ctk.CTkFrame(self.scroll, corner_radius=40, fg_color="#FBFBFD", 
                                            border_width=1, border_color="#E5E5E7")
        self.chart_container.pack(fill="x", pady=10)
        
        # КАРТОЧКА ИИ (AI INSIGHTS)
        self.ai_card = ctk.CTkFrame(self.scroll, corner_radius=30, fg_color="#F0F7FF", 
                                    border_width=1, border_color="#007AFF")
        self.ai_card.pack(fill="x", pady=35)
        
        ctk.CTkLabel(self.ai_card, text="✨ AI CLINICAL INSIGHT", 
                     font=("Segoe UI Variable", 11, "bold"), 
                     text_color="#007AFF").pack(anchor="w", padx=35, pady=(25,5))
        
        self.ai_label = ctk.CTkLabel(self.ai_card, text="Аналитика подготавливается...", 
                                     font=("Segoe UI Variable", 16), text_color="#1D1D1F", 
                                     wraplength=1050, justify="left")
        self.ai_label.pack(padx=35, pady=(0,30), anchor="w")

        # ИСТОРИЯ ОСМОТРОВ
        ctk.CTkLabel(self.scroll, text="История осмотров", 
                     font=("Segoe UI Variable Display", 32, "bold"), 
                     text_color="#1D1D1F").pack(anchor="w", pady=25)
        
        self.history_f = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.history_f.pack(fill="x")

        self.refresh_view()

    def change_period(self, p):
        self.current_period = p; self.refresh_view()

    def refresh_view(self):
        """Очистка и полная перерисовка данных из БД"""
        for w in self.chart_container.winfo_children(): w.destroy()
        for w in self.history_f.winfo_children(): w.destroy()
        
        for p, b in self.p_btns.items():
            b.configure(fg_color="#007AFF" if p == self.current_period else "#F2F2F7", 
                        text_color="white" if p == self.current_period else "#1D1D1F")

        data = APIService.get_patient_analytics(self.patient['user_id'], self.current_period)
        self.draw_chart(data)
        self.ai_label.configure(text=data.get("ai", "Нет данных"))

        exams = APIService.get_patient_exams(self.patient['user_id'])
        if not exams:
            ctk.CTkLabel(self.history_f, text="Записей об осмотрах нет", font=("Segoe UI Variable", 16), text_color="gray").pack(pady=40)
        else:
            for ex in exams: self.add_history_row(ex)

    def draw_chart(self, d):
        """Отрисовка динамического графика Matplotlib"""
        plt.close('all')
        fig, ax = plt.subplots(figsize=(12, 5), dpi=100); fig.patch.set_facecolor('#FBFBFD'); ax.set_facecolor('#FBFBFD')
        
        if d.get("x") and d.get("y"):
            ax.plot(d["x"], d["y"], color='#007AFF', marker=None, linewidth=3)
            ax.fill_between(d["x"], d["y"], color='#007AFF', alpha=0.1)
            step = max(1, len(d["x"]) // 10)
            ax.set_xticks(range(0, len(d["x"]), step))
            ax.set_xticklabels([d["x"][i] for i in range(0, len(d["x"]), step)], fontsize=8)
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        else:
            ax.text(0.5, 0.5, "НЕТ ДАННЫХ ДЛЯ ОТОБРАЖЕНИЯ", transform=ax.transAxes, ha='center', color='gray')
            
        FigureCanvasTkAgg(fig, master=self.chart_container).get_tk_widget().pack(fill="both", expand=True, padx=35, pady=35)

    def add_history_row(self, ex):
        card = ctk.CTkFrame(self.history_f, corner_radius=25, fg_color="#FBFBFD", border_width=1, border_color="#E5E5E7")
        card.pack(fill="x", pady=8); row = ctk.CTkFrame(card, fg_color="transparent"); row.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(row, text=f"📅 {ex['date']}", font=("Segoe UI Variable", 17, "bold")).pack(side="left")
        ctk.CTkLabel(row, text=ex.get('diagnosis', 'Осмотр'), font=("Segoe UI Variable", 17), text_color="#424245").pack(side="left", padx=40)
        
        # Кнопка удаления (Центральное окно)
        ctk.CTkButton(row, text="Удалить", width=100, height=35, corner_radius=10, 
                      fg_color="#FF3B30", hover_color="#D32F2F", font=("Segoe UI Variable", 13, "bold"),
                      command=lambda eid=ex.get('exam_id'): self.show_luxury_confirm(eid)).pack(side="right", padx=(10, 0))

        ctk.CTkButton(row, text="Открыть справку", width=140, height=35, corner_radius=10, 
                      fg_color="#F2F2F7", text_color="#007AFF", font=("Segoe UI Variable", 13, "bold"),
                      command=lambda: self.open_report(ex)).pack(side="right")

    def show_luxury_confirm(self, eid):
        """МОДАЛЬНОЕ ОКНО ПОДТВЕРЖДЕНИЯ С БЕЛЫМ ОВЕРЛЕЕМ"""
        root = self.winfo_toplevel()
        overlay = ctk.CTkFrame(root, fg_color="white", corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        dialog = ctk.CTkToplevel(self)
        dialog.overrideredirect(True); dialog.attributes("-topmost", True)
        dialog.configure(fg_color="white")
        
        d_w, d_h = 480, 320
        root.update_idletasks()
        pos_x = root.winfo_x() + (root.winfo_width() // 2) - (d_w // 2)
        pos_y = root.winfo_y() + (root.winfo_height() // 2) - (d_h // 2)
        dialog.geometry(f"{d_w}x{d_h}+{pos_x}+{pos_y}")

        inner = ctk.CTkFrame(dialog, fg_color="white", corner_radius=40, border_width=2, border_color="#F2F2F7")
        inner.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(inner, text="⚠️", font=("Arial", 60)).pack(pady=(40, 5))
        ctk.CTkLabel(inner, text="Подтверждение", font=("Segoe UI Variable Display", 26, "bold")).pack()
        ctk.CTkLabel(inner, text="Вы точно желаете удалить эту запись?\nДанные исчезнут безвозвратно.", font=("Segoe UI Variable", 16), text_color="gray").pack(pady=10)

        btns = ctk.CTkFrame(inner, fg_color="transparent"); btns.pack(pady=35)
        def close(del_it=False):
            overlay.destroy(); dialog.destroy()
            if del_it: self.refresh_view()

        ctk.CTkButton(btns, text="Удалить", width=170, height=50, corner_radius=20, fg_color="#FF3B30", command=lambda: close(APIService.delete_exam(eid))).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Отмена", width=170, height=50, corner_radius=20, fg_color="#F2F2F7", text_color="black", command=lambda: close(False)).pack(side="left", padx=10)

    def open_report(self, ex):
        for w in self.master.master.content.winfo_children(): w.destroy()
        from views.medical_report_view import MedicalReportView
        MedicalReportView(self.master.master.content, self.patient, ex, on_back=lambda: self.master.master.open_profile(self.patient)).pack(fill="both", expand=True)

    def open_new_exam(self):
        for w in self.master.master.content.winfo_children(): w.destroy()
        from views.followup_exam_view import FollowupExamView
        FollowupExamView(self.master.master.content, self.patient, on_save=lambda: self.master.master.open_profile(self.patient)).pack(fill="both", expand=True)
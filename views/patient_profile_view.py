import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PatientProfileView(ctk.CTkFrame):
    def __init__(self, master, patient, on_back):
        super().__init__(master, fg_color="transparent")
        from api_service import APIService
        d = APIService.get_patient_history(patient['user_id'])

        nav = ctk.CTkFrame(self, fg_color="transparent"); nav.pack(fill="x", padx=40, pady=20)
        ctk.CTkButton(nav, text="← Назад", command=on_back, corner_radius=15, fg_color="#F0F0F2", text_color="black").pack(side="left")

        s = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0); s.pack(fill="both", expand=True, padx=40)
        ctk.CTkLabel(s, text=patient['username'], font=("Segoe UI Variable Display", 46, "bold")).pack(anchor="w")
        
        c_f = ctk.CTkFrame(s, corner_radius=40, fg_color="white", border_width=1, border_color="#E5E5E7"); c_f.pack(fill="x", pady=20)
        self.draw(c_f, d)

        ai = ctk.CTkFrame(s, corner_radius=30, fg_color="#F0F7FF", border_width=1, border_color="#007AFF"); ai.pack(fill="x", pady=20)
        ctk.CTkLabel(ai, text="✨ AI CLINICAL INSIGHT", font=("Segoe UIVariable", 13, "bold"), text_color="#007AFF").pack(anchor="w", padx=30, pady=(20,5))
        ctk.CTkLabel(ai, text=d.get('ai_report', 'Анализ проводится...'), font=("Segoe UIVariable", 16), wraplength=1000, justify="left").pack(padx=30, pady=(0,20))

        ctk.CTkLabel(s, text="История осмотров", font=("Segoe UI Variable", 24, "bold")).pack(anchor="w", pady=(20, 10))
        for exam in d.get('exams', []):
            card = ctk.CTkFrame(s, corner_radius=20, fg_color="white", border_width=1, border_color="#E5E5E7")
            card.pack(fill="x", pady=5)
            ctk.CTkLabel(card, text=f"{exam['date']} — {exam.get('diagnosis','')} (Угол: {exam.get('cobb','-')}°)", font=("Segoe UI", 16), padx=20, pady=20).pack(side="left")

    def draw(self, master, d):
        plt.close('all')
        fig, ax = plt.subplots(figsize=(15, 5), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        ax.plot(d.get('dates', []), d.get('telemetry', []), color='#007AFF', marker='o', linewidth=4)
        ax.axis('off')
        FigureCanvasTkAgg(fig, master=master).get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
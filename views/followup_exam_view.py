import customtkinter as ctk
from api_service import APIService
from datetime import date

class FollowupExamView(ctk.CTkFrame):
    def __init__(self, master, patient, on_save):
        super().__init__(master, fg_color="#FFFFFF")
        self.patient, self.on_save = patient, on_save

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", border_width=0)
        scroll.pack(fill="both", expand=True, padx=80, pady=40)

        ctk.CTkLabel(scroll, text="Новый протокол осмотра", font=("Segoe UI Variable Display", 40, "bold")).pack(anchor="w")
        ctk.CTkLabel(scroll, text=f"Пациент: {patient['username']}", font=("Segoe UI Variable", 18), text_color="gray").pack(anchor="w", pady=(0, 40))

        self.fields = {}
        # Расширенные секции
        self.add_section(scroll, "Антропометрия", [("Рост (см)", "h"), ("Вес (кг)", "w"), ("Обхват груди", "chest"), ("ИМТ", "bmi")])
        self.add_section(scroll, "Рентгенография", [("Кобб (грудной)°", "cobb_th"), ("Кобб (поясн.)°", "cobb_l"), ("Угол Кифоза°", "kyph"), ("Nash-Moe (ст.)", "nash")])
        self.add_section(scroll, "Функциональные тесты", [("Тест Адамса°", "atr"), ("Шкала боли (0-10)", "pain"), ("Жизн. емкость легких", "lung")])

        ctk.CTkLabel(scroll, text="Развернутое клиническое заключение", font=("Segoe UI Variable", 16, "bold")).pack(anchor="w", pady=(30, 5))
        self.notes = ctk.CTkTextbox(scroll, height=180, corner_radius=25, border_width=1, border_color="#E5E5E7", font=("Segoe UI Variable", 15))
        self.notes.pack(fill="x", pady=10)

        ctk.CTkButton(scroll, text="СОХРАНИТЬ В БАЗУ ДАННЫХ", height=80, corner_radius=40, 
                      fg_color="#007AFF", font=("Segoe UI Variable", 18, "bold"), command=self.save).pack(fill="x", pady=40)
        
        ctk.CTkButton(scroll, text="Отмена", fg_color="transparent", text_color="gray", font=("Segoe UI Variable", 14), command=on_save).pack()

    def add_section(self, master, title, items):
        ctk.CTkLabel(master, text=title, font=("Segoe UI Variable", 17, "bold")).pack(anchor="w", pady=(25, 10))
        f = ctk.CTkFrame(master, fg_color="#FBFBFD", corner_radius=25, border_width=1, border_color="#E5E5E7")
        f.pack(fill="x", pady=5)
        for name, key in items:
            box = ctk.CTkFrame(f, fg_color="transparent"); box.pack(side="left", padx=25, pady=25, expand=True)
            ctk.CTkLabel(box, text=name, font=("Segoe UI Variable", 12), text_color="gray").pack()
            e = ctk.CTkEntry(box, width=130, height=45, corner_radius=10, border_width=0, fg_color="#F2F2F7", justify="center", font=("Segoe UI Variable", 16, "bold"))
            e.pack(pady=5); self.fields[key] = e

    def save(self):
        # Собираем данные и отправляем в API
        data = {k: v.get() for k, v in self.fields.items()}
        data['notes'] = self.notes.get("0.0", "end")
        data['date'] = date.today().strftime("%d.%m.%Y")
        APIService.save_new_exam(self.patient['user_id'], data)
        # Возврат в карту пациента
        self.on_save()
import customtkinter as ctk
import os
from PIL import Image
from datetime import date
import threading
from tkinter import messagebox
from api_service import APIService
from views.patient_profile_view import PatientProfileView
from views.initial_exam_view import InitialExamView
from views.registration_view import PatientRegistrationView
from views.pairing_view import PairingView

class DoctorView(ctk.CTkFrame):
    def __init__(self, master, uid, name, on_logout, rid):
        # Основной контейнер чисто белый
        super().__init__(master, fg_color="#FFFFFF")
        self.uid = uid
        self.name = name
        self.all_patients = []
        
        # Загружаем профиль врача из API
        self.doc_info = APIService.get_doctor_profile(self.uid)
        
        # Загрузка иконки поиска
        asset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "assets")
        try:
            self.search_icon = ctk.CTkImage(
                light_image=Image.open(os.path.join(asset_path, "search.png")), 
                size=(20, 20)
            )
        except:
            self.search_icon = None

        # --- SIDEBAR (Apple Grey Style) ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#FBFBFD", border_width=0)
        self.sidebar.pack(side="left", fill="y")
        
        # 1. Логотип и заголовок
        header_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_section.pack(pady=(50, 10), padx=30, fill="x")

        ctk.CTkLabel(header_section, text="🏥", font=("Arial", 45)).pack()
        ctk.CTkLabel(header_section, text="Smart Korset", 
                     font=("Segoe UI Variable Display", 22, "bold"), 
                     text_color="#1D1D1F").pack(pady=(5, 0))

        # 2. Бейдж роли
        self.role_badge = ctk.CTkLabel(
            self.sidebar, 
            text="ПАНЕЛЬ ВРАЧА", 
            font=("Segoe UI Variable", 9, "bold"), 
            text_color="#FFFFFF",
            fg_color="#007AFF", 
            corner_radius=10,
            height=24,
            width=120
        )
        self.role_badge.pack(pady=(10, 20))

        # 3. Блок профиля врача в сайдбаре
        profile_section = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        profile_section.pack(pady=(0, 25), padx=20, fill="x")

        ctk.CTkLabel(profile_section, text=self.doc_info.get('speciality', 'ВРАЧ').upper(), 
                     font=("Segoe UI Variable", 10, "bold"), 
                     text_color="#86868B",
                     wraplength=240,
                     justify="center").pack(pady=(0, 2))
        
        ctk.CTkLabel(profile_section, text=self.name, 
                     font=("Segoe UI Variable Display", 18, "bold"), 
                     text_color="#007AFF").pack(pady=(2, 0))

        # --- НАВИГАЦИЯ ---
        self.nav_btns = {}
        nav_style = {
            "font": ("Segoe UI Variable", 15, "bold"),
            "height": 50,
            "fg_color": "transparent",
            "text_color": "#1D1D1F",
            "anchor": "w",
            "hover_color": "#E8E8ED",
            "corner_radius": 12,
            "border_width": 0
        }

        btn_p = ctk.CTkButton(self.sidebar, text="  👥  Пациенты", command=lambda: self.show("p"), **nav_style)
        btn_p.pack(fill="x", padx=20, pady=2)
        self.nav_btns["p"] = btn_p

        btn_a = ctk.CTkButton(self.sidebar, text="  📊  Аналитика", command=lambda: self.show("a"), **nav_style)
        btn_a.pack(fill="x", padx=20, pady=2)
        self.nav_btns["a"] = btn_a

        self.logout_btn = ctk.CTkButton(self.sidebar, text="Выйти из системы", 
                                        text_color="#FF3B30", 
                                        fg_color="transparent",
                                        font=("Segoe UI Variable", 13, "bold"), 
                                        hover_color="#FFF0F0", 
                                        corner_radius=10,
                                        command=on_logout)
        self.logout_btn.pack(side="bottom", pady=40, padx=30, fill="x")

        # --- КОНТЕНТНАЯ ОБЛАСТЬ (ПРАВАЯ ЧАСТЬ) ---
        self.content = ctk.CTkFrame(self, fg_color="#FFFFFF")
        self.content.pack(side="right", fill="both", expand=True)

        # По умолчанию открываем список пациентов
        self.show("p")

    def show(self, vid):
        """Интеллектуальный роутер контента"""
        for child in self.content.winfo_children():
            child.destroy()
        
        for k, b in self.nav_btns.items():
            if k == vid:
                b.configure(fg_color="#E8E8ED", text_color="#007AFF")
            else:
                b.configure(fg_color="transparent", text_color="#1D1D1F")

        if vid == "p":
            self.render_patients()
        else:
            # Заглушка для аналитики
            msg_f = ctk.CTkFrame(self.content, fg_color="transparent")
            msg_f.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(msg_f, text="📊", font=("Arial", 80)).pack()
            ctk.CTkLabel(msg_f, text="Общая аналитика", font=("Segoe UI Variable Display", 32, "bold")).pack()
            ctk.CTkLabel(msg_f, text="Раздел находится в разработке", font=("Segoe UI Variable", 16), text_color="gray").pack(pady=10)

    def render_patients(self):
        """Отрисовка главного экрана со списком пациентов"""
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x", padx=60, pady=(60, 20))
        
        ctk.CTkLabel(header, text="Мои пациенты", font=("Segoe UI Variable Display", 48, "bold"), text_color="#1D1D1F").pack(side="left")
        
        ctk.CTkButton(header, text="+ Регистрация", width=180, height=50, corner_radius=25, 
                      fg_color="#34C759", hover_color="#28A745", font=("Segoe UI Variable", 14, "bold"), 
                      command=self.open_reg).pack(side="right")

        # Поле поиска
        search_f = ctk.CTkFrame(self.content, fg_color="#F2F2F7", corner_radius=27, height=55)
        search_f.pack(fill="x", padx=60, pady=(10, 30))
        search_f.pack_propagate(False)

        if self.search_icon:
            ctk.CTkLabel(search_f, text="", image=self.search_icon).pack(side="left", padx=(25, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_list)
        ctk.CTkEntry(search_f, placeholder_text="Поиск пациента по ФИО...", textvariable=self.search_var, 
                     border_width=0, fg_color="transparent", font=("Segoe UI Variable", 16), 
                     text_color="#1D1D1F").pack(side="left", fill="both", expand=True, padx=(0, 25))

        # Область прокрутки для карточек
        self.scroll = ctk.CTkScrollableFrame(self.content, fg_color="transparent", border_width=0)
        self.scroll.pack(fill="both", expand=True, padx=60)

        # Загрузка данных
        data = APIService.get_patients(self.uid)
        self.all_patients = sorted(data, key=lambda x: x.get('username', ''))
        self.update_list(self.all_patients)

    def filter_list(self, *args):
        """Фильтрация списка при вводе в поиск"""
        q = self.search_var.get().lower().strip()
        filtered = [p for p in self.all_patients if q in p.get('username', '').lower()]
        self.update_list(filtered)

    def update_list(self, p_list):
        """Генерация карточек пациентов в скролле"""
        for child in self.scroll.winfo_children():
            child.destroy()

        if not p_list:
            ctk.CTkLabel(self.scroll, text="Список пациентов пуст", font=("Segoe UI Variable", 18), text_color="gray").pack(pady=100)
            return

        for p in p_list:
            card = ctk.CTkFrame(self.scroll, height=110, corner_radius=30, fg_color="#FFFFFF", 
                                border_width=1, border_color="#E0E0E2")
            card.pack(fill="x", pady=8)
            card.pack_propagate(False)
            
            # Аватар
            avatar_f = ctk.CTkFrame(card, width=60, height=60, corner_radius=30, fg_color="#F2F2F7")
            avatar_f.pack(side="left", padx=25)
            avatar_f.pack_propagate(False)
            ctk.CTkLabel(avatar_f, text="👤", font=("Arial", 30)).pack(expand=True)
            
            # Инфо
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", pady=20)
            ctk.CTkLabel(info, text=p.get('username', 'Неизвестно'), 
                         font=("Segoe UI Variable Display", 20, "bold"), text_color="#1D1D1F").pack(anchor="w")
            
            st_text = p.get('status', 'В лечении')
            st_color = p.get('status_color', '#34C759')
            ctk.CTkLabel(info, text=f"● {st_text}", font=("Segoe UI Variable", 14, "bold"), text_color=st_color).pack(anchor="w")

            # Кнопка открытия профиля
            ctk.CTkButton(card, text="Карта пациента", width=160, height=44, corner_radius=22, 
                          fg_color="#F2F2F7", text_color="#007AFF", 
                          font=("Segoe UI Variable", 13, "bold"), hover_color="#E8E8ED",
                          command=lambda x=p: self.open_profile(x)).pack(side="right", padx=30)

    def open_reg(self):
        """Открытие экрана регистрации"""
        for child in self.content.winfo_children():
            child.destroy()
        PatientRegistrationView(self.content, self.start_exam, lambda: self.show("p")).pack(fill="both", expand=True)

    def start_exam(self, name, dob):
        """ФИКС: Регистрация с индикатором загрузки в отдельном потоке"""
        # Показываем статус загрузки
        for child in self.content.winfo_children():
            child.destroy()
        
        loading_f = ctk.CTkFrame(self.content, fg_color="transparent")
        loading_f.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(loading_f, text="Создание профиля...", font=("Segoe UI Variable Display", 28, "bold")).pack()
        ctk.CTkLabel(loading_f, text="Пожалуйста, подождите, идет связь с сервером", font=("Segoe UI Variable", 16), text_color="gray").pack(pady=10)

        def run_api_call():
            # Вызов API
            res = APIService.register_new_patient(self.uid, name)
            
            if res and 'patient_id' in res:
                # Рассчитываем возраст
                today = date.today()
                try:
                    birth_year = int(dob.get('year', today.year))
                    age = today.year - birth_year
                except:
                    age = ""
                
                # Возвращаемся в главный поток для смены экрана
                self.after(0, lambda: self.go_to_initial_exam(res, name, age))
            else:
                # Ошибка
                self.after(0, lambda: [
                    messagebox.showerror("Ошибка", "Не удалось зарегистрировать пациента. Возможно, имя уже занято."),
                    self.show("p")
                ])

        # Запуск в фоне
        threading.Thread(target=run_api_call, daemon=True).start()

    def go_to_initial_exam(self, res, name, age):
        """Переход к первичному осмотру после успешной регистрации"""
        for child in self.content.winfo_children():
            child.destroy()
        InitialExamView(self.content, res['patient_id'], name, res['invite_code'], age, self.show_pairing_screen).pack(fill="both", expand=True)

    def show_pairing_screen(self, p_id, p_name, code):
        """Переход к экрану с QR-кодом"""
        for child in self.content.winfo_children():
            child.destroy()
        patient_obj = {"user_id": p_id, "username": p_name}
        PairingView(self.content, p_id, p_name, code, lambda: self.open_profile(patient_obj)).pack(fill="both", expand=True)

    def open_profile(self, p):
        """Открытие детальной аналитики пациента"""
        for child in self.content.winfo_children():
            child.destroy()
        PatientProfileView(self.content, p, lambda: self.show("p")).pack(fill="both", expand=True)
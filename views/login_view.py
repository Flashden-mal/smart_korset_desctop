import customtkinter as ctk
from PIL import Image
import os

class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color="transparent")
        self.on_login_success = on_login_success
        self.password_visible = False

        # Загрузка иконок
        asset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "assets")
        try:
            self.img_on = ctk.CTkImage(Image.open(os.path.join(asset_path, "eye.png")), size=(22,22))
            self.img_off = ctk.CTkImage(Image.open(os.path.join(asset_path, "eye_off.png")), size=(22,22))
        except: self.img_on = self.img_off = None

        # Карточка
        self.card = ctk.CTkFrame(self, width=540, height=720, corner_radius=50, fg_color="#FFFFFF", border_width=1, border_color="#E5E5E7")
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        ctk.CTkLabel(self.card, text="Smart Korset", font=("Segoe UI Variable Display", 65, "bold")).pack(pady=(100, 60))

        e_style = {"width": 420, "height": 65, "corner_radius": 30, "fg_color": "#F5F5F7", "border_width": 0, "font": ("Segoe UI Variable", 17)}
        
        # Поле Логин
        self.u_e = ctk.CTkEntry(self.card, placeholder_text="Логин", **e_style)
        self.u_e.pack(pady=12)
        # ПРИВЯЗКА ENTER
        self.u_e.bind("<Return>", lambda e: self.submit())

        # Поле Пароль
        self.p_f = ctk.CTkFrame(self.card, fg_color="#F5F5F7", width=420, height=65, corner_radius=30)
        self.p_f.pack(pady=12); self.p_f.pack_propagate(False)
        self.p_e = ctk.CTkEntry(self.p_f, placeholder_text="Пароль", show="●", width=340, height=60, border_width=0, fg_color="transparent", font=e_style["font"])
        self.p_e.pack(side="left", padx=25)
        # ПРИВЯЗКА ENTER
        self.p_e.bind("<Return>", lambda e: self.submit())

        self.e_b = ctk.CTkButton(self.p_f, image=self.img_on, text="", width=35, height=35, fg_color="transparent", hover_color="#E8E8ED", command=self.toggle)
        self.e_b.place(relx=0.91, rely=0.5, anchor="center")

        self.err = ctk.CTkLabel(self.card, text="", text_color="#FF3B30", font=("Segoe UI Variable", 13))
        self.err.pack()

        # --- ТВОЕ ИЗМЕНЕНИЕ: КНОПКИ ЕЩЕ НИЖЕ (pady=100) ---
        self.l_b = ctk.CTkButton(self.card, text="Войти", width=420, height=72, corner_radius=35, 
                                 font=("Segoe UI Variable Display", 20, "bold"), fg_color="#007AFF", 
                                 command=self.submit)
        self.l_b.pack(pady=(100, 10))

        ctk.CTkButton(self.card, text="Забыли пароль?", fg_color="transparent", text_color="#007AFF", 
                      hover_color="#F5F5F7", font=("Segoe UI Variable", 14)).pack(pady=10)

    def toggle(self):
        self.password_visible = not self.password_visible
        self.p_e.configure(show="" if self.password_visible else "●")
        if self.img_on: self.e_b.configure(image=self.img_off if self.password_visible else self.img_on)

    def submit(self):
        self.on_login_success(self.u_e.get(), self.p_e.get(), self.err, self.l_b)
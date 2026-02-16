import customtkinter as ctk
import threading
from api_service import APIService
from views.login_view import LoginView
from views.doctor_view import DoctorView

class SmartKorsetApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Korset Pro")
        
        # --- ЖЕЛЕЗОБЕТОННЫЙ ФИКС РАЗВОРОТА НА ВЕСЬ ЭКРАН ---
        # Сначала даем системе понять, что окно будет большим
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        # Через 200 мс принудительно максимизируем (это убирает баг мини-окна)
        self.after(200, lambda: self.state('zoomed'))
        
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#F5F5F7") 
        
        self.user_id = None
        self.user_name = None
        self.show_login()

    def clear_screen(self):
        for widget in self.winfo_children(): widget.destroy()

    def show_login(self):
        self.clear_screen()
        lv = LoginView(self, self.handle_login)
        lv.pack(fill="both", expand=True)

    def handle_login(self, u, p, err_label, btn):
        btn.configure(state="disabled", text="Проверка...")
        def run():
            res = APIService.login(u, p)
            if res and res.status_code == 200:
                data = res.json()
                self.user_id = data["user_id"]
                self.user_name = u
                self.after(0, lambda: self.show_dashboard(data["role_id"]))
            else:
                self.after(0, lambda: [err_label.configure(text="ОШИБКА АВТОРИЗАЦИИ"), btn.configure(state="normal", text="Войти")])
        threading.Thread(target=run, daemon=True).start()

    def show_dashboard(self, role_id):
        self.clear_screen()
        self.main_view = DoctorView(self, self.user_id, self.user_name, self.show_login, role_id)
        self.main_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = SmartKorsetApp()
    app.mainloop()
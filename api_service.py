import requests

class APIService:
    URL = "http://127.0.0.1:8000"

    @staticmethod
    def login(u, p):
        try: return requests.post(f"{APIService.URL}/login", json={"username": u, "password": p}, timeout=5)
        except: return None

    @staticmethod
    def get_doctor_profile(uid):
        try:
            res = requests.get(f"{APIService.URL}/doctor/{uid}/profile", timeout=5)
            return res.json() if res.status_code == 200 else {"username": "User", "speciality": "ВРАЧ-ОРТОПЕД"}
        except: return {"username": "User", "speciality": "ВРАЧ-ОРТОПЕД"}

    @staticmethod
    def get_patients(doc_id):
        try:
            res = requests.get(f"{APIService.URL}/doctor/{doc_id}/patients", timeout=5)
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def get_patient_analytics(p_id, period="День"):
        try:
            res = requests.get(f"{APIService.URL}/patient/{p_id}/analytics", params={"period": period}, timeout=5)
            if res.status_code == 200: return res.json()
            # Мок данные с РАЗНЫМ временем для нормального графика
            return {
                "x": ["08:00", "10:00", "12:00", "14:00", "16:00"], 
                "y": [10, 25, 15, 30, 12], 
                "ai": "Анализ: зафиксированы пики сутулости в 10:00 и 14:00. Средний угол 18 градусов."
            }
        except: return {"x": [], "y": [], "ai": "Ошибка связи"}

    @staticmethod
    def get_patient_exams(p_id):
        try:
            res = requests.get(f"{APIService.URL}/patient/{p_id}/exams", timeout=5)
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def save_new_exam(p_id, data):
        try: return requests.post(f"{APIService.URL}/exams/save", json={"patient_id": p_id, "data": data}, timeout=5)
        except: return None
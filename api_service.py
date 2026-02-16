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
            return res.json() if res.status_code == 200 else {"username": "User", "speciality": "ВРАЧ"}
        except: return {"username": "User", "speciality": "ВРАЧ"}

    @staticmethod
    def get_patients(doc_id):
        """Запрос списка пациентов. Статус и цвет теперь вычисляет ИИ на сервере."""
        try:
            res = requests.get(f"{APIService.URL}/doctor/{doc_id}/patients", timeout=5)
            if res.status_code == 200:
                # Сервер возвращает данные, где color уже определен ИИ-алгоритмом
                return res.json()
            return []
        except: return []

    @staticmethod
    def register_new_patient(doc_id, name):
        try:
            res = requests.post(f"{APIService.URL}/doctor/register_patient", 
                                 json={"doctor_id": doc_id, "name": name}, timeout=5)
            if res.status_code == 200: return res.json()
            return None
        except: return None

    @staticmethod
    def save_exam(p_id, data):
        try: return requests.post(f"{APIService.URL}/exams/save", json={"patient_id": p_id, "data": data}, timeout=5)
        except: return None

    @staticmethod
    def get_patient_history(p_id):
        try:
            res = requests.get(f"{APIService.URL}/patient/{p_id}/history", timeout=5)
            if res.status_code == 200: return res.json()
            return {}
        except: return {}
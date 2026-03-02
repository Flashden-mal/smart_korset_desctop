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
        try:
            res = requests.get(f"{APIService.URL}/doctor/{doc_id}/patients", timeout=5)
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def register_new_patient(doc_id, name):
        try:
            res = requests.post(f"{APIService.URL}/doctor/{doc_id}/register_patient", json={"username": name}, timeout=10)
            return res.json() if res.status_code == 200 else None
        except: return None

    @staticmethod
    def get_patient_analytics(p_id, period="День"):
        try:
            res = requests.get(f"{APIService.URL}/patient/{p_id}/analytics", params={"period": period}, timeout=5)
            return res.json() if res.status_code == 200 else {"x": [], "y": [], "ai": "Ошибка"}
        except: return {"x": [], "y": [], "ai": "Ошибка связи"}

    @staticmethod
    def get_patient_exams(p_id):
        try:
            res = requests.get(f"{APIService.URL}/patient/{p_id}/exams", timeout=5)
            return res.json() if res.status_code == 200 else []
        except: return []

    @staticmethod
    def delete_exam(eid):
        try:
            res = requests.delete(f"{APIService.URL}/exams/{eid}", timeout=5)
            return res.status_code == 200
        except: return False

    @staticmethod
    def save_exam(p_id, data):
        try: return requests.post(f"{APIService.URL}/exams/save", json={"patient_id": p_id, "data": data}, timeout=5)
        except: return None
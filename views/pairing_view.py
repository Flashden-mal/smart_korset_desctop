import customtkinter as ctk
import qrcode
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PairingView(ctk.CTkFrame):
    def __init__(self, master, p_id, p_name, code, on_finish):
        super().__init__(master, fg_color="transparent")
        self.p_id, self.p_name, self.code, self.on_finish = p_id, p_name, code, on_finish

        # Центрированная карточка (Apple Style)
        self.card = ctk.CTkFrame(self, width=700, height=750, corner_radius=50, fg_color="#FFFFFF", border_width=1, border_color="#E5E5E7")
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Header
        ctk.CTkLabel(self.card, text="Подключение пациента", font=("Segoe UI Variable Display", 40, "bold"), text_color="#1D1D1F").pack(pady=(60, 5))
        ctk.CTkLabel(self.card, text="Передайте эти данные пациенту для настройки корсета", font=("Segoe UI Variable", 16), text_color="gray").pack(pady=(0, 40))

        # QR Code Generation (Retina Quality)
        qr_path = self.generate_qr(code)
        self.qr_img = ctk.CTkImage(Image.open(qr_path), size=(260, 260))
        
        qr_display = ctk.CTkLabel(self.card, image=self.qr_img, text="", corner_radius=20)
        qr_display.pack(pady=10)

        # Pairing Code Card
        code_box = ctk.CTkFrame(self.card, fg_color="#F2F2F7", corner_radius=25, width=450, height=100)
        code_box.pack(pady=30); code_box.pack_propagate(False)
        
        ctk.CTkLabel(code_box, text=f"КОД: {code}", font=("Segoe UI Variable Display", 36, "bold"), text_color="#007AFF").place(relx=0.5, rely=0.5, anchor="center")

        # Action Buttons
        btn_f = ctk.CTkFrame(self.card, fg_color="transparent")
        btn_f.pack(pady=40)

        self.pdf_btn = ctk.CTkButton(btn_f, text="📄 ПЕЧАТЬ В PDF", width=220, height=60, corner_radius=30, 
                                     fg_color="#F2F2F7", text_color="#1D1D1F", hover_color="#E5E5E7",
                                     font=("Segoe UI Variable", 15, "bold"), command=self.export_pdf)
        self.pdf_btn.pack(side="left", padx=15)

        self.done_btn = ctk.CTkButton(btn_f, text="ОТКРЫТЬ КАРТУ", width=220, height=60, corner_radius=30, 
                                      fg_color="#007AFF", hover_color="#0062CC",
                                      font=("Segoe UI Variable", 15, "bold"), command=on_finish)
        self.done_btn.pack(side="left", padx=15)

    def generate_qr(self, data):
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(data); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        path = "assets/temp_qr.png"
        if not os.path.exists('assets'): os.makedirs('assets')
        img.save(path)
        return path

    def export_pdf(self):
        filename = f"Pairing_Card_{self.p_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        c.setFont("Helvetica-Bold", 26)
        c.drawString(100, 750, "Smart Korset - Pairing Card")
        c.setFont("Helvetica", 18)
        c.drawString(100, 710, f"Patient Name: {self.p_name}")
        c.drawString(100, 685, f"Pairing Code: {self.code}")
        c.line(100, 670, 500, 670)
        c.drawInlineImage("assets/temp_qr.png", 150, 400, width=250, height=250)
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(100, 350, "Scan this QR code in the Smart Korset mobile app to link your device.")
        c.showPage(); c.save()
        os.startfile(filename)
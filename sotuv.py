import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import func
import json
import time
class SellWindow:
    def __init__(self, root, order, Eapi, Ebot,kod,reqid):
        self.root = root
        self.order = order
        self.Eapi = Eapi
        self.Ebot=''
        self.root.title("Sotish")
        self.root.geometry("700x800")
        self.root.configure(bg="#f5f5f5")
        self.EGazBot=Ebot
        self.kod=kod    
        self.detail=func.extract_td_a(self.EGazBot.get_detail(str(order['id'])),self.kod)
        self.reqid=reqid
       
        # func.extract_td_a(self.detail)
        
        # Header
        self.create_header()
        
        # Order info
        self.create_order_info()
        
        # Input fields
        self.create_input_fields()
        
        # Action button
        self.create_action_button()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#43cea2", height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🛒", font=("Arial", 30),
                bg="#43cea2", fg="white").pack(side=tk.LEFT, padx=(30, 15), pady=15)
        
        tk.Label(header_frame, text="SOTISH JARAYONI", 
                font=("Arial", 16, "bold"), bg="#43cea2", fg="white").pack(side=tk.LEFT, pady=15)
        
        # Close button
        close_btn = tk.Button(header_frame, text="✕", 
                             font=("Arial", 16, "bold"),
                             bg="#e74c3c", fg="white", relief=tk.FLAT,
                             cursor="hand2", padx=15, pady=5,
                             command=self.root.destroy)
        close_btn.pack(side=tk.RIGHT, padx=30, pady=15)
    
    def create_order_info(self):
        info_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(info_frame, bg="#667eea")
        title_frame.pack(fill=tk.X)
        
        tk.Label(title_frame, text=f"BUYURTMA №{self.order.get('numb', 'N/A')}", 
                font=("Arial", 13, "bold"),
                bg="#667eea", fg="white", pady=10).pack()
        
        # Info content
        content_frame = tk.Frame(info_frame, bg="white")
        content_frame.pack(fill=tk.X, padx=20, pady=15)
        
        info_items = [
            ("GTSH:", self.order.get('gns_name', 'N/A')),
            ("Qabul qilindi:", f"{self.order.get('accepted_qty', 0)} ta"),
            ("Sotilgan:", f"{self.order.get('passed_qty', 0)} ta"),
            ("Summa:", f"{float(self.order.get('amount', 0)):,.0f}".replace(",", " ") + " so'm")
        ]
        
        for label, value in info_items:
            row = tk.Frame(content_frame, bg="white")
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(row, text=label, font=("Arial", 10, "bold"),
                    bg="white", fg="#666", anchor="w", width=15).pack(side=tk.LEFT)
            
            tk.Label(row, text=value, font=("Arial", 10),
                    bg="white", fg="#333", anchor="w").pack(side=tk.LEFT)
    
    def create_input_fields(self):
        input_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, borderwidth=2)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Title
        tk.Label(input_frame, text="MA'LUMOTLARNI KIRITING", 
                font=("Arial", 12, "bold"),
                bg="#667eea", fg="white", pady=10).pack(fill=tk.X)
        
        # Content
        content = tk.Frame(input_frame, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Start Latitude
        self.create_field(content, "📍 Start Latitude:", 0)
        self.start_lat_entry = tk.Entry(content, font=("Arial", 11), 
                                        relief=tk.FLAT, bg="#f0f0f0")
        self.start_lat_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Start Longitude
        self.create_field(content, "📍 Start Longitude:", 1)
        self.start_lon_entry = tk.Entry(content, font=("Arial", 11), 
                                        relief=tk.FLAT, bg="#f0f0f0")
        self.start_lon_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Stop Latitude
        self.create_field(content, "📍 Stop Latitude:", 2)
        self.stop_lat_entry = tk.Entry(content, font=("Arial", 11), 
                                    relief=tk.FLAT, bg="#f0f0f0")
        self.stop_lat_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Stop Longitude
        self.create_field(content, "📍 Stop Longitude:", 3)
        self.stop_lon_entry = tk.Entry(content, font=("Arial", 11), 
                                    relief=tk.FLAT, bg="#f0f0f0")
        self.stop_lon_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Abonent raqamlari
        tk.Label(content, text="📱 Abonent raqamlari:", 
                font=("Arial", 10, "bold"),
                bg="white", fg="#666", anchor="w").grid(row=4, column=0, sticky="w", pady=(15, 5))
        
        tk.Label(content, text="(Har bir raqamni yangi qatorga kiriting)", 
                font=("Arial", 8, "italic"),
                bg="white", fg="#999", anchor="w").grid(row=5, column=0, columnspan=2, sticky="w")
        
        # TextBox for abonent raqamlari
        self.abonent_text = scrolledtext.ScrolledText(content, 
                                                    font=("Arial", 11),
                                                    height=8, 
                                                    relief=tk.FLAT, 
                                                    bg="#f0f0f0",
                                                    wrap=tk.WORD)
        self.abonent_text.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # Yuklab olish tugmasi
        download_btn = tk.Button(content, text="⬇️ Kodlarni Yuklab Olish", 
                                font=("Arial", 11, "bold"),
                                bg="#3498db", fg="white", relief=tk.FLAT, cursor="hand2",
                                command=self.load_codes_to_textbox)
        download_btn.grid(row=7, column=0, columnspan=2, pady=15)
        
        # Configure grid
        content.grid_columnconfigure(1, weight=1)

# Yangi funksiya
    def load_codes_to_textbox(self):
        self.abonent_text.delete("1.0", tk.END)  # TextBoxni tozalash
        codes = self.detail.get('codes', [])
        for code in codes:
            self.abonent_text.insert(tk.END, code + "\n")

    
    def create_field(self, parent, label, row):
        tk.Label(parent, text=label, 
                font=("Arial", 10, "bold"),
                bg="white", fg="#666", anchor="w").grid(row=row, column=0, sticky="w", pady=5)
    
    def create_action_button(self):
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        start_btn = tk.Button(button_frame, 
                             text="🚀 Savdoni Boshlash", 
                             font=("Arial", 13, "bold"),
                             bg="#43cea2", fg="white",
                             activebackground="#38b090",
                             activeforeground="white",
                             relief=tk.FLAT, cursor="hand2",
                             padx=40, pady=15,
                             command=self.start_sale)
        start_btn.pack()
    
    def start_sale(self):
        # Ma'lumotlarni olish
        start_lat = self.start_lat_entry.get().strip()
        start_lon = self.start_lon_entry.get().strip()
        stop_lat = self.stop_lat_entry.get().strip()
        stop_lon = self.stop_lon_entry.get().strip()
        abonent_numbers = self.abonent_text.get("1.0", tk.END).strip()
        
        # Validatsiya
        if not all([start_lat, start_lon, stop_lat, stop_lon, abonent_numbers]):
            messagebox.showwarning("Ogohlantirish", 
                                  "Iltimos, barcha maydonlarni to'ldiring!")
            return
        
        # Abonent raqamlarini qatorlarga bo'lish
        numbers_list = abonent_numbers.split('\n')
        numbers_list = [num.strip() for num in numbers_list if num.strip()]
        
        # Ma'lumotlarni ko'rsatish
        info_message = (
            f"📦 BUYURTMA: №{self.order.get('numb', 'N/A')}\n\n"
            f"📍 Start Latitude: {start_lat}\n"
            f"📍 Start Longitude: {start_lon}\n"
            f"📍 Stop Latitude: {stop_lat}\n"
            f"📍 Stop Longitude: {stop_lon}\n\n"
            f"📱 Abonent raqamlari ({len(numbers_list)} ta):\n"
        )
        global Ebot
        
        Ebot=self.EGazBot
        trackid=0
        balonid=0
        indx=0
        track=func.generate_path(float(start_lat), float(start_lon), float(stop_lat), float(stop_lon), 120)
        
        for idx, num in enumerate(numbers_list, 1):
            info_message += f"  {idx}. {num}\n"
            st=Ebot.get_subscriber(num)
            time.sleep(0.5)
            if st['balance']=="0.00 СУМ":
                print(f"{num} balans 0 to'lashimiz")
            else:
                ballonkod=self.detail['codes'][idx-1]   
                
                lat,long=track[idx-1]
                # write 
                self.Eapi.submit_ballon_request(oper='realization',abonent_kod=self.kod,next_rdt=40,id_rgs=self.order['numb'],id_request=self.reqid,ballon_kod=ballonkod,location_lon=long,location_lat=lat,abon_pinfl=st['jshshir'],photo_path="rasm.jpg")
                
            print(st)     
            
            
            
        
        # info_message += f"\n✅ Savdo muvaffaqiyatli boshlandi!"
        
        # messagebox.showinfo("Savdo ma'lumotlari", info_message)
        
        # Oynani yopish
        self.root.destroy()

# Test uchun
# if __name__ == "__main__":
#     test_order = {
#         'id': 1269233,
#         'numb': 3190110,
#         'dt_creation': '2025-11-23',
#         'gns_name': 'Ширин газ сервис МЧЖ ГТС',
#         'rgs_name': 'Асака туман ГАЗ',
#         'amount': '4720000.00',
#         'accepted_qty': 118,
#         'passed_qty': 1,
#         'returned_qty': 0,
#         'created_by': 'Рахимова Одина Акрамхуджаевна',
#         'accepted_by': 'MADAMINOV BOBIRJON MIRZAJON О\'G\'LI',
#         'dt_acception': '2025-11-23 11:14:18'
#     }
    
#     root = tk.Tk()
#     app = SellWindow(root, test_order, None)
#     root.mainloop()
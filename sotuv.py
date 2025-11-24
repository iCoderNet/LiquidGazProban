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
        self.start_lat_entry.insert(0, "40.200722")
        self.start_lat_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Start Longitude
        self.create_field(content, "📍 Start Longitude:", 1)
        self.start_lon_entry = tk.Entry(content, font=("Arial", 11), 
                                        relief=tk.FLAT, bg="#f0f0f0")
        self.start_lon_entry.insert(0, "71.749894")
        self.start_lon_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Stop Latitude
        self.create_field(content, "📍 Stop Latitude:", 2)
        self.stop_lat_entry = tk.Entry(content, font=("Arial", 11), 
                                    relief=tk.FLAT, bg="#f0f0f0")
        self.stop_lat_entry.insert(0, "40.202732")
        self.stop_lat_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Stop Longitude
        self.create_field(content, "📍 Stop Longitude:", 3)
        self.stop_lon_entry = tk.Entry(content, font=("Arial", 11), 
                                    relief=tk.FLAT, bg="#f0f0f0")
        self.stop_lon_entry.insert(0, "71.752475")
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

    def load_codes_to_textbox(self):
        self.abonent_text.delete("1.0", tk.END)
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
        """Ma'lumotlarni validatsiya qilib progress oynasini ochish"""
        start_lat = self.start_lat_entry.get().strip()
        start_lon = self.start_lon_entry.get().strip()
        stop_lat = self.stop_lat_entry.get().strip()
        stop_lon = self.stop_lon_entry.get().strip()
        abonent_numbers = self.abonent_text.get("1.0", tk.END).strip()
        
        if not all([start_lat, start_lon, stop_lat, stop_lon, abonent_numbers]):
            messagebox.showwarning("Ogohlantirish", "Iltimos, barcha maydonlarni to'ldiring!")
            return
        
        numbers_list = abonent_numbers.split('\n')
        numbers_list = [num.strip() for num in numbers_list if num.strip()]
        
        self.create_progress_window(numbers_list, start_lat, start_lon, stop_lat, stop_lon)
    
    def create_progress_window(self, numbers_list, start_lat, start_lon, stop_lat, stop_lon):
        """Progress oynasini yaratish"""
        progress_root = tk.Toplevel(self.root)
        progress_root.title("Sotish Jarayoni")
        progress_root.geometry("850x700")
        progress_root.configure(bg="#f5f5f5")
        progress_root.resizable(True, True)
        
        # Header
        header_frame = tk.Frame(progress_root, bg="#43cea2", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⏳ SOTISH JARAYONI", 
                font=("Arial", 16, "bold"), bg="#43cea2", fg="white").pack(pady=15)
        
        # Info
        info_frame = tk.Frame(progress_root, bg="white", relief=tk.RAISED, borderwidth=1)
        info_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        total_balloons = len(self.detail.get('balon_id', []))
        tk.Label(info_frame, text=f"Jami: {len(numbers_list)} ta abonent | Mavjud balonlar: {total_balloons} ta", 
                font=("Arial", 11, "bold"), bg="white", fg="#333").pack(pady=10)
        
        # Progress canvas with scrollbar
        canvas_frame = tk.Frame(progress_root, bg="#f5f5f5")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        progress_frame = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((0, 0), window=progress_frame, anchor="nw")
        
        progress_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
        
        # Stats
        stats_frame = tk.Frame(progress_root, bg="white", relief=tk.RAISED, borderwidth=1)
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        success_label = tk.Label(stats_frame, text="✅ Muvaffaqiyatli: 0", 
                                font=("Arial", 10, "bold"), bg="white", fg="#43cea2")
        success_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        skipped_label = tk.Label(stats_frame, text="⏭️ O'tkazildi: 0", 
                                font=("Arial", 10, "bold"), bg="white", fg="#f39c12")
        skipped_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        error_label = tk.Label(stats_frame, text="❌ Xatolik: 0", 
                              font=("Arial", 10, "bold"), bg="white", fg="#e74c3c")
        error_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        available_label = tk.Label(stats_frame, text=f"🎈 Qolgan: {total_balloons}", 
                                  font=("Arial", 10, "bold"), bg="white", fg="#3498db")
        available_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Start processing
        progress_root.after(100, lambda: self.process_sales_professional(
            numbers_list, start_lat, start_lon, stop_lat, stop_lon, 
            progress_frame, success_label, skipped_label, error_label, available_label, progress_root
        ))
    
    def process_sales_professional(self, numbers_list, start_lat, start_lon, stop_lat, stop_lon, 
                                   progress_frame, success_label, skipped_label, error_label, available_label, progress_root):
        """Professional balloon allocation with smart retry logic"""
        global Ebot
        Ebot = self.EGazBot
        track = func.generate_path(float(start_lat), float(start_lon), float(stop_lat), float(stop_lon), 120)
        
        success_count = 0
        skipped_count = 0
        error_count = 0
        
        # Balon poolini yaratish
        available_balloons = self.detail.get('balon_id', []).copy()
        total_balloons = len(available_balloons)
        
        for idx, num in enumerate(numbers_list, 1):
            # UI yaratish
            item_frame = tk.Frame(progress_frame, bg="white", relief=tk.SOLID, borderwidth=1)
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(item_frame, text=f"{idx}. {num}", 
                    font=("Arial", 10, "bold"), bg="white", fg="#333", 
                    anchor="w", width=18).pack(side=tk.LEFT, padx=10, pady=8)
            
            status_label = tk.Label(item_frame, text="⏳ Tekshirilmoqda...", 
                                   font=("Arial", 9), bg="white", fg="#666", anchor="w")
            status_label.pack(side=tk.LEFT, padx=10, pady=8, fill=tk.X, expand=True)
            
            progress_frame.update_idletasks()
            
            try:
                # Abonent ma'lumotlari
                st = Ebot.get_subscriber(num)
                time.sleep(0.3)
                
                # Balans tekshirish
                if st.get('balance') == "0.00 СУМ":
                    status_label.config(text="⏭️ Balans 0 - o'tkazildi", fg="#f39c12")
                    item_frame.config(bg="#fff8e1")
                    skipped_count += 1
                    continue
                
                # Balon borligini tekshirish
                if not available_balloons:
                    status_label.config(text="❌ Balonlar tugadi!", fg="#e74c3c")
                    item_frame.config(bg="#ffebee")
                    error_count += 1
                    continue
                
                # GPS
                if idx - 1 < len(track):
                    lat, long = track[idx-1]
                else:
                    lat, long = track[-1]
                
                # WHILE LOOP - Retry logic bilan balon berish
                balloon_success = False
                attempt = 0
                max_attempts = min(5, len(available_balloons))
                
                while not balloon_success and attempt < max_attempts and available_balloons:
                    current_balloon = available_balloons[0]
                    attempt += 1
                    
                    status_label.config(
                        text=f"🔄 Urinish {attempt}/{max_attempts} - Balon: {current_balloon}", 
                        fg="#3498db"
                    )
                    progress_root.update()
                    
                    try:
                        result = self.Eapi.submit_ballon_request(
                            oper='realization',
                            abonent_kod=num,
                            next_rdt=40,
                            id_rgs=self.order['numb'],
                            id_request=self.reqid,
                            ballon_kod=current_balloon,
                            location_lon=long,
                            location_lat=lat,
                            abon_pinfl=st.get('jshshir', ''),
                            photo_path="rasm.jpg"
                        )
                        
                        api_message = result.get('api_message', '')
                        
                        if result.get('api_status') == 1:
                            # SUCCESS!
                            status_label.config(
                                text=f"✅ Sotildi! Balon: {current_balloon} (urinish: {attempt})", 
                                fg="#43cea2"
                            )
                            item_frame.config(bg="#e8f5e9")
                            balloon_success = True
                            success_count += 1
                            available_balloons.remove(current_balloon)
                            
                        elif api_message == "Баллон не найден в БД!":
                            # Balon topilmadi - keyingisini sinash
                            print(f"⚠️ Balon {current_balloon} topilmadi, olib tashlanmoqda...")
                            available_balloons.remove(current_balloon)
                            time.sleep(0.2)
                            
                        elif api_message == "Реализация запрещена! Не существует абонент с таким кодом!":
                            # User topilmadi - bu userni skip qilish
                            status_label.config(
                                text="⏭️ Abonent tizimda topilmadi - o'tkazildi", 
                                fg="#f39c12"
                            )
                            item_frame.config(bg="#fff8e1")
                            skipped_count += 1
                            break  # while'den chiqish
                            
                        else:
                            # Boshqa xatolik - balonni olib tashlash va davom etish
                            print(f"⚠️ Xatolik: {api_message}, boshqa balonni sinaymiz...")
                            available_balloons.remove(current_balloon)
                            time.sleep(0.2)
                            
                    except Exception as e:
                        print(f"Exception: {e}")
                        if current_balloon in available_balloons:
                            available_balloons.remove(current_balloon)
                        break
                
                # Agar hech narsa muvaffaqiyatli bo'lmasa
                if not balloon_success and api_message != "Реализация запрещена! Не существует абонент с таким кодом!":
                    if not available_balloons:
                        status_label.config(text="❌ Balonlar tugadi", fg="#e74c3c")
                    else:
                        status_label.config(text=f"❌ {attempt} marta urinish - muvaffaqiyatsiz", fg="#e74c3c")
                    item_frame.config(bg="#ffebee")
                    if "⏭️" not in status_label.cget("text"):
                        error_count += 1
                        
            except Exception as e:
                status_label.config(text=f"❌ Fatal: {str(e)[:45]}", fg="#e74c3c")
                item_frame.config(bg="#ffebee")
                error_count += 1
            
            # Statistikani yangilash
            success_label.config(text=f"✅ Muvaffaqiyatli: {success_count}")
            skipped_label.config(text=f"⏭️ O'tkazildi: {skipped_count}")
            error_label.config(text=f"❌ Xatolik: {error_count}")
            available_label.config(text=f"🎈 Qolgan: {len(available_balloons)}/{total_balloons}")
            
            progress_root.update()
        
        # Yakuniy xabar
        messagebox.showinfo("Yakunlandi!", 
                          f"Sotish jarayoni tugadi!\n\n"
                          f"📊 Jami: {len(numbers_list)} ta\n"
                          f"✅ Muvaffaqiyatli: {success_count}\n"
                          f"⏭️ O'tkazildi: {skipped_count}\n"
                          f"❌ Xatolik: {error_count}\n\n"
                          f"🎈 Qolgan balonlar: {len(available_balloons)}/{total_balloons}")

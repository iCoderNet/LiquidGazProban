import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import func
import json
import time
import threading
from logger import get_logger

# Initialize logger for sales module
logger = get_logger('sotuv')

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
        self.map_coordinates = None  # Xaritadan olingan koordinatalar
        
        # Log window initialization
        logger.info(f"🛒 Sotish oynasi ochildi - Buyurtma №{order.get('numb', 'N/A')}")
        logger.debug(f"Buyurtma tafsilotlari: GTSH={order.get('gns_name')}, Qabul={order.get('accepted_qty')}, Sotilgan={order.get('passed_qty')}")
        logger.debug(f"Mavjud balonlar: {len(self.detail.get('balon_id', []))} ta, Taklif qilingan abonentlar: {len(self.detail.get('codes', []))} ta")
       
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
        
        # Default Latitude
        self.create_field(content, "📍 Default Latitude:", 0)
        self.default_lat_entry = tk.Entry(content, font=("Arial", 11), 
                                        relief=tk.FLAT, bg="#f0f0f0")
        self.default_lat_entry.insert(0, "41.31")
        self.default_lat_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Default Longitude
        self.create_field(content, "📍 Default Longitude:", 1)
        self.default_lon_entry = tk.Entry(content, font=("Arial", 11), 
                                        relief=tk.FLAT, bg="#f0f0f0")
        self.default_lon_entry.insert(0, "69.24")
        self.default_lon_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)
        
        # Map button
        map_btn = tk.Button(content, text="🗺️ Xaritani Ochish", 
                           font=("Arial", 12, "bold"),
                           bg="#667eea", fg="white", relief=tk.FLAT, cursor="hand2",
                           pady=10,
                           command=self.open_map_and_get_coordinates)
        map_btn.grid(row=2, column=0, columnspan=2, pady=(10, 10), sticky="ew")
        
        # Map status label
        self.map_status_label = tk.Label(content, text="❌ Xarita ma'lumotlari yuklanmagan", 
                                        font=("Arial", 9, "italic"),
                                        bg="white", fg="#e74c3c")
        self.map_status_label.grid(row=3, column=0, columnspan=2, pady=(0, 15))
        
        # Sleep Time
        self.create_field(content, "⏱️ Kutish vaqti (sekund):", 4)
        self.sleep_entry = tk.Entry(content, font=("Arial", 11), 
                                    relief=tk.FLAT, bg="#f0f0f0")
        self.sleep_entry.insert(0, "0")
        self.sleep_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0), ipady=8)

        # Abonent raqamlari
        tk.Label(content, text="📱 Abonent raqamlari:", 
                font=("Arial", 10, "bold"),
                bg="white", fg="#666", anchor="w").grid(row=5, column=0, sticky="w", pady=(15, 5))
        
        tk.Label(content, text="(Har bir raqamni yangi qatorga kiriting)", 
                font=("Arial", 8, "italic"),
                bg="white", fg="#999", anchor="w").grid(row=6, column=0, columnspan=2, sticky="w")
        
        # TextBox for abonent raqamlari
        self.abonent_text = scrolledtext.ScrolledText(content, 
                                                    font=("Arial", 11),
                                                    height=8, 
                                                    relief=tk.FLAT, 
                                                    bg="#f0f0f0",
                                                    wrap=tk.WORD)
        self.abonent_text.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # Yuklab olish tugmasi
        download_btn = tk.Button(content, text="⬇️ Kodlarni Yuklab Olish", 
                                font=("Arial", 11, "bold"),
                                bg="#3498db", fg="white", relief=tk.FLAT, cursor="hand2",
                                command=self.load_codes_to_textbox)
        download_btn.grid(row=8, column=0, columnspan=2, pady=15)
        
        # Configure grid
        content.grid_columnconfigure(1, weight=1)

    def load_codes_to_textbox(self):
        self.abonent_text.delete("1.0", tk.END)
        codes = self.detail.get('codes', [])
        for code in codes:
            self.abonent_text.insert(tk.END, code + "\n")
    
    def open_map_and_get_coordinates(self):
        """Xaritani Playwright orqali ochish va JSON ma'lumotlarni olish"""
        logger.info("🗺️ Xarita ochilmoqda - Playwright browser boshlandi")
        
        try:
            from playwright.sync_api import sync_playwright
            
            logger.debug("Playwright kutubxonasi yuklandi")
            
            with sync_playwright() as p:
                # Browser ochish (headed mode - ko'rinishda)
                logger.debug("Browser ishga tushirilmoqda (headed mode)...")
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                
                # Xarita sahifasiga o'tish
                default_lat = self.default_lat_entry.get().strip()
                default_lon = self.default_lon_entry.get().strip()
                
                map_url = "http://127.0.0.1:5000/"
                if default_lat and default_lon:
                    map_url = f"http://127.0.0.1:5000/?lat={default_lat}&long={default_lon}"
                
                logger.info(f"📍 Xarita sahifasiga o'tilmoqda: {map_url}")
                page.goto(map_url, timeout=10000)
                
                logger.info("⏳ Foydalanuvchi pozitsiyalarni tanlashini kutmoqda...")
                
                # JSON redirect'ni kutish
                # URL o'zgarishini kuzatish
                json_data = None
                timeout = 300000  # 5 minut timeout
                
                logger.debug("JSON redirect kutilmoqda...")
                
                try:
                    # Wait for navigation to JSON URL
                    with page.expect_navigation(timeout=timeout) as nav_info:
                        pass
                    
                    # Check if redirected to JSON endpoint
                    current_url = page.url
                    logger.info(f"🔄 Redirect aniqlandi: {current_url}")
                    
                    if "data_timesnap.json" in current_url or current_url.endswith(".json"):
                        # JSON sahifani o'qish
                        logger.debug("JSON ma'lumotlarni o'qish...")
                        content = page.content()
                        
                        # Extract JSON from page (it might be wrapped in <pre> tags)
                        import json
                        from bs4 import BeautifulSoup
                        
                        soup = BeautifulSoup(content, 'html.parser')
                        # Try to find JSON in <pre> or <body>
                        pre_tag = soup.find('pre')
                        if pre_tag:
                            json_text = pre_tag.get_text()
                        else:
                            # Try getting from body
                            body_tag = soup.find('body')
                            json_text = body_tag.get_text() if body_tag else content
                        
                        # Parse JSON
                        json_data = json.loads(json_text.strip())
                        logger.info(f"✅ JSON ma'lumotlar olindi: {len(json_data)} ta koordinata juftligi")
                        logger.debug(f"JSON ma'lumot: {json_data[:2]}..." if len(json_data) > 2 else f"JSON ma'lumot: {json_data}")
                        
                    else:
                        logger.warning(f"⚠️ Kutilmagan URL: {current_url}")
                        messagebox.showwarning("Ogohlantirish", 
                                             f"Kutilmagan URL: {current_url}\n"
                                             "JSON fayl kutilgan edi.")
                        browser.close()
                        return
                        
                except Exception as e:
                    logger.error(f"❌ Navigation xatosi: {str(e)}")
                    messagebox.showerror("Xatolik", 
                                       f"Xarita ma'lumotlarini olishda xatolik:\n{str(e)}\n\n"
                                       "Iltimos, xaritada pozitsiyalarni tanlab 'Yuborish' tugmasini bosing.")
                    browser.close()
                    return
                
                # Browser yopish
                browser.close()
                logger.info("🔒 Browser yopildi")
                
                if json_data:
                    self.map_coordinates = json_data
                    # Update status label
                    self.map_status_label.config(
                        text=f"✅ {len(json_data)} ta koordinata juftligi yuklandi",
                        fg="#43cea2"
                    )
                    messagebox.showinfo("Muvaffaqiyat", 
                                      f"Xarita ma'lumotlari muvaffaqiyatli yuklandi!\n"
                                      f"Koordinata juftliklari: {len(json_data)} ta")
                else:
                    logger.warning("⚠️ JSON ma'lumot bo'sh")
                    messagebox.showwarning("Ogohlantirish", "Ma'lumot topilmadi!")
                    
        except ImportError:
            logger.error("❌ Playwright kutubxonasi topilmadi")
            messagebox.showerror("Xatolik", 
                               "Playwright kutubxonasi o'rnatilmagan!\n\n"
                               "O'rnatish uchun:\n"
                               "pip install playwright\n"
                               "playwright install chromium")
        except Exception as e:
            logger.error(f"❌ Xarita ochishda xatolik: {str(e)}", exc_info=True)
            messagebox.showerror("Xatolik", f"Xaritani ochishda xatolik:\n{str(e)}")

    
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
                             command=self.start_sale)
        start_btn.pack()
    
    def start_sale(self):
        """Ma'lumotlarni validatsiya qilib progress oynasini ochish"""
        logger.info("🚀 Sotish jarayoni boshlandi - Ma'lumotlar validatsiya qilinmoqda")
        
        sleep_time_str = self.sleep_entry.get().strip()
        abonent_numbers = self.abonent_text.get("1.0", tk.END).strip()
        
        # Check if map coordinates are selected
        if not self.map_coordinates:
            logger.warning("⚠️ Validatsiya xatosi: Xarita ma'lumotlari tanlanmagan")
            messagebox.showwarning("Ogohlantirish", 
                                 "Iltimos, avval 'Xaritani Ochish' tugmasini bosib koordinatalarni tanlang!")
            return
        
        if not all([abonent_numbers, sleep_time_str]):
            logger.warning("⚠️ Validatsiya xatosi: Ba'zi maydonlar to'ldirilmagan")
            messagebox.showwarning("Ogohlantirish", "Iltimos, barcha maydonlarni to'ldiring!")
            return
        
        try:
            sleep_time = int(sleep_time_str)
            if sleep_time < 0:
                raise ValueError
        except ValueError:
            logger.warning(f"⚠️ Validatsiya xatosi: Noto'g'ri kutish vaqti - {sleep_time_str}")
            messagebox.showwarning("Ogohlantirish", "Kutish vaqti musbat butun son bo'lishi kerak!")
            return

        numbers_list = abonent_numbers.split('\n')
        numbers_list = [num.strip() for num in numbers_list if num.strip()]
        
        logger.info(f"✅ Validatsiya muvaffaqiyatli: {len(numbers_list)} ta abonent, kutish vaqti: {sleep_time}s")
        logger.info(f"📍 Xarita koordinatalari: {len(self.map_coordinates)} ta juftlik")
        
        self.create_progress_window(numbers_list, sleep_time)
    
    def create_progress_window(self, numbers_list, sleep_time):
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
        tk.Label(info_frame, text=f"Jami: {len(numbers_list)} ta abonent | Mavjud balonlar: {total_balloons} ta | Kutish: {sleep_time}s", 
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
        
        # Start processing in a separate thread
        threading.Thread(target=self.process_sales_professional, args=(
            numbers_list, 
            progress_frame, success_label, skipped_label, error_label, available_label, progress_root, sleep_time
        ), daemon=True).start()
    
    def process_sales_professional(self, numbers_list, 
                                   progress_frame, success_label, skipped_label, error_label, available_label, progress_root, sleep_time):
        """Professional balloon allocation with smart retry logic and threading"""
        logger.info("="*80)
        logger.info(f"🎯 SOTISH JARAYONI BOSHLANDI - Buyurtma №{self.order.get('numb', 'N/A')}")
        logger.info(f"📊 Jami abonentlar: {len(numbers_list)} ta")
        logger.info(f"🎈 Mavjud balonlar: {len(self.detail.get('balon_id', []))} ta")
        logger.info(f"⏱️ Kutish vaqti: {sleep_time} sekund")
        logger.info("="*80)
        
        global Ebot
        Ebot = self.EGazBot
        
        # Use map coordinates directly
        track = self.map_coordinates
        if not track:
            logger.error("❌ Xarita koordinatalari mavjud emas!")
            return
        
        success_count = 0
        skipped_count = 0
        error_count = 0
        
        # Balon poolini yaratish
        available_balloons = self.detail.get('balon_id', []).copy()
        total_balloons = len(available_balloons)
        
        logger.debug(f"Balon pool yaratildi: {available_balloons[:5]}..." if len(available_balloons) > 5 else f"Balon pool: {available_balloons}")
        
        for idx, num in enumerate(numbers_list, 1):
            logger.info(f"\n{'─'*60}")
            logger.info(f"📱 [{idx}/{len(numbers_list)}] Abonent: {num}")
            
            # UI yaratish (Main thread'da bajarilishi kerak)
            item_frame = None
            status_label = None
            
            def create_ui_item():
                nonlocal item_frame, status_label
                item_frame = tk.Frame(progress_frame, bg="white", relief=tk.SOLID, borderwidth=1)
                item_frame.pack(fill=tk.X, padx=10, pady=5)
                
                tk.Label(item_frame, text=f"{idx}. {num}", 
                        font=("Arial", 10, "bold"), bg="white", fg="#333", 
                        anchor="w", width=18).pack(side=tk.LEFT, padx=10, pady=8)
                
                status_label = tk.Label(item_frame, text="⏳ Tekshirilmoqda...", 
                                       font=("Arial", 9), bg="white", fg="#666", anchor="w")
                status_label.pack(side=tk.LEFT, padx=10, pady=8, fill=tk.X, expand=True)
                
                progress_frame.update_idletasks()
            
            progress_root.after(0, create_ui_item)
            
            # UI yaratilishini kutish (oddiy yechim)
            time.sleep(0.1)
            while item_frame is None:
                time.sleep(0.05)

            # Helper functions for UI updates
            def update_status(text, color):
                progress_root.after(0, lambda: status_label.config(text=text, fg=color))
            
            def update_bg(color):
                progress_root.after(0, lambda: item_frame.config(bg=color))
                
            def update_stats():
                progress_root.after(0, lambda: success_label.config(text=f"✅ Muvaffaqiyatli: {success_count}"))
                progress_root.after(0, lambda: skipped_label.config(text=f"⏭️ O'tkazildi: {skipped_count}"))
                progress_root.after(0, lambda: error_label.config(text=f"❌ Xatolik: {error_count}"))
                progress_root.after(0, lambda: available_label.config(text=f"🎈 Qolgan: {len(available_balloons)}/{total_balloons}"))

            balloon_success = False
            try:
                # Abonent ma'lumotlari
                logger.debug(f"Abonent ma'lumotlarini olish: {num}")
                st = Ebot.get_subscriber(num)
                time.sleep(0.3)
                
                logger.debug(f"Abonent ma'lumotlari: Balans={st.get('balance')}, JSHSHIR={st.get('jshshir', 'N/A')}")
                
                # Balans tekshirish
                if st.get('balance') == "0.00 СУМ":
                    logger.info(f"⏭️ O'tkazildi - Balans 0: {num}")
                    update_status("⏭️ Balans 0 - o'tkazildi", "#f39c12")
                    update_bg("#fff8e1")
                    skipped_count += 1
                    update_stats()
                    continue
                
                # Balon borligini tekshirish
                if not available_balloons:
                    logger.error(f"❌ BALONLAR TUGADI! Qolgan abonentlar: {len(numbers_list) - idx}")
                    update_status("❌ Balonlar tugadi!", "#e74c3c")
                    update_bg("#ffebee")
                    error_count += 1
                    update_stats()
                    continue
                
                # GPS
                if idx - 1 < len(track):
                    coord_data = track[idx-1]
                    # JSON format: {"startlat": ..., "startlong": ..., "stoplat": ..., "stoplong": ...}
                    # We use startlat/startlong for the sale location
                    lat = float(coord_data.get('startlat', 0))
                    long = float(coord_data.get('startlong', 0))
                else:
                    # Fallback to last coordinate if we run out
                    coord_data = track[-1]
                    lat = float(coord_data.get('startlat', 0))
                    long = float(coord_data.get('startlong', 0))
                logger.info(f" Lat: {lat}, Long: {long}")
                
                # WHILE LOOP - Retry logic bilan balon berish
                attempt = 0
                max_attempts = min(5, len(available_balloons))
                # rasm_url= func.get_pic_url(st['ps'], st['birth_date']) 

                # if rasm_url is None: 
                #         rasm_url='rasm.jpg'
                #         logger.error(f"❌ Rasm topilmadi: ")

                rasm_url='rasm.jpg'
                if st['photo'] != "":
                    logger.info(f"🔄 Rasm yuklanmoqda: {st['photo']}")
                    photo_url = func.get_pic_url(st['photo'], st['ps'])
                    if photo_url is None:
                        logger.error(f"❌ Rasm yuklanmadi: ")
                    else:
                        logger.info(f"🔄 Rasm yuklandi: {photo_url}")
                        rasm_url = photo_url

                logger.info(f"🔄 Rasm URL: {rasm_url}")
                
                logger.info(f"🔄 Balon berish jarayoni boshlandi - Maksimal urinishlar: {max_attempts}")
                
                while not balloon_success and attempt < max_attempts and available_balloons:
                    current_balloon = available_balloons[0]
                    attempt += 1
                    
                    logger.debug(f"Urinish {attempt}/{max_attempts} - Balon: {current_balloon}")
                    update_status(f"🔄 Urinish {attempt}/{max_attempts} - Balon: {current_balloon}", "#3498db")

                    
                    
                    
                    
                    try:
                        logger.debug(f"API so'rov yuborilmoqda: Abonent={num}, Balon={current_balloon}, GPS=({lat}, {long})")
                        logger.debug(f"JSHSHIR: {st['jshshir']}")
                        print(st['jshshir'])
                        
                        result = self.Eapi.submit_ballon_request(
                            oper='realization',
                            abonent_kod=num,
                            next_rdt=40,
                            id_rgs=self.order['numb'],
                            id_request=self.reqid,
                            ballon_kod=current_balloon,
                            location_lon=long,
                            location_lat=lat, 
                            abon_pinfl=st['jshshir'],
                            photo_path=rasm_url
                        )

                        api_message = result.get('api_message', '')
                        api_status = result.get('api_status')
                        
                        logger.debug(f"API javobi: status={api_status}, message={api_message}")
                        
                        if result.get('api_status') == 1:
                            # SUCCESS!
                            logger.info(f"✅ MUVAFFAQIYAT! Abonent: {num}, Balon: {current_balloon}, Urinish: {attempt}")
                            update_status(f"✅ Sotildi! Balon: {current_balloon} (urinish: {attempt})", "#43cea2")
                            update_bg("#e8f5e9")
                            balloon_success = True
                            success_count += 1
                            available_balloons.remove(current_balloon)
                            
                        elif api_message == "Баллон не найден в БД!":
                            # Balon topilmadi - keyingisini sinash
                            logger.warning(f"⚠️ Balon topilmadi: {current_balloon} - Olib tashlanmoqda")
                            available_balloons.remove(current_balloon)
                            time.sleep(0.2)
                            
                        elif api_message == "Реализация запрещена! Не существует абонент с таким кодом!":
                            # User topilmadi - bu userni skip qilish
                            logger.warning(f"⏭️ Abonent tizimda topilmadi: {num}")
                            update_status("⏭️ Abonent tizimda topilmadi - o'tkazildi", "#f39c12")
                            update_bg("#fff8e1")
                            skipped_count += 1
                            break  # while'den chiqish
                            
                        else:
                            # Boshqa xatolik - balonni olib tashlash va davom etish
                            logger.warning(f"⚠️ API xatosi: {api_message} - Balon: {current_balloon}")
                            available_balloons.remove(current_balloon)
                            time.sleep(0.2)
                            
                    except Exception as e:
                        logger.error(f"❌ Exception yuz berdi: {str(e)}", exc_info=True)
                        if current_balloon in available_balloons:
                            available_balloons.remove(current_balloon)
                        break
                
                # Agar hech narsa muvaffaqiyatli bo'lmasa
                if not balloon_success and api_message != "Реализация запрещена! Не существует абонент с таким кодом!":
                    if not available_balloons:
                        logger.error(f"❌ Xatolik: Balonlar tugadi - Abonent: {num}")
                        update_status("❌ Balonlar tugadi", "#e74c3c")
                    else:
                        logger.error(f"❌ Muvaffaqiyatsiz: {attempt} marta urinish - Abonent: {num}")
                        update_status(f"❌ {attempt} marta urinish - muvaffaqiyatsiz", "#e74c3c")
                    update_bg("#ffebee")
                    # Check if not skipped to avoid double counting
                    if "⏭️" not in status_label.cget("text"): # Note: cget might not be thread safe, but we rely on previous logic
                        error_count += 1
                        
            except Exception as e:
                logger.error(f"❌ FATAL ERROR - Abonent: {num}, Xatolik: {str(e)}", exc_info=True)
                update_status(f"❌ Fatal: {str(e)[:45]}", "#e74c3c")
                update_bg("#ffebee")
                error_count += 1
            
            # Statistikani yangilash
            update_stats()
            
            # Oraliq statistika
            logger.debug(f"Oraliq natija: ✅ {success_count} | ⏭️ {skipped_count} | ❌ {error_count} | 🎈 {len(available_balloons)}")
            
            # Sleep delay (User defined)
            if balloon_success and sleep_time > 0:
                logger.debug(f"⏳ Muvaffaqiyatli sotish - Kutish: {sleep_time} sekund")
                update_status(f"✅ Sotildi! Kutish: {sleep_time}s...", "#43cea2")
                time.sleep(sleep_time)
            elif not balloon_success:
                logger.debug(f"⏭️ Xatolik/O'tkazish - Sleep o'tkazib yuborildi")
        
        # Yakuniy statistika
        logger.info("\n" + "="*80)
        logger.info("🏁 SOTISH JARAYONI YAKUNLANDI")
        logger.info(f"📊 Jami abonentlar: {len(numbers_list)} ta")
        logger.info(f"✅ Muvaffaqiyatli: {success_count} ta ({success_count/len(numbers_list)*100:.1f}%)")
        logger.info(f"⏭️ O'tkazildi: {skipped_count} ta ({skipped_count/len(numbers_list)*100:.1f}%)")
        logger.info(f"❌ Xatolik: {error_count} ta ({error_count/len(numbers_list)*100:.1f}%)")
        logger.info(f"🎈 Ishlatilgan balonlar: {total_balloons - len(available_balloons)}/{total_balloons} ta")
        logger.info(f"🎈 Qolgan balonlar: {len(available_balloons)} ta")
        logger.info("="*80 + "\n")
        
        # Yakuniy xabar
        def show_final_message():
            messagebox.showinfo("Yakunlandi!", 
                              f"Sotish jarayoni tugadi!\n\n"
                              f"📊 Jami: {len(numbers_list)} ta\n"
                              f"✅ Muvaffaqiyatli: {success_count}\n"
                              f"⏭️ O'tkazildi: {skipped_count}\n"
                              f"❌ Xatolik: {error_count}\n\n"
                              f"🎈 Qolgan balonlar: {len(available_balloons)}/{total_balloons}")
        
        progress_root.after(0, show_final_message)

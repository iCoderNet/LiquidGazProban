import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from sotuv import SellWindow

class OrdersWindow:
    def __init__(self, root, orders_data, Eapi, insname, EgazBot,kod):
        self.root = root
        self.orders_data = orders_data
        self.root.title("Buyurtmalarni ko'rish")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5f5")
        self.Eapi = Eapi
        self.EgazBot=EgazBot
        self.insname = insname
        self.kod=kod
      
        # Faqat o'z buyurtmalarini filter qilish
        self.filtered_orders = [
            order for order in self.orders_data 
            if order.get('accepted_by', '') == self.insname
        ]
        
        # Header
        self.create_header()
        
        # Main content with scroll
        self.create_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#667eea", height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(header_frame, bg="#667eea")
        title_frame.pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Label(title_frame, text="📦", font=("Arial", 30), 
                bg="#667eea", fg="white").pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(title_frame, text="MENING BUYURTMALARIM", 
                font=("Arial", 16, "bold"), bg="#667eea", fg="white").pack(side=tk.LEFT)
        
        # Jami buyurtmalar soni
        count_label = tk.Label(header_frame, 
                              text=f"Jami: {len(self.filtered_orders)} ta buyurtma", 
                              font=("Arial", 11, "bold"), 
                              bg="#764ba2", fg="white",
                              padx=20, pady=8, relief=tk.FLAT)
        count_label.pack(side=tk.RIGHT, padx=30, pady=15)
        
        # Orqaga qaytish tugmasi
        back_btn = tk.Button(header_frame, text="⬅ Orqaga", 
                            font=("Arial", 10, "bold"),
                            bg="#764ba2", fg="white", relief=tk.FLAT,
                            cursor="hand2", padx=15, pady=5,
                            command=self.go_back)
        back_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=15)
    
    def create_content(self):
        # Agar buyurtmalar bo'lmasa
        if len(self.filtered_orders) == 0:
            self.show_empty_message()
            return
        
        # Main container with canvas and scrollbar
        container = tk.Frame(self.root, bg="#f5f5f5")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas
        canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame inside canvas
        self.orders_frame = tk.Frame(canvas, bg="#f5f5f5")
        canvas_window = canvas.create_window((0, 0), window=self.orders_frame, anchor="nw")
        
        # Update scrollregion when frame size changes
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        self.orders_frame.bind("<Configure>", configure_scroll_region)
        
        # Adjust frame width to canvas width
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Mouse wheel scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Create order cards
        self.create_order_cards()
    
    def show_empty_message(self):
        # Bo'sh xabar ko'rsatish
        empty_frame = tk.Frame(self.root, bg="#f5f5f5")
        empty_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=50)
        
        tk.Label(empty_frame, text="📭", font=("Arial", 80),
                bg="#f5f5f5", fg="#ccc").pack(pady=(50, 20))
        
        tk.Label(empty_frame, text="Buyurtmalar topilmadi", 
                font=("Arial", 18, "bold"),
                bg="#f5f5f5", fg="#666").pack(pady=10)
        
        tk.Label(empty_frame, text=f"Siz ({self.insname}) tomonidan qabul qilingan buyurtmalar yo'q", 
                font=("Arial", 11),
                bg="#f5f5f5", fg="#999").pack(pady=5)
    
    def create_order_cards(self):
        for idx, order in enumerate(self.filtered_orders):
            self.create_order_card(order, idx)
    
    def create_order_card(self, order, index):
        # Card container
        card = tk.Frame(self.orders_frame, bg="white", 
                       relief=tk.RAISED, borderwidth=2)
        card.pack(fill=tk.X, pady=10, padx=5)
        
        # Top section - Header
        header_frame = tk.Frame(card, bg="#667eea", height=45)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Buyurtma raqami
        order_num_label = tk.Label(header_frame, 
                                   text=f"BUYURTMA №: {order.get('numb', 'N/A')}", 
                                   font=("Arial", 13, "bold"),
                                   bg="#667eea", fg="white")
        order_num_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Sana
        date_label = tk.Label(header_frame, 
                             text=order.get('dt_creation', 'N/A'),
                             font=("Arial", 11, "bold"),
                             bg="#764ba2", fg="white",
                             padx=15, pady=5)
        date_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Content section
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # GTSH Operatori
        self.create_info_row(content_frame, "🏢 GTSH Operatori:", 
                            order.get('gns_name', 'N/A'), 0)
        
        # GTB
        self.create_info_row(content_frame, "📍 GTB:", 
                            order.get('rgs_name', 'N/A'), 1)
        
        # Yaratdi
        self.create_info_row(content_frame, "👤 Yaratdi:", 
                            order.get('created_by', 'N/A'), 2)
        
        # Qabul qildi
        self.create_info_row(content_frame, "✅ Qabul qilgan:", 
                            order.get('accepted_by', 'N/A'), 3)
        
        # Separator
        separator = tk.Frame(content_frame, bg="#e0e0e0", height=1)
        separator.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        
        # Statistics section
        stats_frame = tk.Frame(content_frame, bg="white")
        stats_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        
        # Qabul qilindi
        self.create_stat_box(stats_frame, "Qabul qilindi", 
                            order.get('accepted_qty', 0), "#667eea", 0)
        
        # Sotilgan
        self.create_stat_box(stats_frame, "Sotilgan", 
                            order.get('passed_qty', 0), "#43cea2", 1)
        
        # Qaytdi
        self.create_stat_box(stats_frame, "Qaytdi", 
                            order.get('returned_qty', 0), "#e74c3c", 2)
        
        # Summa
        amount = float(order.get('amount', 0))
        formatted_amount = f"{amount:,.0f}".replace(",", " ")
        self.create_stat_box(stats_frame, "Summa", 
                            f"{formatted_amount} so'm", "#f39c12", 3)
        
        # Configure grid weights
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Bottom section - Qabul qilingan sana va Sotish tugmasi
        bottom_frame = tk.Frame(card, bg="#f8f9fa")
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Qabul qilingan vaqt
        if order.get('dt_acception'):
            tk.Label(bottom_frame, 
                    text=f"⏰ Qabul qilingan: {order.get('dt_acception', 'N/A')}", 
                    font=("Arial", 9, "italic"),
                    bg="#f8f9fa", fg="#666").pack(pady=8)
        
        # Sotish tugmasi
        sell_button = tk.Button(bottom_frame, 
                               text="🛒 Sotish", 
                               font=("Arial", 11, "bold"),
                               bg="#43cea2", fg="white", 
                               activebackground="#38b090",
                               activeforeground="white",
                               relief=tk.FLAT, cursor="hand2",
                               padx=30, pady=10,
                               command=lambda o=order: self.sell_order(o))
        sell_button.pack(pady=15)
    
    def create_info_row(self, parent, label, value, row):
        # Label
        label_widget = tk.Label(parent, text=label, 
                               font=("Arial", 10, "bold"),
                               bg="white", fg="#666", anchor="w")
        label_widget.grid(row=row, column=0, sticky="w", pady=5, padx=(0, 10))
        
        # Value
        value_widget = tk.Label(parent, text=value, 
                               font=("Arial", 10),
                               bg="white", fg="#333", anchor="w",
                               wraplength=500)
        value_widget.grid(row=row, column=1, sticky="w", pady=5)
        
        # Configure column weights
        parent.grid_columnconfigure(0, weight=0, minsize=150)
        parent.grid_columnconfigure(1, weight=1)
    
    def create_stat_box(self, parent, label, value, color, col):
        box = tk.Frame(parent, bg=color, relief=tk.RAISED, borderwidth=1)
        box.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        
        # Value
        value_label = tk.Label(box, text=str(value), 
                              font=("Arial", 16, "bold"),
                              bg=color, fg="white")
        value_label.pack(pady=(15, 5))
        
        # Label
        label_widget = tk.Label(box, text=label, 
                               font=("Arial", 9),
                               bg=color, fg="white")
        label_widget.pack(pady=(0, 15))
    
    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#333", height=35)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, 
                text=f"© 2025 GAZ Dashboard | Jami buyurtmalar: {len(self.filtered_orders)}", 
                font=("Arial", 9), bg="#333", fg="white").pack(pady=8)
    
    def go_back(self):
        self.root.destroy()
    
    def sell_order(self, order):
        # Sotish funksiyasi
        order_num = order.get('numb', 'N/A')
        order_qty = order.get('accepted_qty', 0)
        # print(order)    
        root = tk.Tk()
        # print(order)
        SellWindow(root, order, self.Eapi,self.EgazBot,self.kod,order['id'])
        self.root.destroy()
        
        

# # Test uchun
# if __name__ == "__main__":
#     # API dan kelgan ma'lumotlar (namuna)
#     test_orders = [
#         {
#             'id': 1269205,
#             'numb': 3190082,
#             'dt_creation': '2025-11-23',
#             'gns_name': 'Ширин газ сервис МЧЖ ГТС',
#             'rgs_name': 'Асака туман ГАЗ',
#             'amount': '4720000.00',
#             'accepted_qty': 118,
#             'passed_qty': 0,
#             'returned_qty': 0,
#             'created_by': 'Рахимова Одина Акрамхуджаевна',
#             'accepted_by': "Alijonov Bexruzbek Axlidin o'g'li",
#             'dt_acception': '2025-11-23 10:18:31'
#         },
#         {
#             'id': 1269233,
#             'numb': 3190110,
#             'dt_creation': '2025-11-23',
#             'gns_name': 'Ширин газ сервис МЧЖ ГТС',
#             'rgs_name': 'Асака туман ГАЗ',
#             'amount': '4720000.00',
#             'accepted_qty': 118,
#             'passed_qty': 1,
#             'returned_qty': 0,
#             'created_by': 'Рахимова Одина Акрамхуджаевна',
#             'accepted_by': 'MADAMINOV BOBIRJON MIRZAJON О\'G\'LI',
#             'dt_acception': '2025-11-23 11:14:18'
#         },
#         {
#             'id': 1268485,
#             'numb': 3189362,
#             'dt_creation': '2025-11-22',
#             'gns_name': 'Ширин газ сервис МЧЖ ГТС',
#             'rgs_name': 'Асака туман ГАЗ',
#             'amount': '4720000.00',
#             'accepted_qty': 118,
#             'passed_qty': 0,
#             'returned_qty': 0,
#             'created_by': 'Рахимова Одина Акрамхуджаевна',
#             'accepted_by': 'QURBONOV SHAROBIDDIN',
#             'dt_acception': '2025-11-22 09:18:04'
#         }
#     ]
    
#     test_insname = "MADAMINOV BOBIRJON MIRZAJON О'G'LI"
    
#     root = tk.Tk()
#     app = OrdersWindow(root, test_orders, None, test_insname)
#     root.mainloop()
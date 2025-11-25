import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox, ttk
from datetime import datetime
from product import OrdersWindow

class DashboardApp:
    def __init__(self, root, user_data,Eapi,EgazBot):
        self.root = root
        self.user_data = user_data
        self.root.title("Asosiy Panel")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")
        self.Eapi=Eapi
        self.auth_hash= ''
        self.inspector_kod=self.user_data.get('kod','')
        self.id_org=self.user_data.get('id_org','')
        self.EgazBot=EgazBot    
        
        
        # Header
        self.create_header()
        
        # Main content
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo va title
        title_frame = tk.Frame(header_frame, bg="#667eea")
        title_frame.pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Label(title_frame, text="🏢", font=("Arial", 30), 
                bg="#667eea", fg="white").pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(title_frame, text="GAZ DASHBOARD", 
                font=("Arial", 18, "bold"), bg="#667eea", fg="white").pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(header_frame, bg="#667eea")
        user_frame.pack(side=tk.RIGHT, padx=30, pady=15)
        
        tk.Label(user_frame, text=f"👤 {self.user_data.get('name', 'N/A')}", 
                font=("Arial", 11, "bold"), bg="#667eea", fg="white").pack(anchor="e")
        
        tk.Label(user_frame, text=f"{self.user_data.get('privileges_name', 'N/A')}", 
                font=("Arial", 9), bg="#667eea", fg="#e0e0e0").pack(anchor="e")
        
        # Logout button
        logout_btn = tk.Button(user_frame, text="Chiqish", font=("Arial", 9), 
                              bg="#764ba2", fg="white", relief=tk.FLAT,
                              cursor="hand2", padx=15, pady=5,
                              command=self.logout)
        logout_btn.pack(anchor="e", pady=(5, 0))
    
    def create_main_content(self):
        content_frame = tk.Frame(self.root, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Info cards container
        cards_frame = tk.Frame(content_frame, bg="#f5f5f5")
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1: Shaxsiy ma'lumotlar
        self.create_info_card(cards_frame, "📋 SHAXSIY MA'LUMOTLAR", [
            ("ID:", str(self.user_data.get('id', 'N/A'))),
            ("F.I.O:", self.user_data.get('name', 'N/A')),
            ("Email:", self.user_data.get('email', 'N/A')),
            ("Kod:", self.user_data.get('kod', 'N/A')),
            ("Status:", self.user_data.get('status', 'N/A'))
        ], 0)
        
        # Card 2: Tashkilot ma'lumotlari
        self.create_info_card(cards_frame, "🏢 TASHKILOT", [
            ("Tashkilot:", self.user_data.get('org_name', 'N/A')),
            ("Lavozim:", self.user_data.get('privileges_name', 'N/A')),
            ("Region ID:", str(self.user_data.get('id_region', 'N/A'))),
            ("Tuman ID:", str(self.user_data.get('id_district', 'N/A'))),
            ("Tashkilot ID:", str(self.user_data.get('id_org', 'N/A')))
        ], 1)
        
        # Card 3: Oxirgi kirish
        last_login = self.user_data.get('lastlogin', 'N/A')
        if last_login != 'N/A':
            try:
                dt = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                formatted_date = dt.strftime('%d.%m.%Y')
                formatted_time = dt.strftime('%H:%M:%S')
            except:
                formatted_date = last_login
                formatted_time = ''
        else:
            formatted_date = 'N/A'
            formatted_time = ''
        
        self.create_info_card(cards_frame, "🕐 OXIRGI KIRISH", [
            ("Sana:", formatted_date),
            ("Vaqt:", formatted_time),
            ("", ""),
            ("", ""),
            ("", "")
        ], 2)
        
        # Menu buttons
        menu_frame = tk.Frame(content_frame, bg="#f5f5f5")
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(menu_frame, text="ASOSIY MENYU", font=("Arial", 14, "bold"),
                bg="#f5f5f5", fg="#333").pack(anchor="w", pady=(0, 15))
        
        # Menu buttons grid
        buttons_frame = tk.Frame(menu_frame, bg="#f5f5f5")
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        menu_items = [
            ("📦Buyurtmalarni ko'rish", "#667eea"),
            ("💳To'lovlar tarixi", "#6a11cb"),
            ("📊Hisobotlar", "#43cea2"),
            
        ]
        
        for idx, (text, color) in enumerate(menu_items):
            row = idx // 3
            col = idx % 3
            self.create_menu_button(buttons_frame, text, color, row, col)
    
    def create_info_card(self, parent, title, items, col):
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        # Title
        title_frame = tk.Frame(card, bg="#667eea")
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text=title, font=("Arial", 12, "bold"),
                bg="#667eea", fg="white", pady=12).pack()
        
        # Content
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        for label, value in items:
            if label:  # Faqat bo'sh bo'lmagan labellarni ko'rsatish
                item_frame = tk.Frame(content_frame, bg="white")
                item_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(item_frame, text=label, font=("Arial", 9, "bold"),
                        bg="white", fg="#666", anchor="w").pack(side=tk.LEFT)
                
                tk.Label(item_frame, text=value, font=("Arial", 9),
                        bg="white", fg="#333", anchor="w").pack(side=tk.LEFT, padx=(10, 0))
    
    def create_menu_button(self, parent, text, color, row, col):
        btn = tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                       bg=color, fg="white", relief=tk.FLAT,
                       cursor="hand2", height=3,
                       activebackground=color, activeforeground="white",
                       command=lambda: self.menu_action(text))
        btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
    
    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#333", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, 
                text=f"© 2025 GAZ Dashboard | Foydalanuvchi: {self.user_data.get('kod', 'N/A')}", 
                font=("Arial", 9), bg="#333", fg="white").pack(pady=10)
    
    def menu_action(self, menu_name):
        if menu_name == "📦Buyurtmalarni ko'rish" :
            chk=self.Eapi.inspector_data(oper='detail',
            inspector_kod=self.inspector_kod,
            type='rgs',
            id_org=str(self.id_org),
            auth_hash=self.auth_hash
            )
            # print(chk)
            blns=self.Eapi.ballon_requests_rgs(oper='list',id_rgs=self.id_org,auth_hash=self.auth_hash,take=100) 
            
            # Clear current window
            for widget in self.root.winfo_children():
                widget.destroy()
                
            OrdersWindow(self.root, blns['data'],Eapi=self.Eapi,insname=chk['data']['name'],EgazBot=self.EgazBot,kod=self.inspector_kod)
            
            
        
            
            
    
    def logout(self):
        result = messagebox.askyesno("Chiqish", "Tizimdan chiqmoqchimisiz?")
        if result:
            self.root.destroy()

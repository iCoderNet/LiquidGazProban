import tkinter as tk
from tkinter import messagebox, ttk
from  api.inspector_login import EgazAPI
from bot import EGazBot
from dashboard import DashboardApp
import xtokens
Eapi=''
Ebot=''
Prf=''
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kirish")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        
        # Gradient background rangini sozlash
        self.root.configure(bg="#667eea")
        
        # Markaziy frame
        main_frame = tk.Frame(root, bg="white", relief=tk.RAISED, borderwidth=3)
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=480)
        
        # Logo
        logo_frame = tk.Frame(main_frame, bg="#667eea", width=80, height=80)
        logo_frame.pack(pady=(30, 10))
        logo_label = tk.Label(logo_frame, text="🔐", font=("Arial", 40), bg="#667eea", fg="white")
        logo_label.pack(expand=True)
        
        # Sarlavha
        title_label = tk.Label(main_frame, text="Xush Kelibsiz", 
                               font=("Arial", 24, "bold"), bg="white", fg="#667eea")
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(main_frame, text="Akkauntingizga kiring", 
                                 font=("Arial", 11), bg="white", fg="#666")
        subtitle_label.pack(pady=(0, 30))
        
        # Login input
        login_label = tk.Label(main_frame, text="Login", 
                              font=("Arial", 10, "bold"), bg="white", fg="#333")
        login_label.pack(anchor="w", padx=30)
        
        self.login_entry = tk.Entry(main_frame, font=("Arial", 12), 
                                   relief=tk.FLAT, bg="#f0f0f0", fg="#333")
        self.login_entry.pack(pady=(5, 15), padx=30, ipady=10, fill=tk.X)
        self.login_entry.insert(0, "")
        
        # Parol input
        password_label = tk.Label(main_frame, text="Parol", 
                                 font=("Arial", 10, "bold"), bg="white", fg="#333")
        password_label.pack(anchor="w", padx=30)
        
        self.password_entry = tk.Entry(main_frame, font=("Arial", 12), 
                                      show="●", relief=tk.FLAT, bg="#f0f0f0", fg="#333")
        self.password_entry.pack(pady=(5, 10), padx=30, ipady=10, fill=tk.X)
        
        # Parolni ko'rsatish checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(main_frame, text="Parolni ko'rsatish", 
                                            variable=self.show_password_var,
                                            command=self.toggle_password,
                                            font=("Arial", 9), bg="white", 
                                            activebackground="white", fg="#666")
        show_password_check.pack(anchor="w", padx=30, pady=(0, 20))
        
        # Kirish tugmasi
        login_button = tk.Button(main_frame, text="Kirish", 
                                font=("Arial", 12, "bold"), 
                                bg="#667eea", fg="white", 
                                activebackground="#5568d3",
                                activeforeground="white",
                                relief=tk.FLAT, cursor="hand2",
                                command=self.login)
        login_button.pack(pady=10, padx=30, ipady=12, fill=tk.X)
        
        # Parolni unutdingizmi?
        forgot_label = tk.Label(main_frame, text="Parolni unutdingizmi?", 
                               font=("Arial", 9, "underline"), 
                               bg="white", fg="#667eea", cursor="hand2")
        forgot_label.pack(pady=(10, 20))
        forgot_label.bind("<Button-1>", lambda e: self.forgot_password())
        
        # Pastki chiziq
        separator = tk.Frame(main_frame, bg="#e0e0e0", height=1)
        separator.pack(fill=tk.X, padx=30, pady=10)
        
        # Ro'yxatdan o'tish
        register_frame = tk.Frame(main_frame, bg="white")
        register_frame.pack(pady=10)
        
        tk.Label(register_frame, text="Akkauntingiz yo'qmi?", 
                font=("Arial", 9), bg="white", fg="#666").pack(side=tk.LEFT)
        
        register_label = tk.Label(register_frame, text=" Ro'yxatdan o'tish", 
                                 font=("Arial", 9, "bold"), 
                                 bg="white", fg="#667eea", cursor="hand2")
        register_label.pack(side=tk.LEFT)
        register_label.bind("<Button-1>", lambda e: self.register())
        
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()
        global Eapi, Ebot, Prf, EgazAPI, EGazBot
        Eapi=EgazAPI(xtokens.Xauthorization_token,xtokens.timestamp)
        # Eapi=EgazAPI('731ada0befa4af7e163aeac38e2ec51a','1763952717753')
        lgn=Eapi.inspector_login(login,password)
        Ebot=EGazBot()
        
        info = Ebot.get_subscriber("01000099813")
        
        
        if lgn['api_status']==1:
            messagebox.showinfo("Muvaffaqiyatli", "Kirish muvaffaqiyatli!")
            root=tk.Tk()
            # print(lgn)
            EgazAPI=Eapi
            EGazBot=Ebot
            Prf=DashboardApp(root,lgn['data'],Eapi,EGazBot)
            auth_hash = xtokens.make_hash(login,str(lgn['data']['id']),xtokens.timestamp)
            Prf.auth_hash = auth_hash
            Eapi.auth_hash = auth_hash
            
             
            
            self.root.destroy()
        else:
            messagebox.showerror("Xato", "Login yoki parol noto'g'ri.")
            
        
        
        
    
    def forgot_password(self):
        messagebox.showinfo("Parolni tiklash", 
                          "Parolni tiklash uchun admin bilan bog'laning.")
    
    def register(self):
        messagebox.showinfo("Ro'yxatdan o'tish", 
                          "Ro'yxatdan o'tish sahifasi ochiladi...")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
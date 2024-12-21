import tkinter as tk
from tkinter import ttk, messagebox
import firebase_admin
from firebase_admin import credentials, auth
import subprocess

cred = credentials.Certificate("backend\\firebase.json")
firebase_admin.initialize_app(cred)

class DarkTechnicalLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Login")
        self.root.geometry("400x500")
        self.root.configure(bg='#0f172a')
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (400/2)
        y = (screen_height/2) - (500/2)
        self.root.geometry(f'400x500+{int(x)}+{int(y)}')
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#0f172a')
        style.configure('Dark.TLabel', 
                       background='#0f172a',
                       foreground='#e2e8f0',
                       font=('Segoe UI', 10))
        style.configure('DarkHeader.TLabel',
                       background='#0f172a',
                       foreground='#e2e8f0',
                       font=('Segoe UI', 24, 'bold'))
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(main_frame,
                 text="VerboVisions",
                 style='DarkHeader.TLabel').pack(pady=(0, 30))
        
        entry_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        entry_frame.pack(fill='x', padx=40)
        
        ttk.Label(entry_frame,
                 text="EMAIL ADDRESS",
                 style='Dark.TLabel').pack(anchor='w')
        
        self.email_entry = tk.Entry(entry_frame,
                                  bg='#1e293b',
                                  fg='#e2e8f0',
                                  insertbackground='#e2e8f0',
                                  relief='flat',
                                  font=('Segoe UI', 10))
        self.email_entry.pack(fill='x', ipady=8, pady=(5, 15))
        
        ttk.Label(entry_frame,
                 text="PASSWORD",
                 style='Dark.TLabel').pack(anchor='w')
        
        self.password_entry = tk.Entry(entry_frame,
                                     bg='#1e293b',
                                     fg='#e2e8f0',
                                     insertbackground='#e2e8f0',
                                     relief='flat',
                                     font=('Segoe UI', 10),
                                     show="●")
        self.password_entry.pack(fill='x', ipady=8, pady=(5, 20))
        
        login_button = tk.Button(entry_frame,
                               text="LOGIN",
                               command=self.login,
                               bg='#0284c7',
                               fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               relief='flat',
                               cursor='hand2')
        login_button.pack(fill='x', ipady=10, pady=(0, 10))
        
        separator = ttk.Separator(entry_frame, orient='horizontal')
        separator.pack(fill='x', pady=15)
        
        signup_button = tk.Button(entry_frame,
                                text="CREATE ACCOUNT",
                                command=self.open_signup,
                                bg='#1e293b',
                                fg='#e2e8f0',
                                font=('Segoe UI', 10),
                                relief='flat',
                                cursor='hand2')
        signup_button.pack(fill='x', ipady=10)
        
        for button, hover_color, leave_color in [
            (login_button, '#0369a1', '#0284c7'),
            (signup_button, '#334155', '#1e293b')
        ]:
            button.bind('<Enter>',
                       lambda e, btn=button, c=hover_color: btn.configure(bg=c))
            button.bind('<Leave>',
                       lambda e, btn=button, c=leave_color: btn.configure(bg=c))
    
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            user = auth.get_user_by_email(email)
            if not user.email_verified:
                messagebox.showerror("Access Denied", "Email verification required.")
                return
                
            with open("user_session.txt", "w") as session_file:
                session_file.write(email)
                
            messagebox.showinfo("Access Granted", "Authentication successful.")
            self.root.destroy()
            subprocess.run(["python", "app/main.py"])
            
        except firebase_admin.exceptions.FirebaseError:
            messagebox.showerror("Access Denied", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("System Error", str(e))
    
    def open_signup(self):
        self.root.destroy()
        subprocess.run(["python", "signup.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkTechnicalLogin(root)
    root.mainloop()
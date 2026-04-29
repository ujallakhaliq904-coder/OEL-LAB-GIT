import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import Style

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.BG_COLOR)
        self.controller = controller
        
        # Center Frame
        center_frame = tk.Frame(self, bg=Style.WHITE, padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        tk.Label(center_frame, text="Hotel Management System", font=Style.FONT_TITLE, bg=Style.WHITE, fg=Style.PRIMARY).pack(pady=(0, 20))
        tk.Label(center_frame, text="Admin Login", font=Style.FONT_SUBTITLE, bg=Style.WHITE, fg=Style.TEXT_MAIN).pack(pady=(0, 20))
        
        # Username
        tk.Label(center_frame, text="Username", font=Style.FONT_NORMAL, bg=Style.WHITE, fg=Style.TEXT_MAIN).pack(anchor="w")
        self.username_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.username_var, font=Style.FONT_NORMAL, width=30).pack(pady=(5, 15))
        
        # Password
        tk.Label(center_frame, text="Password", font=Style.FONT_NORMAL, bg=Style.WHITE, fg=Style.TEXT_MAIN).pack(anchor="w")
        self.password_var = tk.StringVar()
        tk.Entry(center_frame, textvariable=self.password_var, show="*", font=Style.FONT_NORMAL, width=30).pack(pady=(5, 20))
        
        # Login Button
        btn = tk.Button(center_frame, text="Login", font=Style.FONT_BUTTON, bg=Style.PRIMARY, fg=Style.WHITE, 
                        command=self.login, width=20, cursor="hand2")
        btn.pack(pady=10)
        
    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty.")
            return
            
        success, user = AuthService.login(username, password)
        if success:
            self.controller.current_user = user
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

if __name__ == "__main__":
    class MockController:
        current_user = None
        def show_frame(self, name): print(f"Switching to {name}")
    root = tk.Tk()
    root.geometry("800x600")
    view = LoginView(root, MockController())
    view.pack(fill="both", expand=True)
    root.mainloop()

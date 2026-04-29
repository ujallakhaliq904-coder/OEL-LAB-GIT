import sys
import os

# Ensure the parent directory is in sys.path so 'app' can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import tkinter as tk
from app.utils.database import init_db
from app.services.auth import AuthService
from app.views.login import LoginView
from app.views.dashboard import DashboardView
from app.views.rooms import RoomsView
from app.views.booking import BookingView
from app.views.billing import BillingView

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Initialize DB and create an admin if not exists
        init_db()
        from app.models.user import User
        if not User.get_user_by_username("admin"):
            AuthService.create_admin("admin", "admin123")
            
        self.current_user = None
        
        # Container for all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (LoginView, DashboardView, RoomsView, BookingView, BillingView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame("LoginView")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.mainloop()

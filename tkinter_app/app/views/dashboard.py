import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from app.utils.style import Style

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.BG_COLOR)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg=Style.PRIMARY, height=80)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Admin Dashboard", font=Style.FONT_TITLE, bg=Style.PRIMARY, fg=Style.WHITE).pack(side=tk.LEFT, padx=20, pady=20)
        tk.Button(header, text="Logout", font=Style.FONT_BUTTON, bg=Style.DANGER, fg=Style.WHITE, 
                  command=self.logout, cursor="hand2").pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Main Content
        content = tk.Frame(self, bg=Style.BG_COLOR)
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Nav Buttons Grid
        buttons = [
            ("Room Management", "RoomsView"),
            ("Customer & Booking", "BookingView"),
            ("Billing & Checkout", "BillingView")
        ]
        
        for i, (text, frame_name) in enumerate(buttons):
            btn = tk.Button(content, text=text, font=Style.FONT_SUBTITLE, bg=Style.WHITE, fg=Style.PRIMARY,
                            width=25, height=3, cursor="hand2",
                            command=lambda f=frame_name: self.controller.show_frame(f))
            btn.grid(row=i//2, column=i%2, padx=20, pady=20)
            
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")

if __name__ == "__main__":
    class MockController:
        current_user = None
        def show_frame(self, name): print(f"Switching to {name}")
    root = tk.Tk()
    root.geometry("800x600")
    view = DashboardView(root, MockController())
    view.pack(fill="both", expand=True)
    root.mainloop()

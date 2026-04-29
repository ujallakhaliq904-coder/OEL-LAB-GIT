import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import Style
from app.models.room import Room

class RoomsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.BG_COLOR)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg=Style.PRIMARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Room Management", font=Style.FONT_TITLE, bg=Style.PRIMARY, fg=Style.WHITE).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(header, text="Back to Dashboard", font=Style.FONT_BUTTON, command=lambda: controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Form Frame
        form_frame = tk.Frame(self, bg=Style.WHITE, padx=20, pady=20)
        form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(form_frame, text="Room No:", bg=Style.WHITE).grid(row=0, column=0, padx=5, pady=5)
        self.room_no_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.room_no_var).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Type:", bg=Style.WHITE).grid(row=0, column=2, padx=5, pady=5)
        self.type_var = tk.StringVar()
        type_cb = ttk.Combobox(form_frame, textvariable=self.type_var, values=["Single", "Double", "Deluxe"])
        type_cb.grid(row=0, column=3, padx=5, pady=5)
        type_cb.current(0)
        
        tk.Label(form_frame, text="Price:", bg=Style.WHITE).grid(row=0, column=4, padx=5, pady=5)
        self.price_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.price_var).grid(row=0, column=5, padx=5, pady=5)
        
        tk.Button(form_frame, text="Add Room", bg=Style.SUCCESS, fg=Style.WHITE, command=self.add_room).grid(row=0, column=6, padx=20, pady=5)
        
        # Table Frame
        table_frame = tk.Frame(self, bg=Style.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        columns = ("id", "room_no", "type", "price", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("room_no", text="Room No")
        self.tree.heading("type", text="Type")
        self.tree.heading("price", text="Price")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_rooms()

    def load_rooms(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rooms = Room.get_all_rooms()
        for r in rooms:
            self.tree.insert("", tk.END, values=(r['room_id'], r['room_number'], r['type'], r['price'], r['status']))

    def add_room(self):
        room_no = self.room_no_var.get()
        room_type = self.type_var.get()
        price = self.price_var.get()
        
        if not room_no or not price:
            messagebox.showerror("Error", "Room number and price are required.")
            return
            
        try:
            price = float(price)
            if price <= 0: raise ValueError
        except:
            messagebox.showerror("Error", "Price must be a positive number.")
            return
            
        if Room.add_room(room_no, room_type, price):
            messagebox.showinfo("Success", "Room added successfully.")
            self.room_no_var.set("")
            self.price_var.set("")
            self.load_rooms()
        else:
            messagebox.showerror("Error", "Failed to add room. Room number may already exist.")

if __name__ == "__main__":
    from app.utils.database import init_db
    init_db()
    class MockController:
        current_user = None
        def show_frame(self, name): print(f"Switching to {name}")
    root = tk.Tk()
    root.geometry("800x600")
    view = RoomsView(root, MockController())
    view.pack(fill="both", expand=True)
    view.load_rooms()
    root.mainloop()

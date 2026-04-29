import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from app.utils.style import Style
from app.services.booking_service import BookingService
from app.models.room import Room
from app.models.booking import Booking

class BookingView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.BG_COLOR)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg=Style.PRIMARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Customer & Booking", font=Style.FONT_TITLE, bg=Style.PRIMARY, fg=Style.WHITE).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(header, text="Back to Dashboard", font=Style.FONT_BUTTON, command=lambda: controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        # Content split
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=Style.BG_COLOR)
        paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form Frame
        form_frame = tk.Frame(paned, bg=Style.WHITE, padx=20, pady=20)
        paned.add(form_frame, minsize=400)
        
        tk.Label(form_frame, text="New Booking", font=Style.FONT_SUBTITLE, bg=Style.WHITE).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        fields = ["Name:", "CNIC:", "Phone:", "Email:"]
        self.vars = {f: tk.StringVar() for f in fields}
        
        for i, f in enumerate(fields):
            tk.Label(form_frame, text=f, bg=Style.WHITE).grid(row=i+1, column=0, sticky="w", pady=5)
            tk.Entry(form_frame, textvariable=self.vars[f], width=30).grid(row=i+1, column=1, pady=5)

        tk.Label(form_frame, text="Room:", bg=Style.WHITE).grid(row=5, column=0, sticky="w", pady=5)
        self.room_var = tk.StringVar()
        self.room_cb = ttk.Combobox(form_frame, textvariable=self.room_var, state="readonly", width=27)
        self.room_cb.grid(row=5, column=1, pady=5)
        
        tk.Label(form_frame, text="Check-in:", bg=Style.WHITE).grid(row=6, column=0, sticky="w", pady=5)
        self.check_in_var = tk.StringVar()
        self.check_in_date = DateEntry(form_frame, textvariable=self.check_in_var, date_pattern='y-mm-dd', width=27)
        self.check_in_date.grid(row=6, column=1, pady=5)
        
        tk.Label(form_frame, text="Check-out:", bg=Style.WHITE).grid(row=7, column=0, sticky="w", pady=5)
        self.check_out_var = tk.StringVar()
        self.check_out_date = DateEntry(form_frame, textvariable=self.check_out_var, date_pattern='y-mm-dd', width=27)
        self.check_out_date.grid(row=7, column=1, pady=5)
        
        tk.Button(form_frame, text="Book Room", bg=Style.SUCCESS, fg=Style.WHITE, font=Style.FONT_BUTTON,
                  command=self.book_room).grid(row=8, column=0, columnspan=2, pady=20)

        # Active Bookings
        list_frame = tk.Frame(paned, bg=Style.WHITE)
        paned.add(list_frame)
        
        tk.Label(list_frame, text="Active Bookings", font=Style.FONT_SUBTITLE, bg=Style.WHITE).pack(pady=(10, 5))
        
        columns = ("booking_id", "customer", "cnic", "room", "in", "out")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("booking_id", text="ID")
        self.tree.heading("customer", text="Name")
        self.tree.heading("cnic", text="CNIC")
        self.tree.heading("room", text="Room No")
        self.tree.heading("in", text="Check-in")
        self.tree.heading("out", text="Check-out")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(list_frame, bg=Style.WHITE)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Button(btn_frame, text="Cancel Selected", bg=Style.DANGER, fg=Style.WHITE, command=self.cancel_booking).pack(side=tk.RIGHT)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()

    def load_data(self):
        # Load rooms
        rooms = Room.get_available_rooms()
        self.room_cb['values'] = [f"{r['room_id']} - Room {r['room_number']} ({r['type']})" for r in rooms]
        if rooms: self.room_cb.current(0)
        
        # Load active bookings
        for item in self.tree.get_children():
            self.tree.delete(item)
        bookings = Booking.get_active_bookings()
        for b in bookings:
            self.tree.insert("", tk.END, values=(b['booking_id'], b['name'], b['cnic'], b['room_number'], b['check_in'], b['check_out']))

    def book_room(self):
        name = self.vars["Name:"].get()
        cnic = self.vars["CNIC:"].get()
        phone = self.vars["Phone:"].get()
        email = self.vars["Email:"].get()
        room_str = self.room_var.get()
        if not room_str:
            messagebox.showerror("Error", "Please select a room.")
            return
        room_id = int(room_str.split(" ")[0])
        check_in = self.check_in_var.get()
        check_out = self.check_out_var.get()
        
        success, msg = BookingService.register_and_book(name, cnic, phone, email, room_id, check_in, check_out)
        if success:
            messagebox.showinfo("Success", msg)
            for v in self.vars.values(): v.set("")
            self.load_data()
        else:
            messagebox.showerror("Error", msg)

    def cancel_booking(self):
        selected = self.tree.selection()
        if not selected: return
        booking_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            Booking.cancel_booking(booking_id)
            self.load_data()

if __name__ == "__main__":
    from app.utils.database import init_db
    init_db()
    class MockController:
        current_user = None
        def show_frame(self, name): print(f"Switching to {name}")
    root = tk.Tk()
    root.geometry("800x600")
    view = BookingView(root, MockController())
    view.pack(fill="both", expand=True)
    view.load_data()
    root.mainloop()

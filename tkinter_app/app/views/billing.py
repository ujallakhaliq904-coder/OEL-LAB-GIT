import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import Style
from app.models.booking import Booking
from app.services.billing_service import BillingService

class BillingView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Style.BG_COLOR)
        self.controller = controller
        
        # Header
        header = tk.Frame(self, bg=Style.PRIMARY, height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Billing & Checkout", font=Style.FONT_TITLE, bg=Style.PRIMARY, fg=Style.WHITE).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(header, text="Back to Dashboard", font=Style.FONT_BUTTON, command=lambda: controller.show_frame("DashboardView")).pack(side=tk.RIGHT, padx=20, pady=15)

        # Content split
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=Style.BG_COLOR)
        paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel (Select Booking & Services)
        left_frame = tk.Frame(paned, bg=Style.WHITE, padx=20, pady=20)
        paned.add(left_frame, minsize=400)
        
        tk.Label(left_frame, text="Select Booking", font=Style.FONT_SUBTITLE, bg=Style.WHITE).pack(anchor="w", pady=(0, 10))
        
        self.booking_var = tk.StringVar()
        self.booking_cb = ttk.Combobox(left_frame, textvariable=self.booking_var, state="readonly", width=40)
        self.booking_cb.pack(fill=tk.X, pady=(0, 20))
        self.booking_cb.bind("<<ComboboxSelected>>", self.on_booking_select)
        
        tk.Label(left_frame, text="Add Services", font=Style.FONT_SUBTITLE, bg=Style.WHITE).pack(anchor="w", pady=(10, 10))
        
        self.service_var = tk.StringVar()
        self.service_cb = ttk.Combobox(left_frame, textvariable=self.service_var, state="readonly", width=30)
        self.service_cb.pack(side=tk.LEFT, pady=5)
        
        tk.Button(left_frame, text="Add", bg=Style.PRIMARY, fg=Style.WHITE, command=self.add_service_to_booking).pack(side=tk.LEFT, padx=10)
        
        # Right Panel (Bill Display)
        self.right_frame = tk.Frame(paned, bg=Style.WHITE, padx=20, pady=20)
        paned.add(self.right_frame)
        
        tk.Label(self.right_frame, text="Invoice Summary", font=Style.FONT_TITLE, bg=Style.WHITE).pack(pady=(0, 20))
        
        self.bill_text = tk.Text(self.right_frame, width=50, height=15, font=("Courier", 12))
        self.bill_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.bill_text.config(state=tk.DISABLED)
        
        tk.Button(self.right_frame, text="Confirm Checkout & Pay", font=Style.FONT_BUTTON, bg=Style.SUCCESS, fg=Style.WHITE,
                  command=self.checkout).pack(pady=10)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()

    def load_data(self):
        # Load active bookings
        bookings = Booking.get_active_bookings()
        self.booking_cb['values'] = [f"{b['booking_id']} - {b['name']} (Room {b['room_number']})" for b in bookings]
        if bookings: self.booking_cb.current(0)
        
        # Load services
        services = BillingService.get_services()
        # Seed some services if empty
        if not services:
            BillingService.add_service("Breakfast", 500)
            BillingService.add_service("Laundry", 300)
            BillingService.add_service("Room Cleaning", 200)
            services = BillingService.get_services()
            
        self.service_cb['values'] = [f"{s['service_id']} - {s['name']} (Rs.{s['price']})" for s in services]
        if services: self.service_cb.current(0)
        self.on_booking_select(None)

    def on_booking_select(self, event):
        val = self.booking_var.get()
        if not val:
            self.update_bill_text("Select a booking to view invoice.")
            return
            
        booking_id = int(val.split(" ")[0])
        booking = Booking.get_booking_details(booking_id)
        if not booking: return
        
        bill = BillingService.calculate_bill(booking_id)
        if not bill: return
        
        text = f"HOTEL MANAGEMENT SYSTEM\n"
        text += "="*40 + "\n"
        text += f"Booking ID : {booking['booking_id']}\n"
        text += f"Customer   : {booking['name']}\n"
        text += f"Room       : {booking['room_number']}\n"
        text += f"Check-In   : {booking['check_in']}\n"
        text += f"Check-Out  : {booking['check_out']}\n"
        text += "-"*40 + "\n"
        text += f"Room Charges ({bill['days']} days) : Rs.{bill['room_total']}\n"
        text += f"Service Charges      : Rs.{bill['service_total']}\n"
        text += "-"*40 + "\n"
        text += f"Subtotal             : Rs.{bill['subtotal']}\n"
        text += f"Tax (10%)            : Rs.{bill['tax']}\n"
        text += "="*40 + "\n"
        text += f"TOTAL AMOUNT         : Rs.{bill['total']}\n"
        text += "="*40 + "\n"
        
        self.update_bill_text(text)
        
    def update_bill_text(self, text):
        self.bill_text.config(state=tk.NORMAL)
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, text)
        self.bill_text.config(state=tk.DISABLED)

    def add_service_to_booking(self):
        b_val = self.booking_var.get()
        s_val = self.service_var.get()
        
        if not b_val or not s_val:
            return
            
        booking_id = int(b_val.split(" ")[0])
        service_id = int(s_val.split(" ")[0])
        
        BillingService.add_service_to_booking(booking_id, service_id)
        self.on_booking_select(None)
        messagebox.showinfo("Success", "Service added to bill.")

    def checkout(self):
        val = self.booking_var.get()
        if not val: return
        
        booking_id = int(val.split(" ")[0])
        if messagebox.askyesno("Confirm Checkout", "Are you sure you want to checkout and mark bill as paid?"):
            success, msg = BillingService.generate_bill_and_checkout(booking_id)
            if success:
                messagebox.showinfo("Success", "Checkout completed successfully!")
                self.booking_var.set("")
                self.load_data()
                self.update_bill_text("")
            else:
                messagebox.showerror("Error", msg)

if __name__ == "__main__":
    from app.utils.database import init_db
    init_db()
    class MockController:
        current_user = None
        def show_frame(self, name): print(f"Switching to {name}")
    root = tk.Tk()
    root.geometry("800x600")
    view = BillingView(root, MockController())
    view.pack(fill="both", expand=True)
    view.load_data()
    root.mainloop()

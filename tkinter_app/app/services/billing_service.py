import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.database import get_connection
from datetime import datetime

class BillingService:
    @staticmethod
    def get_services():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services")
        services = cursor.fetchall()
        conn.close()
        return services

    @staticmethod
    def add_service(name, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO services (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()

    @staticmethod
    def add_service_to_booking(booking_id, service_id, quantity=1):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO booking_services (booking_id, service_id, quantity) VALUES (?, ?, ?)", 
                       (booking_id, service_id, quantity))
        conn.commit()
        conn.close()

    @staticmethod
    def calculate_bill(booking_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get booking details
        cursor.execute("""
            SELECT b.check_in, b.check_out, r.price 
            FROM bookings b
            JOIN rooms r ON b.room_id = r.room_id
            WHERE b.booking_id = ?
        """, (booking_id,))
        booking = cursor.fetchone()
        
        if not booking:
            conn.close()
            return None
            
        check_in = datetime.strptime(booking['check_in'], "%Y-%m-%d")
        check_out = datetime.strptime(booking['check_out'], "%Y-%m-%d")
        days = (check_out - check_in).days
        if days <= 0: days = 1
        
        room_total = days * booking['price']
        
        # Get services total
        cursor.execute("""
            SELECT SUM(s.price * bs.quantity) as service_total
            FROM booking_services bs
            JOIN services s ON bs.service_id = s.service_id
            WHERE bs.booking_id = ?
        """, (booking_id,))
        service_data = cursor.fetchone()
        service_total = service_data['service_total'] if service_data['service_total'] else 0
        
        subtotal = room_total + service_total
        tax = subtotal * 0.10 # 10% tax
        total = subtotal + tax
        
        conn.close()
        return {
            'days': days,
            'room_total': room_total,
            'service_total': service_total,
            'subtotal': subtotal,
            'tax': tax,
            'total': total
        }

    @staticmethod
    def generate_bill_and_checkout(booking_id):
        bill_details = BillingService.calculate_bill(booking_id)
        if not bill_details:
            return False, "Booking not found."
            
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Create billing record
            cursor.execute("INSERT INTO billing (booking_id, total_amount) VALUES (?, ?)", 
                           (booking_id, bill_details['total']))
                           
            # Complete booking and release room
            from app.models.booking import Booking
            Booking.complete_booking(booking_id)
            
            cursor.execute("SELECT room_id FROM bookings WHERE booking_id = ?", (booking_id,))
            room = cursor.fetchone()
            from app.models.room import Room
            Room.update_status(room['room_id'], 'available')
            
            conn.commit()
            conn.close()
            return True, bill_details
        except Exception as e:
            conn.close()
            return False, str(e)

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.database import get_connection

class Booking:
    @staticmethod
    def create_booking(customer_id, room_id, check_in, check_out):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (customer_id, room_id, check_in, check_out, status) VALUES (?, ?, ?, ?, 'active')", 
                       (customer_id, room_id, check_in, check_out))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return booking_id

    @staticmethod
    def get_active_bookings():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.booking_id, c.name, c.cnic, r.room_number, b.check_in, b.check_out, r.room_id 
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            WHERE b.status = 'active'
        """)
        bookings = cursor.fetchall()
        conn.close()
        return bookings
        
    @staticmethod
    def get_booking_details(booking_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.booking_id, c.name, c.cnic, r.room_number, r.price, b.check_in, b.check_out, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN rooms r ON b.room_id = r.room_id
            WHERE b.booking_id = ?
        """, (booking_id,))
        booking = cursor.fetchone()
        conn.close()
        return booking

    @staticmethod
    def complete_booking(booking_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET status = 'completed' WHERE booking_id = ?", (booking_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def cancel_booking(booking_id):
        conn = get_connection()
        cursor = conn.cursor()
        # First get room_id
        cursor.execute("SELECT room_id FROM bookings WHERE booking_id = ?", (booking_id,))
        room = cursor.fetchone()
        
        cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE booking_id = ?", (booking_id,))
        if room:
            cursor.execute("UPDATE rooms SET status = 'available' WHERE room_id = ?", (room['room_id'],))
            
        conn.commit()
        conn.close()

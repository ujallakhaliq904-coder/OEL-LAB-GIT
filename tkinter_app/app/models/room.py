import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.database import get_connection

class Room:
    @staticmethod
    def get_all_rooms():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        conn.close()
        return rooms
        
    @staticmethod
    def get_available_rooms():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE status = 'available'")
        rooms = cursor.fetchall()
        conn.close()
        return rooms

    @staticmethod
    def add_room(room_number, room_type, price):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO rooms (room_number, type, price, status) VALUES (?, ?, ?, 'available')", 
                           (room_number, room_type, price))
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def update_status(room_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET status = ? WHERE room_id = ?", (status, room_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_room(room_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rooms WHERE room_id = ?", (room_id,))
        conn.commit()
        conn.close()

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.database import get_connection

class Customer:
    @staticmethod
    def add_customer(name, cnic, phone, email):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO customers (name, cnic, phone, email) VALUES (?, ?, ?, ?)", 
                           (name, cnic, phone, email))
            conn.commit()
            customer_id = cursor.lastrowid
            conn.close()
            return customer_id
        except Exception as e:
            conn.close()
            return None

    @staticmethod
    def get_customer_by_cnic(cnic):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE cnic = ?", (cnic,))
        customer = cursor.fetchone()
        conn.close()
        return customer

    @staticmethod
    def get_all_customers():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        conn.close()
        return customers
        
    @staticmethod
    def update_customer(customer_id, name, phone, email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE customers SET name = ?, phone = ?, email = ? WHERE customer_id = ?", 
                       (name, phone, email, customer_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_customer(customer_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        conn.commit()
        conn.close()

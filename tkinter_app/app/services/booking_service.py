import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.customer import Customer
from app.models.room import Room
from app.models.booking import Booking
from app.utils.validation import Validation

class BookingService:
    @staticmethod
    def register_and_book(name, cnic, phone, email, room_id, check_in, check_out):
        # Validations
        if not all([name, cnic, phone, email, room_id, check_in, check_out]):
            return False, "All fields are required."
            
        if not Validation.is_valid_name(name):
            return False, "Invalid name."
        if not Validation.is_valid_cnic(cnic):
            return False, "Invalid CNIC format (12345-1234567-1)."
        if not Validation.is_valid_phone(phone):
            return False, "Invalid phone number."
        if not Validation.is_valid_email(email):
            return False, "Invalid email format."
        if not Validation.is_valid_booking_dates(check_in, check_out):
            return False, "Invalid check-in/check-out dates."

        # Check if customer already exists
        customer = Customer.get_customer_by_cnic(cnic)
        if customer:
            customer_id = customer['customer_id']
        else:
            customer_id = Customer.add_customer(name, cnic, phone, email)
            if not customer_id:
                return False, "Failed to register customer."

        # Create booking
        try:
            booking_id = Booking.create_booking(customer_id, room_id, check_in, check_out)
            # Update room status
            Room.update_status(room_id, 'booked')
            return True, "Booking successful!"
        except Exception as e:
            return False, f"Failed to create booking: {str(e)}"

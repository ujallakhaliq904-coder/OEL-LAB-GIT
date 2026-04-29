import re
from datetime import datetime

class Validation:
    @staticmethod
    def is_not_empty(text):
        return bool(text and text.strip())

    @staticmethod
    def is_valid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_phone(phone):
        return phone.isdigit() and 10 <= len(phone) <= 15

    @staticmethod
    def is_valid_cnic(cnic):
        pattern = r"^\d{5}-\d{7}-\d{1}$"
        return re.match(pattern, cnic) is not None

    @staticmethod
    def is_valid_name(name):
        return all(part.isalpha() or part.isspace() for part in name) and len(name.strip()) > 0

    @staticmethod
    def is_valid_date_format(date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_booking_dates(check_in_str, check_out_str):
        if not Validation.is_valid_date_format(check_in_str) or not Validation.is_valid_date_format(check_out_str):
            return False
        
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d")
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d")
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if check_in < today:
            return False
        if check_out <= check_in:
            return False
            
        return True

    @staticmethod
    def is_positive_number(value):
        try:
            val = float(value)
            return val >= 0
        except ValueError:
            return False

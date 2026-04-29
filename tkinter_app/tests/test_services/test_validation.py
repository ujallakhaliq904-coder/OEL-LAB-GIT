import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from app.utils.validation import Validation

def test_is_valid_email():
    assert Validation.is_valid_email("test@example.com") == True
    assert Validation.is_valid_email("invalid-email") == False

def test_is_valid_phone():
    assert Validation.is_valid_phone("1234567890") == True
    assert Validation.is_valid_phone("123") == False
    assert Validation.is_valid_phone("abc1234567") == False

def test_is_valid_cnic():
    assert Validation.is_valid_cnic("12345-1234567-1") == True
    assert Validation.is_valid_cnic("1234512345671") == False
    
def test_is_valid_date_format():
    assert Validation.is_valid_date_format("2025-05-15") == True
    assert Validation.is_valid_date_format("15-05-2025") == False

def test_is_valid_booking_dates():
    # Past dates should fail
    assert Validation.is_valid_booking_dates("2020-01-01", "2020-01-05") == False
    # Check out before check in
    assert Validation.is_valid_booking_dates("2099-01-05", "2099-01-01") == False
    # Valid
    assert Validation.is_valid_booking_dates("2099-01-01", "2099-01-05") == True

if __name__ == "__main__":
    pytest.main([__file__])

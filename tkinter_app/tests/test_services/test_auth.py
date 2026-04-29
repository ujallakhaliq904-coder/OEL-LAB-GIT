import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from app.services.auth import AuthService
import app.utils.database as db
import sqlite3
import os

# Overwrite DB_FILE for tests
db.DB_FILE = "test_hotel_management.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup
    db.init_db()
    yield
    # Teardown
    if os.path.exists("test_hotel_management.db"):
        try:
            os.remove("test_hotel_management.db")
        except:
            pass

def test_create_admin_and_login():
    success = AuthService.create_admin("testadmin", "password123")
    assert success == True
    
    # Test correct login
    success, user = AuthService.login("testadmin", "password123")
    assert success == True
    assert user['username'] == "testadmin"
    
    # Test incorrect login
    success, user = AuthService.login("testadmin", "wrongpass")
    assert success == False
    assert user is None

if __name__ == "__main__":
    pytest.main([__file__])

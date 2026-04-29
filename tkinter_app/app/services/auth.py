import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import bcrypt
from app.models.user import User

class AuthService:
    @staticmethod
    def login(username, password):
        user = User.get_user_by_username(username)
        if user:
            stored_password = user['password']
            # If bcrypt was used to hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, user
        return False, None

    @staticmethod
    def create_admin(username, password):
        # Hash password and create admin
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return User.create_user(username, hashed)

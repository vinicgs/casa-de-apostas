from flask_login import UserMixin
from app import login_manager
from app.db import get_db

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user_row = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    if user_row:
        return User(user_row['id'], user_row['email'])
    return None

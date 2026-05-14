from flask import Flask
from flask_login import LoginManager

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'chave_super_secreta_premium'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes, models
from app.db import init_db

init_db()

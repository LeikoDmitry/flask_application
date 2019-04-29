from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)


app.config['SECRET_KEY'] = '7kRA6AwqgdtmBM2AL34jB4ndzdB5Rfm6bxhCzVpsvMBz9CRretpBNs6AepGY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/fl_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'eae70d6312c61a'
app.config['MAIL_PASSWORD'] = '00f213d89cd10c'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)
mail = Mail(app=app)
login_manager = LoginManager(app=app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import route


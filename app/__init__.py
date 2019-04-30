from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.error.handler import ErrorPagesHandler


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'authorization.login'
login_manager.login_message_category = 'info'


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    login_manager.init_app(app=app)
    db.init_app(app=app)
    bcrypt.init_app(app=app)
    mail.init_app(app=app)
    from app.authorization.route import authorization
    from app.post.route import post
    from app.main.route import main
    app.register_blueprint(blueprint=authorization)
    app.register_blueprint(blueprint=post)
    app.register_blueprint(blueprint=main)
    app.register_error_handler(403, ErrorPagesHandler.page_forbidden)
    app.register_error_handler(404, ErrorPagesHandler.page_not_found)
    app.register_error_handler(500, ErrorPagesHandler.internal_server_error)
    return app

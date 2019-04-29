from datetime import datetime
from app import db, login_manager
from flask import current_app as app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    image_file = db.Column(db.String(120), unique=True, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Article', backref='author', lazy=True)

    def get_reset_token(self, expires_sec: int = 3600):
        s = Serializer(secret_key=app.config['SECRET_KEY'], expires_in=expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token: str):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{ self.username }, {self.email}, {self.image_file}')"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Article('{ self.title }, {self.date_posted}')"

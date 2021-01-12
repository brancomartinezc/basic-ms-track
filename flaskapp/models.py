from flask import current_app
from flaskapp import db, login_mng
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_mng.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    watched = db.relationship('Watched', backref='user', lazy=True)
    to_watch = db.relationship('ToWatch', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}, {self.email}')"

class Watched(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Watched('{self.name}')"

class ToWatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ToWatch('{self.name}')"
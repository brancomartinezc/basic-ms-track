from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskapp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_mng = LoginManager()
login_mng.login_view = 'users.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_mng.init_app(app)
    mail.init_app(app)

    from flaskapp.users.views import users
    from flaskapp.watched.views import watched
    from flaskapp.towatch.views import towatch
    from flaskapp.main.views import main
    from flaskapp.errors.views import errors
    app.register_blueprint(users)
    app.register_blueprint(watched)
    app.register_blueprint(towatch)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
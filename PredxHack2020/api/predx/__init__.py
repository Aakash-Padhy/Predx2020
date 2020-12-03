from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from predx.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from predx.users.routes import users
    from predx.posts.routes import posts
    from predx.main.routes import main
    from predx.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

def token_required(func):
    def wrapper(*args,**kwargs):

        token = request.headers['x-auth-token']

        if not token:
            return jsonify({'message':'Token is missing'})
        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            request.data = data
        except:
            return jsonify({'message':'invalid token'})
        return func(*args,**kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def create_table(app):
    db.create_all()
    db.commit()
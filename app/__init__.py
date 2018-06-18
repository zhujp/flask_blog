from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from config import config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'backend.login'

moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    from .frontend import frontend as frontend_blueprint
    app.register_blueprint(frontend_blueprint)

    from .backend import backend as backend_blueprint
    app.register_blueprint(backend_blueprint, url_prefix='/backend')

    
    return app
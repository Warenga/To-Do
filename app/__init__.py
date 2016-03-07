from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from config import config
from flask_oauthlib.client import OAuth



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
oauth = OAuth()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	oauth.init_app(app)
	moment.init_app(app)


	from main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app
	
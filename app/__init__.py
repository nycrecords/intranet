import datetime
import json

import os
from flask import Flask, abort, g, render_template, session, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)

    if app.config['USE_SAML']:
        login_manager.login_view = 'auth.saml'
    else:
        login_manager.login_view = 'auth.login'

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/auth")

    @app.before_request
    def before_request():
        app.permanent_session_lifetime = datetime.timedelta(minutes=15)
        session.permanent = True
        session.modified = True
        g.user = current_user

    @app.errorhandler(503)
    def maintenance(e):
        with open(os.path.join(app.instance_path, 'maintenance.json')) as f:
            maintenance_info = json.load(f)
        return render_template('error/maintenance.html',
                               description=maintenance_info['description'],
                               outage_time=maintenance_info['outage_time'])

    @app.before_request
    def check_maintenance_mode():
        if os.path.exists(os.path.join(app.instance_path, 'maintenance.json')):
            if not request.cookies.get('authorized_maintainer', None):
                return abort(503)

    return app

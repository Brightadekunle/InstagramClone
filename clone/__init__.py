from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import config
from elasticsearch import Elasticsearch
# from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class


db = SQLAlchemy()
loginmanager = LoginManager()
migrate = Migrate()
moment = Moment()
mail = Mail()
moment = Moment()
babel = Babel()
# photos = UploadSet('photos', IMAGES)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    loginmanager.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    loginmanager.login_view = 'auth.login'
    loginmanager.session_protection = 'strong'

    from clone.auth import auth
    from clone.main import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app


# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(current_app.config['LANGUAGES'])

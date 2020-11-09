import os


base_dir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # INSTAGRAM_ADMIN = os.environ.get('FLASKY_INSTAGRAM')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(os.getcwd(), 'clone.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'clone/static/images')
    INSTAGRAM_MAIL_SUBJECT_PREFIX = 'From Instagram'
    INSTAGRAM_MAIL_SENDER = 'Instagram Admin'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    USERS_PER_PAGE = 15
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    @staticmethod
    def init_app(app):
        pass


config = {'default': DevelopmentConfig}

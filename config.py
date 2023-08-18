import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USE_LOCAL_AUTH = os.environ.get('USE_LOCAL_AUTH') == "True"

    USE_LDAP = os.environ.get('USE_LDAP') == "True"
    LDAP_SERVER = os.environ.get('LDAP_SERVER') or None
    LDAP_PORT = os.environ.get('LDAP_PORT') or None
    LDAP_USE_TLS = os.environ.get('LDAP_USE_TLS') == "True"
    LDAP_KEY_PATH = os.environ.get('LDAP_KEY_PATH') or None
    LDAP_SA_BIND_DN = os.environ.get('LDAP_SA_BIND_DN') or None
    LDAP_SA_PASSWORD = os.environ.get('LDAP_SA_PASSWORD') or None
    LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN') or None
    LOGIN_REQUIRED = os.environ.get('LOGIN_REQUIRED') == "True"
    DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD')

    USE_SAML = os.environ.get('USE_SAML') == "True"
    SAML_PATH = os.environ.get('SAML_PATH') or None

    USER_DATA = (os.environ.get('USER_DATA') or os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data',
                                                             'users.csv'))
    APP_DEV_INTAKE_EMAIL_RECIPIENTS = os.environ.get('APP_DEV_INTAKE_EMAIL_RECIPIENTS', '').split(',') or []

    POSTS_PER_PAGE = 10

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or '127.0.0.1'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '25'
    MAIL_DEBUG = False

    MONITOR_EMAIL_RECIPIENTS = os.environ.get('MONITOR_EMAIL_RECIPIENTS', '').split(',') or []
    MONITOR_EMAIL_SENDER = os.environ.get('MONITOR_EMAIL_SENDER') or None

    OPENSSL_CONFIG = os.environ.get('OPENSSL_CONFIG') or None

    FRONTEND_RESOLUTION = os.environ.get('FRONTEND_RESOLUTION') or 60000
    REQUEST_PROBE_TIMEOUT = os.environ.get('REQUEST_PROBE_TIMEOUT') or 60

    FILE_UPLOAD_PATH = os.environ.get('FILE_UPLOAD_PATH') or '/vagrant/app/static/documents'
    VIRUS_SCAN_ENABLED = os.environ.get('VIRUS_SCAN_ENABLED') == "True"
    MAX_CONTENT_LENGTH =  512 * 1024 * 1024 # 512 MB

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') or
                               'postgresql://developer@127.0.0.1:5432/intranet')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('TEST_DATABASE_URL') or
                               'postgresql://developer@127.0.0.1:5432/intranet')


class HerokuConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://developer@127.0.0.1:5432/intranet')
    MAIL_SERVER = os.environ.get('MAILGUN_SMTP_SERVER')
    MAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT')
    MAIL_USERNAME = os.environ.get('MAILGUN_SMTP_LOGIN')
    MAIL_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD')
    MAIL_USE_TLES = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://developer@127.0.0.1:5432/intranet')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'heroku': HerokuConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

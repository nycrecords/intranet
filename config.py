import os
from dotenv import load_dotenv
from flask import url_for

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LDAP_SERVER = os.environ.get('LDAP_SERVER') or None
    LDAP_PORT = os.environ.get('LDAP_PORT') or None
    LDAP_USE_TLS = os.environ.get('LDAP_USE_TLS') == "True"
    LDAP_KEY_PATH = os.environ.get('LDAP_KEY_PATH') or None
    LDAP_SA_BIND_DN = os.environ.get('LDAP_SA_BIND_DN') or None
    LDAP_SA_PASSWORD = os.environ.get('LDAP_SA_PASSWORD') or None
    LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN') or None
    LOGIN_REQUIRED = os.environ.get('LOGIN_REQUIRED') == "True"

    USER_DATA = (os.environ.get('USER_DATA') or os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data',
                                                             'users.csv'))

    POSTS_PER_PAGE = 10
    DOCUMENTS_PER_PAGE = 10

    FILE_UPLOAD_PATH = os.environ.get('FILE_UPLOAD_PATH') or '/vagrant/app/static/documents'

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


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL') or
                               'postgresql://developer@127.0.0.1:5432/intranet')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

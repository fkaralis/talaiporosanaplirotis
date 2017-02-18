import os
basedir = os.path.abspath(os.path.dirname(__file__))

import locale
# linux locale
loc = locale.getdefaultlocale()
locale.setlocale(locale.LC_ALL, loc)
# win locale
#locale.setlocale(locale.LC_ALL, 'ell')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '#@SCJ239asbAS<KCsdfhg7757'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    TALAIPANAP_MAIL_SUBJECT_PREFIX  = '[TalaipAnap]'
    TALAIPANAP_MAIL_SENDER = 'TalaipAnap Admin <fivoskaralis@gmail.com>'
    TALAIPANAP_ADMIN = os.environ.get('TALAIPANAP_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
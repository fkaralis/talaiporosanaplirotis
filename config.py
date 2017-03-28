import os
basedir = os.path.abspath(os.path.dirname(__file__))

import locale
# linux locale
#loc = locale.getdefaultlocale()
#locale.setlocale(locale.LC_ALL, loc)
# win locale
locale.setlocale(locale.LC_ALL, 'ell')

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
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = BASE_DIR + '/app/static/'
    TEMP_PATH = DATA_PATH + 'temp/'

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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.TALAIPANAP_MAIL_SENDER,
            toaddrs=[cls.TALAIPANAP_ADMIN],
            subject=cls.TALAIPANAP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }
class Configuration:
    DEBUG = True
    SECRET_KEY = '7kRA6AwqgdtmBM2AL34jB4ndzdB5Rfm6bxhCzVpsvMBz9CRretpBNs6AepGY'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@127.0.0.1:5432/fl_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME= 'eae70d6312c61a'
    MAIL_PASSWORD = '00f213d89cd10c'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

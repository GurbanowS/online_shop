import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://myshop_user:myshop_pass@127.0.0.1:5433/myshop",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asfjashfjsbj121'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'shop/static/images')
    LANGUAGES = ['en', 'ru']
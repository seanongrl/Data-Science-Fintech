import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://fintech_user:fintech_Pass123@18.139.88.89/fintech'
    SQLALCHEMY_TRACK_MODIFICATIONS = False



import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root@localhost/api_h')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
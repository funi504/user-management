import redis
import os
class ApplicationConfig:
    SECRET_KEY = "azjEMb$hfnvn@djcbvhf123cb4d"

    SQLACHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    
    SESSION_TYPE ="redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    if os.environ.get('REDIS_URL'):
        SESSION_REDIS = os.environ.get('REDIS_URL')
    else:
        SESSION_REDIS = r"sqlite:///./db.sqlite"

import redis
import os
class ApplicationConfig:
    SECRET_KEY = "azjEMb$hfnvn@djcbvhf123cb4d"

    SQLACHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    SQLALCHEMY_DATABASE_URI = r"postgres://database_user_management_database_user:nExgXpGz4OCvh3F13g8dfOhJXY3yP2Ov@dpg-cocl5ha1hbls73ct1hh0-a/database_user_management_database"
    
    SESSION_TYPE ="redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.environ['REDIS_URL'])
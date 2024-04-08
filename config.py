class ApplicationConfig:
    SECRET_KEY = "azjEMb$hfnvn@djcbvhf123cb4d"

    SQLACHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"

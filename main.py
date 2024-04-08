import flask
from flask import *
from config import ApplicationConfig
from models import db , User , AdminUser
from flask_bcrypt import Bcrypt
import json
from routes.signup import register
app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)

app.secret_key = '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'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    resp = register(request,bcrypt ,User ,db , jsonify)
    return resp



# main driver function
if __name__ == '__main__':
 
    app.run('localhost', 8080)
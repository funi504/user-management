import flask
from flask import *
from flask import Flask, session
from flask_session import Session 

from config import ApplicationConfig
from models import db , User , AdminUser
from flask_bcrypt import Bcrypt
import json
from routes.signup import register
from routes.signin import login


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)

app.config.from_object(__name__)
Session(app)

app.secret_key = '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'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    resp = register(request,bcrypt ,User ,db , jsonify)
    return resp

@app.route("/signin" , methods=['POST','GET'])
def signin():
    resp = login(request , User , jsonify , bcrypt , session ,flask)
    return resp

# main driver function
if __name__ == '__main__':
 
    app.run('localhost', 8080)
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
from routes.profile import user_profile


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
bcrypt = Bcrypt(app)

app.config.from_object(__name__)
Session(app)

app.secret_key = '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'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST','GET'])
def signup():
    resp = register(request,bcrypt ,User ,db , jsonify)
    return resp

@app.route("/signin" , methods=['POST','GET'])
def signin():
    resp = login(request , User , bcrypt , session ,flask)
    return resp

@app.route("/profile" , methods=['POST','GET' , 'DELETE'])
def profile_user():
    resp = user_profile(request , session, User , db , jsonify , bcrypt)
    return resp

@app.route("/home" , methods=['POST','GET'])
def homepage():

    user_id = session.get("user_id")
    
    if user_id is not None:
        user = User.query.filter_by(id = user_id).first()
        email = user.email
        username = user.username

        return render_template('home.html', email=email , username=username)
    else:
        flash(" please first  login")
        return redirect(url_for('signin'))

# main driver function
if __name__ == '__main__':
 
    app.run('localhost', port=8080 , debug=True )
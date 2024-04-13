import flask
from flask import *
from flask import Flask, session , flash
from flask_session import Session 
from config import ApplicationConfig
from models import db , User , AdminUser
from flask_bcrypt import Bcrypt
import json
from routes.signup import register
from routes.signin import login
from routes.profile import user_profile
from routes.admin import admin
from routes.superadmin import superadmin



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
    resp = login(request , User , bcrypt , session ,flask,db)
    return resp

@app.route("/signout" , methods=['POST','GET'])
def signout():
    session.pop("user_id")
    flash("you logged out")
    return redirect(url_for('signin'))

@app.route("/profile" , methods=['POST','GET' , 'DELETE'])
def profile_user():
    resp = user_profile(request , session, User , db , jsonify , bcrypt , AdminUser)
    return resp

@app.route("/home" , methods=['POST','GET'])
def homepage():

    user_id = session.get("user_id")
    print("user id is ", user_id)

    if user_id is not None:
        user = User.query.filter_by(id = user_id).first()

        if user is None:
            flash(" please first  login")
            return redirect(url_for('signin'))

        email = user.email
        username = user.username

        isAdmin = False

        admin = AdminUser.query.filter_by(id=user_id).first()

        if admin is None:
            return render_template('home.html', email=email , username=username  , isAdmin = isAdmin)
        else:
            isAdmin = True
        
        return render_template('home.html', email=email , username=username , isAdmin = isAdmin)
    else:
        flash(" please first  login")
        return redirect(url_for('signin'))

"""@app.route('/createAdmin' , methods=['GET'])
def createadmins():
    email = 'superAdmin@gmail.com'
    username = 'superAdmin'
    password = 'superAdmin123'


    hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email , password=hashedPassword , username=username )
    db.session.add(new_user)
    db.session.commit()
    print("user created")
    print("new user id",new_user.id)

    new_superadmin = AdminUser(id=new_user.id , AccessLevel='SuperAdmin')
    db.session.add(new_superadmin)
    db.session.commit()
    print("super admin created")
    return 'created' """

#TODO: admin view,  create , read , update , delete and suspend users
@app.route('/admin' , methods=['GET','POST','PUT','DELETE'])
def adminpage():
    resp = admin( session , AdminUser , User , request, jsonify , db ,bcrypt)
    return resp

#TODO: superadmin view , create , read , delete and suspend admin
@app.route('/superadmin', methods=['GET' , 'POST' , 'PUT' , 'DELETE'])
def superadminpage():
    resp = superadmin( session , AdminUser , User , request , db , jsonify)
    return resp

@app.route('/suspend', methods=['POST'])
def suspend():
    user_id = session.get("user_id")

    if user_id is None:
        flash("session expired please login")
        return redirect(url_for('signin'))
    
    admin_user = AdminUser.query.filter_by(id=user_id).first()

    if admin_user is None:
        return redirect(url_for('homepage'))
    if request.method =='POST':

        id = request.form.get('id')
        user = User.query.filter_by(id=id).first()

        if user is None:
            flash("user does not exists")
            return redirect(url_for('homepage'))

        if not user.is_suspended:
            user.is_suspended = True
            db.session.commit()
            
            return redirect(url_for('adminpage'))

        if user.is_suspended:
            
            user.is_suspended = False
            user.login_attempt = 0
            db.session.commit()
            
            return redirect(url_for('adminpage'))


# main driver function
if __name__ == '__main__':
 
    app.run('localhost', port=8080  )

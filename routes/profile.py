import gladiator as gl 
from flask import redirect, url_for, flash

def user_profile(request , session, User , db ,jsonify , bcrypt , AdminUser):

    user_id = session.get("user_id") 
    #print(f"user Id : {user_id} ")

    if  user_id is None:
        flash("session expired please login")
        return redirect(url_for('signin'))
    #this post method act as a put method
    if request.method == "POST":
        try:
            user = User.query.filter_by(id=user_id).first()
            email = request.form.get("email")
            username =  request.form.get("username")
            new_password =request.form.get("password")
            print(email , username ,new_password)

            if new_password == '':
                
                data = {
                    'email':email,
                    'username': username,
                }

                field_validations = ( 
                        ('email', gl.required, gl.format_email), 
                        ('username', gl.required, gl.type_(str))
                    )

                if not gl.validate(field_validations, data):
                    flash('validation error', 'info')
                    jsonify({'error': 'failed'}),500

                user.email = email
                user.username = username
                db.session.commit()

                flash("user information updated")
                return redirect(url_for('homepage'))
            else:
                data = {
                    'email':email,
                    'username': username,
                    'new_password': new_password
                }

                field_validations = ( 
                        ('email', gl.required, gl.format_email), 
                        ('username', gl.required, gl.type_(str)),
                        ('new_password', gl.required, gl.type_(str) , gl.length_min(5))
                    )

                if not gl.validate(field_validations, data) :
                    flash('validation error', 'info')
                    return redirect(url_for('homepage'))

                hashedPassword = bcrypt.generate_password_hash(new_password).decode('utf-8')
                user.email = email
                user.username = username
                user.password = hashedPassword
                db.session.commit()

                flash("user information updated")
                return redirect(url_for('homepage'))
        
        except Exception as e:
            print(e)
            flash("something went wrong , try later")
            return redirect(url_for('homepage'))

    if request.method == "DELETE":
        try:
            user = User.query.filter_by(id=user_id).first()
            password = request.json["password"]

            if not bcrypt.check_password_hash(user.password, password):
                return jsonify({"error": "unauthorized"}), 401
            
            admin_user = AdminUser.query.filter_by(id=user_id).first()
            if admin_user is None:
                pass
            else:
                db.session.delete(admin_user)
                db.session.commit()

            db.session.delete(user)
            db.session.commit()
            session.pop("user_id")

            flash("account deleted successfully")
            return jsonify({'message': 'success'}),200

        except  Exception as e:

            print("errer is ",e)
            flash("failed to delete account , try again later")
            return jsonify({'error': 'failed'}),500

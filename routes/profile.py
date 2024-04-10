from flask import redirect, url_for, flash

def user_profile(request , session, User , db ,jsonify , bcrypt):

    user_id = session.get("user_id") 
    print(f"user Id : {user_id} ")
    if not user_id:
        
        flash("session expired please login")
        return redirect(url_for('signin'))

    if request.method == "POST":
        try:
            user = User.query.filter_by(id=user_id).first()
            email = request.form.get("email")
            username =  request.form.get("username")

            user.email = email
            user.username = username
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
            
            db.session.delete(user)
            db.session.commit()
            session.pop("user_id")

            flash("account deleted successfully")
            return jsonify({'message': 'success'}),200

        except  Exception as e:

            print("errer is ",e)
            flash("failed to delete account , try again later")
            return jsonify({'error': 'failed'}),500

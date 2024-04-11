import gladiator as gl 
from flask import redirect, url_for, flash, render_template
#TODO: admin view,  create , read , update , delete and suspend users
def admin( session , AdminUser , User , request , jsonify, db):
    
    user_id = session.get("user_id")

    if user_id is None:
        flash("session expired please login")
        return redirect(url_for('signin'))
    
    admin_user = AdminUser.query.filter_by(id=user_id).first()

    if admin_user is None:
        return redirect(url_for('homepage'))

    isSuperAdmin = False
    if admin_user.AccessLevel == 'SuperAdmin':
        isSuperAdmin = True

    if request.method == 'GET':
        all_users = User.query.all()
        users = []

        for user in all_users:
            isAdmin = AdminUser.query.filter_by(id=user.id).first()
            if isAdmin is None:
                users.append(user)

        return render_template('admin.html' , users = users , isSuperAdmin= isSuperAdmin)

    if request.method == 'PUT':

        username = request.json["username"]
        print("username",username)
        email = request.json["email"]
        id = request.json["id"]

        data = {
                'email':email,
                'username': username,
                'id': id
            }

        field_validations = ( 
                ('email', gl.required, gl.format_email), 
                ('username', gl.required, gl.type_(str)),
                ('id', gl.required, gl.type_(str))
                )

        if not gl.validate(field_validations, data) :
            flash('validation error', 'info')
            return redirect(url_for('homepage'))

        user = User.query.filter_by(id=id).first()
        
        if user is None:
            return jsonify({'message': 'user not found'}),404
        
        user.email = email
        user.username = username
        db.session.commit()

        return jsonify({'message': 'user info updated'}), 200

    if request.method == "DELETE":
        try:
            
            id = request.json["id"]
            user = User.query.filter_by(id=id).first()
            
            db.session.delete(user)
            db.session.commit()

            flash("account deleted successfully")
            return jsonify({'message': 'success'}),200

        except  Exception as e:

            print("errer is ",e)
            flash("failed to delete account , try again later")
            return jsonify({'error': 'failed'}),500
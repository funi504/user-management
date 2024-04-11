from os import access
from flask import redirect, url_for, flash , render_template

#TODO: admin view,  create , read , update and delete : later do suspend users
def superadmin( session , AdminUser , User , request , db):
    
    user_id = session.get("user_id")

    if user_id is None:
        flash("session expired please login")
        return redirect(url_for('signin'))
    
    admin_user = AdminUser.query.filter_by(id=user_id).first()

    if admin_user.AccessLevel != 'SuperAdmin':

        return redirect(url_for('homepage')) 

    if request.method == 'GET':
        all_admins = AdminUser.query.all()
        all_admins_list = []

        for admin in all_admins:
            admin_user = User.query.filter_by(id=admin.id).first()
            #if isAdmin is None:
            all_admins_list.append(admin_user)

        return render_template('superadmin.html' , all_admins = all_admins_list )

    if request.method == 'POST':
        admin_id = request.form.get("id")

        isAdmin = AdminUser.query.filter_by(id=admin_id).first()

        if isAdmin is None:
            new_superadmin = AdminUser(id=admin_id , AccessLevel='Admin')
            db.session.add(new_superadmin)
            db.session.commit()
            flash("new admin created")
            return redirect(url_for('superadminpage'))
        
        else:
            flash("User already an admin")
            return redirect(url_for('superadminpage'))




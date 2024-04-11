from flask import redirect, url_for, flash, render_template
#TODO: admin view,  create , read , update , delete and suspend users
def admin( session , AdminUser , User , request):
    
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


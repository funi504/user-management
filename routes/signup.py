import gladiator as gl 
from flask import render_template, redirect, url_for , flash

def register(request,bcrypt ,User ,db , jsonify):

    if request.method == 'GET':

        return render_template('register.html',)

    if request.method == 'POST':

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        data = {
            'email':email,
            'username': username,
            'password':password
        }

        field_validations = ( 
                ('email', gl.required, gl.format_email), 
                ('password', gl.required, gl.length_min(5)), 
                ('username', gl.required, gl.type_(str))
            )

        if not gl.validate(field_validations, data) :
            flash('validation error', 'info')
            return redirect(url_for('signup'))

        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')

        user_exists = User.query.filter_by(email=email).first() is not None
        username_exists = User.query.filter_by(username=username).first() is not None

        if user_exists:
            flash('account with this email already exists')
            return redirect(url_for('signup'))
        
        if username_exists:
            flash('account with this username already exists')
            return redirect(url_for('signup'))
        
        new_user = User(email=email , password=hashedPassword , username=username )

        db.session.add(new_user)
        db.session.commit()

        """return jsonify({
            "id": new_user.id,
            "email": new_user.email,
            "message":"accocunt created"
        })"""

        flash(f'account created successfully , login to your account')
        return redirect(url_for('signin'))

    else:
        flash(f'something went wrong try a bit later')
        return redirect(url_for('signup'))

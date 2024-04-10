import gladiator as gl 
from flask import render_template, redirect, url_for, flash

def login(request , User , bcrypt , session ,flask):
    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        data = {
            'email':email,
            'password':password
        }

        field_validations = ( 
                ('email', gl.required, gl.format_email), 
                ('password', gl.required, gl.length_min(5)), 
            )

        if not gl.validate(field_validations, data) :
            flash('validation error', 'info')
            return redirect(url_for('signin'))

        user = User.query.filter_by(email=email).first()

        if user is None :
            flash('incorect information ', 'info')
            return redirect(url_for('signin'))

        if not bcrypt.check_password_hash(user.password, password):
            flash('incorect information ', 'info')
            return redirect(url_for('signin'))

        session['user_id'] = user.id
        flask.session['user_id'] = user.id

        """return jsonify({
        "id": user.id,
        "email": user.email,
        })"""
        flash('logged in successfully , welcome to your profile page', 'info')
        return redirect(url_for('homepage'))

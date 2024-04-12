import gladiator as gl 
from flask import render_template, redirect, url_for, flash

def login(request , User , bcrypt , session ,flask ,db):
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

        if user.is_suspended:
            flash('your account is suspended ', 'info')
            return redirect(url_for('signin'))

        if not bcrypt.check_password_hash(user.password, password):
            attempt = user.login_attempt + 1
            user.login_attempt = attempt
            db.session.commit()

            if attempt > 3 :
                user.is_suspended = True
                db.session.commit()
                flash(f'account has been suspended contact support', 'info')
                return redirect(url_for('signin'))


            flash(f'incorect information , you have : {3 - attempt} left ', 'info')
            return redirect(url_for('signin'))
            
        user.login_attempt = 0
        db.session.commit()
        session['user_id'] = user.id
        flask.session['user_id'] = user.id

        """return jsonify({
        "id": user.id,
        "email": user.email,
        })"""
        flash('logged in successfully , welcome to your profile page', 'info')
        return redirect(url_for('homepage'))

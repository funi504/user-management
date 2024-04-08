import gladiator as gl 

def login(request , User , jsonify , bcrypt , session ,flask):
    
    if request.method == 'POST':

        email = request.json['email']
        password = request.json['password']

        data = {
            'email':email,
            'password':password
        }

        field_validations = ( 
                ('email', gl.required, gl.format_email), 
                ('password', gl.required, gl.length_min(5)), 
            )

        if not gl.validate(field_validations, data) :
            return jsonify({"error": "validation error",})

        user = User.query.filter_by(email=email).first()

        if user is None :
            return jsonify({"error": "unauthorized"}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "unauthorized"}), 401

        session['user_id'] = user.id
        flask.session['user_id'] = user.id

        return jsonify({
        "id": user.id,
        "email": user.email,
        })

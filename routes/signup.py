import gladiator as gl 

def register(request,bcrypt ,User ,db , jsonify):
    if request.method == 'POST':

        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]

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
            return jsonify({"error": "validation error",})

        hashedPassword = bcrypt.generate_password_hash(password)

        user_exists = User.query.filter_by(email=email).first() is not None
        username_exists = User.query.filter_by(username=username).first() is not None

        if user_exists:
            return jsonify({"error": "email already exists"}), 409
        
        if username_exists:
            return jsonify({"error": "username already exists"}), 409
        
        new_user = User(email=email , password=hashedPassword , username=username )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "id": new_user.id,
            "email": new_user.email,
            "message":"accocunt created"
        })

    else:
        return jsonify({ "error": "invalid method"}), 401
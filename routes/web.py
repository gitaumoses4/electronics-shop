from flask import render_template, request, jsonify
from models import User, RevokedToken
from flask_jwt_extended import JWTManager, jwt_required, get_raw_jwt
from flask import session, Session


def create_routes(app):
    jwt = JWTManager(app)
    # Session(app)

    user_routes(app)
    admin_routes(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)

    @app.route("/logout", methods=['POST'])
    @jwt_required
    def logout():
        print(get_raw_jwt())
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedToken(token=jti)
        revoked_token.save()

        return {'message': "Logout successful"}, 200


def user_routes(app):
    @app.route('/')
    def index():
        return render_template("index.html")


def admin_routes(app):
    @app.route('/admin/login', methods=['POST', 'GET'])
    def admin_login():
        if request.method == 'POST':
            if not request.form.get('username'):
                return jsonify({'errors': ['Username is required']}), 400
            if not request.form.get('password'):
                return jsonify({'errors': ['Password is required']}), 400

            user = User.query.filter_by(username=request.form['username']).first()
            if not user or not user.valid_password(request.form['password']):
                return jsonify({'errors': ['Invalid credentials']}), 400

            session['username'] = user.username
            session['email'] = user.email
            session['profile_picture'] = user.profile_picture
            return jsonify({
                'message': 'Login successful'
            }), 200
        else:
            return render_template("admin/login.html")

    @app.route('/admin/register', methods=['POST', 'GET'])
    def admin_register():
        if request.method == 'GET':
            return render_template('admin/register.html')
        else:
            if User.query.filter_by(
                    username=request.form['username']).first():
                return jsonify({'errors': ['Username already exists.']}), 400
            if User.query.filter_by(
                    email=request.form['email']).first():
                return jsonify({'errors': ['Email already in use']}), 400

            user = User(username=request.form['username'],
                        email=request.form['email'],
                        password=request.form['password'],
                        role=User.USER_ADMIN)

            user.save()

            session['username'] = user.username
            session['email'] = user.email
            session['profile_picture'] = user.profile_picture

            return jsonify({
                'message': 'Registration successful'
            }), 201

    @app.route("/admin", methods=['GET'])
    def admin_index():
        if session['username'] is None:
            return "Not Logged in"
        else:
            return "Logged in"

from flask import Flask, render_template, redirect, url_for, request, session, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
from backend.models import DatabaseManager, User
import os


db_mng = DatabaseManager()
db_mng.connect()

app = Flask('FLASK-VUE',
            static_folder="dist",
            template_folder="dist")


login_manager = LoginManager()
login_manager.init_app(app)


from backend.api.api import api


app.register_blueprint(api, url_prefix="/api")


CORS(app, resources={r"/api/*": {"origins": "*"}})


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        
        print(f"Session contents: {session}")
        if 'logged_in' not in session:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    result = db_mng.fetch_query("SELECT * FROM tbl_users WHERE id = %s", (user_id,))
    if result:
        user_data = result[0]
        return User(user_data['id'], user_data['name'], user_data['email'], user_data['password'])
    return None


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template('index.html')


@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(app.static_folder, 'service-worker.js')




@app.route('/account/register', methods=['POST'])
def register():
    user_name = request.form['user_name']
    email = request.form['email']
    password = request.form['password']

    
    hashed_password = generate_password_hash(password)

    
    sql_check_user = "SELECT * FROM tbl_users WHERE email = %s"
    params_check_user = (email,)
    existing_user = db_mng.fetch_query(sql_check_user, params_check_user)
    if existing_user:
        error = 'Email address is already registered.'
        return jsonify({'status': 'error', 'message': error}), 400

    
    user_id = "uid_" + str(uuid.uuid4())

    
    sql_insert_user = "INSERT INTO tbl_users (id, name, email, password, active) VALUES (%s, %s, %s, %s, %s)"
    params_insert_user = (user_id, user_name, email, hashed_password, True)
    db_mng.execute_query(sql_insert_user, params_insert_user)

    
    user = User(user_id, user_name, email, hashed_password, True)

    
    login_user(user)

    return jsonify({'status': 'success', 'message': 'Registration successful'}), 200



@app.route('/account/login', methods=['POST'])
def login():
    identifier = request.form['identifier']
    password = request.form['password']

    
    if '@' in identifier:
        sql_check_user = "SELECT * FROM tbl_users WHERE email = %s"
    else:
        sql_check_user = "SELECT * FROM tbl_users WHERE name = %s"
    params_check_user = (identifier,)
    
    user = db_mng.fetch_query(sql_check_user, params_check_user)
    print("user: ", user)
    if user and check_password_hash(user[0]['password'], password):
        session['logged_in'] = True
        session['user_id'] = user[0]['id']
        session['username'] = user[0]['name']
        
        response = {
            'status': 'success',
            'message': 'Login successful'
        }
        return jsonify(response), 200
    else:
        
        response = {
            'status': 'error',
            'message': 'Invalid email/username or password'
        }
        return jsonify(response), 401



@app.route('/account/check_session', methods=['GET'])
def check_session():
    if 'logged_in' in session:
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})


@app.route('/account/logout')
@login_required
def logout():
    session.clear()
    return jsonify({'success': True})

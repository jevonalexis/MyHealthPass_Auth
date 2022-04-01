from app import app, login_manager
from flask import request, jsonify, session
from flask_login import login_required, login_user, logout_user
from app.Services.ValidationService import ValidationService
from .Models.User import User
from .Database.DBService import DBService
from app.config import AppConfig
from app.policy_config import USER_LOCKOUT_POLICY as UL_POLICY
from .Services.Decorators import limit_locked_user, limit_locked_req_sig
from .Validator.Hasher import Hasher


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.filter(User.user_id == user_id).first()
    except Exception:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return 'You need to be logged in'


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = AppConfig.PERMANENT_SESSION_LIFESPAN


# Assume password confirmation handled on FE
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        validation_service = ValidationService()
        db_wrapper = DBService()
        res = validation_service.make_valid_user(**data)
        if type(res) is not User:
            return jsonify(f'{res.__repr__()} not created'), 400

        db_wrapper.insert_row(res)
        return jsonify(res.__repr__()), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': False,
            "message": "Error registering user",
            "error": str(e)
        }), 500


@app.route('/login', methods=['POST'])
@limit_locked_user
@limit_locked_req_sig
def login():
    try:
        data = request.get_json()
        user_agent = request.user_agent.string
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        cookies = request.cookies
        # get request signature
        request_signature = Hasher.cal_request_sig(user_agent, client_ip, cookies)

        validation_service = ValidationService()
        db_service = DBService()
        # get user from DB
        user = db_service.get_user(data['email'])
        if user is None:
            return jsonify({'status': False, "message": "User not found"}), 404

        if user.locked:
            return jsonify({'status': False, "message": "User Locked"}), 403
        # if password is incorrect increment user attempt count
        if not validation_service.verify_password(user, data['password']):
            rs_attempts = validation_service.increment_failed_attempts_rs(request_signature)
            user_attempts = validation_service.increment_failed_attempts(data['email'])
            if user_attempts == UL_POLICY['LOGIN_ATTEMPTS']:
                db_service.lock_user(data['email'])
                return jsonify({'status': False, "message": "User Locked"}), 403
            return jsonify({'status': False,
                            "message": f"Incorrect password. "
                                       f"{UL_POLICY['LOGIN_ATTEMPTS']-user_attempts} attempt(s) left"}
                           ), 403

        login_user(user)
        validation_service.init_failed_attempts(data['email'])
        return jsonify({
            'status': True,
            'message': 'login successful'
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': False,
            "message": "Error logging user in",
            "error": str(e)
        }), 500


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({
        'status': True,
    }), 200


@app.route('/check_token', methods=['GET', 'POST'])
def check_token():
    data = request.args
    token = data['token']
    email = data['email']
    err_msg = ''
    validation_service = ValidationService()
    if not validation_service.token_exist(email):
        err_msg = 'Token expired'
    elif validation_service.token_activated(email):
        err_msg = 'Token already activated'
    else:
        token_invalidated = validation_service.invalidate_token(email, token)
        if not token_invalidated:
            err_msg = 'Incorrect token'

    if err_msg:
        return jsonify({
            'status': False,
            'message': err_msg
        }), 400
    else:
        return jsonify({
            'status': True,
            'message': 'User unlocked'
        }), 200


@app.route('/unlock_user', methods=['POST'])
def unlock_user():
    data = request.get_json()
    email = data['email']
    host_url = request.host_url

    validation_service = ValidationService()
    token = validation_service.set_token(email)
    reset_link = f'{host_url}check_token?token={token}&email={email}'

    # this link would be sent to the user's email
    return jsonify({
        'status': True,
        'message': reset_link
    }), 200


"""
@app.route('/debug/secure_route', methods=['GET', 'POST'])
@login_required
def secure():
    return jsonify({
        'status': True,
        'message': 'top secret'
    }), 200


@app.route('/debug/unlock_user', methods=['GET'])
def debug_unlock_user():
    try:
        data = request.args
        db_service = DBService()
        db_service.unlock_user(data['email'])
        return 'unlocked'
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 'error'
"""

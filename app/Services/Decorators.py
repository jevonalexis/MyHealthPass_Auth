from functools import wraps
from flask import request, jsonify
from app.Services.ValidationService import ValidationService
from app.policy_config import USER_LOCKOUT_POLICY as UL_POLICY
from app.Validator.Hasher import Hasher


def limit_locked_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        validation_service = ValidationService()
        # db_service = DBService()
        if validation_service.get_failed_attempts(data['email']) == UL_POLICY['LOGIN_ATTEMPTS']:
            return jsonify({'status': False, "message": "User Locked"}), 403

        '''
        user = db_service.get_user(data['email'])
        if user is None:
            return jsonify({'status': False, "message": "User not found"}), 404

        if user.locked:
            return jsonify({'status': False, "message": "User Locked"}), 403

        if not validation_service.verify_password(user, data['password']):
            curr_attempts = validation_service.increment_failed_attempts(data['email'])
            if curr_attempts == UL_POLICY['LOGIN_ATTEMPTS']:
                db_service.lock_user(data['email'])
                return jsonify({'status': False, "message": "User Locked"}), 403
            return jsonify({'status': False,
                            "message": f"Incorrect password. "
                                       f"{UL_POLICY['LOGIN_ATTEMPTS']-curr_attempts} attempt(s) left"}
                           ), 403
        '''
        return f(*args, **kwargs)
    return decorated


def limit_locked_req_sig(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_agent = request.user_agent.string
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        cookies = request.cookies
        request_signature = Hasher.cal_request_sig(user_agent, client_ip, cookies)

        validation_service = ValidationService()
        if validation_service.is_rs_locked(request_signature):
            return jsonify({'status': False, "message": "Too many failed attempts. TIMEOUT!"}), 403

        return f(*args, **kwargs)
    return decorated

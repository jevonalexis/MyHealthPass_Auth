from app.Database.RedisProxy import RedisProxy
from app.Models.User import User
from app.Validator.ComplexityPolicy import ComplexityPolicy
from app.Validator.EmailValidator import EmailValidator
from app.Validator.Hasher import Hasher
from app.Validator.PasswordValidator import PasswordValidator
from app.policy_config import PASSWORD_COMPLEXITY_POLICY as PWC_POLICY, USER_LOCKOUT_POLICY as UL_POLICY, \
    REQUEST_SIGNATURE_LOCKOUT_POLICY as RSL_POLICY
from app.Database.prefixes import LGN_ATT, PW_TKN, REQ_SIG
from datetime import datetime
from app.config import REDIS_CONFIG


class ValidationService:
    password_validator: PasswordValidator
    email_validator: EmailValidator
    hasher: Hasher
    redis: RedisProxy

    def __init__(self):
        cp = ComplexityPolicy(**PWC_POLICY)
        self.password_validator = PasswordValidator(cp)
        self.email_validator = EmailValidator()
        self.hasher = Hasher()
        self.redis = RedisProxy()

    def make_valid_user(self, email, password, firstname='', lastname=''):
        if not email:
            raise ValueError('Email is required')
        if not password:
            raise ValueError('Password is required')

        resp = self.email_validator.validate(email)
        if not resp['valid']:
            return resp['errors']
        resp = self.password_validator.validate(password)
        if not resp['valid']:
            return resp['errors']
        return User(email, self.hasher.hash(password), firstname, lastname)

    def verify_password(self, user: User, password: str):
        return self.hasher.verify_password(user.password, password)

    def increment_failed_attempts(self, email: str):
        current_count = self.redis.get(f'{LGN_ATT}{email}')
        if not current_count:
            current_count = 0
        if current_count is not None and current_count < UL_POLICY['LOGIN_ATTEMPTS']:
            self.redis.set(f'{LGN_ATT}{email}', current_count + 1)
        return int(current_count) + 1

    def init_failed_attempts(self, email: str):
        self.redis.set(f'{LGN_ATT}{email}', 0)
        return 0

    def get_failed_attempts(self, email: str):
        if self.redis.key_exists(f'{LGN_ATT}{email}'):
            return int(self.redis.get(f'{LGN_ATT}{email}'))
        return -1

    def set_token(self, email: str, time_to_live: int = None):
        token = self.hasher.generate_token()
        self.redis.hashmap_set(f'{PW_TKN}{email}', {'token': token, 'activated': 0}, time_to_live)
        return token

    def token_exist(self, email: str):
        return self.redis.key_exists(f'{PW_TKN}{email}')

    def token_activated(self, email: str):
        return bool(int(self.redis.hash_get(f'{PW_TKN}{email}', 'activated')))

    def invalidate_token(self, email: str, token: str):
        if self.redis.hash_get(f'{PW_TKN}{email}', 'token') == token:
            self.redis.hash_set(f'{PW_TKN}{email}', 'activated', 1)
            return True
        return False

    def request_signature_exist(self, request_signature: str):
        return self.redis.key_exists(f'{REQ_SIG}{request_signature}')

    def _get_rs_attempts_count(self, request_signature: str):
        count = 0
        for _ in self.redis.r.scan_iter(f"{REDIS_CONFIG['options']['prefix']}{REQ_SIG}{request_signature}*"):
            count += 1
        return count

    def increment_failed_attempts_rs(self, request_signature: str):
        rs_attempts = self._get_rs_attempts_count(request_signature)
        print(rs_attempts)
        if rs_attempts < RSL_POLICY['LOGIN_ATTEMPTS']:
            key = self.get_time_key(request_signature)
            self.redis.set(key, 1, RSL_POLICY['TIME_SPAN'])
        if rs_attempts + 1 == RSL_POLICY['LOGIN_ATTEMPTS']:
            self.lock_rs(request_signature)
        return int(rs_attempts) + 1

    def get_time_key(self, request_signature: str):
        time_key = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f'{REQ_SIG}{request_signature}{time_key}'

    def lock_rs(self, request_signature: str):
        self.redis.set(f'{REQ_SIG}{request_signature}_locked', 1)
        self.redis.set_expiration(f'{REQ_SIG}{request_signature}_locked', RSL_POLICY['LOCKOUT_DURATION'])

    def is_rs_locked(self, request_signature: str):
        return self.redis.key_exists(f'{REQ_SIG}{request_signature}_locked')


if __name__ == '__main__':
    vs = ValidationService()
    print(vs.token_activated('u2@m.com'))

    # print(RSL_POLICY['TIME_SPAN'])

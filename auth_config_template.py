SESSION_LENGTH = 60 * 60 * 24

PASSWORD_COMPLEXITY_POLICY = {
    'min_length': 8,
    'max_length': 128,
    'lowercase_needed': True,
    'uppercase_needed': True,
    'number_needed': True,
    'special_characters': '''[ !"#$%&'()*+,-./<:=;>?@[\]^_`{|}~]''',
}

USER_LOCKOUT_POLICY = {
    'LOGIN_ATTEMPTS': 3
}

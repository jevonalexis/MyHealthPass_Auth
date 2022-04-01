import re
from app.Validator.ComplexityPolicy import ComplexityPolicy
from app.Validator.IValidator import IValidator, ValidationResponse

"""
Object of interface, IValidator for password validation 
"""


class PasswordValidator(IValidator):
    #: password complexity policy of type @ComplexityPolicy
    policy: ComplexityPolicy

    #: mapping of `function` to execute to validate a given `key` - criteria and `error` to return is validation fails
    criteria_map: dict

    def __init__(self, policy: ComplexityPolicy):
        self.policy = policy
        self.errors = []
        self.create_criteria_action_map()

    def validate_min_length(self, password: str) -> bool:
        return len(password) >= self.policy.min_length

    def validate_max_length(self, password: str) -> bool:
        return len(password) <= self.policy.max_length

    def validate_has_number(self, password: str) -> bool:
        if not self.policy.number_needed:
            return True
        return re.search(r'\d', password) is not None

    def validate_has_lowercase(self, password: str) -> bool:
        if not self.policy.lowercase_needed:
            return True
        return re.search(r'[a-z]', password) is not None

    def validate_has_uppercase(self, password: str) -> bool:
        if not self.policy.uppercase_needed:
            return True
        return re.search(r'[A-Z]', password) is not None

    def validate_has_special_char(self, password: str) -> bool:
        """
        :param password: password to validate for special characters
        :return: True if the password @policy.special_characters is empty or the password contains at least 1 of the
        characters specified, False otherwise
        """
        if not self.policy.special_characters:
            return True
        return re.search(self.policy.special_characters, password) is not None

    def create_criteria_action_map(self) -> None:
        self.criteria_map = {
            'min_length': {'function': self.validate_min_length,
                           'error': f'Password must be at least {self.policy.min_length} characters long'},
            'max_length': {'function': self.validate_max_length,
                           'error': f'Password must not be more than {self.policy.max_length} characters long'},
            'lowercase_needed': {'function': self.validate_has_lowercase,
                                 'error': 'Password must be contain at least 1 lowercase character'},
            'uppercase_needed': {'function': self.validate_has_uppercase,
                                 'error': 'Password must be contain at least 1 uppercase character'},
            'number_needed': {'function': self.validate_has_number,
                              'error': 'Password must be contain at least 1 number'},
            'special_characters': {'function': self.validate_has_special_char,
                                   'error': f'Password must be contain at least 1 special character '
                                            f'{self.policy.special_characters}'}
        }

    def validate(self, password: str) -> ValidationResponse:
        """

        :param password: password to validate for all criteria in the @policy
        :return: ValidationResponse {`valid`: True, `errors`: []} if valid
                ValidationResponse {`valid`: False, `errors`: [errors...]} if invalid
        """
        if password is None or password == "":
            self.errors.append('Password is required')
            return {'valid': len(self.errors) == 0, 'errors': self.errors}

        for criteria, criteria_action in self.criteria_map.items():
            if not criteria_action['function'](password):
                self.errors.append(criteria_action['error'])
        return {'valid': len(self.errors) == 0, 'errors': self.errors}


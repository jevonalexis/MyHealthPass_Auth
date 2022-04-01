import re
from app.Validator.IValidator import IValidator, ValidationResponse

"""
Object of interface, IValidator for email validation 
"""


class EmailValidator(IValidator):

    def validate(self, email: str) -> ValidationResponse:
        """

        :param email: email address to be validated
        :return: ValidationResponse with key `valid` True and empty `errors` array if email is valid,
         False and a string array containing an error otherwise
        """
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return {'valid': True, 'errors': []}
        return {'valid': False, 'errors': ['Invalid email address']}

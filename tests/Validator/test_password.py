import unittest
import mock_data as mock
from app.Validator.ComplexityPolicy import ComplexityPolicy
from app.Validator.PasswordValidator import PasswordValidator
from app.Validator.Hasher import Hasher


class TestPassword(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.policy = ComplexityPolicy(8, 16, True, True, True, r'[!@#$%^&*_+]')
        cls.password_validator = PasswordValidator(cls.policy)

    def test_hash(self):
        stored_hash = mock.hashed_password
        password = mock.password
        salt = mock.salt
        hashed_password = Hasher.hash(password, salt)
        self.assertEqual(hashed_password, stored_hash)

    def test_verify_hashed_password(self):
        stored_password = mock.hashed_password
        provided_password = mock.password
        self.assertTrue(Hasher.verify_password(stored_password, provided_password))

    def test_password_min_length(self):
        password = 'Sh0r+'
        self.assertFalse(self.password_validator.validate_min_length(password))
        password = 'Sh0r+123'
        self.assertTrue(self.password_validator.validate_min_length(password))

    def test_long_password(self):
        password = 'P@sswordi5TooL0ng'
        self.assertFalse(self.password_validator.validate_max_length(password))
        password = 'P@ssword123'
        self.assertTrue(self.password_validator.validate_max_length(password))

    def test_password_has_number(self):
        password = 'NoNumber'
        self.assertFalse(self.password_validator.validate_has_number(password))
        password = 'Passw0rd'
        self.assertTrue(self.password_validator.validate_has_number(password))

    def test_password_has_upper(self):
        password = 'password'
        self.assertFalse(self.password_validator.validate_has_uppercase(password))
        password = 'Password'
        self.assertTrue(self.password_validator.validate_has_uppercase(password))

    def test_password_has_lower(self):
        password = 'PASSWORD'
        self.assertFalse(self.password_validator.validate_has_lowercase(password))
        password = 'Password'
        self.assertTrue(self.password_validator.validate_has_lowercase(password))

    def test_password_has_special_char(self):
        password = 'Passw0rd'
        self.assertFalse(self.password_validator.validate_has_special_char(password))
        password = 'P@ssw0rd'
        self.assertTrue(self.password_validator.validate_has_special_char(password))

    def test_password_is_empty(self):
        password = ''
        resp = self.password_validator.validate(password)
        self.assertFalse(resp['valid'])

    def test_password_is_compliant(self):
        password = 'P@ssw0rd'
        resp = self.password_validator.validate(password)
        self.assertTrue(resp['valid'])

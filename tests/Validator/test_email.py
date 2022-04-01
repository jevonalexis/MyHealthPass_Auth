import unittest
from app.Validator.EmailValidator import EmailValidator


class TestEmail(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.email_validator = EmailValidator()

    def test_valid_email(self):
        email = 'bob@somemail.com'
        email_w_sld = 'bob@somemail.foo.com'
        resp = self.email_validator.validate(email)
        self.assertTrue(resp['valid'])
        resp = self.email_validator.validate(email_w_sld)
        self.assertTrue(resp['valid'])

    def test_invalid_emails(self):
        email_w_space = 'bob@ somemail.com'
        email_wo_at = 'bobsomemail.com'
        email_wo_dot = 'bob@ somemail.com'
        email_wo_domain = 'bob@somemail.'
        for e in [email_w_space, email_wo_at, email_wo_dot, email_wo_domain]:
            resp = self.email_validator.validate(e)
            self.assertFalse(resp['valid'])

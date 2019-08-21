import os

from unittest import TestCase
from tempfile import NamedTemporaryFile

from django_recipes import (
    get_random_secure_token,
    get_secret,
)


class TestRandomSecureToken(TestCase):
    def test_requested_length_too_short(self):
        self.assertRaises(ValueError, get_random_secure_token, length=3)


class TestGettingSecretFromPreferredLocation(TestCase):
    def setUp(self):
        # Generate a random secret value to be read from a file
        self.secret_from_file = get_random_secure_token()
        # Make a temporary file to write the secret's value
        self.secret_file = NamedTemporaryFile()

        # Set an environment variable to the path of the file storing the secret
        os.environ['SOME_SECRET_KEY_FILE'] = self.secret_file.name

        # Write the secret's value to file path
        with open(os.environ['SOME_SECRET_KEY_FILE'], 'w') as some_secret_file:
            some_secret_file.write(self.secret_from_file)

        # Generate another different random secret value to be read from an environment variable
        self.secret_from_env = get_random_secure_token()
        os.environ['SOME_SECRET_KEY'] = self.secret_from_env

    def tearDown(self):
        self.secret_file.close()

    def test_getting_secret_from_file(self):
        self.assertIsNotNone(self.secret_from_file)
        self.assertIsNotNone(get_secret('SOME_SECRET_KEY'))
        self.assertEqual(self.secret_from_file, get_secret('SOME_SECRET_KEY'))

    def test_getting_secret_from_environment_variable(self):
        del os.environ['SOME_SECRET_KEY_FILE']

        self.assertIsNotNone(self.secret_from_env)
        self.assertIsNotNone(get_secret('SOME_SECRET_KEY'))
        self.assertEqual(self.secret_from_env, get_secret('SOME_SECRET_KEY'))

    def test_getting_secret_while_not_allowing_null(self):
        del os.environ['SOME_SECRET_KEY_FILE']
        del os.environ['SOME_SECRET_KEY']

        self.assertRaises(KeyError, get_secret, 'SOME_SECRET_KEY')

    def test_getting_secret_and_allow_null(self):
        del os.environ['SOME_SECRET_KEY_FILE']
        del os.environ['SOME_SECRET_KEY']

        self.assertIsNone(get_secret('SOME_SECRET_KEY', allow_null=True))

    def test_getting_secret_when_value_is_empty_string(self):
        os.environ['SOME_SECRET_KEY'] = ''
        self.assertRaises(AssertionError, get_secret, 'SOME_SECRET_KEY')

        os.environ['SOME_SECRET_KEY_FILE'] = '/dev/null'
        self.assertRaises(AssertionError, get_secret, 'SOME_SECRET_KEY')

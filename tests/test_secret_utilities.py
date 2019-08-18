import os

from unittest import TestCase
from tempfile import NamedTemporaryFile

from django.test import override_settings
from django.core.management.utils import get_random_secret_key

from django_recipes import (
    get_random_secure_token,
    get_secret_key,
    get_django_secret_key,
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
        self.assertIsNotNone(get_secret_key('SOME_SECRET_KEY'))
        self.assertEqual(self.secret_from_file, get_secret_key('SOME_SECRET_KEY'))

    def test_getting_secret_from_environment_variable(self):
        del os.environ['SOME_SECRET_KEY_FILE']

        self.assertIsNotNone(self.secret_from_env)
        self.assertIsNotNone(get_secret_key('SOME_SECRET_KEY'))
        self.assertEqual(self.secret_from_env, get_secret_key('SOME_SECRET_KEY'))

    def test_getting_secret_while_not_allowing_null(self):
        del os.environ['SOME_SECRET_KEY_FILE']
        del os.environ['SOME_SECRET_KEY']

        self.assertRaises(KeyError, get_secret_key, 'SOME_SECRET_KEY')

    def test_getting_secret_and_allow_null(self):
        del os.environ['SOME_SECRET_KEY_FILE']
        del os.environ['SOME_SECRET_KEY']

        self.assertIsNone(get_secret_key('SOME_SECRET_KEY', allow_null=True))


class TestGettingDjangoSecretKey(TestCase):
    def setUp(self):
        # Generate a Django SECRET_KEY value to be stored in a file
        self.django_secret_key_from_file = get_random_secret_key()
        # Create a corresponding file to store the secret's value
        self.django_secret_key_file = NamedTemporaryFile()

        # Set an environment variable to the file path where the secret is written
        os.environ['DJANGO_SECRET_KEY_FILE'] = self.django_secret_key_file.name

        # Write the SECRET_KEY value to the temporary file
        with open(os.environ['DJANGO_SECRET_KEY_FILE'], 'w') as django_secret_key_file:
            django_secret_key_file.write(self.django_secret_key_from_file)

        # Generate another different random SECRET_KEY value to be read from an environment variable
        self.django_secret_key_from_env = get_random_secret_key()
        os.environ['DJANGO_SECRET_KEY'] = self.django_secret_key_from_env

    def tearDown(self):
        self.django_secret_key_file.close()

    def test_getting_django_secret_key_from_file(self):
        self.assertIsNotNone(self.django_secret_key_from_file)
        self.assertIsNotNone(get_django_secret_key())
        self.assertEqual(get_django_secret_key(), self.django_secret_key_from_file)

    def test_getting_django_secret_key_from_environment_variable(self):
        del os.environ['DJANGO_SECRET_KEY_FILE']

        self.assertIsNotNone(self.django_secret_key_from_env)
        self.assertIsNotNone(get_django_secret_key())
        self.assertEqual(get_django_secret_key(), self.django_secret_key_from_env)

    def test_getting_django_secret_key_with_random_not_allowed(self):
        # Neither of these environment variables should be set to apply to this test case
        del os.environ['DJANGO_SECRET_KEY_FILE']
        del os.environ['DJANGO_SECRET_KEY']

        secret_key_value = get_django_secret_key()

        # The value of the secret key should be null if random fallback is not allowed
        self.assertIsNone(secret_key_value)

    def test_getting_django_secret_key_and_allow_random(self):
        # Neither of these environment variables should be set to apply to this test case
        del os.environ['DJANGO_SECRET_KEY_FILE']
        del os.environ['DJANGO_SECRET_KEY']

        secret_key_value = get_django_secret_key(allow_random=True)

        # The random SECRET_KEY shouldn't be the same as the one from the file or environment variable
        self.assertIsNot(self.django_secret_key_from_file, secret_key_value)
        self.assertIsNot(self.django_secret_key_from_env, secret_key_value)
        # The value of the SECRET_KEY shouldn't be null but instead some random value
        self.assertIsNotNone(secret_key_value)
        # The SECRET_KEY should be lengthy (at least the same or longer than a default "django-admin startproject")
        self.assertGreaterEqual(len(secret_key_value), 50)

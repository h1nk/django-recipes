from unittest import TestCase

from django.test import override_settings

from django_recipes import get_database_url


class TestGetDjangoDatabaseURL(TestCase):
    # I only use SQLite 3, PostgreS, and Redis for personal projects, therefore those are the only URI schemes I really
    # care about being able to work...

    @override_settings(DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    })
    def test_sqlite_in_memory(self):
        self.assertEqual(
            'sqlite://:memory:',
            get_database_url(),
        )

    @override_settings(DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/file.db',
        }
    })
    def test_sqlite_flat_file(self):
        self.assertEqual(
            'sqlite:///tmp/file.db',
            get_database_url(),
        )

    @override_settings(DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': 'host.example.com',
            'USER': 'bob',
            'PASSWORD': 'super_secret_password',
            'NAME': 'other-db',
            'OPTIONS': {
                'connect_timeout': 10,
            }
        }
    })
    def test_postgres(self):
        self.assertEqual(
            'postgresql://bob:super_secret_password@host.example.com/other-db?connect_timeout=10',
            get_database_url(),
        )

    @override_settings(CACHES={
        # FIXME
    })
    def test_redis(self):
        pass

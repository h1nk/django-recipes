from django.core.management.utils import get_random_secret_key

SECRET_KEY = get_random_secret_key()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

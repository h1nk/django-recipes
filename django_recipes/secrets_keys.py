import os
import re
import string
import secrets

from typing import Optional

from django.core.management.utils import get_random_secret_key

__all___ = (
    'get_random_secure_token',
    'get_secret_key',
    'get_django_secret_key',
)


def get_random_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically strong `URL-safe <https://tools.ietf.org/html/rfc4648#section-5>`_
    alphanumeric string suitable for a privilege or login token. If you'd like to create 1-time or single-use login
    tokens you may also want to consider using Django's cryptographic signing features.

    :param length: Length of the randomly generated string. Must be a minimum of 32 characters in length.
    :type length: int
    :raises ValueError: If the token length is too low (less than 32). This is merely to ensure all token lengths are
    of a minimum secure length.
    :return: A randomly generated string
    :rtype: str
    """

    if length < 32:
        raise ValueError

    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_secret_key(name: str, allow_null=False):
    """
    Obtain the value of a named secret from the most preferred location

    The search order when looking for a suitable secret value is as follows:

    * First from the contents of a file path indicated by the capitalized ``name_FILE`` environment variable
      (recommended for production environments).
    * Directly from the value of the capitalized ``name`` environment variable.
    * Lastly if permitted fail by returning null.

    :param name: Name of the secret
    :type name: str
    :param allow_null: Whether or not to permit returning ``None`` if no secret could be found. Disabled by default.
    :type allow_null: bool
    :raises: KeyError
    :return: Secret value from preferred mechanism
    :rtype: Optional[str]
    """

    secret_file_env_varname = re.sub(r'\W+', '_', name).upper()
    secret_env_varname = '_'.join((name, 'FILE'))

    secret_file_path = os.getenv(secret_env_varname)
    secret_from_file = None

    if secret_file_path and os.access(secret_file_path, os.R_OK) and os.path.isfile(secret_file_path):
        with open(secret_file_path, 'r') as secret_file_path:
            secret_from_file = secret_file_path.read()

    secret_from_env = os.getenv(secret_file_env_varname)

    if not allow_null and not secret_from_file and not secret_from_env:
        raise KeyError("Unable to find a suitable secret value for secret")

    return secret_from_file or secret_from_env


def get_django_secret_key(allow_random: bool = False) -> Optional[str]:
    """
    Obtain a value suitable for the `Django SECRET_KEY setting
    <https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY>`_
    by searching in order from the following places:

    * From the contents of a file path indicated by the ``DJANGO_SECRET_KEY_FILE`` environment variable
      (recommended for production environments).
    * Directly from the value of the ``DJANGO_SECRET_KEY`` environment variable.
    * A randomly generated key if permitted. This option is only usually acceptable for use with
      `runserver <https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver>`_ and local
      development/debugging environment where sudden invalidation of user sessions is not a problem.
    * Lastly if a randomly generated fallback is not permitted return ``None`` and fail.

    :param allow_random: Whether to permit fallback to randomly generated secret key or not. ``False`` by default.
    :type allow_random: bool
    :return: A value suitable for the Django ``SECRET_KEY`` setting or ``None`` if all else fails
    :rtype: Optional[str]
    """

    secret_from_random = get_random_secret_key() if allow_random else None

    return get_secret_key('DJANGO_SECRET_KEY', allow_null=True) or secret_from_random

import os
import re
import secrets
import string

__all___ = (
    'get_random_secure_token',
    'get_secret_key',
)


def get_random_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically strong `URL-safe <https://tools.ietf.org/html/rfc4648#section-5>`_
    alphanumeric string suitable for a privilege or login token. If you'd like to create 1-time or single-use login
    tokens you may also want to consider using Django's cryptographic signing features.

    :param length: Length of the randomly generated string. Must be a minimum of 32 characters in length.
    :type length: int

    :return: A randomly generated string
    :rtype: str

    :raises ValueError: If the token length is too low (less than 32 characters). This is merely to ensure all token
     lengths are of a minimum secure length.
    """

    if length < 32:
        raise ValueError

    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_secret_key(name: str, allow_null=False):
    """
    Get the value of a named secret by searching the following locations in this order:

    * From the contents of a file at a path indicated by the capitalized ``name`` environment variable
      (recommended for production environments).
    * Directly from the value of the capitalized ``name`` environment variable.
    * Lastly, return ``None`` if permitted.

    :param name: Name of the secret
    :type name: str
    :param allow_null: Whether or not to permit returning ``None`` if no secret could be found.
    :type allow_null: bool

    :return: Value of the secret
    :rtype: Optional[str]

    :raises KeyError: If no suitable value for secret could be found
    :raises AssertionError: If secret is an empty string value
    """

    secret_file_env_varname = re.sub(r'\W+', '_', name).upper()
    secret_env_varname = '_'.join((name, 'FILE'))

    secret_file_path = os.getenv(secret_env_varname)
    secret_from_file = None

    secret_from_env = os.getenv(secret_file_env_varname)

    if secret_from_env is not None:
        assert len(secret_from_env) >= 1

    if secret_file_path:
        with open(secret_file_path, 'r') as secret_file_path:
            secret_from_file = secret_file_path.read()

        assert len(secret_from_file) >= 1

    if not allow_null and not secret_from_file and not secret_from_env:
        raise KeyError("Unable to find a suitable secret value for secret")

    return secret_from_file or secret_from_env

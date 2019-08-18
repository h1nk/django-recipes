from urllib.parse import urlunparse, urlencode

from django.conf import settings

__all__ = (
    'get_database_url',
)


def get_database_url(alias: str = 'default') -> str:
    """
    This is a pretty big and messy hack. It would be much nicer if there were some utility functions internal to Django
    that could be used for getting the database URL from a ``settings.DATABASES`` alias. This function is basically the
    inverse functionality of the ``dj-database-url`` package (which is a required to be installed in order to call this
    function), i.e. it will un-parse a database configuration from your Django settings into a database connection URL
    string.

    :param alias: Django database alias. Default is "default"
    :type alias: str
    :return: A database connection URL string
    :rtype: str
    """

    from dj_database_url import SCHEMES as database_schemes

    # Invert dj-database-urls's protocol scheme dictionary
    schemes = {v: k for k, v in database_schemes.items()}
    # The URI scheme designator for PostgreS can be either postgresql:// or postgres:// see:
    # https://www.postgresql.org/docs/current/libpq-connect.html#id-1.7.3.8.3.6
    # Just simply use "postgresql://" for our URIs
    schemes['django.db.backends.postgresql'] = 'postgresql'
    # Get the specified database alias...
    database_dict = settings.DATABASES[alias]
    # As well as its database engine, name, login credentials and host/port
    engine = database_dict['ENGINE']
    name = database_dict.get('NAME')
    user, password = database_dict.get('USER'), database_dict.get('PASSWORD')
    host, port = database_dict.get('HOST'), database_dict.get('PORT')

    # Special handling for SQLite in-memory databases:
    # https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-TEST_NAME
    # https://docs.djangoproject.com/en/stable/ref/settings/#name
    # https://github.com/kennethreitz/dj-database-url/blob/master/dj_database_url.py#L75-L82
    if engine == database_schemes['sqlite']:
        if name == ':memory:' or name is None:
            return 'sqlite://:memory:'

        return 'sqlite://' + name

    if host and port:
        # Only include the port if necessary
        network_location = ':'.join((host, port))
    else:
        # Otherwise omit the default port
        network_location = host

    # Build the network host part with username & password included
    network_location = '@'.join((':'.join((user, password)) if user and password else user, network_location))
    # And the rest of the connection URL parameters...
    url_parts = (schemes[engine], network_location, name, None, urlencode(database_dict.get('OPTIONS')), None)

    return urlunparse(url_parts)

<div align="center">

# Django Recipes

</div>

This is a small library package I made in an effort to eliminate the repetition of common boilerplate code in my [Django-powered](https://www.djangoproject.com/) projects.

## Features

- Functions for sourcing secret key values from the most preferred storage mechanism in a consistent way. I primarily added this to make Django projects easier to integrate with Docker and other containerized deployment environments where secret tokens and API keys are often stored in securely mounted volumes rather than from environment variables, which is what I typically use in local development.
- A simple [serializer](https://docs.djangoproject.com/en/stable/topics/serialization/) for [MessagePack](https://msgpack.org/) that works quite well with Django's [cryptographic signing functionality](https://docs.djangoproject.com/en/stable/topics/signing/). This has allowed me to create more efficiently packed data as well as shorten the length of URLs that contain signed data.
- Minor fixes/changes to core Django, most notably:
    - A [customized](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#customizing-makemessages) [`makemessages` management command](https://docs.djangoproject.com/en/stable/ref/django-admin/#django-admin-makemessages) that tames the quite obnoxious default [fuzzy matching behavior](https://code.djangoproject.com/ticket/10852) with [`msgmerge`](https://www.gnu.org/software/gettext/manual/html_node/msgmerge-Invocation.html).
- Custom management commands for operations that I would commonly run in the interactive interpreter shell:
    - A `deletesessions` management command to compliment [`clearsessions`](https://docs.djangoproject.com/en/stable/ref/django-admin/#clearsessions) that simply purges any database-backed sessions and forces users to re-login.
- A [queryset](https://docs.djangoproject.com/en/stable/ref/models/querysets/) wrapper for [redis](https://redis.io/) [sorted sets](https://redis.io/topics/data-types#sorted-sets) and an [itertools-like](https://docs.python.org/3/library/itertools.html) `group` utility function for iterating over slices of an object.
- Database and cache URL reconstruction/un-parsing. Essentially the opposite of [`dj-database-url`](https://github.com/jacobian/dj-database-url). I've often found this convenient when doing direct database and cache access through other client libraries like [`aioredis`](https://github.com/aio-libs/aioredis) and [`aiopg`](https://github.com/aio-libs/aiopg) in order to keep connection details consistent with Django's [`DATABASES`](https://docs.djangoproject.com/en/stable/ref/settings/#databases) and [`CACHES`](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-CACHES) settings.
- View decorators for adding view patterns directly into your [URLconf](https://docs.djangoproject.com/en/stable/topics/http/urls/) that work with both function and class-based views.

## Installation

```bash
$ pipenv install git+https://github.com/h1nk/django-recipes.git@stable#egg=django-recipes.git
```

Additionally, if you care to have access to the additional management commands then you must add the reusable app to your [`INSTALLED_APPS`](https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps) in your Django project settings:

```python
INSTALLED_APPS = [
    ...
    
    # NOTE: because some of the management commands provided by this package override default django-admin
    # commands you must insert the entry above Django's own apps
    'django_recipes',
    
    ...
]
```
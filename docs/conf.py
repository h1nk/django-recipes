import os
import sys

# Add project root to sys.path for autodoc discoverability
sys.path.insert(0, os.path.abspath('../'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '_ext')))

project = 'Django Recipes'
# noinspection PyShadowingBuiltins
copyright = '2019, hink'
author = 'hink'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',

    'djangodocs',
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'alabaster'
html_static_path = ['_static']

intersphinx_mapping = {
    'py': ('https://docs.python.org/{0.major}.{0.minor}'.format(sys.version_info), None),
    'dj': ('https://docs.djangoproject.com/en/stable/', 'https://docs.djangoproject.com/en/stable/_objects/'),
    'redis-py': ('https://redis-py.readthedocs.io/en/stable/', None),
}

def setup(app):
    # https://github.com/django/django/blob/master/docs/_ext/djangodocs.py#L27-L31
    app.add_crossref_type(
        directivename="setting",
        rolename="setting",
        indextemplate="pair: %s; setting",
    )

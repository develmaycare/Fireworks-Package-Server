"""
JSON decorators.

> Note: This module is named `jsond` in order to avoid conflicts with the
> Python's built in `json` module.
"""

# Python Imports
from json import dumps as json_encode

# Django Imports
from django.shortcuts import get_object_or_404, render_to_response

# Local Imports
from packages.models import Package

# Supporting Functions

def is_json_request(http_accept):
    """Detect whether the HTTP_ACCEPT is (or includes) application/json."""

    # As with is_html_request under `decorators/html.py` his detection code may
    # be a little brittle based on the browser that's requesting the page.
    # We'll see.
    accept_types = http_accept.split(',')
    if list == type(accept_types):
        for t in accept_types:
            if 'application/json' == t:
                return True
    else:
        if 'application/json' == http_accept:
            return True

    return False

# Decorators

def index(f):
    """Return JSON output for the root URL registry."""
    def wrapper(request, *args, **kwargs):

        if not is_json_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        packages = dict()
        for Pkg in Package.objects.all():
            if Pkg.is_local():
                j = dict()
                for V in Pkg.versions.all():
                    j[V.number] = dict()
                    j[V.number]['name'] = Pkg.name
                    j[V.number]['version'] = V.number
                    j[V.number]['main'] = V.main
                    j[V.number]['description'] = Pkg.description
                    j[V.number]['dist'] = 'NOT IMPLEMENTED'
                packages[Pkg.name] = j
            else:
                packages[Pkg.name] = 'NOT IMPLEMENTED (external URL) should go here'

        tokens = dict()
        tokens['output'] = json_encode(packages)

        return render_to_response("packages/index.json", tokens, mimetype="application/json")

    return wrapper

def package(f):
    """Return a package object."""

    def wrapper(request, *args, **kwargs):

        if not is_json_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        Pkg = get_object_or_404(Package,name=kwargs['package_name'])

        tokens = dict()
        tokens['Package'] = Pkg
        tokens['display_specific_package'] = False

        if 'package_version' in kwargs:
            tokens['display_specific_package'] = True
            tokens['package_version'] = kwargs['package_version']

        return render_to_response("packages/package.json", tokens, mimetype="application/json")

    return wrapper

def testing(f):
    """Display the testing/sandbox in JSON format."""

    def wrapper(request, *args, **kwargs):
        if not is_json_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        tokens = dict()
        tokens['request'] = request
        tokens['output'] = 'testing 123'
        
        return render_to_response("packages/testing.txt", tokens, mimetype="application/json")

    return wrapper

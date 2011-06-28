"""
HTML decorators display packages as standard HTML pages, and are there for the
default rendering tool when a visitor looks at the package index.
"""

# Django Imports
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

# Local Imports
from packages.models import Package

# Supporting Functions

def is_html_request(http_accept):
    """Detect whether the HTTP_ACCEPT is (or includes) text/html."""

    # Don't know yet, but this detection code may be a little brittle based on 
    # the browser that's requesting the page. We'll see.
    accept_types = http_accept.split(',')
    if list == type(accept_types):
        for t in accept_types:
            if 'text/html' == t:
                return True
    else:
        if 'text/html' == http_accept:
            return True

    return False

# Decorators

def index(f):
    """Return output for the given view function as HTML."""
    def wrapper(request, *args, **kwargs):

        if not is_html_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        
        # TODO: Implement paging for package display.

        # QUESTION: How should packages be sorted by default?
        tokens = dict()
        tokens['packages'] = Package.objects.all()
        print "here"
        return direct_to_template(request, 'packages/index.html', tokens)

    return wrapper

def package(f):
    """Display a package home page as HTML."""

    def wrapper(request, *args, **kwargs):

        if not is_html_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        """Use this for testing:
        tokens = dict()
        tokens['request'] = request
        tokens['output'] = kwargs
        return direct_to_template(request, "packages/testing.html", tokens)
        """

        Pkg = get_object_or_404(Package, name=kwargs['package_name'])

        tokens = dict()
        tokens['Package'] = Pkg
        tokens['display_specific_page'] = False

        if 'version_number' in kwargs:
            tokens['display_specific_package'] = True
            tokens['version_number'] = kwargs['version_number']

        return direct_to_template(request, 'packages/package.html', tokens)

    return wrapper

def testing(f):
    """Display the testing/sandbox HTML page."""

    def wrapper(request, *args, **kwargs):
        if not is_html_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        tokens = dict()
        tokens['request'] = request
        tokens['output'] = "testing 123"
        return direct_to_template (request, "packages/testing.html", tokens)

    return wrapper

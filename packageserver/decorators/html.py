"""
HTML decorators.
"""

# Imports #
#import simplejson as json
from django.http import HttpResponse
from django.template import Context, loader

from packageserver.models import Contact, Package, Repo

# Supporting Functions #

def is_html_request(http_accept):
    """Detect whether the HTTP_ACCEPT is (or includes) text/html."""

    """
    Don't know yet, but this detection code may be a brittle 
    based on the browser that's requesting the page. We'll 
    see.
    """
    accept_types = http_accept.split(',')
    if list == type(accept_types):
        for t in accept_types:
            if 'text/html' == t:
                return True
    else:
        if 'text/html' == http_accept:
            return True

    return False


# Decorators #

def index(f):
    """Return output for the given view function as HTML."""
    def wrapper(request, *args, **kwargs):

        if not is_html_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        T = loader.get_template('index.html')
        C = Context({'packages': Package.objects.all()})
        return HttpResponse(T.render(C),mimetype="text/html")

    return wrapper

def package(f):
    """Display a package home page as HTML."""

    def wrapper(request, *args, **kwargs):

        if not is_html_request(request.META['HTTP_ACCEPT']):
            return f(request, *args, **kwargs)

        """Use this for testing:
        context = {
            'request': request,
            'output': kwargs,
        }
        T = loader.get_template('testing.html')
        C = Context(context)
        return HttpResponse(T.render(C),mimetype="text/html")
        """

        Pkg = Package.objects.get(name=kwargs['package_name'])


        tokens = {
            'Package': Pkg,
            'display_specific_package': False,
        }
        if 'package_version' in kwargs:
            tokens['display_specific_package'] = True
            tokens['package_version'] = kwargs['package_version']

        C = Context(tokens)

        T = loader.get_template('package.html')
        return HttpResponse(T.render(C),mimetype="text/html")

    return wrapper

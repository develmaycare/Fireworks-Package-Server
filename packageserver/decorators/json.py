"""
JSON decorators.
"""

# Imports #
import simplejson as json
from django.conf import settings as SETTINGS
from django.http import HttpResponse
from django.template import Context, loader

from packageserver.models import Contact, Package, Repo

# Supporting Functions #

def package_to_dictionary(Object):
    """Convert a Package object to a dictionary that may be used by simplejson.
    Note that we can't just use Object.__dict__ because we need to be 
    selective above what is in the output.
    """
    pass

class JsonPackage(object):
    """A collector for package data that will be serialized to a JSON string."""
    pass

# Decorators #

def index(f):
    """Return JSON output for the root URL registry."""
    def wrapper(request, *args, **kwargs):

        if 'application/json' <> request.META['HTTP_ACCEPT']:
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
        output = json.dumps(packages)

        T = loader.get_template('index.json')
        C = Context({'request':request,'output':output})
        return HttpResponse(T.render(C),mimetype="text/html")

        C = Context({'request': request,'output': output})
        
        if SETTINGS.DEBUG:
            T = loader.get_template('testing.txt')
            return HttpResponse(T.render(C),mimetype="text/html")
        else:
            T = loader.get_template('index.json')
            return HttpResponse(T.render(C), mimetype="application/json")

    return wrapper

def package(f):
    """Return a package object."""

    def wrapper(request, *args, **kwargs):

        if 'application/json' <> request.META['HTTP_ACCEPT']:
            return f(request, *args, **kwargs)

        """Use this for testing:
        context = {
            'request': request,
            'output': kwargs,
        }
        T = loader.get_template('testing.txt')
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

        if SETTINGS.DEBUG:
            T = loader.get_template('testing.txt')
            T = loader.get_template('package.json')
            return HttpResponse(T.render(C), mimetype="application/json")
            return HttpResponse(T.render(C),mimetype="text/html")
        else:
            T = loader.get_template('package.json')
            return HttpResponse(T.render(C), mimetype="application/json")

    return wrapper

def testing(f):
    """Display the testing/sandbox in JSON format."""

    def wrapper(request, *args, **kwargs):
        if 'application/json' <> request.META['HTTP_ACCEPT']:
            return f(request, *args, **kwargs)

        T = loader.get_template('testing.txt')
        C = Context({
            'request': request,
            'output': 'This is a test.'
        })
        return HttpResponse(T.render(C),mimetype="text/html")
    return wrapper

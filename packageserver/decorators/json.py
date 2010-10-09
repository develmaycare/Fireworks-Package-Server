"""
JSON decorators.
"""

# Imports #
#import simplejson as json
from django.conf import settings as SETTINGS
from django.http import HttpResponse
from django.template import Context, loader

from packageserver.models import Contact, Package, Repo

# Decorators #

def index(f):
    """Return output for the given view function as JSON."""
    def wrapper(request, *args, **kwargs):

        if 'application/json' <> request.META['HTTP_ACCEPT']:
            return f(request, *args, **kwargs)

        j = '{'
        for Pkg in Package.objects.all():
            if Pkg.is_local():
                j += '"%s": %s"' %(Pkg.name,Pkg.to_commonjs())
            else:
                j += '"%s": %s"' %(Pkg.name,Pkg.repositories.all()[0])
            j += ','
        j += '}' 
        print j

        C = Context({'request': request,'output': j})
        
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
